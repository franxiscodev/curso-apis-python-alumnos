# Clase Extra: APIRouter y Organizacion de Proyecto

Hola a todos. Hoy vamos a hablar de algo que probablemente ya intuyen que necesitan: como organizar un proyecto FastAPI cuando empieza a crecer. Hasta ahora hemos trabajado con un solo archivo por API, y para los ejemplos del curso funciona perfecto. Pero en un proyecto real, meter 50 endpoints en un solo archivo es una receta para el desastre.

## Parte 1: El Problema (15 minutos)

Abran `api_productos.py` de la clase 06. Miren cuantas lineas tiene: modelos, base de datos, endpoints de productos, endpoints de categorias, endpoints de estadisticas... todo junto. Ahora imaginen que esa API tiene 10 veces mas endpoints, que trabajan en equipo, y que cada persona modifica el mismo archivo. Conflictos de merge constantemente, dificultad para encontrar funciones, y si alguien rompe algo en la seccion de productos, afecta al archivo completo.

Este es el problema clasico del monolito. No del monolito como arquitectura de despliegue, sino del monolito como organizacion de codigo: todo en un solo lugar.

La solucion de FastAPI para esto se llama `APIRouter`. Piensen en un APIRouter como una mini-aplicacion. Pueden definir rutas en un router exactamente igual que en la app principal, con `@router.get`, `@router.post`, etc. La diferencia es que el router no corre solo; se monta en la aplicacion principal.

Si vienen de Flask, es el equivalente a un Blueprint. Si vienen de Django, es como tener urls.py separados por app. Si vienen de Express.js, es `Router()`. La idea es la misma en todos los frameworks: separar rutas en modulos independientes.

Vamos a ver el ejemplo `01_apirouter_basico.py` para entender la mecanica fundamental.

## Parte 2: APIRouter Basico (20 minutos)

Abran `01_apirouter_basico.py`. Lo primero que van a notar es que en lugar de definir rutas sobre `app`, las definimos sobre dos objetos: `router_productos` y `router_usuarios`.

Fijense en como se crea un router:

```python
router_productos = APIRouter()
```

Y como se registran rutas:

```python
@router_productos.get("/")
def listar_productos():
    ...
```

Es identico a `@app.get`. La unica diferencia es que estamos decorando con el router en vez de con la app.

El momento clave es cuando montamos los routers en la aplicacion:

```python
app.include_router(router_productos, prefix="/productos", tags=["Productos"])
app.include_router(router_usuarios, prefix="/usuarios", tags=["Usuarios"])
```

`include_router` tiene tres parametros que importan: el router en si, el `prefix` que se antepone a todas las rutas del router, y los `tags` que agrupan los endpoints en Swagger UI.

El prefix es lo que elimina la repeticion. Sin prefix, tendrian que escribir `@router.get("/productos")`, `@router.post("/productos")`, `@router.get("/productos/{id}")` repitiendo "/productos" en cada ruta. Con `prefix="/productos"`, las rutas del router son simplemente `"/"`, `"/"` y `"/{id}"`. El prefijo se agrega automaticamente.

Ejecuten el ejemplo y abran `/docs`. Van a ver que Swagger UI agrupa los endpoints por tags: una seccion "Productos" y otra "Usuarios". Eso es puramente organizativo para la documentacion, pero ayuda mucho cuando la API tiene muchos endpoints.

## Parte 3: Estructura de Proyecto (20 minutos)

El ejemplo 01 les mostro la mecanica de APIRouter. Ahora vamos a ver como esto se traduce en una organizacion de proyecto real.

Abran `02_estructura_proyecto.py`. Este archivo simula la estructura que tendrian en un proyecto con archivos separados. Fijense en los comentarios que indican donde iria cada seccion: modelos en `models/schemas.py`, logica de negocio en `services/biblioteca.py`, y routers en `routers/libros.py` y `routers/autores.py`.

Lo nuevo aqui son tres cosas:

**Primero, la separacion de logica de negocio.** La clase `BibliotecaService` contiene toda la logica: buscar libros, crear autores, validar existencia. Los endpoints del router solo llaman a metodos del servicio. Esto es importante porque la logica de negocio no deberia depender de HTTP. Si manana necesitan una interfaz de linea de comandos o un worker que procese colas, la misma logica les sirve.

