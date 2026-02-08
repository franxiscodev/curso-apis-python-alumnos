"""
Solucion Ejercicio 01: Separar API en Routers
==============================================
API de libreria refactorizada con APIRouter.

Ejecutar:
    uvicorn ejercicio_01_solucion:app --reload
"""

from fastapi import FastAPI, HTTPException, APIRouter, status
from pydantic import BaseModel, Field

app = FastAPI(title="Libreria API")

# --- Base de datos en memoria ---
libros_db = {}
autores_db = {}
contador_libros = 0
contador_autores = 0


# --- Modelos ---
class Libro(BaseModel):
    titulo: str = Field(min_length=1)
    autor: str = Field(min_length=1)
    precio: float = Field(gt=0)


class Autor(BaseModel):
    nombre: str = Field(min_length=1)
    nacionalidad: str = Field(min_length=1)


# =============================================================================
# Router de Libros
# =============================================================================

router_libros = APIRouter(prefix="/libros", tags=["Libros"])


@router_libros.get("/")
def listar_libros():
    return list(libros_db.values())


@router_libros.post("/", status_code=status.HTTP_201_CREATED)
def crear_libro(libro: Libro):
    global contador_libros
    contador_libros += 1
    nuevo = {"id": contador_libros, **libro.model_dump()}
    libros_db[contador_libros] = nuevo
    return nuevo


@router_libros.get("/{libro_id}")
def obtener_libro(libro_id: int):
    if libro_id not in libros_db:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libros_db[libro_id]


@router_libros.delete("/{libro_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_libro(libro_id: int):
    if libro_id not in libros_db:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    del libros_db[libro_id]


# =============================================================================
# Router de Autores
# =============================================================================

router_autores = APIRouter(prefix="/autores", tags=["Autores"])


@router_autores.get("/")
def listar_autores():
    return list(autores_db.values())


@router_autores.post("/", status_code=status.HTTP_201_CREATED)
def crear_autor(autor: Autor):
    global contador_autores
    contador_autores += 1
    nuevo = {"id": contador_autores, **autor.model_dump()}
    autores_db[contador_autores] = nuevo
    return nuevo


@router_autores.get("/{autor_id}")
def obtener_autor(autor_id: int):
    if autor_id not in autores_db:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autores_db[autor_id]


# =============================================================================
# Montar routers
# =============================================================================

app.include_router(router_libros)
app.include_router(router_autores)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
