# Clase Extra: APIRouter y Organizacion de Proyecto - Explicacion de Ejemplos

En las clases 06 y 07 construyeron APIs completas con FastAPI: rutas, parametros, CRUD, paginacion, filtrado. Todo en un solo archivo. Los tres archivos de esta clase resuelven la pregunta que surge naturalmente cuando el proyecto crece: como organizar el codigo para que sea mantenible. `APIRouter` es la herramienta de FastAPI para esto, y al final de estas explicaciones van a poder refactorizar cualquier API monolitica a una estructura modular.

---

## `01_apirouter_basico.py` -- Crear Routers, Prefix y Tags

Este archivo es el punto de partida: dos routers independientes (productos y usuarios) montados en una misma aplicacion. El objetivo es entender la mecanica fundamental de APIRouter sin complicaciones adicionales.

### Creacion de un router

```python
from fastapi.routing import APIRouter

router_productos = APIRouter()
```

`APIRouter()` se importa de `fastapi.routing` (tambien se puede importar directamente de `fastapi`). Al instanciarlo, obtenemos un objeto que acepta los mismos decoradores que `FastAPI()`: `.get()`, `.post()`, `.put()`, `.delete()`, `.patch()`. La diferencia es que un router no crea un servidor; es un contenedor de rutas que despues se monta en la app.

> **Pregunta frecuente**: "¿Cual es la diferencia entre `from fastapi import APIRouter` y `from fastapi.routing import APIRouter`?"
>
> Ninguna. `fastapi` re-exporta `APIRouter` desde `fastapi.routing` por conveniencia. Ambos imports son equivalentes. En el ejemplo usamos `fastapi.routing` para que quede claro de donde viene la clase, pero en codigo de produccion es mas comun `from fastapi import APIRouter`.

### Registrar rutas en el router

```python
@router_productos.get("/", response_model=list[ProductoResponse])
def listar_productos():
    """Lista todos los productos."""
    return list(productos_db.values())


@router_productos.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: Producto):
    """Crea un nuevo producto."""
    global contador_productos
    contador_productos += 1
    nuevo = {"id": contador_productos, **producto.model_dump()}
    productos_db[contador_productos] = nuevo
    return nuevo
```

Fijense que las rutas son `"/"` y `"/{producto_id}"`, no `"/productos"` ni `"/productos/{producto_id}"`. El prefijo se agrega al montar el router en la app. Esto es intencional: el router no sabe (ni le importa) bajo que URL va a vivir.

Los decoradores funcionan exactamente igual que sobre `app`: `response_model`, `status_code`, `summary`, `tags`, todo disponible. Si ya saben hacer endpoints con `@app.get`, saben hacerlos con `@router.get`.

### Montar routers con include_router

```python
app = FastAPI(
    title="APIRouter Basico",
    description="Ejemplo introductorio de APIRouter con multiples routers",
    version="1.0.0"
)

app.include_router(
    router_productos,
    prefix="/productos",
    tags=["Productos"]
)

app.include_router(
    router_usuarios,
    prefix="/usuarios",
    tags=["Usuarios"]
)
```

`include_router` es el pegamento. Toma un router y lo integra en la app. Los parametros clave:

- **`prefix`**: se antepone a todas las rutas del router. La ruta `"/"` del router se convierte en `"/productos"`. La ruta `"/{producto_id}"` se convierte en `"/productos/{producto_id}"`.
- **`tags`**: agrupan los endpoints en Swagger UI. Cuando abran `/docs`, van a ver una seccion "Productos" y otra "Usuarios" con sus endpoints respectivos.

> **Pregunta frecuente**: "¿Puedo montar el mismo router dos veces con prefijos diferentes?"
>
> Si. Podrian hacer `app.include_router(router_productos, prefix="/v1/productos")` y `app.include_router(router_productos, prefix="/v2/productos")`. Ambos conjuntos de endpoints funcionarian. Es un patron poco frecuente pero valido para versionado rapido.

