"""
Ejemplo 04: Simulación de Cola de Tareas
==========================================
Patrón productor-consumidor con asyncio.Queue.

Ejecutar:
    uvicorn ejemplos.04_colas_tareas:app --reload
"""

import asyncio
from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Cola de Tareas", version="1.0.0")


# === MODELOS ===


class Tarea(BaseModel):
    tipo: str
    datos: dict = {}


# === COLA EN MEMORIA ===

cola: asyncio.Queue | None = None
tareas_procesadas: list[dict] = []
tareas_pendientes: list[dict] = []


@app.on_event("startup")
async def startup():
    """Inicializa la cola y el worker."""
    global cola
    cola = asyncio.Queue(maxsize=100)
    asyncio.create_task(worker())


async def worker():
    """Consumidor que procesa tareas de la cola."""
    while True:
        tarea = await cola.get()
        print(f"Procesando: {tarea['tipo']}")
        # Simular procesamiento
        await asyncio.sleep(1)
        tarea["estado"] = "completada"
        tarea["completada_en"] = datetime.now(timezone.utc).isoformat()
        tareas_procesadas.append(tarea)
        # Remover de pendientes
        tareas_pendientes[:] = [
            t for t in tareas_pendientes if t["id"] != tarea["id"]
        ]
        cola.task_done()
        print(f"Completada: {tarea['tipo']}")


# === ENDPOINTS ===


@app.post("/tareas", tags=["Cola"])
async def agregar_tarea(tarea: Tarea):
    """Agrega una tarea a la cola."""
    item = {
        "id": len(tareas_pendientes) + len(tareas_procesadas) + 1,
        "tipo": tarea.tipo,
        "datos": tarea.datos,
        "estado": "pendiente",
        "creada_en": datetime.now(timezone.utc).isoformat(),
    }
    tareas_pendientes.append(item)
    await cola.put(item)
    return {"mensaje": "Tarea encolada", "tarea": item}


@app.get("/tareas/pendientes", tags=["Cola"])
async def ver_pendientes():
    """Tareas pendientes en la cola."""
    return {
        "pendientes": len(tareas_pendientes),
        "tareas": tareas_pendientes,
    }


@app.get("/tareas/completadas", tags=["Cola"])
async def ver_completadas():
    """Tareas procesadas."""
    return {
        "completadas": len(tareas_procesadas),
        "tareas": tareas_procesadas[-10:],
    }


@app.get("/tareas/estado", tags=["Cola"])
async def estado_cola():
    """Estado general de la cola."""
    return {
        "en_cola": cola.qsize() if cola else 0,
        "pendientes": len(tareas_pendientes),
        "completadas": len(tareas_procesadas),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
