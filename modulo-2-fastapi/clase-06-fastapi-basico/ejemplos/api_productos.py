"""
API de Productos Completa
=========================
Ejemplo completo que combina todos los conceptos.

Ejecutar:
    uvicorn api_productos:app --reload

Endpoints:
    GET    /productos           - Listar productos
    GET    /productos/{id}      - Obtener producto
    POST   /productos           - Crear producto
    PUT    /productos/{id}      - Actualizar producto
    DELETE /productos/{id}      - Eliminar producto
"""

from fastapi import FastAPI, HTTPException, Query, Path, status
from pydantic import BaseModel, Field


# =============================================================================
# APLICACIÓN
# =============================================================================


app = FastAPI(
    title="API de Productos",
    description="API REST completa para gestión de productos",
    version="1.0.0",
    contact={
        "name": "Curso APIs Python",
        "email": "curso@ejemplo.com"
    }
)


# =============================================================================
# MODELOS
# =============================================================================


class ProductoBase(BaseModel):
    """Campos comunes de producto."""
    nombre: str = Field(min_length=1, max_length=100, examples=["Laptop Gaming"])
    descripcion: str | None = Field(default=None, max_length=500)
    precio: float = Field(gt=0, examples=[999.99])
    categoria: str = Field(min_length=1, examples=["Electrónica"])
    stock: int = Field(default=0, ge=0)


class ProductoCrear(ProductoBase):
    """Modelo para crear producto."""
    pass


class ProductoActualizar(BaseModel):
    """Modelo para actualizar (todo opcional)."""
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    descripcion: str | None = None
    precio: float | None = Field(default=None, gt=0)
    categoria: str | None = None
    stock: int | None = Field(default=None, ge=0)


class ProductoResponse(ProductoBase):
    """Modelo de respuesta."""
    id: int
    disponible: bool = True


# =============================================================================
# "BASE DE DATOS" EN MEMORIA
# =============================================================================


productos_db: dict[int, dict] = {}
contador_id = 0


def siguiente_id() -> int:
    """Genera el siguiente ID."""
    global contador_id
    contador_id += 1
    return contador_id


# Datos iniciales de ejemplo
def inicializar_datos():
    """Crea algunos productos de ejemplo."""
    productos_ejemplo = [
        ProductoCrear(
            nombre="Laptop Pro",
            descripcion="Laptop de alto rendimiento",
            precio=1299.99,
            categoria="Electrónica",
            stock=10
        ),
        ProductoCrear(
            nombre="Mouse Inalámbrico",
            precio=29.99,
            categoria="Accesorios",
            stock=50
        ),
        ProductoCrear(
            nombre="Teclado Mecánico",
            descripcion="Teclado RGB con switches azules",
            precio=89.99,
            categoria="Accesorios",
            stock=25
        )
    ]

    for prod in productos_ejemplo:
        id = siguiente_id()
        productos_db[id] = {
            "id": id,
            **prod.model_dump(),
            "disponible": prod.stock > 0
        }


inicializar_datos()


# =============================================================================
# ENDPOINTS
# =============================================================================


@app.get("/")
def raiz():
    """Información de la API."""
    return {
        "api": "Productos API",
        "version": "1.0.0",
        "documentacion": "/docs"
    }


