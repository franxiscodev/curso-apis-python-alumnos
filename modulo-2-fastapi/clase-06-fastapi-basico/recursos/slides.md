---
marp: true
theme: default
paginate: true
header: 'Clase 06: FastAPI Básico'
footer: 'Curso APIs Avanzadas con Python'
---

# FastAPI Básico
## Rutas y Parámetros

Clase 06 - Módulo 2: FastAPI

---

# ¿Qué es FastAPI?

Framework **moderno** y de **alto rendimiento** para APIs en Python

| Característica | Beneficio |
|----------------|-----------|
| Rápido | Comparable a Node.js y Go |
| Tipado | Basado en type hints |
| Validación | Automática con Pydantic |
| Documentación | Swagger UI automático |

---

# Stack de FastAPI

```
Tu Código (FastAPI)
       ↓
   Pydantic (Validación)
       ↓
   Starlette (Framework ASGI)
       ↓
   Uvicorn (Servidor)
```

Cada capa tiene una responsabilidad específica

---

# Primera Aplicación

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def raiz():
    return {"mensaje": "¡Hola, FastAPI!"}
```

**Ejecutar:**
```bash
uvicorn main:app --reload
```

---

# Documentación Automática

Una vez ejecutando, visita:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

FastAPI genera documentación interactiva automáticamente

---

# Métodos HTTP

```python
@app.get("/items")        # Leer/Listar
def listar(): ...

@app.post("/items")       # Crear
def crear(): ...

@app.put("/items/{id}")   # Reemplazar
def reemplazar(id: int): ...

@app.patch("/items/{id}") # Actualizar parcial
def actualizar(id: int): ...

@app.delete("/items/{id}") # Eliminar
def eliminar(id: int): ...
```

---

# Path Parameters

Valores en la URL:

```python
@app.get("/usuarios/{usuario_id}")
def obtener_usuario(usuario_id: int):
    return {"id": usuario_id}
```

**Validación automática del tipo:**
- `GET /usuarios/42` → `{"id": 42}`
- `GET /usuarios/abc` → Error 422

---

# Path con Validación

```python
from fastapi import Path

@app.get("/items/{item_id}")
def obtener_item(
    item_id: int = Path(
        ge=1,        # >= 1
        le=1000,     # <= 1000
        description="ID del item"
    )
):
    return {"item_id": item_id}
```

---

# Query Parameters

Valores después del `?`:

```python
@app.get("/items")
def listar(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

**Ejemplos:**
- `GET /items` → skip=0, limit=10
- `GET /items?skip=5&limit=20` → skip=5, limit=20

---

# Query con Validación

```python
from fastapi import Query

@app.get("/buscar")
def buscar(
    q: str = Query(
        min_length=3,
        max_length=50,
        description="Término de búsqueda"
    ),
    page: int = Query(default=1, ge=1)
):
    return {"query": q, "page": page}
```

---

# Request Body

Datos en el cuerpo (POST, PUT, PATCH):

```python
from pydantic import BaseModel

class ItemCrear(BaseModel):
    nombre: str
    precio: float
    cantidad: int = 1

@app.post("/items")
def crear_item(item: ItemCrear):
    return {"item": item.model_dump()}
```

---

# Combinando Todo

```python
@app.put("/items/{item_id}")
def actualizar(
    item_id: int,              # Path
    item: ItemActualizar,      # Body
    notify: bool = False       # Query
):
    return {
        "id": item_id,
        "cambios": item.model_dump(),
        "notificar": notify
    }
```

---

# Response Model

Controla qué datos retornas:

```python
class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    # Sin password

@app.post("/usuarios", response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCrear):
    # Aunque retornemos password,
    # FastAPI lo filtra
    return usuario_guardado
```

---

# Status Codes

```python
from fastapi import status

@app.post("/items", status_code=status.HTTP_201_CREATED)
def crear():
    return {"id": 1}

@app.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id: int):
    return None
```

---

# HTTPException

```python
from fastapi import HTTPException, status

@app.get("/items/{item_id}")
def obtener(item_id: int):
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} no encontrado"
        )
    return items_db[item_id]
```

---

# Resumen

| Concepto | Sintaxis |
|----------|----------|
| Ruta GET | `@app.get("/path")` |
| Path param | `/items/{id}` → `def f(id: int)` |
| Query param | `?key=val` → `def f(key: str = None)` |
| Body | `def f(item: MiModelo)` |
| Response | `response_model=Modelo` |
| Status | `status_code=201` |

---

# Ejercicio Práctico

Crear una **API de Tareas (TODO)**:

1. Modelos Pydantic para crear/actualizar/respuesta
2. CRUD completo con endpoints
3. Filtros por query parameters
4. Status codes apropiados
5. HTTPException para errores

---

# Próxima Clase

**Clase 07: CRUD Completo**

- Base de datos en memoria estructurada
- Operaciones CRUD completas
- Manejo de errores avanzado
- Validaciones de negocio

---

# Recursos

- **Documentación**: https://fastapi.tiangolo.com
- **Uvicorn**: https://www.uvicorn.org
- **Pydantic**: https://docs.pydantic.dev

**Practica:**
```bash
uvicorn ejemplos.01_hola_mundo:app --reload
```
