# APIRouter - Cheatsheet

Guia rapida de APIRouter y organizacion de proyecto en FastAPI.

---

## Crear un Router

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/libros",
    tags=["Libros"],
)
```

---

## Montar en la App

```python
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)
```

---

## prefix y tags

```python
router = APIRouter(
    prefix="/libros",     # Prefijo de URL para todas las rutas
    tags=["Libros"],      # Agrupacion en Swagger UI (/docs)
)
```

| Parametro | Tipo | Efecto |
|-----------|------|--------|
| `prefix` | `str` | Se antepone a cada ruta del router |
| `tags` | `list[str]` | Agrupa endpoints en la documentacion |
| `dependencies` | `list[Depends]` | Dependencias para cada endpoint |
| `responses` | `dict` | Respuestas comunes para todos los endpoints |

---

## Rutas Relativas

Las rutas dentro del router son **relativas** al prefix:

```python
router = APIRouter(prefix="/libros")

@router.get("/")          # URL final: GET /libros/
@router.post("/")         # URL final: POST /libros/
@router.get("/{id}")      # URL final: GET /libros/{id}
@router.put("/{id}")      # URL final: PUT /libros/{id}
@router.delete("/{id}")   # URL final: DELETE /libros/{id}
```

**NO repetir el prefix en las rutas:**
```python
# MAL: genera /libros/libros
@router.get("/libros")

# BIEN: genera /libros/
@router.get("/")
```

---

## Dependencias Compartidas

```python
from fastapi import Depends

def verificar_auth():
    # logica de autenticacion
    pass

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(verificar_auth)],  # Se ejecuta en cada endpoint
)
```

---

## Estructura de Proyecto

### Minima (archivo unico)
```python
# main.py
from fastapi import FastAPI, APIRouter

router_libros = APIRouter(prefix="/libros", tags=["Libros"])
router_autores = APIRouter(prefix="/autores", tags=["Autores"])

# ... endpoints ...

app = FastAPI()
app.include_router(router_libros)
app.include_router(router_autores)
```

### Modular (multiples archivos)
```
proyecto/
├── main.py
├── routers/
│   ├── __init__.py
│   ├── libros.py
│   └── autores.py
└── models/
    ├── __init__.py
    └── schemas.py
```

```python
# routers/libros.py
from fastapi import APIRouter
router = APIRouter(prefix="/libros", tags=["Libros"])

@router.get("/")
def listar():
    return []
```

```python
# main.py
from fastapi import FastAPI
from routers import libros, autores

app = FastAPI()
app.include_router(libros.router)
app.include_router(autores.router)
```

---

## Parametros de include_router

```python
app.include_router(
    router,
    prefix="/api/v1/libros",        # Sobreescribir prefix
    tags=["Libros v1"],             # Sobreescribir tags
    dependencies=[Depends(auth)],   # Agregar dependencias
    responses={404: {"description": "No encontrado"}},
)
```

Se pueden sobreescribir prefix, tags y dependencias al montar.

---

## Tips

1. **Rutas relativas**: Nunca repetir el prefix dentro del router
2. **Un router por dominio**: libros, autores, utilidades = 3 routers
3. **Dependencias a nivel de router**: Ideal para auth y logging
4. **main.py limpio**: Solo crear app + include_router, sin logica de endpoints
5. **Tags descriptivos**: Mejoran la navegacion en Swagger UI
6. **Prefix con `/`**: Siempre empezar con `/` (ej: `/libros`, no `libros`)
7. **Orden de montaje**: El orden de include_router define el orden en /docs
