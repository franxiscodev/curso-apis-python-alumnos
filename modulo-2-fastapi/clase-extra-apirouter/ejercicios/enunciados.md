# Ejercicios: APIRouter y Organizacion de Proyecto

## Ejercicio 1: Separar en Routers

Tienen la siguiente API monolitica de una tienda de libros. Refactoricenla usando `APIRouter` para separar los endpoints en dos routers: uno para libros y otro para autores.

### Codigo original (monolitico)

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Libreria API")

libros_db = {}
autores_db = {}
contador_libros = 0
contador_autores = 0


class Libro(BaseModel):
    titulo: str = Field(min_length=1)
    autor: str = Field(min_length=1)
    precio: float = Field(gt=0)


class Autor(BaseModel):
    nombre: str = Field(min_length=1)
    nacionalidad: str = Field(min_length=1)


@app.get("/libros")
def listar_libros():
    return list(libros_db.values())


@app.post("/libros", status_code=status.HTTP_201_CREATED)
def crear_libro(libro: Libro):
    global contador_libros
    contador_libros += 1
    nuevo = {"id": contador_libros, **libro.model_dump()}
    libros_db[contador_libros] = nuevo
    return nuevo


@app.get("/libros/{libro_id}")
def obtener_libro(libro_id: int):
    if libro_id not in libros_db:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libros_db[libro_id]


@app.delete("/libros/{libro_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_libro(libro_id: int):
    if libro_id not in libros_db:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    del libros_db[libro_id]


@app.get("/autores")
def listar_autores():
    return list(autores_db.values())


@app.post("/autores", status_code=status.HTTP_201_CREATED)
def crear_autor(autor: Autor):
    global contador_autores
    contador_autores += 1
    nuevo = {"id": contador_autores, **autor.model_dump()}
    autores_db[contador_autores] = nuevo
    return nuevo


@app.get("/autores/{autor_id}")
def obtener_autor(autor_id: int):
    if autor_id not in autores_db:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autores_db[autor_id]
```

### Requisitos

1. Crear `router_libros` con prefix `/libros` y tags `["Libros"]`
2. Crear `router_autores` con prefix `/autores` y tags `["Autores"]`
3. Mover los endpoints correspondientes a cada router
4. Las rutas en cada router deben ser relativas (sin repetir el prefijo)
5. Montar ambos routers en la app con `include_router`
6. Verificar que `/docs` muestra los endpoints agrupados por tags

---

## Ejercicio 2: Refactorizar la API de Contactos

Tomen `api_contactos.py` de la clase 07 y refactoricenla usando APIRouter. La API tiene endpoints de CRUD para contactos y un endpoint de estadisticas.

### Requisitos

1. Crear `router_contactos` con prefix `/contactos` y tags `["Contactos"]`
2. Crear `router_utilidades` con prefix `/utilidades` y tags `["Utilidades"]`
3. Mover los endpoints CRUD al router de contactos
4. Mover el endpoint de estadisticas al router de utilidades
5. Agregar una dependencia compartida que registre en consola (con `print`) cada peticion que llega al router de contactos. Ejemplo:

```python
def log_peticion():
    print("Peticion recibida en router de contactos")
```

6. Montar ambos routers en la app
7. Verificar que la funcionalidad es identica a la version original

---

## Ejercicio 3 (Opcional): Estructura de Proyecto Real

Creen una estructura de directorios completa para una API de gestion de tareas (TODO app). No necesitan implementar la logica completa; el objetivo es la estructura.

### Requisitos

1. Crear la siguiente estructura de archivos:

```
todo_app/
├── main.py
├── routers/
│   ├── __init__.py
│   ├── tareas.py
│   └── categorias.py
├── models/
│   ├── __init__.py
│   └── schemas.py
└── services/
    ├── __init__.py
    └── tareas.py
```

2. En `models/schemas.py`: definir los modelos Pydantic (TareaBase, TareaCrear, TareaResponse, Categoria)
3. En `routers/tareas.py`: crear un router con al menos GET (listar) y POST (crear)
4. En `routers/categorias.py`: crear un router con al menos GET (listar categorias)
5. En `main.py`: importar y montar los routers
6. Verificar que la app arranca con `uvicorn main:app --reload` y que `/docs` muestra los endpoints agrupados
