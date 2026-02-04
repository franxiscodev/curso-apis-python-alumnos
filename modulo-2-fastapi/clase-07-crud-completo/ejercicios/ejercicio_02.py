"""
Ejercicio 02: Paginación y Filtros
====================================
Extender una API de libros con paginación y filtrado.

OBJETIVO:
Practicar paginación con metadata y query params de filtrado.

INSTRUCCIONES:
1. Completar el modelo LibrosPaginados con metadata (total, page, size, pages)

2. Implementar GET /libros con:
   - Paginación: page (default 1), size (default 10, max 50)
   - Filtro por autor (opcional, búsqueda parcial case-insensitive)
   - Filtro por género (opcional, exacto)
   - Filtro por rango de año: año_min, año_max (opcionales)
   - Ordenamiento: sort_by (titulo/autor/año), order (asc/desc)

3. La respuesta debe incluir metadata de paginación

PRUEBAS:
    uvicorn ejercicio_02:app --reload

    # Listar con paginación
    GET http://localhost:8000/libros?page=1&size=5

    # Filtrar por autor
    GET http://localhost:8000/libros?autor=García

    # Filtrar por género y ordenar
    GET http://localhost:8000/libros?genero=Novela&sort_by=año&order=desc

PISTAS:
- Usa math.ceil(total / size) para calcular total de páginas
- Para búsqueda parcial: "buscar".lower() in campo.lower()
- Aplica filtros primero, luego ordena, luego pagina
"""

import math
from typing import Literal

from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Biblioteca API v2",
    description="API con paginación y filtros",
    version="2.0.0"
)


# =============================================================================
# MODELOS
# =============================================================================


class LibroBase(BaseModel):
    """Campos comunes de libro."""
    titulo: str = Field(min_length=1, max_length=200)
    autor: str = Field(min_length=1, max_length=100)
    genero: str = Field(min_length=1, max_length=50)
    año: int = Field(ge=1000, le=2030)
    paginas: int = Field(gt=0)


class LibroCrear(LibroBase):
    """Modelo para crear libro."""
    pass


class LibroResponse(LibroBase):
    """Modelo de respuesta."""
    id: int


class LibrosPaginados(BaseModel):
    """Respuesta paginada de libros."""
    # TODO: Definir campos: items, total, page, size, pages
    pass


# =============================================================================
# "BASE DE DATOS" CON DATOS INICIALES
# =============================================================================


libros_db: dict[int, dict] = {}
contador_id = 0


def siguiente_id() -> int:
    """Genera siguiente ID."""
    global contador_id
    contador_id += 1
    return contador_id


def inicializar_datos():
    """Crea libros de ejemplo."""
    libros = [
        LibroCrear(titulo="Cien Años de Soledad", autor="Gabriel García Márquez",
                   genero="Novela", año=1967, paginas=471),
        LibroCrear(titulo="Don Quijote", autor="Miguel de Cervantes",
                   genero="Clásico", año=1605, paginas=863),
        LibroCrear(titulo="El Principito", autor="Antoine de Saint-Exupéry",
                   genero="Fábula", año=1943, paginas=96),
        LibroCrear(titulo="La Casa de los Espíritus", autor="Isabel Allende",
                   genero="Novela", año=1982, paginas=433),
        LibroCrear(titulo="Rayuela", autor="Julio Cortázar",
                   genero="Novela", año=1963, paginas=600),
        LibroCrear(titulo="El Amor en los Tiempos del Cólera",
                   autor="Gabriel García Márquez", genero="Novela",
                   año=1985, paginas=348),
        LibroCrear(titulo="Pedro Páramo", autor="Juan Rulfo",
                   genero="Novela", año=1955, paginas=124),
        LibroCrear(titulo="Ficciones", autor="Jorge Luis Borges",
                   genero="Cuento", año=1944, paginas=174),
    ]
    for libro in libros:
        nuevo_id = siguiente_id()
        libros_db[nuevo_id] = {"id": nuevo_id, **libro.model_dump()}


inicializar_datos()


# =============================================================================
# ENDPOINTS - TODO: Implementar
# =============================================================================


# TODO: GET /libros - Listar con paginación, filtros y ordenamiento
# Parámetros:
#   - autor: str | None (búsqueda parcial case-insensitive)
#   - genero: str | None (filtro exacto)
#   - año_min: int | None
#   - año_max: int | None
#   - sort_by: Literal["titulo", "autor", "año"] = "titulo"
#   - order: Literal["asc", "desc"] = "asc"
#   - page: int = 1 (ge=1)
#   - size: int = 10 (ge=1, le=50)
# Response: LibrosPaginados


# TODO: GET /libros/{libro_id} - Obtener por ID (404 si no existe)


# TODO: GET /generos - Listar géneros disponibles (set de géneros únicos)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
