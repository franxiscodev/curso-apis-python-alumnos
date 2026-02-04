"""
Ejercicio 03: API Observable Completa (Proyecto Integrador)
============================================================
API que integra TODOS los conceptos del curso.

INSTRUCCIONES:
Construir una API de gestión de proyectos que incluya:

1. Modelos Pydantic (Clase 05):
   - ProyectoCrear, ProyectoResponse

2. CRUD completo (Clase 07):
   - GET /proyectos (con paginación)
   - POST /proyectos
   - GET /proyectos/{id}
   - DELETE /proyectos/{id}

3. Autenticación simulada (Clase 09):
   - Header X-API-Key requerido

4. Logging estructurado (Clase 15):
   - JSON con request_id

5. Métricas (Clase 15):
   - requests_total, por_endpoint, latencia

6. Health checks (Clase 15):
   - GET /health, GET /ready, GET /metrics

PRUEBAS:
    uvicorn ejercicio_03:app --reload

    GET /health
    POST /proyectos (con header X-API-Key: mi-clave)
    GET /proyectos?page=1&size=10
    GET /metrics
"""

from fastapi import FastAPI

app = FastAPI(title="Proyecto Integrador", version="1.0.0")

# TODO: Modelos Pydantic (ProyectoCrear, ProyectoResponse)

# TODO: Logger JSON

# TODO: Métricas en memoria

# TODO: Middleware de logging + métricas + request_id

# TODO: Dependencia de autenticación (verificar X-API-Key)

# TODO: CRUD de proyectos con paginación

# TODO: Health checks (/health, /ready, /metrics)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
