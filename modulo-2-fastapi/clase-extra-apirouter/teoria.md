# Teoria: APIRouter y Organizacion de Proyecto

## El Problema del Archivo Monolitico

Hasta ahora, todas las APIs del curso viven en un solo archivo:

```python
# api_productos.py - todo junto
app = FastAPI()

@app.get("/productos")
def listar_productos(): ...

@app.post("/productos")
def crear_producto(): ...

@app.get("/categorias")
def listar_categorias(): ...

@app.get("/estadisticas")
def estadisticas(): ...
```

Esto funciona para ejemplos y APIs pequenas. Pero cuando la API crece a 20, 50 o 100 endpoints, un solo archivo se vuelve inmanejable: conflictos de merge en equipos, dificultad para encontrar funciones, y todo acoplado sin separacion logica.

---

## ¿Que es APIRouter?

`APIRouter` es una clase de FastAPI que funciona como una **mini-aplicacion**. Permite definir rutas exactamente igual que con `FastAPI()`, pero sin crear un servidor completo. Despues, se **monta** el router en la aplicacion principal.

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def listar():
    return []

@router.post("/")
def crear():
    return {"creado": True}
```

Es lo mismo que `@app.get` y `@app.post`, pero sobre un `router` en vez de `app`.

### Analogias con Otros Frameworks

| Framework | Concepto Equivalente |
|-----------|---------------------|
| **FastAPI** | `APIRouter` |
| **Flask** | `Blueprint` |
| **Django** | `URLconf` por app |
| **Express.js** | `Router()` |

La idea es identica en todos: separar rutas en modulos independientes que se montan en la aplicacion principal.

---

## include_router: Montando Routers

Para que un router sea parte de la aplicacion, se usa `include_router()`:

```python
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)
```

### Parametros Clave

| Parametro | Descripcion | Ejemplo |
|-----------|-------------|---------|
| `router` | Instancia de APIRouter | `router_productos` |
| `prefix` | Prefijo de URL para todas las rutas | `"/productos"` |
| `tags` | Agrupacion en Swagger UI | `["Productos"]` |
| `dependencies` | Dependencias para TODAS las rutas | `[Depends(verificar_auth)]` |
| `responses` | Respuestas comunes documentadas | `{404: {"description": "No encontrado"}}` |

### Prefijos Acumulativos

Los prefijos se acumulan. Si el router tiene `prefix="/libros"` y se monta con `prefix="/api/v1"`:

```python
router = APIRouter(prefix="/libros")
app.include_router(router, prefix="/api/v1")

# Ruta final: /api/v1/libros
```

---

## Donde Definir prefix y tags

Hay dos lugares para definir `prefix` y `tags`: en el constructor del router o en `include_router()`.

### Opcion A: En el constructor

```python
router = APIRouter(prefix="/productos", tags=["Productos"])

# En main.py
app.include_router(router)
```

### Opcion B: En include_router

```python
router = APIRouter()

# En main.py
app.include_router(router, prefix="/productos", tags=["Productos"])
```

### ¿Cual usar?

- **Opcion A** si el router siempre tendra el mismo prefijo (lo comun)
- **Opcion B** si el mismo router podria montarse en diferentes prefijos (poco frecuente)

En la practica, la opcion A es mas clara porque el router declara su propio prefijo.

---

## Patron de Organizacion: Monolitico vs Modular

### Estilo Monolitico (un archivo)

```
mi_api/
└── main.py          # TODO aqui: app, modelos, rutas, logica
```

### Estilo Modular (multiples archivos)

```
mi_api/
├── main.py              # Solo crea app y monta routers
├── routers/
│   ├── __init__.py
│   ├── productos.py     # Router de productos
│   ├── categorias.py    # Router de categorias
│   └── utilidades.py    # Router de utilidades
├── models/
│   ├── __init__.py
│   └── schemas.py       # Modelos Pydantic
└── services/
    ├── __init__.py
    └── tienda.py        # Logica de negocio
```

### El main.py Modular

```python
# main.py - limpio y declarativo
from fastapi import FastAPI
from routers import productos, categorias, utilidades

app = FastAPI(title="Tienda API")

app.include_router(productos.router)
app.include_router(categorias.router)
app.include_router(utilidades.router)
```

El `main.py` solo se encarga de crear la aplicacion y montar los routers. No tiene logica de negocio ni definiciones de modelos.

---

## Dependencias Compartidas en Routers

Una de las ventajas mas practicas de APIRouter es aplicar dependencias a nivel de router:

```python
router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(verificar_admin)]
)

# TODAS las rutas de este router requieren verificar_admin
@router.get("/usuarios")
def listar_usuarios(): ...

@router.delete("/usuarios/{id}")
def eliminar_usuario(id: int): ...
```

Sin APIRouter, tendrian que agregar `Depends(verificar_admin)` a cada endpoint individual.

---

## ¿Cuando Conviene Separar en Routers?

| Situacion | ¿Separar? | Razon |
|-----------|-----------|-------|
| API con 3-5 endpoints | No | Un archivo es suficiente |
| API con 10+ endpoints | Si | Mejora navegacion y mantenimiento |
| Multiples recursos (productos, usuarios, pedidos) | Si | Cada recurso en su router |
| Equipos trabajando en paralelo | Si | Evita conflictos de merge |
| Dependencias diferentes por grupo de rutas | Si | Dependencias a nivel de router |
| Prototipo o prueba rapida | No | No sobre-disenar |

La regla practica: si tienen que hacer scroll para encontrar un endpoint, es momento de separar.

---

## Resumen

- `APIRouter` es una mini-aplicacion que agrupa rutas relacionadas
- `include_router()` monta el router en la aplicacion con prefijo, tags y dependencias
- Los prefijos eliminan repeticion en las URLs de cada endpoint
- Los tags organizan automaticamente la documentacion en Swagger UI
- El patron modular separa la aplicacion en `routers/`, `models/` y `services/`
- Las dependencias a nivel de router aplican a todas sus rutas sin repetir codigo
- No toda API necesita routers; es una herramienta para cuando el proyecto crece
