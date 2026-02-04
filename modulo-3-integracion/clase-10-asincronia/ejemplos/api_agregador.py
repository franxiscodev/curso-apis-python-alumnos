"""
API Agregadora Asíncrona
==========================
API que agrega datos de múltiples fuentes concurrentemente.

Ejecutar:
    uvicorn ejemplos.api_agregador:app --reload

Endpoints:
    GET /fuentes/{id}      - Obtener datos de una fuente
    GET /agregar            - Agregar datos de todas las fuentes
    GET /agregar/rapido     - Agregar concurrentemente (async)
    GET /health             - Estado del servicio
"""

import asyncio
import time

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel


app = FastAPI(
    title="API Agregadora Async",
    description="Agrega datos de múltiples fuentes concurrentemente",
    version="1.0.0"
)


# =============================================================================
# SIMULACIÓN DE FUENTES DE DATOS
# =============================================================================


class DatosFuente(BaseModel):
    """Datos de una fuente."""
    fuente: str
    datos: list[float]
    tiempo_respuesta: float


async def obtener_fuente(fuente_id: str, latencia: float) -> DatosFuente:
    """Simula obtener datos de una fuente externa."""
    inicio = time.perf_counter()
    await asyncio.sleep(latencia)  # Simula latencia de red

    # Datos simulados
    import random
    datos = [round(random.uniform(0, 100), 2) for _ in range(5)]

    return DatosFuente(
        fuente=fuente_id,
        datos=datos,
        tiempo_respuesta=round(time.perf_counter() - inicio, 3)
    )


# Configuración de fuentes
FUENTES = {
    "ventas": 0.5,
    "inventario": 0.3,
    "clientes": 0.7,
    "analytics": 0.4,
}


# =============================================================================
# ENDPOINTS
# =============================================================================


@app.get("/fuentes/{fuente_id}", response_model=DatosFuente, tags=["Fuentes"])
async def obtener_una_fuente(fuente_id: str):
    """Obtener datos de una fuente específica."""
    if fuente_id not in FUENTES:
        raise HTTPException(status_code=404, detail=f"Fuente '{fuente_id}' no existe")
    return await obtener_fuente(fuente_id, FUENTES[fuente_id])


@app.get("/agregar/secuencial", tags=["Agregación"])
async def agregar_secuencial():
    """Agrega datos de todas las fuentes SECUENCIALMENTE (lento)."""
    inicio = time.perf_counter()
    resultados = []
    for fuente_id, latencia in FUENTES.items():
        resultado = await obtener_fuente(fuente_id, latencia)
        resultados.append(resultado)
    total = time.perf_counter() - inicio

    return {
        "modo": "secuencial",
        "fuentes": resultados,
        "tiempo_total": f"{total:.2f}s",
        "nota": "Cada fuente espera a la anterior"
    }


@app.get("/agregar/concurrente", tags=["Agregación"])
async def agregar_concurrente():
    """Agrega datos de todas las fuentes CONCURRENTEMENTE (rápido)."""
    inicio = time.perf_counter()
    tareas = [obtener_fuente(fid, lat) for fid, lat in FUENTES.items()]
    resultados = await asyncio.gather(*tareas)
    total = time.perf_counter() - inicio

    return {
        "modo": "concurrente",
        "fuentes": list(resultados),
        "tiempo_total": f"{total:.2f}s",
        "nota": "Todas las fuentes se consultan al mismo tiempo"
    }


@app.get("/agregar/estadisticas", tags=["Agregación"])
async def agregar_con_estadisticas():
    """Agrega datos y calcula estadísticas."""
    tareas = [obtener_fuente(fid, lat) for fid, lat in FUENTES.items()]
    resultados = await asyncio.gather(*tareas)

    todos_los_datos = []
    for r in resultados:
        todos_los_datos.extend(r.datos)

    return {
        "fuentes_consultadas": len(resultados),
        "total_datos": len(todos_los_datos),
        "promedio": round(sum(todos_los_datos) / len(todos_los_datos), 2),
        "minimo": min(todos_los_datos),
        "maximo": max(todos_los_datos),
    }


@app.get("/health", tags=["Sistema"])
async def health():
    """Estado del servicio."""
    return {
        "status": "ok",
        "fuentes_disponibles": list(FUENTES.keys())
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
