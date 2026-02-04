"""
Ejercicio 01: CRUD de Biblioteca
=================================
Implementar un CRUD completo para gestión de libros.

OBJETIVO:
Practicar el patrón de modelos separados (Create/Update/Response) y CRUD completo.

INSTRUCCIONES:
1. Completar los modelos Pydantic:

   LibroCrear:
   - titulo: str, 1-200 caracteres
   - autor: str, 1-100 caracteres
   - genero: str, 1-50 caracteres
   - año: int, entre 1000 y 2030
   - paginas: int, mayor a 0

   LibroActualizar (todo opcional):
   - titulo: str opcional
   - autor: str opcional
   - genero: str opcional
   - año: int opcional
   - paginas: int opcional

   LibroResponse:
   - id: int
   - (todos los campos de LibroCrear)

2. Implementar endpoints:
   - GET    /libros           → Listar todos los libros
   - POST   /libros           → Crear libro (status 201)
   - GET    /libros/{id}      → Obtener libro (404 si no existe)
   - PUT    /libros/{id}      → Actualizar libro (update parcial)
   - DELETE /libros/{id}      → Eliminar libro (status 204)

PRUEBAS:
    uvicorn ejercicio_01:app --reload

    # Crear libro
    POST http://localhost:8000/libros
    Body: {"titulo": "Don Quijote", "autor": "Cervantes",
           "genero": "Novela", "año": 1605, "paginas": 863}

    # Actualizar solo el género
    PUT http://localhost:8000/libros/1
    Body: {"genero": "Clásico"}

PISTAS:
- Usa model_dump(exclude_none=True) para updates parciales
- HTTPException con status_code=404 para recursos no encontrados
- El modelo Update NO hereda de Base (todos los campos son opcionales)
"""

from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Biblioteca API",
    description="API de gestión de libros",
    version="1.0.0"
)


# =============================================================================
# MODELOS - TODO: Completar los modelos
# =============================================================================


class LibroBase(BaseModel):
    """Campos comunes de libro."""
    # TODO: Definir campos comunes
    pass


class LibroCrear(LibroBase):
    """Modelo para crear libro."""
    # TODO: Hereda de LibroBase
    pass


class LibroActualizar(BaseModel):
    """Modelo para actualizar (todo opcional)."""
    # TODO: Definir campos opcionales
    pass


class LibroResponse(LibroBase):
    """Modelo de respuesta con ID."""
    # TODO: Agregar campo id
    pass


# =============================================================================
# "BASE DE DATOS"
# =============================================================================


libros_db: dict[int, dict] = {}
contador_id = 0


def siguiente_id() -> int:
    """Genera siguiente ID."""
    global contador_id
    contador_id += 1
    return contador_id


# =============================================================================
# ENDPOINTS - TODO: Implementar
# =============================================================================


# TODO: GET /libros - Listar todos los libros
# response_model=list[LibroResponse]


# TODO: POST /libros - Crear libro
# response_model=LibroResponse, status_code=201


# TODO: GET /libros/{libro_id} - Obtener libro por ID
# Retornar 404 si no existe


# TODO: PUT /libros/{libro_id} - Actualizar libro
# Usar model_dump(exclude_none=True) para update parcial


# TODO: DELETE /libros/{libro_id} - Eliminar libro
# status_code=204, retornar None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
