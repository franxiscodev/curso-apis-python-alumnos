"""
Aplicacion Modular Completa
============================
Refactorizacion del estilo monolitico (como api_productos.py de clase-06)
a una arquitectura modular con multiples APIRouters.

Ejecutar:
    uvicorn ejemplos.03_app_modular:app --reload

Endpoints (Productos):
    GET    /productos              - Listar productos (con filtros)
    POST   /productos              - Crear producto
    GET    /productos/{id}         - Obtener producto
    PUT    /productos/{id}         - Actualizar producto
    DELETE /productos/{id}         - Eliminar producto

Endpoints (Categorias):
    GET    /categorias             - Listar categorias
    GET    /categorias/{nombre}    - Productos por categoria

Endpoints (Utilidades):
    GET    /utilidades/estadisticas - Estadisticas generales
    GET    /utilidades/salud        - Health check
"""

from fastapi import FastAPI, APIRouter, HTTPException, Query, Path, status
from pydantic import BaseModel, Field


# =============================================================================
# MODELOS
# =============================================================================


class ProductoBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=100, examples=["Laptop Gaming"])
    descripcion: str | None = Field(default=None, max_length=500)
    precio: float = Field(gt=0, examples=[999.99])
    categoria: str = Field(min_length=1, examples=["Electronica"])
    stock: int = Field(default=0, ge=0)


class ProductoCrear(ProductoBase):
    pass


class ProductoActualizar(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    descripcion: str | None = None
    precio: float | None = Field(default=None, gt=0)
    categoria: str | None = None
    stock: int | None = Field(default=None, ge=0)


class ProductoResponse(ProductoBase):
    id: int
    disponible: bool = True


# =============================================================================
# "BASE DE DATOS" EN MEMORIA
# =============================================================================


productos_db: dict[int, dict] = {}
contador_id = 0


def siguiente_id() -> int:
    global contador_id
    contador_id += 1
    return contador_id


# Datos iniciales
def inicializar_datos():
    productos_ejemplo = [
        ProductoCrear(
            nombre="Laptop Pro", descripcion="Laptop de alto rendimiento",
            precio=1299.99, categoria="Electronica", stock=10
        ),
        ProductoCrear(
            nombre="Mouse Inalambrico",
            precio=29.99, categoria="Accesorios", stock=50
        ),
        ProductoCrear(
            nombre="Teclado Mecanico", descripcion="Switches azules RGB",
            precio=89.99, categoria="Accesorios", stock=25
        ),
        ProductoCrear(
            nombre="Monitor 4K", descripcion="27 pulgadas IPS",
            precio=449.99, categoria="Electronica", stock=15
        ),
        ProductoCrear(
            nombre="Webcam HD",
            precio=59.99, categoria="Accesorios", stock=0
        ),
    ]
    for prod in productos_ejemplo:
        pid = siguiente_id()
        productos_db[pid] = {
            "id": pid,
            **prod.model_dump(),
            "disponible": prod.stock > 0
        }


inicializar_datos()


# =============================================================================
# ROUTER: PRODUCTOS
# =============================================================================


router_productos = APIRouter(
    prefix="/productos",
    tags=["Productos"],
    responses={404: {"description": "Producto no encontrado"}}
)


@router_productos.get("/", response_model=list[ProductoResponse])
def listar_productos(
    categoria: str | None = Query(default=None, description="Filtrar por categoria"),
    precio_min: float | None = Query(default=None, ge=0, description="Precio minimo"),
    precio_max: float | None = Query(default=None, ge=0, description="Precio maximo"),
    disponible: bool | None = Query(default=None, description="Solo disponibles"),
    skip: int = Query(default=0, ge=0, description="Saltar N productos"),
    limit: int = Query(default=10, ge=1, le=100, description="Limite de resultados")
):
    """Lista productos con filtros opcionales y paginacion."""
    resultados = list(productos_db.values())

    if categoria:
        resultados = [p for p in resultados if p["categoria"] == categoria]
    if precio_min is not None:
        resultados = [p for p in resultados if p["precio"] >= precio_min]
    if precio_max is not None:
        resultados = [p for p in resultados if p["precio"] <= precio_max]
    if disponible is not None:
        resultados = [p for p in resultados if p["disponible"] == disponible]

    return resultados[skip:skip + limit]


@router_productos.post(
    "/",
    response_model=ProductoResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_producto(producto: ProductoCrear):
    """Crea un nuevo producto."""
    pid = siguiente_id()
    nuevo = {
        "id": pid,
        **producto.model_dump(),
        "disponible": producto.stock > 0
    }
    productos_db[pid] = nuevo
    return nuevo


@router_productos.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: int = Path(ge=1)):
    """Obtiene un producto por ID."""
    if producto_id not in productos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto {producto_id} no encontrado"
        )
    return productos_db[producto_id]


