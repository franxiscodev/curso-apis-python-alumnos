"""
Ejercicio 01: Separar API en Routers
=====================================
Tienen una API monolitica de una libreria con endpoints de libros y autores.
Refactoricenla usando APIRouter para separar los endpoints.

OBJETIVO:
Practicar la creacion de APIRouter y la separacion de endpoints por dominio.

INSTRUCCIONES:
1. Crear `router_libros` con prefix="/libros" y tags=["Libros"]
2. Crear `router_autores` con prefix="/autores" y tags=["Autores"]
3. Mover los endpoints de libros al router_libros (rutas RELATIVAS: "/" y "/{id}")
4. Mover los endpoints de autores al router_autores (rutas RELATIVAS)
5. Montar ambos routers en la app con app.include_router()
6. Verificar que /docs muestra los endpoints agrupados por tags

PRUEBAS:
    uvicorn ejercicio_01:app --reload

    # Probar con curl o navegador:
    GET  http://localhost:8000/libros
    POST http://localhost:8000/libros
    GET  http://localhost:8000/libros/1
    GET  http://localhost:8000/autores
    POST http://localhost:8000/autores

PISTAS:
- Las rutas en el router son RELATIVAS al prefix (usa "/" en vez de "/libros")
- El prefix del router ya incluye "/libros", no lo repitas en las rutas
- Los tags agrupan endpoints en la documentacion automatica
"""

from fastapi import FastAPI, HTTPException, APIRouter, status
from pydantic import BaseModel, Field

app = FastAPI(title="Libreria API")

# --- Base de datos en memoria (no modificar) ---
libros_db = {}
autores_db = {}
contador_libros = 0
contador_autores = 0


# --- Modelos (no modificar) ---
class Libro(BaseModel):
    titulo: str = Field(min_length=1)
    autor: str = Field(min_length=1)
    precio: float = Field(gt=0)


class Autor(BaseModel):
    nombre: str = Field(min_length=1)
    nacionalidad: str = Field(min_length=1)


# =============================================================================
# TODO: Crear router_libros con prefix="/libros" y tags=["Libros"]
# =============================================================================

# router_libros = APIRouter(...)


# =============================================================================
# TODO: Crear router_autores con prefix="/autores" y tags=["Autores"]
# =============================================================================

# router_autores = APIRouter(...)


# =============================================================================
# ENDPOINTS DE LIBROS
# TODO: Cambiar @app por @router_libros y ajustar las rutas a relativas
# Ejemplo: @app.get("/libros") -> @router_libros.get("/")
# =============================================================================

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


# =============================================================================
# ENDPOINTS DE AUTORES
# TODO: Cambiar @app por @router_autores y ajustar las rutas a relativas
# =============================================================================

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


# =============================================================================
# TODO: Montar los routers en la app
# app.include_router(router_libros)
# app.include_router(router_autores)
# =============================================================================


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
