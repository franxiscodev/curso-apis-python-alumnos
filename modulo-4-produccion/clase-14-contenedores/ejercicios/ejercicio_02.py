"""
Ejercicio 02: Docker Compose con Base de Datos
================================================
Orquestar API + PostgreSQL con Docker Compose.

OBJETIVO:
Practicar Docker Compose con múltiples servicios.

INSTRUCCIONES:
1. Escribir un docker-compose.yml (en docstring) que defina:
   - Servicio 'api': build desde Dockerfile, puerto 8000
   - Servicio 'db': imagen postgres:16-alpine, con healthcheck
   - Volumen para persistir datos de PostgreSQL

2. Implementar la API que lee DATABASE_URL de env var

3. Agregar endpoints:
   - GET /health (incluir check de config DB)
   - GET /config (mostrar tipo de DB configurada, sin secretos)
   - GET /servicios (listar servicios del compose)

PRUEBAS:
    uvicorn ejercicio_02:app --reload

    # Con Docker:
    docker compose up -d
    docker compose logs -f

PISTAS:
- os.getenv("DATABASE_URL", "sqlite:///local.db")
- depends_on con condition: service_healthy
- POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB como env vars
"""

import os

from fastapi import FastAPI

app = FastAPI(title="API con Compose", version="1.0.0")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///local.db")

# TODO: docker-compose.yml en docstring

# TODO: GET /health (check de DB configurada)

# TODO: GET /config (tipo de DB, sin exponer secretos)

# TODO: GET /servicios (listar servicios del stack)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