@router_productos.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(
    producto_id: int = Path(ge=1),
    producto: ProductoActualizar = None
):
    """Actualiza un producto existente (campos parciales)."""
    if producto_id not in productos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto {producto_id} no encontrado"
        )
    actual = productos_db[producto_id]
    if producto:
        for campo, valor in producto.model_dump(exclude_none=True).items():
            actual[campo] = valor
        actual["disponible"] = actual["stock"] > 0
    return actual


@router_productos.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(producto_id: int = Path(ge=1)):
    """Elimina un producto."""
    if producto_id not in productos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto {producto_id} no encontrado"
        )
    del productos_db[producto_id]


# =============================================================================
# ROUTER: CATEGORIAS
# =============================================================================


router_categorias = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)


@router_categorias.get("/", response_model=list[str])
def listar_categorias():
    """Lista todas las categorias unicas."""
    return sorted(set(p["categoria"] for p in productos_db.values()))


@router_categorias.get("/{nombre}", response_model=list[ProductoResponse])
def productos_por_categoria(nombre: str):
    """Lista productos de una categoria especifica."""
    resultados = [p for p in productos_db.values() if p["categoria"] == nombre]
    if not resultados:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No hay productos en la categoria '{nombre}'"
        )
    return resultados


# =============================================================================
# ROUTER: UTILIDADES
# =============================================================================


router_utilidades = APIRouter(
    prefix="/utilidades",
    tags=["Utilidades"]
)


@router_utilidades.get("/estadisticas")
def estadisticas():
    """Estadisticas generales de productos."""
    if not productos_db:
        return {"total": 0}

    productos = list(productos_db.values())
    precios = [p["precio"] for p in productos]

    return {
        "total_productos": len(productos),
        "disponibles": sum(1 for p in productos if p["disponible"]),
        "no_disponibles": sum(1 for p in productos if not p["disponible"]),
        "precio_promedio": round(sum(precios) / len(precios), 2),
        "precio_minimo": min(precios),
        "precio_maximo": max(precios),
        "categorias": len(set(p["categoria"] for p in productos))
    }


@router_utilidades.get("/salud")
def health_check():
    """Health check del servicio."""
    return {
        "estado": "ok",
        "productos_cargados": len(productos_db)
    }


# =============================================================================
# APLICACION PRINCIPAL (equivalente a main.py)
# =============================================================================


app = FastAPI(
    title="Tienda API - Modular",
    description=(
        "API de productos refactorizada del estilo monolitico "
        "a arquitectura modular con APIRouter. "
        "Comparen con api_productos.py de clase-06."
    ),
    version="2.0.0"
)

# Montar los tres routers
app.include_router(router_productos)
app.include_router(router_categorias)
app.include_router(router_utilidades)


@app.get("/", tags=["Root"])
def raiz():
    """Punto de entrada de la API."""
    return {
        "api": "Tienda API - Modular",
        "version": "2.0.0",
        "routers": ["/productos", "/categorias", "/utilidades"],
        "documentacion": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
