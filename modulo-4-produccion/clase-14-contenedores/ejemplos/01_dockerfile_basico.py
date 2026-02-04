"""
Ejemplo 01: Dockerfile Básico para FastAPI
============================================
API simple con su Dockerfile correspondiente.

Dockerfile (guardar como 'Dockerfile' en la raíz del proyecto):

    # Imagen base
    FROM python:3.11-slim

    # Directorio de trabajo
    WORKDIR /app

    # Copiar dependencias primero (caché de capas)
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    # Copiar código
    COPY . .

    # Puerto
    EXPOSE 8000

    # Comando de inicio
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

Construir y ejecutar:
    docker build -t mi-api .
    docker run -p 8000:8000 mi-api

Ejecutar sin Docker:
    uvicorn ejemplos.01_dockerfile_basico:app --reload
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="API Containerizada", version="1.0.0")


class Item(BaseModel):
    nombre: str
    precio: float


items: list[dict] = [
    {"id": 1, "nombre": "Widget", "precio": 9.99},
    {"id": 2, "nombre": "Gadget", "precio": 19.99},
]


@app.get("/", tags=["Raíz"])
def raiz():
    """Health check básico."""
    return {"status": "ok", "servicio": "mi-api"}


@app.get("/items", tags=["Items"])
def listar():
    """Lista todos los items."""
    return items


@app.post("/items", status_code=201, tags=["Items"])
def crear(item: Item):
    """Crea un item nuevo."""
    nuevo = {"id": len(items) + 1, **item.model_dump()}
    items.append(nuevo)
    return nuevo


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
