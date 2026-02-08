"""
Ejercicio 03: App de Tareas con Multiples Routers
==================================================
Construyan una API de gestion de tareas (TODO app) desde cero,
organizada con multiples routers desde el inicio.

OBJETIVO:
Disenar una API modular con routers, modelos Pydantic y endpoints CRUD.

INSTRUCCIONES:
1. Definir los modelos Pydantic:
   - TareaBase: titulo (str, min 1), descripcion (str, default "")
   - TareaCrear: hereda de TareaBase, agrega categoria_id (int | None = None)
   - TareaResponse: hereda de TareaBase, agrega id (int), completada (bool), categoria_id
   - Categoria: nombre (str, min 1), descripcion (str, default "")
   - CategoriaResponse: hereda de Categoria, agrega id (int)

2. Crear router_tareas (prefix="/tareas", tags=["Tareas"]):
   - GET  /         -> listar todas las tareas
   - POST /         -> crear tarea (status 201)
   - GET  /{id}     -> obtener tarea por id (404 si no existe)
   - PATCH /{id}    -> marcar tarea como completada
   - DELETE /{id}   -> eliminar tarea (204)

3. Crear router_categorias (prefix="/categorias", tags=["Categorias"]):
   - GET  /         -> listar categorias
   - POST /         -> crear categoria (status 201)

4. Crear router_utilidades (prefix="/utilidades", tags=["Utilidades"]):
   - GET /estadisticas -> total tareas, completadas, pendientes, por categoria

5. Montar los 3 routers en la app

PRUEBAS:
    uvicorn ejercicio_03:app --reload

    # Probar con curl o /docs:
    POST http://localhost:8000/categorias  (body: {"nombre": "Trabajo"})
    POST http://localhost:8000/tareas      (body: {"titulo": "Revisar PRs", "categoria_id": 1})
    GET  http://localhost:8000/tareas
    PATCH http://localhost:8000/tareas/1
    GET  http://localhost:8000/utilidades/estadisticas

PISTAS:
- Usa dict como base de datos en memoria (como en los ejemplos)
- PATCH para marcar completada solo necesita cambiar el campo `completada`
- Las estadisticas pueden contar con sum() y len()
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
# TODO: Definir los modelos Pydantic
# =============================================================================

# class TareaBase(BaseModel):
#     titulo: str = Field(min_length=1)
#     descripcion: str = ""

# class TareaCrear(TareaBase):
#     categoria_id: int | None = None

# class TareaResponse(TareaBase):
#     id: int
#     completada: bool
#     categoria_id: int | None = None

# class Categoria(BaseModel):
#     nombre: str = Field(min_length=1)
#     descripcion: str = ""

# class CategoriaResponse(Categoria):
#     id: int


# =============================================================================
# TODO: Crear router_tareas con prefix="/tareas", tags=["Tareas"]
# Endpoints: GET /, POST /, GET /{id}, PATCH /{id}, DELETE /{id}
# =============================================================================

# router_tareas = APIRouter(prefix="/tareas", tags=["Tareas"])

# @router_tareas.get("/")
# def listar_tareas():
#     ...

# @router_tareas.post("/", status_code=status.HTTP_201_CREATED)
# def crear_tarea(tarea: TareaCrear):
#     ...

# @router_tareas.get("/{tarea_id}")
# def obtener_tarea(tarea_id: int):
#     ...

# @router_tareas.patch("/{tarea_id}")
# def completar_tarea(tarea_id: int):
#     ...

# @router_tareas.delete("/{tarea_id}", status_code=status.HTTP_204_NO_CONTENT)
# def eliminar_tarea(tarea_id: int):
#     ...


# =============================================================================
# TODO: Crear router_categorias con prefix="/categorias", tags=["Categorias"]
# Endpoints: GET /, POST /
# =============================================================================

# router_categorias = APIRouter(prefix="/categorias", tags=["Categorias"])

# @router_categorias.get("/")
# def listar_categorias():
#     ...

# @router_categorias.post("/", status_code=status.HTTP_201_CREATED)
# def crear_categoria(categoria: Categoria):
#     ...


# =============================================================================
# TODO: Crear router_utilidades con prefix="/utilidades", tags=["Utilidades"]
# Endpoint: GET /estadisticas
# =============================================================================

# router_utilidades = APIRouter(prefix="/utilidades", tags=["Utilidades"])

# @router_utilidades.get("/estadisticas")
# def estadisticas():
#     ...


# =============================================================================
# TODO: Montar los 3 routers en la app
# =============================================================================

# app.include_router(router_tareas)
# app.include_router(router_categorias)
# app.include_router(router_utilidades)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
