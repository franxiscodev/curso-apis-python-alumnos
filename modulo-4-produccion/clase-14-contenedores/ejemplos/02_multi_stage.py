"""
Ejemplo 02: Multi-stage Build y Optimización
==============================================
Dockerfile optimizado con multi-stage.

Dockerfile multi-stage:

    # === ETAPA 1: Builder ===
    FROM python:3.11-slim AS builder

    WORKDIR /build
    COPY requirements.txt .
    RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

    # === ETAPA 2: Runtime ===
    FROM python:3.11-slim

    # Usuario no-root (seguridad)
    RUN useradd --create-home appuser
    USER appuser

    WORKDIR /app

    # Copiar solo las dependencias instaladas
    COPY --from=builder /install /usr/local

    # Copiar código
    COPY --chown=appuser:appuser . .

    EXPOSE 8000

    # Health check
    HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
        CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

.dockerignore (guardar como '.dockerignore'):

    __pycache__
    *.pyc
    .git
    .env
    .venv
    tests/
    docs/
    *.md
    .mypy_cache
    .pytest_cache

Comparación de tamaños:
    - Sin multi-stage:  ~1.0 GB
    - Con multi-stage:  ~200 MB
    - Con slim + multi: ~150 MB

Ejecutar sin Docker:
    uvicorn ejemplos.02_multi_stage:app --reload
"""

import os

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="API Optimizada", version="1.0.0")


class Config(BaseModel):
    """Configuración desde variables de entorno."""
    app_name: str = os.getenv("APP_NAME", "mi-api")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    version: str = os.getenv("APP_VERSION", "1.0.0")


config = Config()


@app.get("/health", tags=["Operaciones"])
def health():
    """Health check para Docker HEALTHCHECK."""
    return {"status": "healthy"}


@app.get("/info", tags=["Operaciones"])
def info():
    """Información del servicio."""
    return {
        "app": config.app_name,
        "version": config.version,
        "debug": config.debug,
        "python_path": os.getenv("PYTHONPATH", "no definido"),
    }


@app.get("/", tags=["Raíz"])
def raiz():
    return {"servicio": config.app_name, "version": config.version}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
