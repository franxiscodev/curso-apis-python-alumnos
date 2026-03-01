"""
Ejercicio 03: API Completa de Inventario - SOLUCIÓN
=====================================================
"""

import math
from typing import Literal

from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Inventario API",
    description="API completa de gestión de inventario",
    version="1.0.0"
)


# =============================================================================
# MODELOS
# =============================================================================


class ProductoBase(BaseModel):
    """Campos comunes de producto."""
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=500)
    precio: float = Field(gt=0)
    categoria: str = Field(min_length=1, max_length=50)
    stock: int = Field(default=0, ge=0)


class ProductoCrear(ProductoBase):
    """Modelo para crear producto."""
    pass


class ProductoActualizar(BaseModel):
    """Modelo para actualizar (todo opcional)."""
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    descripcion: str | None = None
    precio: float | None = Field(default=None, gt=0)
    categoria: str | None = Field(default=None, min_length=1, max_length=50)
    stock: int | None = Field(default=None, ge=0)


class ProductoResponse(ProductoBase):
    """Modelo de respuesta."""
    id: int
    disponible: bool


class ProductosPaginados(BaseModel):
    """Respuesta paginada."""
    items: list[ProductoResponse]
    total: int
    page: int
    size: int
    pages: int


# =============================================================================
# "BASE DE DATOS"
# =============================================================================


productos_db: dict[int, dict] = {}
contador_id = 0


def siguiente_id() -> int:
    """Genera siguiente ID."""
    global contador_id
    contador_id += 1
    return contador_id


def inicializar_datos():
    """Crea productos de ejemplo."""
    productos = [
        ProductoCrear(nombre="Laptop Pro", precio=1299.99,
                      descripcion="Laptop de alto rendimiento",
                      categoria="Electrónica", stock=10),
        ProductoCrear(nombre="Mouse Inalámbrico", precio=29.99,
                      categoria="Accesorios", stock=50),
        ProductoCrear(nombre="Teclado Mecánico", precio=89.99,
                      descripcion="Switches azules, RGB",
                      categoria="Accesorios", stock=25),
        ProductoCrear(nombre="Monitor 27\"", precio=349.99,
                      categoria="Electrónica", stock=0),
        ProductoCrear(nombre="Webcam HD", precio=59.99,
                      descripcion="1080p con micrófono",
                      categoria="Accesorios", stock=30),
        ProductoCrear(nombre="Silla Ergonómica", precio=450.00,
                      categoria="Mobiliario", stock=5),
    ]
    for prod in productos:
        nuevo_id = siguiente_id()
        productos_db[nuevo_id] = {
            "id": nuevo_id,
            **prod.model_dump(),
            "disponible": prod.stock > 0
        }


inicializar_datos()


# =============================================================================
# ENDPOINTS
# =============================================================================


@app.get(
    "/productos",
    response_model=ProductosPaginados,
    tags=["Productos"]
)
def listar_productos(
    categoria: str | None = Query(default=None, description="Filtrar por categoría"),
    precio_min: float | None = Query(default=None, ge=0, description="Precio mínimo"),
    precio_max: float | None = Query(default=None, ge=0, description="Precio máximo"),
    disponible: bool | None = Query(default=None, description="Filtrar disponibles"),
    buscar: str | None = Query(
        default=None, min_length=2, description="Buscar en nombre"
    ),
    sort_by: Literal["nombre", "precio", "categoria"] = Query(
        default="nombre", description="Ordenar por"
    ),
    order: Literal["asc", "desc"] = Query(default="asc", description="Dirección"),
    page: int = Query(default=1, ge=1, description="Página"),
    size: int = Query(default=10, ge=1, le=50, description="Items por página")
):
    """Listar productos con filtros, ordenamiento y paginación."""
    resultados = list(productos_db.values())

    if categoria:
        resultados = [p for p in resultados if p["categoria"] == categoria]

    if precio_min is not None:
        resultados = [p for p in resultados if p["precio"] >= precio_min]

    if precio_max is not None:
        resultados = [p for p in resultados if p["precio"] <= precio_max]

    if disponible is not None:
        resultados = [p for p in resultados if p["disponible"] == disponible]

    if buscar:
        buscar_lower = buscar.lower()
        resultados = [p for p in resultados if buscar_lower in p["nombre"].lower()]

    resultados.sort(key=lambda p: p[sort_by], reverse=(order == "desc"))

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


@app.post(
    "/productos",
    response_model=ProductoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Productos"]
)
def crear_producto(producto: ProductoCrear):
    """Crear producto. 409 si nombre duplicado."""
    for p in productos_db.values():
        if p["nombre"].lower() == producto.nombre.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un producto con nombre '{producto.nombre}'"
            )

    nuevo_id = siguiente_id()
    nuevo = {
        "id": nuevo_id,
        **producto.model_dump(),
        "disponible": producto.stock > 0
    }
    productos_db[nuevo_id] = nuevo
    return nuevo


@app.get(
    "/productos/{producto_id}",
    response_model=ProductoResponse,
    tags=["Productos"]
)
def obtener_producto(producto_id: int = Path(ge=1)):
    """Obtener producto por ID."""
    if producto_id not in productos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    return productos_db[producto_id]


@app.put(
    "/productos/{producto_id}",
    response_model=ProductoResponse,
    tags=["Productos"]
)
def actualizar_producto(
    producto_id: int = Path(ge=1),
    producto: ProductoActualizar = ...
):
    """Actualizar producto (parcial)."""
    if producto_id not in productos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )

    actual = productos_db[producto_id]
    datos = producto.model_dump(exclude_none=True)

    # Validar nombre único si se cambia
    if "nombre" in datos:
        for pid, p in productos_db.items():
            if p["nombre"].lower() == datos["nombre"].lower() and pid != producto_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe un producto con nombre '{datos['nombre']}'"
                )

    for campo, valor in datos.items():
        actual[campo] = valor

    actual["disponible"] = actual["stock"] > 0
    return actual


@app.delete(
    "/productos/{producto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Productos"]
)
def eliminar_producto(producto_id: int = Path(ge=1)):
    """Eliminar producto. 400 si tiene stock."""
    if producto_id not in productos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )

    if productos_db[producto_id]["stock"] > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar un producto con stock disponible"
        )

    del productos_db[producto_id]
    return None


@app.get("/estadisticas", tags=["Utilidades"])
def estadisticas():
    """Estadísticas del inventario."""
    productos = list(productos_db.values())

    if not productos:
        return {"total": 0}

    precios = [p["precio"] for p in productos]
    por_categoria: dict[str, int] = {}
    for p in productos:
        por_categoria[p["categoria"]] = por_categoria.get(p["categoria"], 0) + 1

    return {
        "total_productos": len(productos),
        "disponibles": sum(1 for p in productos if p["disponible"]),
        "sin_stock": sum(1 for p in productos if not p["disponible"]),
        "precio_promedio": round(sum(precios) / len(precios), 2),
        "precio_minimo": min(precios),
        "precio_maximo": max(precios),
        "por_categoria": por_categoria
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
