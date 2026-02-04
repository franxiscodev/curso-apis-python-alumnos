"""
API Observable: Integración Completa
=======================================
Logging + métricas + tracing + health checks.

Ejecutar:
    uvicorn ejemplos.api_observable:app --reload
"""

import json
import logging
import sys
import time
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# === LOGGING JSON ===


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "msg": record.getMessage(),
        }
        for attr in ("request_id", "method", "path", "status"):
            if hasattr(record, attr):
                log[attr] = getattr(record, attr)
        return json.dumps(log)


logger = logging.getLogger("observable")
logger.setLevel(logging.INFO)
h = logging.StreamHandler(sys.stdout)
h.setFormatter(JSONFormatter())
logger.addHandler(h)

# === APP ===

app = FastAPI(title="API Observable", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# === MÉTRICAS EN MEMORIA ===

metricas = {
    "requests_total": 0,
    "errores_total": 0,
    "por_endpoint": {},
    "latencias": [],
}
INICIO = time.time()


# === MIDDLEWARE ===


@app.middleware("http")
async def observabilidad(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])
    request.state.request_id = request_id
    inicio = time.perf_counter()

    metricas["requests_total"] += 1
    endpoint = request.url.path
    metricas["por_endpoint"][endpoint] = metricas["por_endpoint"].get(endpoint, 0) + 1

    logger.info(
        f"→ {request.method} {endpoint}",
        extra={"request_id": request_id, "method": request.method, "path": endpoint},
    )

    response = await call_next(request)
    duracion = time.perf_counter() - inicio

    metricas["latencias"].append(round(duracion, 4))
    metricas["latencias"] = metricas["latencias"][-100:]

    if response.status_code >= 400:
        metricas["errores_total"] += 1

    logger.info(
        f"← {response.status_code} ({duracion:.3f}s)",
        extra={"request_id": request_id, "status": response.status_code},
    )
    response.headers["X-Request-ID"] = request_id
    return response


# === MODELOS ===


class TareaCrear(BaseModel):
    titulo: str
    prioridad: str = "media"


# === DATOS ===

tareas: list[dict] = [
    {"id": 1, "titulo": "Desplegar API", "prioridad": "alta", "completada": False},
]


# === ENDPOINTS OPERACIONALES ===


@app.get("/health", tags=["Ops"])
def health():
    return {"status": "healthy"}


@app.get("/ready", tags=["Ops"])
def ready():
    return {"ready": True}


@app.get("/metrics", tags=["Ops"])
def metrics():
    """Métricas del servicio."""
    latencias = metricas["latencias"]
    avg = sum(latencias) / len(latencias) if latencias else 0
    return {
        "requests_total": metricas["requests_total"],
        "errores_total": metricas["errores_total"],
        "latencia_promedio": round(avg, 4),
        "uptime_seconds": round(time.time() - INICIO, 1),
        "por_endpoint": metricas["por_endpoint"],
    }


# === ENDPOINTS DE NEGOCIO ===


@app.get("/tareas", tags=["Tareas"])
def listar():
    return tareas


@app.post("/tareas", status_code=201, tags=["Tareas"])
def crear(tarea: TareaCrear, request: Request):
    nueva = {"id": len(tareas) + 1, **tarea.model_dump(), "completada": False}
    tareas.append(nueva)
    logger.info(
        f"Tarea creada: {nueva['titulo']}",
        extra={"request_id": request.state.request_id},
    )
    return nueva


@app.get("/tareas/{tarea_id}", tags=["Tareas"])
def obtener(tarea_id: int, request: Request):
    for t in tareas:
        if t["id"] == tarea_id:
            return t
    logger.warning(
        f"Tarea {tarea_id} no encontrada",
        extra={"request_id": request.state.request_id},
    )
    raise HTTPException(status_code=404, detail="Tarea no encontrada")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
