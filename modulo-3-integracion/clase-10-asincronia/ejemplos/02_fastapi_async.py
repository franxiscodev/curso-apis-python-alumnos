"""
Endpoints Async en FastAPI
============================
Diferencia entre endpoints async y sync.

Ejecutar:
    uvicorn ejemplos.02_fastapi_async:app --reload

Conceptos:
    - async def vs def en endpoints
    - Cuándo usar cada uno
    - Simulación de operaciones I/O
"""

import asyncio
import time

from fastapi import FastAPI

app = FastAPI(title="Async Demo", version="1.0.0")


# =============================================================================
# ENDPOINTS ASYNC (para operaciones I/O)
# =============================================================================


@app.get("/async/rapido", tags=["Async"])
async def endpoint_async():
    """Endpoint asíncrono: no bloquea mientras espera."""
    await asyncio.sleep(0.1)  # Simula I/O (BD, API externa)
    return {"tipo": "async", "mensaje": "No bloqueé el servidor"}


@app.get("/async/datos", tags=["Async"])
async def obtener_datos_async():
    """Simula obtener datos de 3 fuentes concurrentemente."""
    inicio = time.perf_counter()

    async def fuente_a():
        await asyncio.sleep(0.5)
        return {"fuente": "A", "datos": [1, 2, 3]}

    async def fuente_b():
        await asyncio.sleep(0.3)
        return {"fuente": "B", "datos": [4, 5, 6]}

    async def fuente_c():
        await asyncio.sleep(0.4)
        return {"fuente": "C", "datos": [7, 8, 9]}

    a, b, c = await asyncio.gather(fuente_a(), fuente_b(), fuente_c())
    total = time.perf_counter() - inicio

    return {
        "resultados": [a, b, c],
        "tiempo_total": f"{total:.2f}s",
        "nota": "3 fuentes en paralelo, no secuencial"
    }


# =============================================================================
# ENDPOINTS SYNC (para operaciones CPU o bloqueantes)
# =============================================================================


@app.get("/sync/calcular", tags=["Sync"])
def calcular_sync():
    """Endpoint síncrono: FastAPI lo ejecuta en un threadpool."""
    # Operación CPU-bound (no se beneficia de async)
    resultado = sum(i * i for i in range(100_000))
    return {"tipo": "sync", "resultado": resultado}


# =============================================================================
# COMPARACIÓN
# =============================================================================


@app.get("/comparar", tags=["Comparación"])
async def comparar():
    """Muestra cuándo usar async vs sync."""
    return {
        "usar_async": [
            "Llamadas a APIs externas",
            "Consultas a BD asíncrona",
            "Lectura de archivos con aiofiles",
            "Cualquier operación I/O"
        ],
        "usar_sync": [
            "Cálculos matemáticos pesados",
            "Procesamiento de imágenes",
            "Librerías que no soportan async",
            "Operaciones rápidas sin I/O"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
