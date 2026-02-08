"""
Solucion Ejercicio 03: App de Tareas con Multiples Routers
==========================================================
API de gestion de tareas organizada con 3 routers.

Ejecutar:
    uvicorn ejercicio_03_solucion:app --reload
"""

from fastapi import FastAPI, HTTPException, APIRouter, status
from pydantic import BaseModel, Field

app = FastAPI(title="TODO App", description="API de gestion de tareas con routers")

# --- Bases de datos en memoria ---
tareas_db: dict[int, dict] = {}
categorias_db: dict[int, dict] = {}
contador_tareas = 0
contador_categorias = 0


# =============================================================================
# Modelos Pydantic
# =============================================================================

class TareaBase(BaseModel):
    titulo: str = Field(min_length=1)
    descripcion: str = ""


class TareaCrear(TareaBase):
    categoria_id: int | None = None


class TareaResponse(TareaBase):
    id: int
    completada: bool
    categoria_id: int | None = None


class Categoria(BaseModel):
    nombre: str = Field(min_length=1)
    descripcion: str = ""


class CategoriaResponse(Categoria):
    id: int


# =============================================================================
# Router de Tareas
# =============================================================================

router_tareas = APIRouter(prefix="/tareas", tags=["Tareas"])


@router_tareas.get("/", response_model=list[TareaResponse])
def listar_tareas():
    return list(tareas_db.values())


@router_tareas.post("/", response_model=TareaResponse, status_code=status.HTTP_201_CREATED)
def crear_tarea(tarea: TareaCrear):
    global contador_tareas
    contador_tareas += 1
    nueva = {
        "id": contador_tareas,
        "completada": False,
        **tarea.model_dump(),
    }
    tareas_db[contador_tareas] = nueva
    return nueva


@router_tareas.get("/{tarea_id}", response_model=TareaResponse)
def obtener_tarea(tarea_id: int):
    if tarea_id not in tareas_db:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tareas_db[tarea_id]


@router_tareas.patch("/{tarea_id}", response_model=TareaResponse)
def completar_tarea(tarea_id: int):
    if tarea_id not in tareas_db:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    tareas_db[tarea_id]["completada"] = True
    return tareas_db[tarea_id]


@router_tareas.delete("/{tarea_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tarea(tarea_id: int):
    if tarea_id not in tareas_db:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    del tareas_db[tarea_id]


# =============================================================================
# Router de Categorias
# =============================================================================

router_categorias = APIRouter(prefix="/categorias", tags=["Categorias"])


@router_categorias.get("/", response_model=list[CategoriaResponse])
def listar_categorias():
    return list(categorias_db.values())


@router_categorias.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def crear_categoria(categoria: Categoria):
    global contador_categorias
    contador_categorias += 1
    nueva = {"id": contador_categorias, **categoria.model_dump()}
    categorias_db[contador_categorias] = nueva
    return nueva


# =============================================================================
# Router de Utilidades
# =============================================================================

router_utilidades = APIRouter(prefix="/utilidades", tags=["Utilidades"])


@router_utilidades.get("/estadisticas")
def estadisticas():
    total = len(tareas_db)
    completadas = sum(1 for t in tareas_db.values() if t["completada"])
    pendientes = total - completadas

    por_categoria: dict[str, int] = {}
    for tarea in tareas_db.values():
        cat_id = tarea.get("categoria_id")
        if cat_id and cat_id in categorias_db:
            nombre = categorias_db[cat_id]["nombre"]
        else:
            nombre = "Sin categoria"
        por_categoria[nombre] = por_categoria.get(nombre, 0) + 1

    return {
        "total_tareas": total,
        "completadas": completadas,
        "pendientes": pendientes,
        "por_categoria": por_categoria,
    }


# =============================================================================
# Montar routers
# =============================================================================

app.include_router(router_tareas)
app.include_router(router_categorias)
app.include_router(router_utilidades)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
