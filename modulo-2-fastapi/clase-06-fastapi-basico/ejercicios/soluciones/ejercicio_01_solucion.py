"""
Ejercicio 01: Endpoints Básicos - SOLUCIÓN
==========================================
"""

from fastapi import FastAPI

app = FastAPI(title="Biblioteca API")


@app.get("/")
def raiz():
    """Endpoint raíz de la API."""
    return {
        "metodo": "GET",
        "endpoint": "/",
        "mensaje": "Bienvenido a la Biblioteca API"
    }


@app.get("/libros")
def listar_libros():
    """Listar todos los libros."""
    return {
        "metodo": "GET",
        "endpoint": "/libros",
        "mensaje": "Listando todos los libros"
    }


@app.post("/libros")
def crear_libro():
    """Crear un nuevo libro."""
    return {
        "metodo": "POST",
        "endpoint": "/libros",
        "mensaje": "Creando nuevo libro"
    }


@app.get("/libros/{libro_id}")
def obtener_libro(libro_id: int):
    """Obtener un libro por su ID."""
    return {
        "metodo": "GET",
        "endpoint": "/libros/{id}",
        "mensaje": f"Obteniendo libro con ID: {libro_id}"
    }


@app.put("/libros/{libro_id}")
def actualizar_libro(libro_id: int):
    """Actualizar un libro existente."""
    return {
        "metodo": "PUT",
        "endpoint": "/libros/{id}",
        "mensaje": f"Actualizando libro con ID: {libro_id}"
    }


@app.delete("/libros/{libro_id}")
def eliminar_libro(libro_id: int):
    """Eliminar un libro."""
    return {
        "metodo": "DELETE",
        "endpoint": "/libros/{id}",
        "mensaje": f"Eliminando libro con ID: {libro_id}"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
