"""
Ejercicio 01: Dockerfile para una API
=======================================
Escribir un Dockerfile para containerizar esta API.

OBJETIVO:
Practicar la creación de Dockerfiles básicos.

INSTRUCCIONES:
1. Escribir un Dockerfile (en el docstring o archivo separado) que:
   - Use python:3.11-slim como base
   - Copie requirements.txt e instale dependencias
   - Copie el código de la app
   - Exponga el puerto 8000
   - Use uvicorn como comando de inicio

2. Agregar endpoint GET /health que retorne {"status": "ok"}

3. Agregar endpoint GET /info con nombre de app y versión

PRUEBAS:
    uvicorn ejercicio_01:app --reload

    # Con Docker:
    docker build -t ejercicio01 .
    docker run -p 8000:8000 ejercicio01

PISTAS:
- FROM python:3.11-slim
- WORKDIR /app
- COPY requirements.txt primero (caché)
- RUN pip install --no-cache-dir -r requirements.txt
- CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

from fastapi import FastAPI

app = FastAPI(title="API Containerizada", version="1.0.0")

# TODO: Dockerfile en docstring o archivo separado

# TODO: GET /health (retorna status ok)

# TODO: GET /info (nombre de app, versión)

# TODO: GET /items (listar items de ejemplo)

# TODO: POST /items (crear item)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
