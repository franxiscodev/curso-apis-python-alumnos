"""
CRUD Organizado con Modelos Separados
======================================
Patrón Base/Create/Update/Response para operaciones CRUD.

Ejecutar:
    uvicorn ejemplos.01_crud_organizado:app --reload

Conceptos:
    - Modelos separados por operación
    - model_dump(exclude_none=True) para updates parciales
    - Herencia de modelos Pydantic
"""

from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel, Field

app = FastAPI(title="CRUD Organizado", version="1.0.0")


# =============================================================================
# MODELOS SEPARADOS
# =============================================================================


class ProductoBase(BaseModel):
    """Campos comunes compartidos por Create y Response."""
    nombre: str = Field(min_length=1, max_length=100, examples=["Laptop Pro"])
    precio: float = Field(gt=0, examples=[999.99])
    categoria: str = Field(min_length=1, examples=["Electrónica"])


class ProductoCrear(ProductoBase):
    """Modelo para crear producto (hereda todos los campos de Base)."""
    stock: int = Field(default=0, ge=0)


class ProductoActualizar(BaseModel):
    """Modelo para actualizar (todo opcional para update parcial)."""
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    precio: float | None = Field(default=None, gt=0)
    categoria: str | None = None
    stock: int | None = Field(default=None, ge=0)


class ProductoResponse(ProductoBase):
    """Modelo de respuesta (incluye ID y campos calculados)."""
    id: int
    stock: int
    disponible: bool


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


# =============================================================================
# ENDPOINTS CRUD
# =============================================================================


@app.get("/productos", response_model=list[ProductoResponse], tags=["CRUD"])
def listar_productos():
    """Listar todos los productos."""
    return list(productos_db.values())


@app.post(
    "/productos",
    response_model=ProductoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["CRUD"]
)
def crear_producto(producto: ProductoCrear):
    """Crear un nuevo producto."""
    nuevo_id = siguiente_id()
    nuevo = {
        "id": nuevo_id,
        **producto.model_dump(),
        "disponible": producto.stock > 0
    }
    productos_db[nuevo_id] = nuevo
    return nuevo


@app.get("/productos/{producto_id}", response_model=ProductoResponse, tags=["CRUD"])
def obtener_producto(producto_id: int = Path(ge=1)):
    """Obtener producto por ID."""
    if producto_id not in productos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto {producto_id} no encontrado"
        )
    return productos_db[producto_id]


@app.put("/productos/{producto_id}", response_model=ProductoResponse, tags=["CRUD"])
def actualizar_producto(producto_id: int = Path(ge=1), producto: ProductoActualizar = ...):
    """Actualizar producto (solo campos enviados)."""
    if producto_id not in productos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto {producto_id} no encontrado"
        )

    actual = productos_db[producto_id]

    # exclude_none=True: solo actualiza campos enviados
    datos = producto.model_dump(exclude_none=True)
    for campo, valor in datos.items():
        actual[campo] = valor

    actual["disponible"] = actual["stock"] > 0
    return actual


@app.delete(
    "/productos/{producto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["CRUD"]
)
def eliminar_producto(producto_id: int = Path(ge=1)):
    """Eliminar producto."""
    if producto_id not in productos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto {producto_id} no encontrado"
        )
    del productos_db[producto_id]
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
