"""
Ejercicio 02: Tests de Endpoints CRUD
=======================================
Testear una API CRUD con TestClient.

INSTRUCCIONES:
1. Escribir tests para todos los endpoints de la API
2. Testear happy path y edge cases (404, 422)
3. Usar fixtures para setup

Ejecutar: pytest ejercicios/ejercicio_02.py -v
"""

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel

# === API ===

app = FastAPI()
libros: dict[int, dict] = {}
next_id = 1


class LibroCrear(BaseModel):
    titulo: str
    autor: str
    paginas: int


@app.get("/libros")
def listar():
    return list(libros.values())


@app.get("/libros/{libro_id}")
def obtener(libro_id: int):
    if libro_id not in libros:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libros[libro_id]


@app.post("/libros", status_code=201)
def crear(libro: LibroCrear):
    global next_id
    nuevo = {"id": next_id, **libro.model_dump()}
    libros[next_id] = nuevo
    next_id += 1
    return nuevo


@app.delete("/libros/{libro_id}", status_code=204)
def eliminar(libro_id: int):
    if libro_id not in libros:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    del libros[libro_id]


# TODO: Fixture que resetea los libros antes de cada test

# TODO: test_listar_vacio

# TODO: test_crear_libro

# TODO: test_obtener_libro

# TODO: test_obtener_libro_no_existe (404)

# TODO: test_crear_libro_invalido (422)

# TODO: test_eliminar_libro

# TODO: test_eliminar_libro_no_existe (404)
