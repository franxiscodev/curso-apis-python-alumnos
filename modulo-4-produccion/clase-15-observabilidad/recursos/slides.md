---
marp: true
theme: default
paginate: true
header: 'Clase 15: Observabilidad y Proyecto Integrador'
footer: 'Curso APIs Avanzadas con Python'
---

# Observabilidad
## Logs, Métricas y Traces

Clase 15 - Módulo 4: Producción y Escalabilidad

---

# Los 3 Pilares

| Pilar | Pregunta | Ejemplo |
|-------|----------|---------|
| **Logs** | ¿Qué pasó? | "Error al conectar a DB" |
| **Métricas** | ¿Cuánto? | 500 req/s, latencia p99=200ms |
| **Traces** | ¿Por dónde? | API → DB → Cache → Respuesta |

---

# Logging Estructurado

```python
# MAL: texto plano
logging.info("Error en request de usuario admin")

# BIEN: JSON estructurado
logging.info("Error en request", extra={
    "request_id": "abc123",
    "usuario": "admin",
    "endpoint": "/items",
    "status": 500
})
```

JSON → fácil de buscar, filtrar, agregar

---

# JSON Formatter

```python
class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", None),
        })
```

---

# Request ID (Correlation ID)

```python
@app.middleware("http")
async def add_request_id(request, call_next):
    request_id = request.headers.get(
        "X-Request-ID", str(uuid.uuid4())[:8]
    )
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
```

Un ID que sigue la request por todo el sistema

---

# Métricas

**Tipos:**
- **Counter**: solo sube (requests totales, errores)
- **Histogram**: distribución (latencias)
- **Gauge**: sube y baja (conexiones activas)

```python
metricas = {
    "requests_total": 0,     # Counter
    "errores_total": 0,      # Counter
    "latencias": [],          # Histogram
}
```

---

# Health Checks

```python
@app.get("/health")    # ¿Está vivo?
def health():
    return {"status": "alive"}

@app.get("/ready")     # ¿Puede recibir tráfico?
def ready():
    db_ok = check_db()
    return {"ready": db_ok}
```

| Probe | Pregunta | Si falla |
|-------|----------|----------|
| Liveness | ¿Vivo? | Reiniciar |
| Readiness | ¿Listo? | No enviar tráfico |

---

# Stack de Observabilidad

```
App → Prometheus → Grafana (dashboards)
App → ELK Stack (logs)
App → Jaeger (traces)
```

Hoy: implementamos la instrumentación en la App

---

# Resumen del Curso

| Módulo | Clases | Temas |
|--------|--------|-------|
| 1. Fundamentos | 01-04 | Python, typing, OOP, REST |
| 2. FastAPI | 05-09 | Pydantic, CRUD, SQLAlchemy, Auth |
| 3. Integración | 10-12 | Async, WebSockets, Integraciones |
| 4. Producción | 13-15 | Testing, Docker, Observabilidad |

---

# Próximos Pasos

- **Kubernetes**: orquestación de contenedores
- **Cloud**: AWS/GCP/Azure deployment
- **GraphQL**: alternativa a REST
- **gRPC**: comunicación entre microservicios
- **Async avanzado**: Celery, workers distribuidos

---

# Recursos

- **structlog**: https://www.structlog.org
- **Prometheus**: https://prometheus.io
- **OpenTelemetry**: https://opentelemetry.io
- **Grafana**: https://grafana.com

**Practica:**
```bash
uvicorn ejemplos.api_observable:app --reload
```
