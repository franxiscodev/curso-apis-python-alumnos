"""
Ejemplo 03: Path y Query Parameters
===================================
Diferentes tipos de parámetros en FastAPI.

Ejecutar:
    uvicorn 03_parametros:app --reload
"""

from fastapi import FastAPI, Path, Query

app = FastAPI(title="Parámetros")


# =============================================================================
# PATH PARAMETERS (en la URL)
# =============================================================================


@app.get("/items/{item_id}")
def obtener_item(item_id: int):
    """
    Path parameter básico.

    El tipo (int) se valida automáticamente.

    Ejemplos:
        GET /items/42   → {"item_id": 42}
        GET /items/abc  → Error 422 (no es int)
    """
    return {"item_id": item_id, "tipo": type(item_id).__name__}


@app.get("/usuarios/{usuario_id}/pedidos/{pedido_id}")
def obtener_pedido(usuario_id: int, pedido_id: int):
    """
    Múltiples path parameters.

    Ejemplo: GET /usuarios/5/pedidos/100
    """
    return {
        "usuario_id": usuario_id,
        "pedido_id": pedido_id
    }


@app.get("/archivos/{ruta_archivo:path}")
def obtener_archivo(ruta_archivo: str):
    """
    Path parameter con barras (path converter).

    Ejemplo: GET /archivos/home/user/documento.txt
    """
    return {"ruta": ruta_archivo}


# =============================================================================
# PATH CON VALIDACIÓN (Path())
# =============================================================================


@app.get("/productos/{producto_id}")
def obtener_producto(
    producto_id: int = Path(
        title="ID del Producto",
        description="Identificador único del producto",
        ge=1,      # Mayor o igual a 1
        le=10000,  # Menor o igual a 10000
        examples=[1, 42, 100]
    )
):
    """
    Path parameter con validación.

    - ge=1: debe ser >= 1
    - le=10000: debe ser <= 10000
    """
    return {"producto_id": producto_id}


# =============================================================================
# QUERY PARAMETERS (después del ?)
# =============================================================================


@app.get("/items")
def listar_items(skip: int = 0, limit: int = 10):
    """
    Query parameters con valores por defecto.

    Ejemplos:
        GET /items                → skip=0, limit=10
        GET /items?skip=5         → skip=5, limit=10
        GET /items?limit=20       → skip=0, limit=20
        GET /items?skip=5&limit=3 → skip=5, limit=3
    """
    return {
        "skip": skip,
        "limit": limit,
        "mensaje": f"Mostrando items {skip} a {skip + limit}"
    }


@app.get("/buscar")
def buscar(q: str):
    """
    Query parameter requerido (sin valor por defecto).

    Ejemplos:
        GET /buscar           → Error 422 (falta q)
        GET /buscar?q=laptop  → {"query": "laptop"}
    """
    return {"query": q}


@app.get("/filtrar")
def filtrar(
    categoria: str | None = None,
    precio_min: float | None = None,
    precio_max: float | None = None,
    disponible: bool = True
):
    """
    Múltiples query parameters opcionales.

    Ejemplos:
        GET /filtrar
        GET /filtrar?categoria=laptops
        GET /filtrar?precio_min=100&precio_max=500
        GET /filtrar?disponible=false
    """
    filtros = {
        "categoria": categoria,
        "precio_min": precio_min,
        "precio_max": precio_max,
        "disponible": disponible
    }
    # Remover valores None
    filtros_activos = {k: v for k, v in filtros.items() if v is not None}
    return {"filtros": filtros_activos}


# =============================================================================
# QUERY CON VALIDACIÓN (Query())
# =============================================================================


@app.get("/productos")
def listar_productos(
    q: str | None = Query(
        default=None,
        min_length=3,
        max_length=50,
        title="Búsqueda",
        description="Término de búsqueda (3-50 caracteres)"
    ),
    page: int = Query(default=1, ge=1, description="Número de página"),
    size: int = Query(default=10, ge=1, le=100, description="Items por página")
):
    """
    Query parameters con validación avanzada.

    Validaciones:
        - q: 3-50 caracteres (si se proporciona)
        - page: >= 1
        - size: 1-100
    """
    return {
        "busqueda": q,
        "pagina": page,
        "tamaño": size
    }


@app.get("/tags")
def obtener_tags(
    tags: list[str] = Query(
        default=[],
        description="Lista de tags para filtrar"
    )
):
    """
    Query parameter como lista.

    Ejemplo: GET /tags?tags=python&tags=fastapi&tags=api
    """
    return {"tags": tags, "cantidad": len(tags)}


# =============================================================================
# COMBINANDO PATH Y QUERY
# =============================================================================


@app.get("/usuarios/{usuario_id}/items")
def items_de_usuario(
    usuario_id: int = Path(ge=1),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)
):
    """
    Combina path y query parameters.

    Ejemplo: GET /usuarios/5/items?skip=10&limit=20
    """
    return {
        "usuario_id": usuario_id,
        "skip": skip,
        "limit": limit
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
