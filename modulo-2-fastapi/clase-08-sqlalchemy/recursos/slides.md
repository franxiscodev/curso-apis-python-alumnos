---
marp: true
theme: default
paginate: true
header: 'Clase 08: SQLAlchemy y Persistencia'
footer: 'Curso APIs Avanzadas con Python'
---

# SQLAlchemy y Persistencia
## De Memoria a Base de Datos

Clase 08 - Módulo 2: FastAPI

---

# El Problema

```python
# Clase 07: datos en memoria
productos_db: dict[int, dict] = {}
# Si reinicias el servidor → datos perdidos
```

**Solución**: Base de datos con SQLAlchemy

---

# SQLAlchemy 2.0

ORM más popular de Python, versión moderna con type hints

```
Tu Código (FastAPI)
       ↓
   Pydantic (Validación API)
       ↓
   SQLAlchemy (ORM → Base de datos)
       ↓
   SQLite / PostgreSQL
```

---

# Setup Básico

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Conexión a SQLite
engine = create_engine("sqlite:///app.db")

# Fábrica de sesiones
SessionLocal = sessionmaker(bind=engine)

# Base para modelos
class Base(DeclarativeBase):
    pass
```

---

# Definir Modelos (Tablas)

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class Producto(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(45))
    precio: Mapped[float]
    stock: Mapped[int] = mapped_column(default=0)
    descripcion: Mapped[str | None] = mapped_column(default=None)
```

---

# Sintaxis Antigua vs Moderna

```python
# SQLAlchemy 1.x (NO usar)
class Producto(Base):
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))

# SQLAlchemy 2.0 (usar esto)
class Producto(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
```

---

# Dos Tipos de Modelos

| SQLAlchemy | Pydantic |
|------------|----------|
| Define la **tabla** | Define la **API** |
| `Mapped[str]` | `str = Field(...)` |
| Hereda de `Base` | Hereda de `BaseModel` |
| Capa de datos | Capa de validación |

Se complementan, no se reemplazan

---

# Conectar Pydantic ↔ SQLAlchemy

```python
class ProductoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    precio: float
```

`from_attributes=True` → Pydantic lee objetos SQLAlchemy

---

# Operaciones CRUD

```python
# CREATE
producto = Producto(nombre="Laptop", precio=999.99)
session.add(producto)
session.commit()

# READ
producto = session.get(Producto, 1)  # Por ID
todos = session.execute(select(Producto)).scalars().all()

# UPDATE
producto.precio = 899.99
session.commit()

# DELETE
session.delete(producto)
session.commit()
```

---

# Consultas con select()

```python
from sqlalchemy import select

# Filtrar
stmt = select(Producto).where(Producto.precio > 100)

# Ordenar
stmt = select(Producto).order_by(Producto.nombre)

# Paginar (a nivel de BD)
stmt = select(Producto).offset(10).limit(5)

# Ejecutar
resultados = session.execute(stmt).scalars().all()
```

---

# Dependency Injection en FastAPI

```python
def get_db():
    db = SessionLocal()
    try:
        yield db      # El endpoint usa la sesión
    finally:
        db.close()    # Siempre se cierra

@app.get("/productos")
def listar(db: Session = Depends(get_db)):
    return db.execute(select(Producto)).scalars().all()
```

---

# Relaciones: One-to-Many

```python
class Categoria(Base):
    __tablename__ = "categorias"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))
    productos: Mapped[list["Producto"]] = relationship(
        back_populates="categoria")

class Producto(Base):
    __tablename__ = "productos"
    categoria_id: Mapped[int] = mapped_column(
        ForeignKey("categorias.id"))
    categoria: Mapped["Categoria"] = relationship(
        back_populates="productos")
```

---

# Usar Relaciones

```python
# Acceder a productos de una categoría
for prod in categoria.productos:
    print(prod.nombre)

# Acceder a la categoría de un producto
print(producto.categoria.nombre)

# Query con join
stmt = (select(Producto)
        .join(Categoria)
        .where(Categoria.nombre == "Electrónica"))
```

---

# Resumen

| Concepto | Herramienta |
|----------|-------------|
| Conexión | `create_engine("sqlite:///...")` |
| Modelos | `Mapped` + `mapped_column` |
| Sesiones | `SessionLocal()` + `get_db` |
| CRUD | `add`, `get`, `delete`, `commit` |
| Consultas | `select().where().order_by()` |
| Relaciones | `relationship` + `ForeignKey` |
| Pydantic ↔ ORM | `from_attributes=True` |

---

# Ejercicio Práctico

Crear **API de Notas** con persistencia:

1. Modelo SQLAlchemy para Nota
2. Schemas Pydantic (Crear, Actualizar, Response)
3. CRUD completo con `Depends(get_db)`
4. Filtros por categoría e importancia

---

# Próxima Clase

**Clase 09: Autenticación y Seguridad**

- JWT (JSON Web Tokens)
- Usuarios en base de datos
- Proteger endpoints
- Roles y permisos

---

# Recursos

- **SQLAlchemy 2.0**: https://docs.sqlalchemy.org/en/20/
- **FastAPI + SQL**: https://fastapi.tiangolo.com/tutorial/sql-databases/
- **Pydantic ConfigDict**: https://docs.pydantic.dev/latest/api/config/

**Practica:**
```bash
uvicorn ejemplos.api_productos_db:app --reload
```
