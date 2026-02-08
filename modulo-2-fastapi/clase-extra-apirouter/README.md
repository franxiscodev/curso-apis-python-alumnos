# Clase Extra: APIRouter y Organizacion de Proyecto

## Informacion General
- **Duracion**: 1.5 horas
- **Modulo**: 2 - FastAPI
- **Prerrequisitos**: Clase 06 (FastAPI Basico) y Clase 07 (CRUD Completo)

## Objetivos de Aprendizaje

Al finalizar esta clase, los estudiantes podran:

1. Crear y configurar instancias de `APIRouter`
2. Registrar rutas en routers independientes con prefijos y tags
3. Montar multiples routers en una aplicacion FastAPI
4. Organizar un proyecto FastAPI en modulos (routers, models, services)
5. Usar dependencias compartidas a nivel de router
6. Refactorizar una API monolitica a arquitectura modular

## Estructura de la Clase

| Tiempo | Actividad | Descripcion |
|--------|-----------|-------------|
| 00:00 - 00:15 | Introduccion | Problema del archivo monolitico, motivacion para APIRouter |
| 00:15 - 00:35 | Ejemplo 01 | APIRouter basico: crear routers, prefix, tags |
| 00:35 - 00:55 | Ejemplo 02 | Estructura de proyecto: dependencias, servicios, organizacion |
| 00:55 - 01:05 | **Descanso** | - |
| 01:05 - 01:25 | Ejemplo 03 | App modular: refactorizacion completa de api_productos.py |
| 01:25 - 01:30 | Ejercicios | Refactorizar APIs existentes con APIRouter |

## Contenido

### Archivos de Ejemplos
```
ejemplos/
├── 01_apirouter_basico.py      # Crear routers, prefix, tags, include_router
├── 02_estructura_proyecto.py   # Organizacion por modulos, dependencias compartidas
└── 03_app_modular.py           # Refactorizacion completa: monolitico a modular
```

### Ejercicios
```
ejercicios/
├── ejercicio_01.py            # Separar API de libreria en routers
├── ejercicio_02.py            # Refactorizar API de contactos + dependencia
├── ejercicio_03.py            # TODO App con multiples routers desde cero
├── enunciados.md              # Enunciados detallados (referencia adicional)
└── soluciones/
    ├── ejercicio_01_solucion.py
    ├── ejercicio_02_solucion.py
    └── ejercicio_03_solucion.py
```

### Recursos
```
recursos/
├── slides.md                  # Presentacion Marp
├── apirouter_cheatsheet.md    # Guia rapida de APIRouter
└── enlaces.md                 # Links a documentacion oficial
```

## Instalacion

Las dependencias de esta clase ya estan declaradas en el `pyproject.toml` del proyecto. Si usas `uv sync` no necesitas instalar nada manualmente.

Paquetes utilizados en esta clase:

```bash
# Ya incluidos en el proyecto - solo como referencia
uv add fastapi
uv add uvicorn
uv add pydantic
```

| Paquete | Uso en esta clase |
|---------|-------------------|
| `fastapi` | Framework web, `APIRouter`, `include_router` |
| `uvicorn` | Servidor ASGI para ejecutar la aplicacion |
| `pydantic` | Modelos para request/response en cada router |

## Comandos Utiles

```bash
# Ejecutar cualquier ejemplo
uvicorn ejemplos.01_apirouter_basico:app --reload
uvicorn ejemplos.02_estructura_proyecto:app --reload
uvicorn ejemplos.03_app_modular:app --reload

# Ver documentacion automatica (notar los tags agrupando endpoints)
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

## Conexiones

### Conceptos Previos
- **Clase 06**: FastAPI basico (rutas, parametros, response models)
- **Clase 07**: CRUD completo (patrones que se benefician de routers)

### Prepara Para
- **Clase 08**: SQLAlchemy (proyecto real con estructura modular)
- **Clase 09**: Autenticacion (dependencias compartidas en routers)

## Recursos Adicionales

- [FastAPI - Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [APIRouter class](https://fastapi.tiangolo.com/reference/apirouter/)
- [FastAPI - Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/)

## Notas para el Instructor

- Esta clase es un puente entre las APIs basicas (clase 06-07) y proyectos reales (clase 08+)
- Mostrar lado a lado `api_productos.py` (clase 06) y `03_app_modular.py` para ver la refactorizacion
- Enfatizar que APIRouter NO cambia la funcionalidad, solo la organizacion
- En Swagger UI, mostrar como los tags agrupan endpoints automaticamente
- Los estudiantes ya conocen dependencias de clase 07; aqui se aplican a nivel de router

## Tarea para Casa

1. Completar los ejercicios de refactorizacion
2. Tomar la API de contactos (clase 07) y separarla en routers
3. (Opcional) Crear una estructura de proyecto con archivos separados para routers, models y services