**Segundo, las dependencias compartidas.** Miren como el router de libros y el de autores comparten la misma dependencia `verificar_api_key`:

```python
router_libros = APIRouter(
    prefix="/libros",
    tags=["Libros"],
    dependencies=[Depends(verificar_api_key)]
)
```

Esa dependencia se ejecuta antes de cada endpoint del router. Sin APIRouter, tendrian que agregar `Depends(verificar_api_key)` a cada funcion individualmente. Con 20 endpoints, son 20 repeticiones que ademas alguien podria olvidar.

**Tercero, los prefijos acumulativos.** Los routers tienen su propio prefix (`/libros`, `/autores`), y al montarlos se agrega otro prefix:

```python
app.include_router(router_libros, prefix="/api/v1")
```

El resultado es `/api/v1/libros`. Los prefijos se suman. Esto es util para versionado de APIs.

Ejecuten el ejemplo con el query parameter `api_key=mi-clave-secreta` y vean como la dependencia aplica a todos los endpoints automaticamente.

---

## Descanso (10 minutos)

---

## Parte 4: Refactorizacion Completa (20 minutos)

Abran `03_app_modular.py` y al lado abran `api_productos.py` de la clase 06. Vamos a compararlos.

Ambos hacen exactamente lo mismo: CRUD de productos, listado de categorias y estadisticas. La funcionalidad es identica. Pero la organizacion es completamente diferente.

En la version monolitica, todo esta en un bloque: modelos, datos, y todos los endpoints directamente sobre `app`. En la version modular, hay tres routers independientes:

- `router_productos`: CRUD completo de productos
- `router_categorias`: consultas por categoria
- `router_utilidades`: estadisticas y health check

Cada router declara su prefix y tags en el constructor. El main solo monta los tres:

```python
app.include_router(router_productos)
app.include_router(router_categorias)
app.include_router(router_utilidades)
```

En un proyecto real, cada router estaria en su propio archivo. El `main.py` solo tendria esas tres lineas de import y tres lineas de include. Limpio, declarativo, facil de entender.

Fijense en algo: los modelos Pydantic y la base de datos en memoria siguen siendo los mismos. APIRouter no cambia como funcionan los modelos, la validacion, las respuestas o los status codes. Solo cambia como organizan las rutas.

Ejecuten el ejemplo y comparen Swagger UI con el de la clase 06. Los endpoints son los mismos, pero ahora estan agrupados por seccion: Productos, Categorias, Utilidades. Eso es efecto directo de los tags en cada router.

## Parte 5: Ejercicios (5 minutos)

Para practicar, les dejo ejercicios de refactorizacion. La idea es tomar APIs que ya conocen del curso y reorganizarlas con APIRouter. Esto les va a dar la confianza de que saben hacerlo en sus propios proyectos.

Los ejercicios estan en `ejercicios/enunciados.md`. El primero es sencillo: tomar endpoints y separarlos en routers. El segundo es mas realista: refactorizar la API de contactos de la clase 07.

## Conclusion

Hoy vieron que APIRouter no agrega funcionalidad nueva a sus APIs. No cambia como funcionan los endpoints, la validacion o las respuestas. Lo que si cambia es la organizacion del codigo, y eso tiene un impacto enorme en la mantenibilidad.

Los tres conceptos clave son: APIRouter para agrupar rutas relacionadas, `include_router` con prefix y tags para montarlos en la app, y dependencias a nivel de router para evitar repeticion.

La regla practica que les dejo: si su API tiene mas de un recurso (productos Y categorias, o usuarios Y pedidos), cada recurso merece su propio router. Si tienen grupos de endpoints con dependencias diferentes (endpoints publicos vs endpoints de admin), eso tambien merece routers separados.

A partir de la clase 08, cuando empecemos con SQLAlchemy y proyectos mas grandes, esta organizacion modular va a ser fundamental. Aprovechen para practicar ahora con los ejercicios.

Nos vemos en la proxima clase.
