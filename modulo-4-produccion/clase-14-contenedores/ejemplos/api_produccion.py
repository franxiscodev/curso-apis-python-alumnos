"""
API Producción: API Lista para Deploy
=======================================
Integra buenas prácticas: config, health, CORS, logging.

Ejecutar:
    uvicorn ejemplos.api_produccion:app --reload
"""

import logging
import os
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic_settings import BaseSettings

# === CONFIGURACIÓN ===


class Settings(BaseSettings):
    """Configuración desde variables de entorno."""
    app_name: str = "api-produccion"
    version: str = "1.0.0"
    debug: bool = False
    allowed_origins: str = "*"
    log_level: str = "INFO"

    model_config = {"env_prefix": "APP_"}


settings = Settings()

# === LOGGING ===

logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(settings.app_name)

# === APP ===

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    docs_url="/docs" if settings.debug else None,
    redoc_url=None,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)


# === MIDDLEWARE DE LOGGING ===


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"{request.method} {request.url.path} → {response.status_code}")
    return response


# === MODELOS ===


class Tarea(BaseModel):
    titulo: str
    completada: bool = False


# === DATOS ===

tareas: list[dict] = []
inicio_app = datetime.now(timezone.utc)


# === ENDPOINTS OPERACIONALES ===


@app.get("/health", tags=["Ops"])
def health():
    """Health check para load balancers y Docker."""
    return {"status": "healthy"}


@app.get("/ready", tags=["Ops"])
def ready():
    """Readiness check."""
    return {"ready": True, "servicios": {"db": "ok", "cache": "ok"}}


@app.get("/info", tags=["Ops"])
def info():
    """Información del servicio."""
    return {
        "app": settings.app_name,
        "version": settings.version,
        "uptime_seconds": (datetime.now(timezone.utc) - inicio_app).total_seconds(),
        "debug": settings.debug,
    }


# === ENDPOINTS DE NEGOCIO ===


@app.get("/tareas", tags=["Tareas"])
def listar():
    return tareas


@app.post("/tareas", status_code=201, tags=["Tareas"])
def crear(tarea: Tarea):
    nueva = {"id": len(tareas) + 1, **tarea.model_dump()}
    tareas.append(nueva)
    logger.info(f"Tarea creada: {nueva['titulo']}")
    return nueva


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
