# FastAPI Cheatsheet

Guía rápida de referencia para FastAPI.

---

## Instalación y Ejecución

```bash
# Instalar
uv add fastapi uvicorn

# Ejecutar servidor
uvicorn main:app --reload

# Con host y puerto
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## Aplicación Básica

```python
from fastapi import FastAPI

app = FastAPI(
    title="Mi API",
    description="Descripción de la API",
    version="1.0.0"
)

@app.get("/")
def raiz():
    return {"mensaje": "Hola"}
```

---

## Métodos HTTP

```python
@app.get("/items")           # Leer/Listar
@app.post("/items")          # Crear
@app.put("/items/{id}")      # Reemplazar completo
@app.patch("/items/{id}")    # Actualizar parcial
@app.delete("/items/{id}")   # Eliminar
```

---

## Path Parameters

```python
# Básico
@app.get("/items/{item_id}")
def obtener(item_id: int):
    return {"id": item_id}

# Con validación
from fastapi import Path

@app.get("/items/{item_id}")
def obtener(
    item_id: int = Path(
        ge=1,                    # >= 1
        le=1000,                 # <= 1000
        title="ID del Item",
        description="ID único"
    )
):
    return {"id": item_id}

# Capturar path completo
@app.get("/files/{file_path:path}")
def archivo(file_path: str):
    return {"path": file_path}
```

---

## Query Parameters

```python
# Con defaults
@app.get("/items")
def listar(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

# Opcional (puede ser None)
@app.get("/items")
def listar(categoria: str | None = None):
    return {"categoria": categoria}

# Requerido (sin default)
@app.get("/buscar")
def buscar(q: str):  # Obligatorio
    return {"query": q}

# Con validación
from fastapi import Query

@app.get("/items")
def listar(
    q: str | None = Query(
        default=None,
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z]+$",
        title="Búsqueda",
        description="Término de búsqueda"
    )
):
    return {"q": q}

# Lista de valores
@app.get("/items")
def listar(tags: list[str] = Query(default=[])):
    return {"tags": tags}
# GET /items?tags=a&tags=b → ["a", "b"]
```

---

## Request Body

```python
from pydantic import BaseModel, Field

class ItemCrear(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    precio: float = Field(gt=0)
    cantidad: int = Field(default=1, ge=1)
    descripcion: str | None = None

@app.post("/items")
def crear(item: ItemCrear):
    return {"item": item.model_dump()}

# Body + Path + Query
@app.put("/items/{item_id}")
def actualizar(
    item_id: int,               # Path
    item: ItemCrear,            # Body
    notify: bool = False        # Query
):
    return {"id": item_id, "item": item.model_dump()}
```

---

## Response Model

```python
class ItemResponse(BaseModel):
    id: int
    nombre: str
    precio: float

# Filtra la respuesta
@app.post("/items", response_model=ItemResponse)
def crear(item: ItemCrear):
    return {"id": 1, **item.model_dump(), "secreto": "no se incluye"}

# Lista como response
@app.get("/items", response_model=list[ItemResponse])
def listar():
    return [...]

# Opciones de response_model
@app.get(
    "/items/{id}",
    response_model=ItemResponse,
    response_model_exclude_unset=True,    # Solo campos establecidos
    response_model_exclude={"campo"},     # Excluir campos
    response_model_include={"campo"}      # Solo estos campos
)
```

---

## Status Codes

```python
from fastapi import status

# Códigos comunes
status.HTTP_200_OK
status.HTTP_201_CREATED
status.HTTP_204_NO_CONTENT
status.HTTP_400_BAD_REQUEST
status.HTTP_404_NOT_FOUND
status.HTTP_409_CONFLICT
status.HTTP_422_UNPROCESSABLE_ENTITY

# En decorador
@app.post("/items", status_code=status.HTTP_201_CREATED)
def crear(item: ItemCrear):
    return {"id": 1}

@app.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id: int):
    return None  # 204 no tiene body
```

---

## HTTPException

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

# Con headers adicionales
raise HTTPException(
    status_code=403,
    detail="No autorizado",
    headers={"X-Error": "Permiso denegado"}
)
```

---

## Documentación de Endpoints

```python
@app.get(
    "/items",
    summary="Listar items",           # Título corto
    description="Descripción larga",  # Detalle
    tags=["Items"],                   # Agrupar en docs
    deprecated=True,                  # Marcar obsoleto
    responses={                       # Documentar responses
        404: {"description": "No encontrado"},
        500: {"description": "Error interno"}
    }
)
def listar():
    """
    Docstring también aparece en docs.

    - **param1**: Descripción
    - **param2**: Descripción
    """
    return []
```

---

## Múltiples Responses

```python
class MensajeError(BaseModel):
    detail: str

@app.get(
    "/items/{id}",
    response_model=ItemResponse,
    responses={
        404: {"model": MensajeError, "description": "No encontrado"},
        500: {"description": "Error interno"}
    }
)
def obtener(id: int):
    ...
```

---

## Orden de Rutas

```python
# ⚠️ El orden importa

# Correcto: ruta específica ANTES de la general
@app.get("/users/me")        # Primero
def usuario_actual(): ...

@app.get("/users/{user_id}") # Después
def obtener_usuario(user_id: int): ...

# Si estuvieran al revés, /users/me intentaría
# convertir "me" a int → Error
```

---

## Validadores de Pydantic

```python
from pydantic import BaseModel, Field, field_validator
from typing import Literal

class Item(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    precio: float = Field(gt=0, le=99999)
    cantidad: int = Field(default=1, ge=0)
    estado: Literal["activo", "inactivo"] = "activo"
    email: EmailStr  # Requiere: uv add pydantic[email]

    @field_validator("nombre")
    @classmethod
    def nombre_capitalizado(cls, v: str) -> str:
        return v.title()
```

---

## Ejecución Programática

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=True  # Solo desarrollo
    )
```

---

## URLs de Documentación

| URL | Descripción |
|-----|-------------|
| `/docs` | Swagger UI (interactivo) |
| `/redoc` | ReDoc (lectura) |
| `/openapi.json` | Esquema OpenAPI |

---

## Ejemplo CRUD Completo

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

class ItemBase(BaseModel):
    nombre: str = Field(min_length=1)
    precio: float = Field(gt=0)

class ItemCrear(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int

items_db: dict[int, dict] = {}
contador = 0

@app.get("/items", response_model=list[ItemResponse])
def listar():
    return list(items_db.values())

@app.get("/items/{item_id}", response_model=ItemResponse)
def obtener(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="No encontrado")
    return items_db[item_id]

@app.post("/items", response_model=ItemResponse, status_code=201)
def crear(item: ItemCrear):
    global contador
    contador += 1
    nuevo = {"id": contador, **item.model_dump()}
    items_db[contador] = nuevo
    return nuevo

@app.delete("/items/{item_id}", status_code=204)
def eliminar(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="No encontrado")
    del items_db[item_id]
```

---

## Tips

1. **Siempre usa type hints** - FastAPI los necesita para validación
2. **Pydantic para bodies** - Nunca uses `dict` directamente
3. **response_model** - Filtra datos sensibles automáticamente
4. **Status codes** - Usa los apropiados (201 crear, 204 delete, etc.)
5. **HTTPException** - Para errores controlados
6. **Orden de rutas** - Específicas antes de genéricas
7. **--reload** - Solo en desarrollo, no en producción
