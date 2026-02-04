# CRUD Completo - Cheatsheet

Guía rápida de patrones CRUD, paginación y filtrado.

---

## Modelos Separados

```python
from pydantic import BaseModel, Field

class ItemBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    precio: float = Field(gt=0)

class ItemCrear(ItemBase):
    pass  # Hereda todo de Base

class ItemActualizar(BaseModel):
    nombre: str | None = None       # Todo opcional
    precio: float | None = None

class ItemResponse(ItemBase):
    id: int                         # Campos extra
    disponible: bool
```

---

## CRUD Completo

```python
from fastapi import FastAPI, HTTPException, Path, status

app = FastAPI()
items_db: dict[int, dict] = {}
contador = 0

# LISTAR
@app.get("/items", response_model=list[ItemResponse])
def listar():
    return list(items_db.values())

# CREAR
@app.post("/items", response_model=ItemResponse, status_code=201)
def crear(item: ItemCrear):
    global contador
    contador += 1
    nuevo = {"id": contador, **item.model_dump()}
    items_db[contador] = nuevo
    return nuevo

# OBTENER
@app.get("/items/{id}", response_model=ItemResponse)
def obtener(id: int = Path(ge=1)):
    if id not in items_db:
        raise HTTPException(status_code=404, detail="No encontrado")
    return items_db[id]

# ACTUALIZAR (parcial)
@app.put("/items/{id}", response_model=ItemResponse)
def actualizar(id: int = Path(ge=1), item: ItemActualizar = ...):
    if id not in items_db:
        raise HTTPException(status_code=404, detail="No encontrado")
    actual = items_db[id]
    datos = item.model_dump(exclude_none=True)
    for campo, valor in datos.items():
        actual[campo] = valor
    return actual

# ELIMINAR
@app.delete("/items/{id}", status_code=204)
def eliminar(id: int = Path(ge=1)):
    if id not in items_db:
        raise HTTPException(status_code=404, detail="No encontrado")
    del items_db[id]
```

---

## Paginación con Metadata

```python
import math
from fastapi import Query
from pydantic import BaseModel

class PaginatedResponse(BaseModel):
    items: list[ItemResponse]
    total: int
    page: int
    size: int
    pages: int

def paginar(items: list, page: int, size: int) -> dict:
    total = len(items)
    pages = math.ceil(total / size) if total > 0 else 0
    start = (page - 1) * size
    return {
        "items": items[start:start + size],
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }

@app.get("/items", response_model=PaginatedResponse)
def listar(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100)
):
    return paginar(list(items_db.values()), page, size)
```

---

## Filtrado

```python
@app.get("/items")
def listar(
    categoria: str | None = Query(default=None),
    precio_min: float | None = Query(default=None, ge=0),
    precio_max: float | None = Query(default=None, ge=0),
    buscar: str | None = Query(default=None, min_length=2),
):
    resultados = list(items_db.values())

    if categoria:
        resultados = [i for i in resultados if i["categoria"] == categoria]
    if precio_min is not None:
        resultados = [i for i in resultados if i["precio"] >= precio_min]
    if precio_max is not None:
        resultados = [i for i in resultados if i["precio"] <= precio_max]
    if buscar:
        resultados = [i for i in resultados
                      if buscar.lower() in i["nombre"].lower()]
    return resultados
```

---

## Ordenamiento

```python
from typing import Literal

@app.get("/items")
def listar(
    sort_by: Literal["nombre", "precio"] = Query(default="nombre"),
    order: Literal["asc", "desc"] = Query(default="asc")
):
    resultados = list(items_db.values())
    resultados.sort(
        key=lambda i: i[sort_by],
        reverse=(order == "desc")
    )
    return resultados
```

---

## Errores HTTP

```python
from fastapi import HTTPException, status

# No encontrado
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Recurso no encontrado"
)

# Duplicado
raise HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Ya existe un recurso con ese nombre"
)

# Error de negocio
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Operación no permitida"
)
```

---

## Status Codes por Operación

| Operación | Éxito | Errores Comunes |
|-----------|-------|-----------------|
| GET lista | 200 OK | - |
| GET uno | 200 OK | 404 Not Found |
| POST | 201 Created | 409 Conflict |
| PUT/PATCH | 200 OK | 404, 400 |
| DELETE | 204 No Content | 404, 400 |

---

## Orden de Procesamiento

```
1. Filtrar    → Reducir resultados
2. Ordenar    → Aplicar sort
3. Paginar    → Cortar en páginas
```

---

## Tips

1. **Siempre separa modelos** - Create, Update y Response tienen necesidades distintas
2. **`exclude_none=True`** - Para updates parciales sin sobrescribir con None
3. **Metadata en paginación** - El frontend necesita saber total y páginas
4. **Filtros opcionales** - Si no se envía, no filtra
5. **Validación de negocio** - HTTPException para reglas que Pydantic no cubre
6. **Status codes correctos** - 201 para crear, 204 para eliminar, 409 para duplicados
