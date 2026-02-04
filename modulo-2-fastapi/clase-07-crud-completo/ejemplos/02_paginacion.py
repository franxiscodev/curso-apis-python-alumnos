"""
Paginación con Metadata
========================
Paginación offset con respuesta que incluye metadata.

Ejecutar:
    uvicorn ejemplos.02_paginacion:app --reload

Conceptos:
    - Modelo PaginatedResponse con metadata
    - Query params page/size con validación
    - Cálculo de total de páginas
    - Datos iniciales para demostración
"""

import math

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Paginación Demo", version="1.0.0")


# =============================================================================
# MODELOS
# =============================================================================


class Articulo(BaseModel):
    """Modelo de artículo."""
    id: int
    titulo: str
    autor: str
    categoria: str


class PaginatedResponse(BaseModel):
    """Respuesta paginada con metadata."""
    items: list[Articulo]
    total: int = Field(description="Total de registros")
    page: int = Field(description="Página actual")
    size: int = Field(description="Items por página")
    pages: int = Field(description="Total de páginas")


# =============================================================================
# DATOS DE EJEMPLO
# =============================================================================


articulos_db: list[dict] = [
    {"id": i, "titulo": f"Artículo {i}", "autor": f"Autor {(i % 5) + 1}",
     "categoria": ["Python", "FastAPI", "Data Science", "ML", "DevOps"][i % 5]}
    for i in range(1, 51)  # 50 artículos de ejemplo
]


# =============================================================================
# HELPER DE PAGINACIÓN
# =============================================================================


def paginar(items: list, page: int, size: int) -> dict:
    """Aplica paginación y retorna items con metadata."""
    total = len(items)
    pages = math.ceil(total / size) if total > 0 else 0
    start = (page - 1) * size
    end = start + size

    return {
        "items": items[start:end],
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }


# =============================================================================
# ENDPOINTS
# =============================================================================


@app.get("/articulos", response_model=PaginatedResponse, tags=["Artículos"])
def listar_articulos(
    page: int = Query(default=1, ge=1, description="Número de página"),
    size: int = Query(default=10, ge=1, le=100, description="Items por página")
):
    """
    Listar artículos con paginación.

    - **page**: Número de página (desde 1)
    - **size**: Cantidad de items por página (1-100)
    """
    return paginar(articulos_db, page, size)


@app.get("/articulos/sin-paginar", response_model=list[Articulo], tags=["Artículos"])
def listar_sin_paginar():
    """Listar todos los artículos (sin paginación, para comparar)."""
    return articulos_db


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