### Que resuelve el prefix

Sin prefix, cada ruta del router tendria que incluir la URL completa:

```python
# SIN prefix - repetitivo
@router.get("/productos")
@router.post("/productos")
@router.get("/productos/{id}")
@router.put("/productos/{id}")
@router.delete("/productos/{id}")
```

Con prefix, las rutas son relativas:

```python
# CON prefix="/productos" - limpio
@router.get("/")
@router.post("/")
@router.get("/{id}")
@router.put("/{id}")
@router.delete("/{id}")
```

Si manana necesitan cambiar `/productos` a `/items` o a `/api/v2/productos`, solo cambian el prefix en un lugar.

**Punto clave**: `APIRouter` separa las rutas en grupos independientes. `include_router` las monta con un prefijo y tags. Las rutas del router son relativas al prefijo. Esto elimina repeticion y permite reorganizar URLs sin tocar los endpoints.

---

## `02_estructura_proyecto.py` -- Organizacion por Modulos

Este archivo da el salto de "como funciona APIRouter" a "como organizo un proyecto real". Introduce tres conceptos nuevos: separacion de logica de negocio, dependencias compartidas a nivel de router, y prefijos acumulativos.

### Separar logica de negocio del routing

```python
class BibliotecaService:
    """Separa la logica de negocio del routing."""

    def __init__(self):
        self.libros_db: dict[int, dict] = {}
        self.autores_db: dict[int, dict] = {}
        self._contador_libros = 0
        self._contador_autores = 0

    def listar_libros(self, genero: str | None = None, anio_min: int | None = None) -> list[dict]:
        resultados = list(self.libros_db.values())
        if genero:
            resultados = [l for l in resultados if l["genero"] == genero]
        if anio_min is not None:
            resultados = [l for l in resultados if l["anio"] >= anio_min]
        return resultados

    def crear_libro(self, datos: LibroCrear) -> dict:
        self._contador_libros += 1
        nuevo = {"id": self._contador_libros, **datos.model_dump()}
        self.libros_db[self._contador_libros] = nuevo
        return nuevo
```

En las clases 06 y 07, la logica de negocio (buscar, filtrar, crear, validar existencia) vivia directamente en las funciones de los endpoints. Aqui la movemos a una clase de servicio separada. Los endpoints del router solo llaman metodos del servicio:

```python
@router_libros.get("/", response_model=list[LibroResponse])
def listar_libros(
    genero: str | None = Query(default=None, description="Filtrar por genero"),
    anio_min: int | None = Query(default=None, ge=1000, description="Anio minimo")
):
    """Lista libros con filtros opcionales."""
    return biblioteca.listar_libros(genero=genero, anio_min=anio_min)
```

El endpoint se encarga de recibir parametros HTTP y retornar respuestas. El servicio se encarga de la logica. Esta separacion tiene ventajas concretas: pueden testear la logica sin levantar el servidor, pueden reusar la logica desde otros contextos (CLI, workers, scripts), y los endpoints quedan cortos y legibles.

> **Pregunta frecuente**: "¿Siempre necesito una clase de servicio?"
>
> No. Para APIs pequenas o CRUD simples, la logica en el endpoint esta bien. La clase de servicio tiene sentido cuando la logica es compleja, cuando necesitan reutilizarla, o cuando quieren testear la logica aislada. No creen abstracciones que no necesitan.

### Dependencias compartidas en el router

```python
def verificar_api_key(api_key: str = Query(description="API key de acceso")):
    if api_key != "mi-clave-secreta":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key invalida"
        )
    return api_key


router_libros = APIRouter(
    prefix="/libros",
    tags=["Libros"],
    dependencies=[Depends(verificar_api_key)]
)
```

El parametro `dependencies` en el constructor del router aplica esa dependencia a **todos** los endpoints del router. No necesitan agregar `Depends(verificar_api_key)` a cada funcion. Si el router tiene 15 endpoints, la dependencia se ejecuta antes de cada uno automaticamente.

