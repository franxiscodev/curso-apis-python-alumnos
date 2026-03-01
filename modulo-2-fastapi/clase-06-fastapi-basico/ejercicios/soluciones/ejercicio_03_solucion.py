"""
Ejercicio 03: API de Tareas (TODO) - SOLUCIÓN
==============================================
"""

from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

app = FastAPI(
    title="TODO API",
    description="API de gestión de tareas",
    version="1.0.0"
)


# =============================================================================
# MODELOS
# =============================================================================


class TareaCrear(BaseModel):
    """Modelo para crear tarea."""
    titulo: str = Field(min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=500)
    prioridad: Literal["baja", "media", "alta"] = "media"
    fecha_limite: str | None = None


class TareaActualizar(BaseModel):
    """Modelo para actualizar tarea (todos opcionales)."""
    titulo: str | None = Field(default=None, min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=500)
    prioridad: Literal["baja", "media", "alta"] | None = None
    completada: bool | None = None
    fecha_limite: str | None = None


class TareaResponse(BaseModel):
    """Modelo de respuesta."""
    id: int
    titulo: str
    descripcion: str | None = None
    prioridad: str
    completada: bool
    fecha_limite: str | None = None
    fecha_creacion: str


# =============================================================================
# "BASE DE DATOS"
# =============================================================================


tareas_db: dict[int, dict] = {}
contador_id = 0


def siguiente_id() -> int:
    """Genera siguiente ID."""
    global contador_id
    contador_id += 1
    return contador_id


# =============================================================================
# ENDPOINTS
# =============================================================================


@app.get("/tareas", response_model=list[TareaResponse])
def listar_tareas(
    completada: bool | None = Query(
        default=None,
        description="Filtrar por estado de completitud"
    ),
    prioridad: Literal["baja", "media", "alta"] | None = Query(
        default=None,
        description="Filtrar por prioridad"
    )
):
    """Listar todas las tareas con filtros opcionales."""
    tareas = list(tareas_db.values())

    if completada is not None:
        tareas = [t for t in tareas if t["completada"] == completada]

    if prioridad is not None:
        tareas = [t for t in tareas if t["prioridad"] == prioridad]

    return tareas


@app.get("/tareas/estadisticas")
def obtener_estadisticas():
    """Obtener estadísticas de las tareas."""
    tareas = list(tareas_db.values())
    total = len(tareas)
    completadas = sum(1 for t in tareas if t["completada"])
    pendientes = total - completadas

    por_prioridad = {"baja": 0, "media": 0, "alta": 0}
    for tarea in tareas:
        por_prioridad[tarea["prioridad"]] += 1

    return {
        "total": total,
        "completadas": completadas,
        "pendientes": pendientes,
        "por_prioridad": por_prioridad
    }


@app.post("/tareas", response_model=TareaResponse, status_code=status.HTTP_201_CREATED)
def crear_tarea(tarea: TareaCrear):
    """Crear una nueva tarea."""
    nuevo_id = siguiente_id()

    nueva_tarea = {
        "id": nuevo_id,
        "titulo": tarea.titulo,
        "descripcion": tarea.descripcion,
        "prioridad": tarea.prioridad,
        "completada": False,
        "fecha_limite": tarea.fecha_limite,
        "fecha_creacion": datetime.now().isoformat()
    }

    tareas_db[nuevo_id] = nueva_tarea
    return nueva_tarea


@app.get("/tareas/{tarea_id}", response_model=TareaResponse)
def obtener_tarea(
    tarea_id: int = Path(ge=1, description="ID de la tarea")
):
    """Obtener una tarea por su ID."""
    if tarea_id not in tareas_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {tarea_id} no encontrada"
        )
    return tareas_db[tarea_id]


@app.put("/tareas/{tarea_id}", response_model=TareaResponse)
def actualizar_tarea(
    tarea_id: int = Path(ge=1, description="ID de la tarea"),
    tarea: TareaActualizar = ...
):
    """Actualizar una tarea existente."""
    if tarea_id not in tareas_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {tarea_id} no encontrada"
        )

    tarea_actual = tareas_db[tarea_id]
    datos_actualizar = tarea.model_dump(exclude_unset=True)

    for campo, valor in datos_actualizar.items():
        tarea_actual[campo] = valor

    return tarea_actual


@app.delete("/tareas/{tarea_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tarea(
    tarea_id: int = Path(ge=1, description="ID de la tarea")
):
    """Eliminar una tarea."""
    if tarea_id not in tareas_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {tarea_id} no encontrada"
        )

    del tareas_db[tarea_id]
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
