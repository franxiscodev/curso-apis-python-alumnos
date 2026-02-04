"""
Ejemplo 01: Logging Estructurado
==================================
Logging JSON con contexto y request ID.

Ejecutar:
    uvicorn ejemplos.01_logging_estructurado:app --reload
"""

import json
import logging
import sys
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI, Request

# === LOGGER JSON ===


class JSONFormatter(logging.Formatter):
    """Formatea logs como JSON."""

    def format(self, record: logging.LogRecord) -> str:
        log = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        # Campos extra
        if hasattr(record, "request_id"):
            log["request_id"] = record.request_id
        if hasattr(record, "extra_data"):
            log.update(record.extra_data)
        return json.dumps(log)


# Configurar logger
logger = logging.getLogger("api")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)

# === APP ===

app = FastAPI(title="Logging Estructurado", version="1.0.0")


# === MIDDLEWARE: REQUEST ID ===


@app.middleware("http")
async def agregar_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])
    request.state.request_id = request_id
    logger.info(
        f"{request.method} {request.url.path}",
        extra={"request_id": request_id},
    )
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    logger.info(
        f"{request.method} {request.url.path} → {response.status_code}",
        extra={"request_id": request_id},
    )
    return response


# === ENDPOINTS ===

items = [{"id": 1, "nombre": "Widget"}]


@app.get("/items", tags=["Items"])
def listar(request: Request):
    logger.info(
        f"Listando {len(items)} items",
        extra={"request_id": request.state.request_id},
    )
    return items


@app.get("/items/{item_id}", tags=["Items"])
def obtener(item_id: int, request: Request):
    for item in items:
        if item["id"] == item_id:
            return item
    logger.warning(
        f"Item {item_id} no encontrado",
        extra={"request_id": request.state.request_id},
    )
    return {"error": "No encontrado"}


@app.get("/error", tags=["Debug"])
def provocar_error(request: Request):
    """Endpoint para demostrar logging de errores."""
    logger.error(
        "Error provocado intencionalmente",
        extra={
            "request_id": request.state.request_id,
            "extra_data": {"endpoint": "/error", "tipo": "demo"},
        },
    )
    return {"error": "Error de demostración"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
