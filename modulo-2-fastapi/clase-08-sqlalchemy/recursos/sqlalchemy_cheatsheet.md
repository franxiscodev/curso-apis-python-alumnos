# SQLAlchemy 2.0 Cheatsheet

Guía rápida de SQLAlchemy 2.0 con FastAPI.

---

## Setup

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# SQLite (archivo local)
engine = create_engine("sqlite:///app.db")

# PostgreSQL
# engine = create_engine("postgresql://user:pass@localhost/dbname")

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

# Crear tablas
Base.metadata.create_all(bind=engine)
```

---

## Definir Modelos

```python
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Producto(Base):
    __tablename__ = "productos"

    # Primary key (autoincrement por defecto)
    id: Mapped[int] = mapped_column(primary_key=True)

    # String con límite
    nombre: Mapped[str] = mapped_column(String(100))

    # Float, int
    precio: Mapped[float]
    stock: Mapped[int] = mapped_column(default=0)

    # Nullable
    descripcion: Mapped[str | None] = mapped_column(String(500), default=None)

    # Unique
    email: Mapped[str] = mapped_column(String(100), unique=True)

    # Foreign key
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"))
```

---

## Relaciones

```python
# One-to-Many: Categoria tiene muchos Productos
class Categoria(Base):
    __tablename__ = "categorias"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))
    productos: Mapped[list["Producto"]] = relationship(back_populates="categoria")

class Producto(Base):
    __tablename__ = "productos"
    id: Mapped[int] = mapped_column(primary_key=True)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"))
    categoria: Mapped["Categoria"] = relationship(back_populates="productos")

# Uso:
# categoria.productos → lista de productos
# producto.categoria → objeto categoría
```

---

## CRUD con Sesiones

```python
from sqlalchemy.orm import Session
from sqlalchemy import select

# CREATE
with Session(engine) as db:
    producto = Producto(nombre="Laptop", precio=999.99)
    db.add(producto)
    db.commit()
    db.refresh(producto)  # Obtener ID generado

# READ por ID
with Session(engine) as db:
    producto = db.get(Producto, 1)

# READ con filtros
with Session(engine) as db:
    stmt = select(Producto).where(Producto.precio > 100)
    productos = db.execute(stmt).scalars().all()

# UPDATE
with Session(engine) as db:
    producto = db.get(Producto, 1)
    producto.precio = 899.99
    db.commit()

# DELETE
with Session(engine) as db:
    producto = db.get(Producto, 1)
    db.delete(producto)
    db.commit()
```

---

## Consultas select()

```python
from sqlalchemy import select, func

# Todos
select(Producto)

# Filtrar
select(Producto).where(Producto.categoria == "Electrónica")
select(Producto).where(Producto.precio > 100)
select(Producto).where(Producto.nombre.contains("laptop"))

# Múltiples filtros
select(Producto).where(
    Producto.precio > 100,
    Producto.stock > 0
)

# Ordenar
select(Producto).order_by(Producto.nombre)
select(Producto).order_by(Producto.precio.desc())

# Paginar
select(Producto).offset(10).limit(5)

# Contar
select(func.count()).select_from(Producto)

# Agregaciones
select(func.avg(Producto.precio))
select(func.min(Producto.precio))
select(func.max(Producto.precio))

# Join
select(Producto).join(Categoria).where(Categoria.nombre == "Electrónica")
```

---

## FastAPI + SQLAlchemy

```python
from fastapi import Depends, FastAPI

# Dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/items")
def listar(db: Session = Depends(get_db)):
    return db.execute(select(Item)).scalars().all()

@app.post("/items", status_code=201)
def crear(item: ItemCrear, db: Session = Depends(get_db)):
    nuevo = Item(**item.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
```

---

## Pydantic + SQLAlchemy

```python
from pydantic import BaseModel, ConfigDict

# Schema que lee desde objetos SQLAlchemy
class ItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    precio: float

# Uso en endpoint
@app.get("/items/{id}", response_model=ItemResponse)
def obtener(id: int, db: Session = Depends(get_db)):
    item = db.get(Item, id)  # Retorna objeto SQLAlchemy
    return item              # Pydantic lo convierte automáticamente
```

---

## Tips

1. **`from_attributes=True`** - Imprescindible para schemas de respuesta
2. **`session.refresh(obj)`** - Después de commit para obtener datos generados (ID)
3. **`select()` no `query()`** - Usa la sintaxis 2.0
4. **`Mapped[tipo]`** - No `Column(Type)` - sintaxis moderna
5. **`get_db` con `yield`** - Garantiza que la sesión se cierra siempre
6. **SQLite para desarrollo** - PostgreSQL para producción, mismo código
7. **Modelos separados** - SQLAlchemy para BD, Pydantic para API
