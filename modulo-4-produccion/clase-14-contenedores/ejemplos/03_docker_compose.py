"""
Ejemplo 03: Docker Compose - Orquestación
===========================================
API + PostgreSQL + Redis en un solo comando.

docker-compose.yml:

    services:
      api:
        build: .
        ports:
          - "8000:8000"
        environment:
          - DATABASE_URL=postgresql://user:pass@db:5432/mydb
          - REDIS_URL=redis://redis:6379
        depends_on:
          db:
            condition: service_healthy
          redis:
            condition: service_started

      db:
        image: postgres:16-alpine
        environment:
          POSTGRES_USER: user
          POSTGRES_PASSWORD: pass
          POSTGRES_DB: mydb
        volumes:
          - pgdata:/var/lib/postgresql/data
        healthcheck:
          test: ["CMD-SHELL", "pg_isready -U user"]
          interval: 5s
          retries: 5

      redis:
        image: redis:7-alpine
        ports:
          - "6379:6379"

    volumes:
      pgdata:

Comandos:
    docker compose up -d          # Levantar todo
    docker compose logs -f api    # Ver logs de la API
    docker compose ps             # Estado de servicios
    docker compose down           # Parar todo
    docker compose down -v        # Parar y borrar volúmenes

Ejecutar sin Docker:
    uvicorn ejemplos.03_docker_compose:app --reload
"""

import os

from fastapi import FastAPI

app = FastAPI(title="API con Compose", version="1.0.0")


# === CONFIGURACIÓN DESDE ENV VARS ===

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///local.db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")


@app.get("/", tags=["Raíz"])
def raiz():
    return {"servicio": "api-compose", "status": "ok"}


@app.get("/config", tags=["Operaciones"])
def ver_config():
    """Muestra la configuración (sin secretos)."""
    return {
        "database": DATABASE_URL.split("@")[-1] if "@" in DATABASE_URL else DATABASE_URL,
        "redis": REDIS_URL,
        "entorno": os.getenv("ENVIRONMENT", "development"),
    }


@app.get("/health", tags=["Operaciones"])
def health():
    """Health check para Docker."""
    checks = {
        "api": "ok",
        "database": "configurada" if "postgresql" in DATABASE_URL else "sqlite",
        "redis": "configurado" if "redis" in REDIS_URL else "no",
    }
    return {"status": "healthy", "checks": checks}


@app.get("/servicios", tags=["Operaciones"])
def servicios():
    """Lista servicios del compose."""
    return {
        "servicios": [
            {"nombre": "api", "puerto": 8000, "estado": "running"},
            {"nombre": "db", "tipo": "PostgreSQL", "puerto": 5432},
            {"nombre": "redis", "tipo": "Redis", "puerto": 6379},
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
