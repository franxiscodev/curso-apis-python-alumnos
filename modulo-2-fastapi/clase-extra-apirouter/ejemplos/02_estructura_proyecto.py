"""
Estructura de Proyecto con APIRouter
=====================================
Patron de organizacion por modulos: routers con dependencias compartidas,
tags para documentacion y separacion de logica de negocio.

Ejecutar:
    uvicorn ejemplos.02_estructura_proyecto:app --reload

Endpoints:
    GET    /api/v1/libros              - Listar libros (con filtros)
    POST   /api/v1/libros              - Crear libro
    GET    /api/v1/libros/{libro_id}   - Obtener libro
    DELETE /api/v1/libros/{libro_id}   - Eliminar libro
    GET    /api/v1/autores             - Listar autores
    POST   /api/v1/autores             - Crear autor
    GET    /api/v1/autores/{autor_id}  - Obtener autor

Estructura sugerida para un proyecto real:
    mi_proyecto/
    ├── main.py              # Crea app y monta routers
    ├── routers/
    │   ├── __init__.py
    │   ├── libros.py        # Router de libros
    │   └── autores.py       # Router de autores
    ├── models/
    │   ├── __init__.py
    │   └── schemas.py       # Modelos Pydantic
    └── services/
        ├── __init__.py
        └── biblioteca.py    # Logica de negocio
"""

from fastapi import FastAPI, APIRouter, HTTPException, Query, Depends, status
from pydantic import BaseModel, Field


# =============================================================================
# MODELOS (en un proyecto real: models/schemas.py)
# =============================================================================


class LibroBase(BaseModel):
    titulo: str = Field(min_length=1, max_length=200, examples=["Don Quijote"])
    autor: str = Field(min_length=1, examples=["Cervantes"])
    anio: int = Field(ge=1000, le=2100, examples=[1605])
    genero: str = Field(min_length=1, examples=["Novela"])


class LibroCrear(LibroBase):
    pass


class LibroResponse(LibroBase):
    id: int


class AutorBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=100, examples=["Gabriel Garcia Marquez"])
    nacionalidad: str = Field(min_length=1, examples=["Colombiana"])


class AutorCrear(AutorBase):
    pass


class AutorResponse(AutorBase):
    id: int


# =============================================================================
# SERVICIOS / LOGICA DE NEGOCIO (en un proyecto real: services/biblioteca.py)
# =============================================================================


class BibliotecaService:
    """Separa la logica de negocio del routing."""

    def __init__(self):
        self.libros_db: dict[int, dict] = {}
        self.autores_db: dict[int, dict] = {}
        self._contador_libros = 0
        self._contador_autores = 0

    def listar_libros(
        self,
        genero: str | None = None,
        anio_min: int | None = None
    ) -> list[dict]:
        resultados = list(self.libros_db.values())
        if genero:
            resultados = [l for l in resultados if l["genero"] == genero]
        if anio_min is not None:
            resultados = [l for l in resultados if l["anio"] >= anio_min]
        return resultados

    def obtener_libro(self, libro_id: int) -> dict:
        if libro_id not in self.libros_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Libro {libro_id} no encontrado"
            )
        return self.libros_db[libro_id]

    def crear_libro(self, datos: LibroCrear) -> dict:
        self._contador_libros += 1
        nuevo = {"id": self._contador_libros, **datos.model_dump()}
        self.libros_db[self._contador_libros] = nuevo
        return nuevo

    def eliminar_libro(self, libro_id: int) -> None:
        if libro_id not in self.libros_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Libro {libro_id} no encontrado"
            )
        del self.libros_db[libro_id]

    def listar_autores(self) -> list[dict]:
        return list(self.autores_db.values())

    def obtener_autor(self, autor_id: int) -> dict:
        if autor_id not in self.autores_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Autor {autor_id} no encontrado"
            )
        return self.autores_db[autor_id]

    def crear_autor(self, datos: AutorCrear) -> dict:
        self._contador_autores += 1
        nuevo = {"id": self._contador_autores, **datos.model_dump()}
        self.autores_db[self._contador_autores] = nuevo
        return nuevo


# Instancia global del servicio
biblioteca = BibliotecaService()


# =============================================================================
# DEPENDENCIA COMPARTIDA
# =============================================================================


def verificar_api_key(api_key: str = Query(description="API key de acceso")):
    """
    Dependencia que simula verificacion de API key.
    En un proyecto real, validaria contra una base de datos.

    Se puede inyectar a nivel de router para que aplique a TODAS
    las rutas del router sin repetirla en cada endpoint.
    """
    if api_key != "mi-clave-secreta":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key invalida"
        )
    return api_key


# =============================================================================
# ROUTER DE LIBROS (en un proyecto real: routers/libros.py)
# =============================================================================


router_libros = APIRouter(
    prefix="/libros",
    tags=["Libros"],
    # Dependencias que aplican a TODAS las rutas de este router
    dependencies=[Depends(verificar_api_key)]
)


@router_libros.get("/", response_model=list[LibroResponse])
def listar_libros(
    genero: str | None = Query(default=None, description="Filtrar por genero"),
    anio_min: int | None = Query(default=None, ge=1000, description="Anio minimo")
):
    """Lista libros con filtros opcionales."""
    return biblioteca.listar_libros(genero=genero, anio_min=anio_min)


@router_libros.post(
    "/",
    response_model=LibroResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_libro(libro: LibroCrear):
    """Crea un nuevo libro."""
    return biblioteca.crear_libro(libro)


@router_libros.get("/{libro_id}", response_model=LibroResponse)
def obtener_libro(libro_id: int):
    """Obtiene un libro por ID."""
    return biblioteca.obtener_libro(libro_id)


@router_libros.delete("/{libro_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_libro(libro_id: int):
    """Elimina un libro."""
    biblioteca.eliminar_libro(libro_id)


# =============================================================================
# ROUTER DE AUTORES (en un proyecto real: routers/autores.py)
# =============================================================================


router_autores = APIRouter(
    prefix="/autores",
    tags=["Autores"],
    dependencies=[Depends(verificar_api_key)]
)


@router_autores.get("/", response_model=list[AutorResponse])
def listar_autores():
    """Lista todos los autores."""
    return biblioteca.listar_autores()


@router_autores.post(
    "/",
    response_model=AutorResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_autor(autor: AutorCrear):
    """Crea un nuevo autor."""
    return biblioteca.crear_autor(autor)


@router_autores.get("/{autor_id}", response_model=AutorResponse)
def obtener_autor(autor_id: int):
    """Obtiene un autor por ID."""
    return biblioteca.obtener_autor(autor_id)


# =============================================================================
# APLICACION PRINCIPAL (en un proyecto real: main.py)
# =============================================================================


app = FastAPI(
    title="Biblioteca API",
    description="API organizada con routers, dependencias compartidas y servicios",
    version="1.0.0"
)

# Montar ambos routers bajo /api/v1
# Los prefijos se acumulan: /api/v1 + /libros = /api/v1/libros
app.include_router(router_libros, prefix="/api/v1")
app.include_router(router_autores, prefix="/api/v1")


@app.get("/")
def raiz():
    """Informacion de la API."""
    return {
        "api": "Biblioteca API",
        "version": "1.0.0",
        "nota": "Todos los endpoints requieren api_key como query parameter",
        "documentacion": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
