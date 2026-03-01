"""
Ejercicio 03: API Completa de Inventario
==========================================
Crear una API completa de inventario desde cero.

OBJETIVO:
Integrar todos los conceptos: CRUD + paginación + filtrado + errores.

INSTRUCCIONES:
1. Modelos para Producto:
   - ProductoCrear: nombre (1-100), descripcion (opcional, max 500),
     precio (>0), categoria (1-50), stock (>=0, default 0)
   - ProductoActualizar: todo opcional
   - ProductoResponse: id + campos + disponible (bool calculado)

2. Endpoints:
   GET    /productos         → Listar con paginación + filtros
   POST   /productos         → Crear (409 si nombre duplicado)
   GET    /productos/{id}    → Obtener (404 si no existe)
   PUT    /productos/{id}    → Actualizar parcial
   DELETE /productos/{id}    → Eliminar (400 si stock > 0)
   GET    /estadisticas      → Total, disponibles, por categoría,
                                precio promedio

3. Filtros en GET /productos:
   - categoria (exacto)
   - precio_min, precio_max (rango)
   - disponible (bool)
   - buscar (parcial en nombre, case-insensitive)
   - sort_by (nombre/precio/categoria), order (asc/desc)
   - page, size (paginación)

4. Reglas de negocio:
   - No crear productos con nombre duplicado (409)
   - No eliminar productos con stock > 0 (400)
   - Disponible se calcula: stock > 0

PRUEBAS:
    uvicorn ejercicio_03:app --reload

    POST /productos {"nombre": "Laptop", "precio": 999.99,
                     "categoria": "Electrónica", "stock": 10}
    GET  /productos?categoria=Electrónica&sort_by=precio&order=desc
    GET  /estadisticas

PISTAS:
- Crea datos iniciales para probar
- El campo "disponible" no se recibe, se calcula
- Recalcular "disponible" al actualizar stock
"""

from typing import Literal

from fastapi import FastAPI, Query, Path, HTTPException, status
from pydantic import BaseModel, Field


app = FastAPI(
    title="Inventario API",
    description="API completa de gestión de inventario",
    version="1.0.0"
)


# TODO: Importar lo necesario (HTTPException, Query, Path, status, BaseModel, Field, etc.)

# TODO: Definir modelos (ProductoCrear, ProductoActualizar, ProductoResponse, Paginado)

class ProductoBase(BaseModel):
    """Campos comunes"""
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=500)
    precio: float = Field(gt=0)
    categoria: str = Field(min_length=1, max_length=50)
    stock: int = Field(default=0, ge=0)


class ProductoCrear(ProductoBase):
    pass


class ProductoActualizar(BaseModel):
    """todos opcionales"""
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=500)
    precio: float | None = Field(default=None, gt=0)
    categoria: str | None = Field(default=None, min_length=1, max_length=50)
    stock: int | None = Field(default=None, ge=0)


class ProductoResponse(ProductoBase):
    id: int
    disponible: bool


class ProductoPaginado(BaseModel):
    items: list[ProductoResponse]
    total: int
    page: int
    size: int
    pages: int

# TODO: Crear "base de datos" en memoria y función siguiente_id()


productos_db: dict[int, dict] = {}
contador_id = 0


def siguiente_id() -> int:
    """Genera siguiente ID."""
    global contador_id
    contador_id += 1
    return contador_id

# TODO: Crear datos iniciales (al menos 5 productos variados)


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

# defino ruta raiz


@app.get("/", tags=["home"])
def home():
    return "Inventario"


# TODO: Implementar GET /productos (paginación + filtros + ordenamiento)
"""
3. Filtros en GET /productos:
   - categoria (exacto)
   - precio_min, precio_max (rango)
   - disponible (bool)
   - buscar (parcial en nombre, case-insensitive)
   - sort_by (nombre/precio/categoria), order (asc/desc)
   - page, size (paginación)
"""


@app.get("/productos", response_model=ProductoPaginado, tags=["productos"])
def listar_productos(
    categoria: str | None = Query(
        default=None, descrition="Filtro por categoría"),
    precio_min: float | None = Query(
        default=None, ge=0, descrition="Precio Mínimo"),
    precio_max: float | None = Query(
        default=None, ge=0, descrition="Precio Máximo"),
    disponible: bool | None = Query(
        default=None, descrition="Filtro disponibles"),
    buscar: str | None = Query(
        default=None, min_length=2, description="Buscar en el nombre"),
    sort_by: Literal["nombre", "precio", "categoria"] = Query(
        default="nombre", description="Ordenar por ..."),
    page: int = Query(default=1, ge=1, description="Página"),
    size: int = Query(default=10, ge=1, le=50, description="Cant items x pag.")

):
    resultados = list(productos_db.values())
    if categoria:
        resultados = [p for p in resultados if p["categoria"] == categoria]

    total = len(resultados)
    # pages = total / size
    # start = (page - 1) * size

    return {
        "items": resultados,
        "total": total,
        "page": page,
        "size": size,
        "pages": 10
    }

# TODO: Implementar POST /productos (validar nombre único)

# TODO: Implementar GET /productos/{producto_id} (404)

# TODO: Implementar PUT /productos/{producto_id} (update parcial)

# TODO: Implementar DELETE /productos/{producto_id} (400 si stock > 0)

# TODO: Implementar GET /estadisticas
