---
marp: true
theme: default
paginate: true
header: 'Clase Extra: APIRouter y Organizacion de Proyecto'
footer: 'Curso APIs Python - Modulo 2'
---

# Clase Extra
## APIRouter y Organizacion de Proyecto

---

# El Problema: API Monolitica

```python
# Todo en un solo archivo... 200, 500, 1000 lineas
@app.get("/libros")
@app.post("/libros")
@app.get("/libros/{id}")
@app.get("/autores")
@app.post("/autores")
@app.get("/autores/{id}")
@app.get("/ventas")
@app.get("/reportes")
# ... y sigue creciendo
```

Dificil de mantener, navegar y trabajar en equipo.

---

# La Solucion: APIRouter

`APIRouter` permite **separar endpoints en grupos logicos**, cada uno en su propio modulo.

```python
from fastapi import APIRouter

router_libros = APIRouter(
    prefix="/libros",
    tags=["Libros"],
)
```

Es como una "mini-app" que luego se monta en la app principal.

---

# Crear un Router

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/libros",    # Prefijo para TODAS las rutas
    tags=["Libros"],     # Agrupacion en /docs
)

@router.get("/")              # → GET /libros/
def listar_libros():
    return [{"titulo": "Python 101"}]

@router.get("/{libro_id}")    # → GET /libros/42
def obtener_libro(libro_id: int):
    return {"id": libro_id}
```

---

# Montar con include_router

```python
from fastapi import FastAPI

app = FastAPI()

# Montar los routers
app.include_router(router_libros)
app.include_router(router_autores)
```

La app principal solo monta routers. Limpio y organizado.

---

# prefix y tags

| Parametro | Efecto |
|-----------|--------|
| `prefix` | Prefijo de URL para todas las rutas del router |
| `tags` | Agrupacion visual en Swagger UI (/docs) |

```python
router = APIRouter(prefix="/libros", tags=["Libros"])

@router.get("/")          # URL final: /libros/
@router.get("/{id}")      # URL final: /libros/{id}
@router.post("/")         # URL final: /libros/
```

Las rutas en el router son **relativas** al prefix.

---

# Rutas Relativas (Clave)

```python
# CORRECTO: ruta relativa al prefix
router = APIRouter(prefix="/libros")

@router.get("/")          # → /libros/
@router.get("/{id}")      # → /libros/{id}
```

```python
# INCORRECTO: repitiendo el prefix
@router.get("/libros")       # → /libros/libros  ❌
@router.get("/libros/{id}")  # → /libros/libros/{id}  ❌
```

---

# Dependencias Compartidas

Ejecutar logica en **cada endpoint** de un router:

```python
from fastapi import Depends

def log_peticion():
    print("Peticion recibida")

router = APIRouter(
    prefix="/contactos",
    tags=["Contactos"],
    dependencies=[Depends(log_peticion)],  # ← En cada endpoint
)
```

Util para: logging, autenticacion, rate limiting.

---

# Patron Modular

```
mi_api/
├── main.py              # App + include_router
├── routers/
│   ├── libros.py        # Router de libros
│   ├── autores.py       # Router de autores
│   └── utilidades.py    # Router de utilidades
└── models/
    └── schemas.py       # Modelos Pydantic
```

Cada router en su propio archivo, importado desde `main.py`.

---

# main.py

```python
from fastapi import FastAPI
from routers import libros, autores, utilidades

app = FastAPI(title="Mi API")

app.include_router(libros.router)
app.include_router(autores.router)
app.include_router(utilidades.router)
```

`main.py` es un **punto de montaje**, no contiene logica de endpoints.

---

# Cuando Separar en Routers

| Situacion | Accion |
|-----------|--------|
| < 5 endpoints | Un solo archivo esta bien |
| 5-15 endpoints | Separar por dominio (libros, autores) |
| > 15 endpoints | Estructura modular completa |
| Trabajo en equipo | Siempre separar (menos conflictos git) |

La regla: **si cuesta encontrar un endpoint, es hora de separar**.

---

# Parametros de include_router

```python
# Se pueden sobreescribir al montar
app.include_router(
    router_libros,
    prefix="/api/v1/libros",   # Sobreescribe prefix del router
    tags=["Libros v1"],        # Sobreescribe tags
    dependencies=[Depends(verificar_api_key)],
)
```

Util para: versionado de API, agregar auth global.

---

# Errores Comunes

| Error | Solucion |
|-------|----------|
| Rutas duplicadas `/libros/libros` | Usar rutas relativas en el router |
| Olvidar `include_router` | La app no registra los endpoints |
| Dependencia no se ejecuta | Verificar `dependencies=[Depends(...)]` |
| Import circular | Separar modelos en archivo aparte |
| Router sin prefix | Los endpoints quedan en la raiz `/` |

---

# Ejercicios

1. `ejercicio_01.py` → Separar API de libreria en 2 routers
2. `ejercicio_02.py` → Refactorizar API de contactos + dependencia
3. `ejercicio_03.py` → TODO App con 3 routers desde cero

---

# Resumen

- `APIRouter` = mini-app para agrupar endpoints
- `prefix` define el prefijo de URL, `tags` agrupa en /docs
- Las rutas dentro del router son **relativas**
- `dependencies` ejecuta logica en cada endpoint del router
- `include_router` monta el router en la app
- Separar por dominio mejora mantenibilidad

---

# Preguntas?

## Proxima clase:
**SQLAlchemy y Bases de Datos**

---

# Tarea para Casa

1. Completar los 3 ejercicios
2. Tomar una API de clase 06 o 07 y separarla en routers
3. (Opcional) Crear estructura multi-archivo con routers en carpetas separadas
