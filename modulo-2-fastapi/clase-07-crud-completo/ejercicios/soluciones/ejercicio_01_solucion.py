"""
Ejercicio 01: CRUD de Biblioteca - SOLUCIÓN
=============================================
"""

from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Biblioteca API",
    description="API de gestión de libros",
    version="1.0.0"
)


# =============================================================================
# MODELOS
# =============================================================================


class LibroBase(BaseModel):
    """Campos comunes de libro."""
    titulo: str = Field(min_length=1, max_length=200)
    autor: str = Field(min_length=1, max_length=100)
    genero: str = Field(min_length=1, max_length=50)
    año: int = Field(ge=1000, le=2030)
    paginas: int = Field(gt=0)


class LibroCrear(LibroBase):
    """Modelo para crear libro."""
    pass


class LibroActualizar(BaseModel):
    """Modelo para actualizar (todo opcional)."""
    titulo: str | None = Field(default=None, min_length=1, max_length=200)
    autor: str | None = Field(default=None, min_length=1, max_length=100)
    genero: str | None = Field(default=None, min_length=1, max_length=50)
    año: int | None = Field(default=None, ge=1000, le=2030)
    paginas: int | None = Field(default=None, gt=0)


class LibroResponse(LibroBase):
    """Modelo de respuesta con ID."""
    id: int


# =============================================================================
# "BASE DE DATOS"
# =============================================================================


libros_db: dict[int, dict] = {}
contador_id = 0


def siguiente_id() -> int:
    """Genera siguiente ID."""
    global contador_id
    contador_id += 1
    return contador_id


# =============================================================================
# ENDPOINTS
# =============================================================================


@app.get("/libros", response_model=list[LibroResponse], tags=["Libros"])
def listar_libros():
    """Listar todos los libros."""
    return list(libros_db.values())


@app.post(
    "/libros",
    response_model=LibroResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Libros"]
)
def crear_libro(libro: LibroCrear):
    """Crear un nuevo libro."""
    nuevo_id = siguiente_id()
    nuevo = {"id": nuevo_id, **libro.model_dump()}
    libros_db[nuevo_id] = nuevo
    return nuevo


@app.get("/libros/{libro_id}", response_model=LibroResponse, tags=["Libros"])
def obtener_libro(libro_id: int = Path(ge=1)):
    """Obtener libro por ID."""
    if libro_id not in libros_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con ID {libro_id} no encontrado"
        )
    return libros_db[libro_id]


@app.put("/libros/{libro_id}", response_model=LibroResponse, tags=["Libros"])
def actualizar_libro(
    libro_id: int = Path(ge=1),
    libro: LibroActualizar = ...
):
    """Actualizar libro (solo campos enviados)."""
    if libro_id not in libros_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con ID {libro_id} no encontrado"
        )

    actual = libros_db[libro_id]
    datos = libro.model_dump(exclude_none=True)
    for campo, valor in datos.items():
        actual[campo] = valor

    return actual


@app.delete(
    "/libros/{libro_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Libros"]
)
def eliminar_libro(libro_id: int = Path(ge=1)):
    """Eliminar libro."""
    if libro_id not in libros_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con ID {libro_id} no encontrado"
        )
    del libros_db[libro_id]
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