@app.get(
    "/productos",
    response_model=list[ProductoResponse],
    summary="Listar productos",
    tags=["Productos"]
)
def listar_productos(
    categoria: str | None = Query(
        default=None,
        description="Filtrar por categoría"
    ),
    precio_min: float | None = Query(
        default=None,
        ge=0,
        description="Precio mínimo"
    ),
    precio_max: float | None = Query(
        default=None,
        ge=0,
        description="Precio máximo"
    ),
    disponible: bool | None = Query(
        default=None,
        description="Filtrar por disponibilidad"
    ),
    skip: int = Query(default=0, ge=0, description="Saltar N productos"),
    limit: int = Query(default=10, ge=1, le=100, description="Límite de resultados")
):
    """
    Lista todos los productos con filtros opcionales.

    - **categoria**: Filtra por categoría exacta
    - **precio_min**: Precio mínimo
    - **precio_max**: Precio máximo
    - **disponible**: Solo disponibles (stock > 0)
    - **skip**: Paginación - saltar N items
    - **limit**: Paginación - máximo items a retornar
    """
    resultados = list(productos_db.values())

    # Aplicar filtros
    if categoria:
        resultados = [p for p in resultados if p["categoria"] == categoria]

    if precio_min is not None:
        resultados = [p for p in resultados if p["precio"] >= precio_min]

    if precio_max is not None:
        resultados = [p for p in resultados if p["precio"] <= precio_max]

    if disponible is not None:
        resultados = [p for p in resultados if p["disponible"] == disponible]

    # Paginación
    return resultados[skip:skip + limit]


@app.get(
    "/productos/{producto_id}",
    response_model=ProductoResponse,
    summary="Obtener producto",
    tags=["Productos"]
)
def obtener_producto(
    producto_id: int = Path(ge=1, description="ID del producto")
):
    """
    Obtiene un producto por su ID.

    Retorna 404 si no existe.
    """
    if producto_id not in productos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    return productos_db[producto_id]


@app.post(
    "/productos",
    response_model=ProductoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear producto",
    tags=["Productos"]
)
def crear_producto(producto: ProductoCrear):
    """
    Crea un nuevo producto.

    Retorna el producto creado con su ID asignado.
    """
    id = siguiente_id()
    nuevo_producto = {
        "id": id,
        **producto.model_dump(),
        "disponible": producto.stock > 0
    }
    productos_db[id] = nuevo_producto
    return nuevo_producto


@app.put(
    "/productos/{producto_id}",
    response_model=ProductoResponse,
    summary="Actualizar producto",
    tags=["Productos"]
)
def actualizar_producto(
    producto_id: int = Path(ge=1),
    producto: ProductoActualizar = None
):
    """
    Actualiza un producto existente.

    Solo se actualizan los campos enviados (no None).
    """
    if producto_id not in productos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )

    producto_actual = productos_db[producto_id]

    # Actualizar solo campos proporcionados
    if producto:
        datos_actualizar = producto.model_dump(exclude_none=True)
        for campo, valor in datos_actualizar.items():
            producto_actual[campo] = valor

        # Recalcular disponibilidad
        producto_actual["disponible"] = producto_actual["stock"] > 0

    return producto_actual


@app.delete(
    "/productos/{producto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar producto",
    tags=["Productos"]
)
def eliminar_producto(
    producto_id: int = Path(ge=1)
):
    """
    Elimina un producto.

    Retorna 204 No Content si se eliminó correctamente.
    Retorna 404 si no existe.
    """
    if producto_id not in productos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )

    del productos_db[producto_id]
    return None


# =============================================================================
# ENDPOINTS ADICIONALES
# =============================================================================


@app.get(
    "/categorias",
    response_model=list[str],
    summary="Listar categorías",
    tags=["Utilidades"]
)
def listar_categorias():
    """Retorna lista de categorías únicas."""
    categorias = set(p["categoria"] for p in productos_db.values())
    return sorted(categorias)


@app.get(
    "/estadisticas",
    summary="Estadísticas de productos",
    tags=["Utilidades"]
)
def estadisticas():
    """Retorna estadísticas de los productos."""
    if not productos_db:
        return {"total": 0}

    productos = list(productos_db.values())
    precios = [p["precio"] for p in productos]

    return {
        "total_productos": len(productos),
        "disponibles": sum(1 for p in productos if p["disponible"]),
        "precio_promedio": round(sum(precios) / len(precios), 2),
        "precio_minimo": min(precios),
        "precio_maximo": max(precios),
        "categorias": len(set(p["categoria"] for p in productos))
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
