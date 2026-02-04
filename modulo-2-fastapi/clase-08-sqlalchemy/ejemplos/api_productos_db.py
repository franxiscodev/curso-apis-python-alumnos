"""
API de Productos con Persistencia
===================================
API completa que migra el patrón de clase-07 a base de datos real.

Ejecutar:
    uvicorn ejemplos.api_productos_db:app --reload

Endpoints:
    GET    /productos           - Listar con paginación y filtros
    GET    /productos/{id}      - Obtener producto
    POST   /productos           - Crear producto
    PUT    /productos/{id}      - Actualizar producto
    DELETE /productos/{id}      - Eliminar producto
    GET    /estadisticas        - Estadísticas
"""

import math

from fastapi import Depends, FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import String, create_engine, func, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    sessionmaker,
)


# =============================================================================
# BASE DE DATOS
# =============================================================================


engine = create_engine("sqlite:///productos.db")
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """Dependency de sesión de BD."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =============================================================================
# MODELO SQLALCHEMY
# =============================================================================


class Producto(Base):
    """Tabla de productos."""
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    descripcion: Mapped[str | None] = mapped_column(String(500), default=None)
    precio: Mapped[float]
    categoria: Mapped[str] = mapped_column(String(50))
    stock: Mapped[int] = mapped_column(default=0)


Base.metadata.create_all(bind=engine)


# =============================================================================
# SCHEMAS PYDANTIC
# =============================================================================


class ProductoCrear(BaseModel):
    """Schema para crear producto."""
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=500)
    precio: float = Field(gt=0)
    categoria: str = Field(min_length=1, max_length=50)
    stock: int = Field(default=0, ge=0)


class ProductoActualizar(BaseModel):
    """Schema para actualizar (todo opcional)."""
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    descripcion: str | None = None
    precio: float | None = Field(default=None, gt=0)
    categoria: str | None = None
    stock: int | None = Field(default=None, ge=0)


class ProductoResponse(BaseModel):
    """Schema de respuesta."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    descripcion: str | None
    precio: float
    categoria: str
    stock: int
    disponible: bool = False

    def __init__(self, **data):
        if "disponible" not in data and "stock" in data:
            data["disponible"] = data["stock"] > 0
        super().__init__(**data)


class ProductosPaginados(BaseModel):
    """Respuesta paginada."""
    items: list[ProductoResponse]
    total: int
    page: int
    size: int
    pages: int


# =============================================================================
# DATOS INICIALES
# =============================================================================


def inicializar_datos():
    """Inserta datos de ejemplo si la tabla está vacía."""
    with SessionLocal() as db:
        count = db.execute(select(func.count()).select_from(Producto)).scalar()
        if count > 0:
            return

        productos = [
            Producto(nombre="Laptop Pro", precio=1299.99,
                     descripcion="Alto rendimiento", categoria="Electrónica", stock=10),
            Producto(nombre="Mouse Inalámbrico", precio=29.99,
                     categoria="Accesorios", stock=50),
            Producto(nombre="Teclado Mecánico", precio=89.99,
                     categoria="Accesorios", stock=25),
            Producto(nombre="Monitor 27\"", precio=349.99,
                     categoria="Electrónica", stock=0),
            Producto(nombre="Silla Ergonómica", precio=450.00,
                     categoria="Mobiliario", stock=5),
        ]
        db.add_all(productos)
        db.commit()


inicializar_datos()


# =============================================================================
# APLICACIÓN
# =============================================================================


app = FastAPI(
    title="API de Productos (con BD)",
    description="CRUD completo con persistencia SQLAlchemy",
    version="1.0.0"
)


@app.get("/productos", response_model=ProductosPaginados, tags=["Productos"])
def listar_productos(
    categoria: str | None = Query(default=None),
    precio_min: float | None = Query(default=None, ge=0),
    precio_max: float | None = Query(default=None, ge=0),
    buscar: str | None = Query(default=None, min_length=2),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Listar productos con filtros y paginación."""
    stmt = select(Producto)

    if categoria:
        stmt = stmt.where(Producto.categoria == categoria)
    if precio_min is not None:
        stmt = stmt.where(Producto.precio >= precio_min)
    if precio_max is not None:
        stmt = stmt.where(Producto.precio <= precio_max)
    if buscar:
        stmt = stmt.where(Producto.nombre.contains(buscar))

    # Contar total antes de paginar
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.execute(count_stmt).scalar() or 0
    pages = math.ceil(total / size) if total > 0 else 0

    # Paginar
    stmt = stmt.offset((page - 1) * size).limit(size)
    items = db.execute(stmt).scalars().all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }


@app.get("/productos/{producto_id}", response_model=ProductoResponse, tags=["Productos"])
def obtener_producto(producto_id: int = Path(ge=1), db: Session = Depends(get_db)):
    """Obtener producto por ID."""
    producto = db.get(Producto, producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto {producto_id} no encontrado"
        )
    return producto


@app.post(
    "/productos",
    response_model=ProductoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Productos"]
)
def crear_producto(producto: ProductoCrear, db: Session = Depends(get_db)):
    """Crear producto."""
    nuevo = Producto(**producto.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@app.put("/productos/{producto_id}", response_model=ProductoResponse, tags=["Productos"])
def actualizar_producto(
    producto_id: int = Path(ge=1),
    datos: ProductoActualizar = ...,
    db: Session = Depends(get_db)
):
    """Actualizar producto (parcial)."""
    producto = db.get(Producto, producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto {producto_id} no encontrado"
        )

    for campo, valor in datos.model_dump(exclude_none=True).items():
        setattr(producto, campo, valor)

    db.commit()
    db.refresh(producto)
    return producto


@app.delete(
    "/productos/{producto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Productos"]
)
def eliminar_producto(producto_id: int = Path(ge=1), db: Session = Depends(get_db)):
    """Eliminar producto."""
    producto = db.get(Producto, producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto {producto_id} no encontrado"
        )
    db.delete(producto)
    db.commit()
    return None


@app.get("/estadisticas", tags=["Utilidades"])
def estadisticas(db: Session = Depends(get_db)):
    """Estadísticas de productos."""
    total = db.execute(select(func.count()).select_from(Producto)).scalar()
    if not total:
        return {"total": 0}

    return {
        "total_productos": total,
        "disponibles": db.execute(
            select(func.count()).select_from(Producto).where(Producto.stock > 0)
        ).scalar(),
        "precio_promedio": round(
            db.execute(select(func.avg(Producto.precio))).scalar() or 0, 2
        ),
        "precio_minimo": db.execute(select(func.min(Producto.precio))).scalar(),
        "precio_maximo": db.execute(select(func.max(Producto.precio))).scalar(),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
