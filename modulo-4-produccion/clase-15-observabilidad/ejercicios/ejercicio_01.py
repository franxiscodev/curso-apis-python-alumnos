"""
Ejercicio 01: Agregar Logging a una API
=========================================
Implementar logging estructurado en JSON.

INSTRUCCIONES:
1. Crear un JSONFormatter que emita logs como JSON
2. Agregar middleware que:
   - Genere un request_id (UUID corto)
   - Logee cada request entrante y su respuesta
3. Usar el logger en los endpoints

PRUEBAS:
    uvicorn ejercicio_01:app --reload
    Observar los logs JSON en la terminal

PISTAS:
- json.dumps({...}) para formatear
- uuid.uuid4() para generar IDs
- request.state para pasar datos entre middleware y endpoint
"""

import logging

from fastapi import FastAPI, Request

app = FastAPI(title="API con Logging", version="1.0.0")

# TODO: Crear JSONFormatter

# TODO: Configurar logger con el formatter

# TODO: Middleware que genera request_id y logea requests

items = [{"id": 1, "nombre": "Widget", "precio": 9.99}]


@app.get("/items", tags=["Items"])
def listar():
    # TODO: Agregar logging
    return items


@app.post("/items", status_code=201, tags=["Items"])
def crear(nombre: str, precio: float):
    nuevo = {"id": len(items) + 1, "nombre": nombre, "precio": precio}
    items.append(nuevo)
    # TODO: Logear creación
    return nuevo


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
