"""
Ejemplo 04: GitHub Actions - Pipeline CI/CD
=============================================
Workflow de CI/CD para API FastAPI.

.github/workflows/ci.yml:

    name: CI/CD Pipeline

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

          - name: Setup Python
            uses: actions/setup-python@v5
            with:
              python-version: "3.11"

          - name: Install dependencies
            run: |
              pip install -r requirements.txt
              pip install pytest pytest-cov

          - name: Run tests
            run: pytest --cov=app --cov-report=xml -v

          - name: Upload coverage
            uses: codecov/codecov-action@v3
            with:
              file: ./coverage.xml

      build:
        needs: test
        runs-on: ubuntu-latest
        if: github.ref == 'refs/heads/main'
        steps:
          - uses: actions/checkout@v4

          - name: Login to Docker Hub
            uses: docker/login-action@v3
            with:
              username: ${{ secrets.DOCKER_USERNAME }}
              password: ${{ secrets.DOCKER_PASSWORD }}

          - name: Build and push
            uses: docker/build-push-action@v5
            with:
              push: true
              tags: usuario/mi-api:latest

Secretos necesarios en GitHub:
    - DOCKER_USERNAME: usuario de Docker Hub
    - DOCKER_PASSWORD: token de Docker Hub

Ejecutar sin Docker:
    uvicorn ejemplos.04_github_actions:app --reload
"""

import os
from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(title="API con CI/CD", version="1.0.0")

# === VARIABLES DEL PIPELINE ===

BUILD_SHA = os.getenv("GITHUB_SHA", "local")
BUILD_REF = os.getenv("GITHUB_REF", "local")
BUILD_RUN = os.getenv("GITHUB_RUN_NUMBER", "0")


@app.get("/", tags=["Raíz"])
def raiz():
    return {"servicio": "api-cicd", "status": "ok"}


@app.get("/version", tags=["Operaciones"])
def version():
    """Información del build (inyectada por CI/CD)."""
    return {
        "commit": BUILD_SHA[:7] if len(BUILD_SHA) > 7 else BUILD_SHA,
        "branch": BUILD_REF,
        "build_number": BUILD_RUN,
        "deployed_at": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/health", tags=["Operaciones"])
def health():
    return {"status": "healthy", "commit": BUILD_SHA[:7]}


# === ENDPOINTS DE EJEMPLO (para testear en CI) ===


@app.get("/sumar", tags=["Ejemplo"])
def sumar(a: int, b: int):
    """Endpoint simple para demostrar tests en CI."""
    return {"resultado": a + b}


@app.get("/echo/{mensaje}", tags=["Ejemplo"])
def echo(mensaje: str):
    """Echo para tests."""
    return {"mensaje": mensaje}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