Comparen con el enfoque sin dependencias de router:

```python
# Sin dependencias de router - repetitivo y fragil
@app.get("/libros")
def listar_libros(api_key: str = Depends(verificar_api_key)):
    ...

@app.post("/libros")
def crear_libro(api_key: str = Depends(verificar_api_key)):
    ...

@app.get("/libros/{id}")
def obtener_libro(id: int, api_key: str = Depends(verificar_api_key)):
    ...
```

Tres endpoints, tres repeticiones. Y si agregan un endpoint nuevo y olvidan la dependencia, queda desprotegido. Con dependencias de router, es imposible olvidarlo.

> **Pregunta frecuente**: "¿Las dependencias del router y las del endpoint se pueden combinar?"
>
> Si. Las dependencias del router se ejecutan primero, y luego las del endpoint. Pueden tener una dependencia de autenticacion a nivel de router y una de permisos especifica en un endpoint particular.

### Prefijos acumulativos

```python
router_libros = APIRouter(prefix="/libros", tags=["Libros"], ...)
router_autores = APIRouter(prefix="/autores", tags=["Autores"], ...)

app.include_router(router_libros, prefix="/api/v1")
app.include_router(router_autores, prefix="/api/v1")
```

El router de libros tiene prefix `/libros`. Al montarlo con prefix `/api/v1`, la ruta final es `/api/v1/libros`. Los prefijos se suman. Esto es util para:

- **Versionado**: montar los mismos routers bajo `/api/v1` y `/api/v2`
- **Agrupacion**: todas las rutas de la API bajo `/api`
- **Aislamiento**: separar la API de rutas de administracion o health checks

**Punto clave**: La estructura de proyecto separa responsabilidades. Los routers manejan HTTP (parametros, respuestas). Los servicios manejan logica de negocio. Los modelos definen la estructura de datos. Las dependencias a nivel de router evitan repeticion y aseguran que ningun endpoint quede desprotegido.

---

## `03_app_modular.py` -- Refactorizacion Completa

Este archivo es la version modular de `api_productos.py` de la clase 06. Misma funcionalidad, diferente organizacion. Es el ejemplo mas realista de la clase y el que van a usar como referencia para sus propios proyectos.

### Tres routers, una app

```python
router_productos = APIRouter(
    prefix="/productos",
    tags=["Productos"],
    responses={404: {"description": "Producto no encontrado"}}
)

router_categorias = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)

router_utilidades = APIRouter(
    prefix="/utilidades",
    tags=["Utilidades"]
)
```

Cada router tiene su prefix y tags. El router de productos ademas tiene `responses={404: {...}}`, que documenta en Swagger UI que sus endpoints pueden retornar 404. Esto no cambia la logica; es pura documentacion.

Fijense en como se distribuyen los endpoints:

| Router | Endpoints | Responsabilidad |
|--------|-----------|-----------------|
| `router_productos` | CRUD completo (GET, POST, PUT, DELETE) | Operaciones sobre productos |
| `router_categorias` | Listar categorias, productos por categoria | Consultas transversales |
| `router_utilidades` | Estadisticas, health check | Operaciones de soporte |

La separacion sigue el principio de **responsabilidad unica**: cada router se encarga de un aspecto de la API.

### Comparacion con la version monolitica

En `api_productos.py` de la clase 06:

```python
# Monolitico - todos los endpoints sobre app
@app.get("/productos", ...)
def listar_productos(): ...

@app.get("/productos/{producto_id}", ...)
def obtener_producto(): ...

@app.get("/categorias", ...)
def listar_categorias(): ...

@app.get("/estadisticas", ...)
def estadisticas(): ...
```

En `03_app_modular.py`:

```python
# Modular - cada grupo en su router
@router_productos.get("/", ...)
def listar_productos(): ...

@router_productos.get("/{producto_id}", ...)
def obtener_producto(): ...

@router_categorias.get("/", ...)
def listar_categorias(): ...

@router_utilidades.get("/estadisticas")
def estadisticas(): ...
```

