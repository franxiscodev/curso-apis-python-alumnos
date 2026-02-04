"""
FastAPI + SQLAlchemy Integrado
===============================
Dependency injection de sesiones en FastAPI.

Ejecutar:
    uvicorn ejemplos.04_fastapi_sqlalchemy:app --reload

Conceptos:
    - get_db con yield para ciclo de vida de sesión
    - Depends() para inyectar sesión en endpoints
    - Schemas Pydantic con from_attributes=True
    - CRUD básico con persistencia real
"""

from fastapi import Depends, FastAPI, HTTPException, Path, status
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


engine = create_engine("sqlite:///fastapi_ejemplo.db")
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


# =============================================================================
# MODELO SQLALCHEMY
# =============================================================================


class Tarea(Base):
    """Modelo de base de datos para tareas."""
    __tablename__ = "tareas"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(100))
    descripcion: Mapped[str | None] = mapped_column(String(500), default=None)
    completada: Mapped[bool] = mapped_column(default=False)


Base.metadata.create_all(bind=engine)


# =============================================================================
# SCHEMAS PYDANTIC (separados del modelo SQLAlchemy)
# =============================================================================


class TareaCrear(BaseModel):
    """Schema para crear tarea."""
    titulo: str = Field(min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=500)


class TareaResponse(BaseModel):
    """Schema de respuesta (lee desde objeto SQLAlchemy)."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    descripcion: str | None
    completada: bool


# =============================================================================
# DEPENDENCY INJECTION
# =============================================================================


def get_db():
    """Crea y cierra sesión de BD para cada request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =============================================================================
# APLICACIÓN FASTAPI
# =============================================================================


app = FastAPI(title="Tareas con BD", version="1.0.0")


@app.get("/tareas", response_model=list[TareaResponse], tags=["Tareas"])
def listar_tareas(db: Session = Depends(get_db)):
    """Listar todas las tareas desde la BD."""
    return db.execute(select(Tarea)).scalars().all()


@app.post(
    "/tareas",
    response_model=TareaResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Tareas"]
)
def crear_tarea(tarea: TareaCrear, db: Session = Depends(get_db)):
    """Crear tarea en la BD."""
    nueva = Tarea(**tarea.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@app.get("/tareas/{tarea_id}", response_model=TareaResponse, tags=["Tareas"])
def obtener_tarea(tarea_id: int = Path(ge=1), db: Session = Depends(get_db)):
    """Obtener tarea por ID."""
    tarea = db.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea {tarea_id} no encontrada"
        )
    return tarea


@app.patch("/tareas/{tarea_id}/completar", response_model=TareaResponse, tags=["Tareas"])
def completar_tarea(tarea_id: int = Path(ge=1), db: Session = Depends(get_db)):
    """Marcar tarea como completada."""
    tarea = db.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea {tarea_id} no encontrada"
        )
    tarea.completada = True
    db.commit()
    db.refresh(tarea)
    return tarea


@app.delete("/tareas/{tarea_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tareas"])
def eliminar_tarea(tarea_id: int = Path(ge=1), db: Session = Depends(get_db)):
    """Eliminar tarea de la BD."""
    tarea = db.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea {tarea_id} no encontrada"
        )
    db.delete(tarea)
    db.commit()
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
