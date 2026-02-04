# Docker y CI/CD - Cheatsheet

Guía rápida de Docker, Compose y GitHub Actions.

---

## Dockerfile Básico

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Multi-stage Build

```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim
RUN useradd --create-home appuser
USER appuser
WORKDIR /app
COPY --from=builder /install /usr/local
COPY --chown=appuser:appuser . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## .dockerignore

```
__pycache__
*.pyc
.git
.env
.venv
tests/
*.md
.mypy_cache
.pytest_cache
```

---

## Comandos Docker

```bash
# Construir
docker build -t mi-api .
docker build -t mi-api:v1.0 .

# Ejecutar
docker run -p 8000:8000 mi-api
docker run -d --name api -p 8000:8000 mi-api    # Background
docker run --env-file .env -p 8000:8000 mi-api   # Con env vars

# Gestión
docker ps                    # Contenedores activos
docker logs api              # Ver logs
docker stop api              # Parar
docker rm api                # Eliminar
docker images                # Listar imágenes
docker rmi mi-api            # Eliminar imagen
```

---

## Docker Compose

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      db:
        condition: service_healthy

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

volumes:
  pgdata:
```

---

## Comandos Compose

```bash
docker compose up -d          # Levantar en background
docker compose up --build     # Reconstruir + levantar
docker compose logs -f        # Ver logs en vivo
docker compose logs -f api    # Solo logs de api
docker compose ps             # Estado
docker compose stop           # Parar
docker compose down           # Parar + eliminar
docker compose down -v        # + eliminar volúmenes
```

---

## GitHub Actions Workflow

```yaml
name: CI/CD
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt && pip install pytest
      - run: pytest -v

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - uses: docker/build-push-action@v5
        with:
          push: false
          tags: mi-api:latest
```

---

## Variables de Entorno en Python

```python
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///local.db"
    secret_key: str = "dev-key"
    debug: bool = False

    model_config = {"env_prefix": "APP_"}

settings = Settings()
# Lee APP_DATABASE_URL, APP_SECRET_KEY, APP_DEBUG
```

---

## Tips

1. **Orden en Dockerfile**: dependencias antes, código después (caché)
2. **Multi-stage**: siempre para producción (imágenes más pequeñas)
3. **No root**: usar `USER appuser` en producción
4. **Secretos**: env vars o GitHub Secrets, NUNCA en código
5. **Health checks**: siempre tener `/health` endpoint
6. **.dockerignore**: excluir .git, __pycache__, .env, tests
