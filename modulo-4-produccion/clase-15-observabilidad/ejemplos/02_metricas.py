"""
Ejemplo 02: Métricas con Prometheus
=====================================
Contadores, histogramas y endpoint /metrics.

Ejecutar:
    uvicorn ejemplos.02_metricas:app --reload
    Abrir http://127.0.0.1:8000/metrics

Nota: requiere prometheus_client (uv add prometheus-client)
Si no está instalado, la API funciona con métricas simuladas.
"""

import time

from fastapi import FastAPI, Request, Response

app = FastAPI(title="Métricas Prometheus", version="1.0.0")

# === MÉTRICAS (simuladas si prometheus_client no está) ===

try:
    from prometheus_client import Counter, Histogram, Gauge, generate_latest

    REQUESTS_TOTAL = Counter(
        "http_requests_total",
        "Total de requests HTTP",
        ["method", "endpoint", "status"],
    )
    REQUEST_DURATION = Histogram(
        "http_request_duration_seconds",
        "Duración de requests en segundos",
        ["method", "endpoint"],
    )
    ACTIVE_REQUESTS = Gauge(
        "http_active_requests",
        "Requests activas actualmente",
    )
    PROMETHEUS_DISPONIBLE = True
except ImportError:
    PROMETHEUS_DISPONIBLE = False


# === MÉTRICAS EN MEMORIA (fallback) ===

metricas_simples: dict[str, int] = {
    "requests_total": 0,
    "errores_total": 0,
}


# === MIDDLEWARE DE MÉTRICAS ===


@app.middleware("http")
async def registrar_metricas(request: Request, call_next):
    metricas_simples["requests_total"] += 1
    inicio = time.perf_counter()

    if PROMETHEUS_DISPONIBLE:
        ACTIVE_REQUESTS.inc()

    response = await call_next(request)
    duracion = time.perf_counter() - inicio

    if PROMETHEUS_DISPONIBLE:
        REQUESTS_TOTAL.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code,
        ).inc()
        REQUEST_DURATION.labels(
            method=request.method,
            endpoint=request.url.path,
        ).observe(duracion)
        ACTIVE_REQUESTS.dec()

    if response.status_code >= 400:
        metricas_simples["errores_total"] += 1

    return response


# === ENDPOINTS ===


@app.get("/metrics", tags=["Métricas"])
def metrics():
    """Endpoint de métricas para Prometheus."""
    if PROMETHEUS_DISPONIBLE:
        return Response(
            content=generate_latest(), media_type="text/plain"
        )
    return metricas_simples


@app.get("/", tags=["Raíz"])
def raiz():
    return {"status": "ok", "prometheus": PROMETHEUS_DISPONIBLE}


@app.get("/items", tags=["Ejemplo"])
def listar():
    return [{"id": 1, "nombre": "Widget"}, {"id": 2, "nombre": "Gadget"}]


@app.get("/lento", tags=["Ejemplo"])
async def endpoint_lento():
    """Endpoint lento para demostrar histograma de latencia."""
    import asyncio
    await asyncio.sleep(0.5)
    return {"mensaje": "Respuesta lenta"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
