# Observabilidad - Cheatsheet

Guía rápida de logging, métricas y health checks.

---

## Logging JSON

```python
import json, logging, sys
from datetime import datetime, timezone

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "msg": record.getMessage(),
        })

logger = logging.getLogger("api")
logger.setLevel(logging.INFO)
h = logging.StreamHandler(sys.stdout)
h.setFormatter(JSONFormatter())
logger.addHandler(h)
```

---

## Request ID Middleware

```python
import uuid
from fastapi import Request

@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    rid = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])
    request.state.request_id = rid
    response = await call_next(request)
    response.headers["X-Request-ID"] = rid
    return response
```

---

## Métricas en Memoria

```python
import time

metricas = {"requests": 0, "errores": 0, "latencias": []}

@app.middleware("http")
async def metricas_middleware(request, call_next):
    metricas["requests"] += 1
    inicio = time.perf_counter()
    response = await call_next(request)
    metricas["latencias"].append(time.perf_counter() - inicio)
    metricas["latencias"] = metricas["latencias"][-100:]
    if response.status_code >= 400:
        metricas["errores"] += 1
    return response

@app.get("/metrics")
def metrics():
    lats = metricas["latencias"]
    return {
        "requests": metricas["requests"],
        "errores": metricas["errores"],
        "latencia_avg": sum(lats) / len(lats) if lats else 0,
    }
```

---

## Prometheus (si disponible)

```python
from prometheus_client import Counter, Histogram, generate_latest
from fastapi import Response

REQUESTS = Counter("requests_total", "Total requests", ["method", "endpoint"])
LATENCY = Histogram("request_duration_seconds", "Latencia", ["endpoint"])

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type="text/plain")
```

```bash
uv add prometheus-client
```

---

## Health Checks

```python
@app.get("/health")
def health():
    """Liveness: ¿está vivo?"""
    return {"status": "alive"}

@app.get("/ready")
def ready():
    """Readiness: ¿puede recibir tráfico?"""
    db_ok = check_database()
    return {"ready": db_ok, "checks": {"db": "ok" if db_ok else "fail"}}

@app.get("/startup")
def startup():
    """Startup: ¿terminó de arrancar?"""
    return {"started": True, "uptime": time.time() - INICIO}
```

---

## Tipos de Probes (Kubernetes)

| Probe | Pregunta | Si falla |
|-------|----------|----------|
| Liveness | ¿Vivo? | Reiniciar pod |
| Readiness | ¿Listo? | Sacar del balanceador |
| Startup | ¿Arrancó? | Esperar más |

---

## Tracing con Correlation ID

```python
class TraceContext:
    def __init__(self):
        self.trace_id = str(uuid.uuid4())[:8]
        self.spans = []

    def start_span(self, nombre):
        span = {"nombre": nombre, "inicio": time.perf_counter()}
        self.spans.append(span)
        return span

    def end_span(self, span):
        span["duracion"] = time.perf_counter() - span["inicio"]
```

---

## Herramientas

| Categoría | Herramienta | Uso |
|-----------|-------------|-----|
| Logs | ELK Stack | Buscar y filtrar logs |
| Logs | CloudWatch | Logs en AWS |
| Métricas | Prometheus | Recolectar métricas |
| Métricas | Grafana | Dashboards |
| Traces | Jaeger | Tracing distribuido |
| Traces | OpenTelemetry | Instrumentación |

---

## Tips

1. **Logs en JSON**: siempre en producción, facilita búsqueda
2. **Request ID**: en TODOS los logs de una request
3. **Métricas**: mínimo requests/s, latencia p99, tasa de error
4. **Health checks**: separar liveness de readiness
5. **No logear secretos**: filtrar passwords, tokens, API keys
6. **Alertas**: configurar en métricas (error rate > 5%, latencia > 500ms)
