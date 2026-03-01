"""
Ejercicio 02: Paginación y Filtros - SOLUCIÓN
===============================================
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
    items: list[LibroResponse]
    total: int
    page: int
    size: int
    pages: int


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
# ENDPOINTS
# =============================================================================


@app.get("/libros", response_model=LibrosPaginados, tags=["Libros"])
def listar_libros(
    autor: str | None = Query(
        default=None, description="Buscar por autor (parcial)"
    ),
    genero: str | None = Query(
        default=None, description="Filtrar por género exacto"
    ),
    año_min: int | None = Query(
        default=None, ge=1000, description="Año mínimo"
    ),
    año_max: int | None = Query(
        default=None, le=2030, description="Año máximo"
    ),
    sort_by: Literal["titulo", "autor", "año"] = Query(
        default="titulo", description="Ordenar por campo"
    ),
    order: Literal["asc", "desc"] = Query(
        default="asc", description="Dirección del orden"
    ),
    page: int = Query(default=1, ge=1, description="Página"),
    size: int = Query(default=10, ge=1, le=50, description="Items por página")
):
    """Listar libros con filtros, ordenamiento y paginación."""
    resultados = list(libros_db.values())

    # Filtrar por autor (búsqueda parcial case-insensitive)
    if autor:
        autor_lower = autor.lower()
        resultados = [l for l in resultados if autor_lower in l["autor"].lower()]

    # Filtrar por género exacto
    if genero:
        resultados = [l for l in resultados if l["genero"] == genero]

    # Filtrar por rango de año
    if año_min is not None:
        resultados = [l for l in resultados if l["año"] >= año_min]

    if año_max is not None:
        resultados = [l for l in resultados if l["año"] <= año_max]

    # Ordenar
    resultados.sort(key=lambda l: l[sort_by], reverse=(order == "desc"))

    # Paginar
    total = len(resultados)
    pages = math.ceil(total / size) if total > 0 else 0
    start = (page - 1) * size

    return {
        "items": resultados[start:start + size],
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }


@app.get("/libros/{libro_id}", response_model=LibroResponse, tags=["Libros"])
def obtener_libro(libro_id: int = Path(ge=1)):
    """Obtener libro por ID."""
    if libro_id not in libros_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con ID {libro_id} no encontrado"
        )
    return libros_db[libro_id]


@app.get("/generos", response_model=list[str], tags=["Utilidades"])
def listar_generos():
    """Listar géneros disponibles."""
    return sorted(set(l["genero"] for l in libros_db.values()))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
