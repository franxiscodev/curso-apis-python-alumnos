"""
Ejercicio 03: API de Tareas (TODO)
==================================
Crear una API completa de gestión de tareas.

OBJETIVO:
Implementar una API REST completa con request body, response models y status codes.

INSTRUCCIONES:
1. Definir los siguientes modelos Pydantic:

   TareaCrear (para crear):
   - titulo: str, 1-100 caracteres
   - descripcion: str opcional, máx 500 caracteres
   - prioridad: Literal["baja", "media", "alta"], default "media"
   - fecha_limite: str opcional (formato fecha como string)

   TareaActualizar (para actualizar, todos opcionales):
   - titulo: str opcional, 1-100 caracteres
   - descripcion: str opcional
   - prioridad: Literal["baja", "media", "alta"] opcional
   - completada: bool opcional
   - fecha_limite: str opcional

   TareaResponse (para respuesta):
   - id: int
   - titulo: str
   - descripcion: str opcional
   - prioridad: str
   - completada: bool
   - fecha_limite: str opcional
   - fecha_creacion: str

2. Implementar endpoints:

   GET /tareas
   - Query: completada (bool opcional), prioridad (str opcional)
   - Response: list[TareaResponse]
   - Retornar lista de tareas (puede ser lista vacía o con datos de ejemplo)

   POST /tareas
   - Body: TareaCrear
   - Response: TareaResponse
   - Status: 201 Created
   - Crear tarea y retornarla con ID asignado

   GET /tareas/{tarea_id}
   - Path: tarea_id >= 1
   - Response: TareaResponse
   - Error 404 si no existe

   PUT /tareas/{tarea_id}
   - Path: tarea_id >= 1
   - Body: TareaActualizar
   - Response: TareaResponse
   - Error 404 si no existe

   DELETE /tareas/{tarea_id}
   - Path: tarea_id >= 1
   - Status: 204 No Content
   - Error 404 si no existe

   GET /tareas/estadisticas
   - Retornar: total, completadas, pendientes, por_prioridad

NOTA: Usar un diccionario en memoria como "base de datos".

PRUEBAS:
    uvicorn ejercicio_03:app --reload

    # Crear tarea
    curl -X POST http://localhost:8000/tareas \
         -H "Content-Type: application/json" \
         -d '{"titulo": "Mi tarea", "prioridad": "alta"}'

    # Listar tareas
    curl http://localhost:8000/tareas

    # Filtrar por prioridad
    curl "http://localhost:8000/tareas?prioridad=alta"

PISTAS:
- Usa HTTPException con status_code=404 para errores
- status.HTTP_201_CREATED para POST exitoso
- status.HTTP_204_NO_CONTENT para DELETE exitoso
- response_model en el decorador para filtrar la respuesta
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
# MODELOS - TODO: Completar los modelos
# =============================================================================


class TareaCrear(BaseModel):
    """Modelo para crear tarea."""
    # TODO: Definir campos
    pass


class TareaActualizar(BaseModel):
    """Modelo para actualizar tarea (todos opcionales)."""
    # TODO: Definir campos
    pass


class TareaResponse(BaseModel):
    """Modelo de respuesta."""
    # TODO: Definir campos
    pass


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
# ENDPOINTS - TODO: Implementar
# =============================================================================


# TODO: GET /tareas - Listar tareas con filtros opcionales


# TODO: GET /tareas/estadisticas - IMPORTANTE: debe ir ANTES de /tareas/{tarea_id}


# TODO: POST /tareas - Crear tarea (status 201)


# TODO: GET /tareas/{tarea_id} - Obtener tarea por ID


# TODO: PUT /tareas/{tarea_id} - Actualizar tarea


# TODO: DELETE /tareas/{tarea_id} - Eliminar tarea (status 204)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