El codigo de cada endpoint es identico. Lo que cambia es donde se registra. Y la app principal queda limpia:

```python
app = FastAPI(title="Tienda API - Modular", ...)

app.include_router(router_productos)
app.include_router(router_categorias)
app.include_router(router_utilidades)
```

Tres lineas. Si manana agregan un router de pedidos, son cuatro lineas. El `main.py` nunca crece mas alla de la lista de routers.

### El endpoint de health check

```python
@router_utilidades.get("/salud")
def health_check():
    """Health check del servicio."""
    return {
        "estado": "ok",
        "productos_cargados": len(productos_db)
    }
```

Es comun tener un endpoint de health check que balanceadores de carga y sistemas de monitoreo usan para verificar que el servicio esta vivo. Ponerlo en un router de utilidades es el patron tipico: no es logica de negocio, es infraestructura.

> **Pregunta frecuente**: "¿En un proyecto real, cada router estaria en su propio archivo `.py`?"
>
> Si. En este ejemplo esta todo en un archivo para que puedan ejecutarlo con un solo `uvicorn`. Pero en produccion, `router_productos` viviria en `routers/productos.py`, `router_categorias` en `routers/categorias.py`, etc. El `main.py` importaria los routers y los montaria.

> **Pregunta frecuente**: "¿APIRouter cambia el rendimiento de la API?"
>
> No. APIRouter es puramente organizativo. Al arrancar, FastAPI resuelve todos los routers y genera las mismas rutas internas que si las hubieran definido directamente sobre `app`. No hay overhead en runtime.

> **Pregunta frecuente**: "¿Puedo mezclar rutas en `app` y en routers?"
>
> Si. La ruta raiz `@app.get("/")` esta definida directamente sobre `app`, y los demas endpoints estan en routers. Esto es perfectamente valido y es el patron comun: la ruta raiz y el health check en `app`, todo lo demas en routers.

**Punto clave**: La refactorizacion de monolitico a modular no cambia la funcionalidad. Los mismos endpoints, los mismos modelos, las mismas respuestas. Lo que cambia es la organizacion: endpoints agrupados por responsabilidad, prefijos que eliminan repeticion, y un `main.py` que declara la estructura de la API en pocas lineas.

---

## Resumen

- **APIRouter** es un contenedor de rutas que se monta en la app con `include_router()`. Acepta los mismos decoradores que `FastAPI()`: `@router.get`, `@router.post`, etc.
- El **prefix** de `include_router` se antepone a todas las rutas del router. Las rutas del router son relativas: `"/"` se convierte en `"/productos"` si el prefix es `"/productos"`. Los prefijos se acumulan cuando el router define uno y `include_router` agrega otro.
- Los **tags** organizan los endpoints en secciones de Swagger UI. Son puramente de documentacion; no afectan URLs ni logica.
- Las **dependencias a nivel de router** (`dependencies=[Depends(...)]`) aplican a todos los endpoints del router. Esto evita repetir `Depends(...)` en cada funcion y asegura que ningun endpoint quede desprotegido.
- La **separacion de logica de negocio** (clases de servicio) desacopla el routing del procesamiento de datos. Los endpoints reciben parametros HTTP y retornan respuestas; los servicios implementan la logica.
- El **patron modular** (`routers/`, `models/`, `services/`) escala con el proyecto. El `main.py` solo importa routers y los monta, manteniendo el punto de entrada limpio y declarativo.
- APIRouter es **organizativo, no funcional**. No cambia el rendimiento, la validacion ni las respuestas. Cambia como se estructura y mantiene el codigo.
- La regla practica: si la API maneja multiples recursos o tiene grupos de endpoints con dependencias diferentes, vale la pena usar routers. Para prototipos y APIs de 3-5 endpoints, un solo archivo sigue siendo valido.
