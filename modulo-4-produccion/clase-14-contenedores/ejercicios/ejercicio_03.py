"""
Ejercicio 03: Pipeline CI/CD Completo
=======================================
Configurar GitHub Actions para tests + build.

OBJETIVO:
Practicar la configuración de CI/CD.

INSTRUCCIONES:
1. Escribir un workflow .github/workflows/ci.yml (en docstring):
   - Trigger en push a main y pull_request
   - Job 'test': instalar deps, correr pytest
   - Job 'build': construir imagen Docker (solo en main)

2. Implementar API con endpoints testeables

3. Agregar endpoint GET /version que muestre:
   - Commit SHA (de env GITHUB_SHA)
   - Branch (de env GITHUB_REF)
   - Build number (de env GITHUB_RUN_NUMBER)

4. Escribir al menos 3 tests inline para la API

PRUEBAS:
    uvicorn ejercicio_03:app --reload
    pytest ejercicio_03.py -v

PISTAS:
- os.getenv("GITHUB_SHA", "local")
- actions/checkout@v4, actions/setup-python@v5
- needs: test para que build dependa de test
"""

import os

from fastapi import FastAPI

app = FastAPI(title="API CI/CD", version="1.0.0")

# TODO: Workflow YAML en docstring

# TODO: GET / (raíz con status)

# TODO: GET /version (info del build desde env vars)

# TODO: GET /sumar?a=1&b=2 (endpoint testeable)

# TODO: Tests inline con TestClient


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
