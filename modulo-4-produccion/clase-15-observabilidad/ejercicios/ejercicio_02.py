"""
Ejercicio 02: Métricas y Health Checks
========================================
Agregar métricas en memoria y health checks.

INSTRUCCIONES:
1. Implementar métricas en memoria:
   - requests_total (contador)
   - errores_total (contador)
   - latencia promedio

2. Implementar middleware que registre métricas

3. Endpoints:
   - GET /health (liveness)
   - GET /ready (readiness con checks)
   - GET /metrics (métricas del servicio)

PRUEBAS:
    uvicorn ejercicio_02:app --reload

    GET /health
    GET /metrics (hacer varias requests primero)

PISTAS:
- time.perf_counter() para medir latencia
- Diccionario global para métricas
- Lista de latencias, limitar a últimas 100
"""

import time

from fastapi import FastAPI, Request

app = FastAPI(title="Métricas", version="1.0.0")

# TODO: Diccionario de métricas globales

# TODO: Estado de servicios para readiness

# TODO: Middleware que registre métricas

# TODO: GET /health (liveness simple)

# TODO: GET /ready (readiness con checks de servicios)

# TODO: GET /metrics (métricas acumuladas)

# Endpoints de ejemplo para generar métricas
@app.get("/items", tags=["Ejemplo"])
def listar():
    return [{"id": 1}, {"id": 2}]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
