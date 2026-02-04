---
marp: true
theme: default
paginate: true
header: 'Clase 14: Containerización y CI/CD'
footer: 'Curso APIs Avanzadas con Python'
---

# Containerización y CI/CD
## Docker, Compose y GitHub Actions

Clase 14 - Módulo 4: Producción y Escalabilidad

---

# ¿Por qué Docker?

| Sin Docker | Con Docker |
|------------|-----------|
| "Funciona en mi máquina" | Funciona en todas |
| Instalar Python manualmente | Todo incluido |
| Conflictos de versiones | Entorno aislado |
| Setup diferente por dev | Un comando: `docker run` |

---

# Dockerfile Básico

```dockerfile
FROM python:3.11-slim
WORKDIR /app

# Dependencias primero (caché)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código después
COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t mi-api .
docker run -p 8000:8000 mi-api
```

---

# Capas y Caché

```
COPY requirements.txt .     ← Capa 1 (se cachea)
RUN pip install ...          ← Capa 2 (se cachea si req no cambia)
COPY . .                     ← Capa 3 (cambia con cada edit)
```

El orden importa: **dependencias antes, código después**

---

# Multi-stage Build

```dockerfile
# Etapa 1: Builder
FROM python:3.11-slim AS builder
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# Etapa 2: Runtime
FROM python:3.11-slim
COPY --from=builder /install /usr/local
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

| | Sin multi-stage | Con multi-stage |
|-|----------------|-----------------|
| Tamaño | ~1 GB | ~200 MB |

---

# Docker Compose

```yaml
services:
  api:
    build: .
    ports: ["8000:8000"]
    depends_on:
      db: { condition: service_healthy }

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: pass
    healthcheck:
      test: ["CMD", "pg_isready"]
```

```bash
docker compose up -d
```

---

# Variables de Entorno

```python
import os
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///local.db")
SECRET_KEY = os.getenv("SECRET_KEY")  # Nunca hardcoded
```

```yaml
# docker-compose.yml
environment:
  - DATABASE_URL=postgresql://user:pass@db:5432/mydb
  - SECRET_KEY=${SECRET_KEY}  # Desde .env
```

**NUNCA** poner secretos en el Dockerfile ni en el código

---

# GitHub Actions

```yaml
name: CI/CD
on:
  push: { branches: [main] }

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install -r requirements.txt
      - run: pytest -v

  build:
    needs: test
    steps:
      - uses: docker/build-push-action@v5
```

---

# Flujo CI/CD

```
Push → Tests → Build → Deploy
  │       │       │       │
  │    pytest   Docker   Servidor
  │    linting  image
  │    coverage push
```

Si los tests fallan → el build NO se ejecuta

---

# Resumen

| Concepto | Herramienta |
|----------|-------------|
| Containerizar | `Dockerfile` |
| Optimizar | Multi-stage build |
| Orquestar | `docker-compose.yml` |
| CI/CD | GitHub Actions |
| Secretos | Env vars / GitHub Secrets |
| Health check | `HEALTHCHECK` + `/health` |

---

# Próxima Clase

**Clase 15: Observabilidad y Proyecto Integrador**

- Logging estructurado
- Métricas y monitoring
- Proyecto final integrando todo

---

# Recursos

- **Docker docs**: https://docs.docker.com
- **GitHub Actions**: https://docs.github.com/en/actions
- **FastAPI Docker**: https://fastapi.tiangolo.com/deployment/docker/

**Practica:**
```bash
uvicorn ejemplos.api_produccion:app --reload
```
