"""
Ejercicio 02: Path y Query Parameters - SOLUCIÓN
=================================================
"""

from fastapi import FastAPI, Path, Query
from typing import Literal

app = FastAPI(title="Películas API")


@app.get("/peliculas")
def listar_peliculas(
    genero: str | None = Query(
        default=None,
        description="Filtrar por género"
    ),
    año_min: int | None = Query(
        default=None,
        ge=1900,
        description="Año mínimo de estreno"
    ),
    año_max: int | None = Query(
        default=None,
        le=2030,
        description="Año máximo de estreno"
    ),
    ordenar: Literal["titulo", "año", "rating"] = Query(
        default="titulo",
        description="Campo por el cual ordenar"
    ),
    page: int = Query(
        default=1,
        ge=1,
        description="Número de página"
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
        description="Resultados por página"
    )
):
    """Listar películas con filtros y paginación."""
    return {
        "filtros": {
            "genero": genero,
            "año_min": año_min,
            "año_max": año_max
        },
        "ordenar": ordenar,
        "paginacion": {
            "page": page,
            "limit": limit
        },
        "mensaje": "Lista de películas con filtros aplicados"
    }


@app.get("/peliculas/{pelicula_id}")
def obtener_pelicula(
    pelicula_id: int = Path(
        ge=1,
        title="ID de Película",
        description="ID único de la película"
    )
):
    """Obtener una película por su ID."""
    return {
        "pelicula_id": pelicula_id,
        "mensaje": f"Obteniendo película con ID: {pelicula_id}"
    }


@app.get("/peliculas/{pelicula_id}/actores")
def obtener_actores(
    pelicula_id: int = Path(
        ge=1,
        title="ID de Película",
        description="ID único de la película"
    ),
    principal: bool | None = Query(
        default=None,
        description="Si True, solo actores principales"
    )
):
    """Obtener actores de una película."""
    return {
        "pelicula_id": pelicula_id,
        "filtro_principal": principal,
        "mensaje": f"Actores de película {pelicula_id}" + (
            " (solo principales)" if principal else ""
        )
    }


@app.get("/buscar")
def buscar(
    q: str = Query(
        min_length=2,
        max_length=100,
        title="Término de búsqueda",
        description="Texto a buscar (2-100 caracteres)"
    ),
    en_titulo: bool = Query(
        default=True,
        description="Buscar en títulos"
    ),
    en_sinopsis: bool = Query(
        default=False,
        description="Buscar en sinopsis"
    )
):
    """Buscar películas por texto."""
    return {
        "query": q,
        "buscar_en": {
            "titulo": en_titulo,
            "sinopsis": en_sinopsis
        },
        "mensaje": f"Buscando '{q}' en " + ", ".join(
            campo for campo, activo in [
                ("títulos", en_titulo),
                ("sinopsis", en_sinopsis)
            ] if activo
        )
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
