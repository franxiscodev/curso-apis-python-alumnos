"""
Ejercicio 03: API Completa con Base de Datos - SOLUCIÓN
========================================================
"""

from fastapi import Depends, FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import String, create_engine, select
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


engine = create_engine("sqlite:///notas.db")
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


# =============================================================================
# MODELO SQLALCHEMY
# =============================================================================


class Nota(Base):
    """Tabla de notas."""
    __tablename__ = "notas"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(100))
    contenido: Mapped[str | None] = mapped_column(String(1000), default=None)
    categoria: Mapped[str] = mapped_column(String(50))
    importante: Mapped[bool] = mapped_column(default=False)


Base.metadata.create_all(bind=engine)


# =============================================================================
# SCHEMAS PYDANTIC
# =============================================================================


class NotaCrear(BaseModel):
    """Schema para crear nota."""
    titulo: str = Field(min_length=1, max_length=100)
    contenido: str | None = Field(default=None, max_length=1000)
    categoria: str = Field(min_length=1, max_length=50)
    importante: bool = False


class NotaActualizar(BaseModel):
    """Schema para actualizar (todo opcional)."""
    titulo: str | None = Field(default=None, min_length=1, max_length=100)
    contenido: str | None = None
    categoria: str | None = None
    importante: bool | None = None


class NotaResponse(BaseModel):
    """Schema de respuesta."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    contenido: str | None
    categoria: str
    importante: bool


# =============================================================================
# DEPENDENCY
# =============================================================================


def get_db():
    """Sesión de BD por request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =============================================================================
# APLICACIÓN
# =============================================================================


app = FastAPI(title="Notas API", version="1.0.0")


@app.get("/notas", response_model=list[NotaResponse], tags=["Notas"])
def listar_notas(
    categoria: str | None = Query(default=None, description="Filtrar por categoría"),
    importante: bool | None = Query(default=None, description="Filtrar por importancia"),
    db: Session = Depends(get_db)
):
    """Listar notas con filtros opcionales."""
    stmt = select(Nota)
    if categoria:
        stmt = stmt.where(Nota.categoria == categoria)
    if importante is not None:
        stmt = stmt.where(Nota.importante == importante)
    return db.execute(stmt).scalars().all()


@app.post(
    "/notas",
    response_model=NotaResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Notas"]
)
def crear_nota(nota: NotaCrear, db: Session = Depends(get_db)):
    """Crear nueva nota."""
    nueva = Nota(**nota.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@app.get("/notas/{nota_id}", response_model=NotaResponse, tags=["Notas"])
def obtener_nota(nota_id: int = Path(ge=1), db: Session = Depends(get_db)):
    """Obtener nota por ID."""
    nota = db.get(Nota, nota_id)
    if not nota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nota {nota_id} no encontrada"
        )
    return nota


@app.put("/notas/{nota_id}", response_model=NotaResponse, tags=["Notas"])
def actualizar_nota(
    nota_id: int = Path(ge=1),
    datos: NotaActualizar = ...,
    db: Session = Depends(get_db)
):
    """Actualizar nota (parcial)."""
    nota = db.get(Nota, nota_id)
    if not nota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nota {nota_id} no encontrada"
        )

    for campo, valor in datos.model_dump(exclude_none=True).items():
        setattr(nota, campo, valor)

    db.commit()
    db.refresh(nota)
    return nota


@app.delete("/notas/{nota_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Notas"])
def eliminar_nota(nota_id: int = Path(ge=1), db: Session = Depends(get_db)):
    """Eliminar nota."""
    nota = db.get(Nota, nota_id)
    if not nota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nota {nota_id} no encontrada"
        )
    db.delete(nota)
    db.commit()
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
