"""
API de Contactos Completa
==========================
API que integra CRUD + paginación + filtrado + errores.

Ejecutar:
    uvicorn ejemplos.api_contactos:app --reload

Endpoints:
    GET    /contactos           - Listar con paginación y filtros
    GET    /contactos/{id}      - Obtener contacto
    POST   /contactos           - Crear contacto
    PUT    /contactos/{id}      - Actualizar contacto
    DELETE /contactos/{id}      - Eliminar contacto
    GET    /estadisticas        - Estadísticas generales
"""

import math
from typing import Literal

from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="API de Contactos",
    description="API REST completa con CRUD, paginación y filtrado",
    version="1.0.0"
)


# =============================================================================
# MODELOS
# =============================================================================


class ContactoBase(BaseModel):
    """Campos comunes de contacto."""
    nombre: str = Field(min_length=1, max_length=100, examples=["Ana García"])
    email: str = Field(min_length=5, max_length=100, examples=["ana@ejemplo.com"])
    telefono: str | None = Field(default=None, max_length=20)
    ciudad: str = Field(min_length=1, examples=["Madrid"])


class ContactoCrear(ContactoBase):
    """Modelo para crear contacto."""
    pass


class ContactoActualizar(BaseModel):
    """Modelo para actualizar (todo opcional)."""
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    email: str | None = Field(default=None, min_length=5, max_length=100)
    telefono: str | None = None
    ciudad: str | None = None


class ContactoResponse(ContactoBase):
    """Modelo de respuesta."""
    id: int


class ContactosPaginados(BaseModel):
    """Respuesta paginada de contactos."""
    items: list[ContactoResponse]
    total: int
    page: int
    size: int
    pages: int


# =============================================================================
# "BASE DE DATOS" EN MEMORIA
# =============================================================================


contactos_db: dict[int, dict] = {}
contador_id = 0


def siguiente_id() -> int:
    """Genera el siguiente ID."""
    global contador_id
    contador_id += 1
    return contador_id


def inicializar_datos():
    """Crea contactos de ejemplo."""
    ejemplos = [
        ContactoCrear(nombre="Ana García", email="ana@ejemplo.com",
                       telefono="600111222", ciudad="Madrid"),
        ContactoCrear(nombre="Luis Pérez", email="luis@ejemplo.com",
                       telefono="600333444", ciudad="Barcelona"),
        ContactoCrear(nombre="María López", email="maria@ejemplo.com",
                       ciudad="Madrid"),
        ContactoCrear(nombre="Carlos Ruiz", email="carlos@ejemplo.com",
                       telefono="600555666", ciudad="Valencia"),
        ContactoCrear(nombre="Laura Martín", email="laura@ejemplo.com",
                       ciudad="Barcelona"),
        ContactoCrear(nombre="Pedro Sánchez", email="pedro@ejemplo.com",
                       telefono="600777888", ciudad="Sevilla"),
    ]
    for contacto in ejemplos:
        nuevo_id = siguiente_id()
        contactos_db[nuevo_id] = {"id": nuevo_id, **contacto.model_dump()}


inicializar_datos()


# =============================================================================
# ENDPOINTS
# =============================================================================


@app.get(
    "/contactos",
    response_model=ContactosPaginados,
    summary="Listar contactos",
    tags=["Contactos"]
)
def listar_contactos(
    ciudad: str | None = Query(default=None, description="Filtrar por ciudad"),
    buscar: str | None = Query(
        default=None, min_length=2, description="Buscar en nombre o email"
    ),
    sort_by: Literal["nombre", "email", "ciudad"] = Query(
        default="nombre", description="Ordenar por campo"
    ),
    order: Literal["asc", "desc"] = Query(default="asc", description="Dirección"),
    page: int = Query(default=1, ge=1, description="Página"),
    size: int = Query(default=10, ge=1, le=50, description="Items por página")
):
    """Listar contactos con filtrado, búsqueda, ordenamiento y paginación."""
    resultados = list(contactos_db.values())

    # Filtrar por ciudad
    if ciudad:
        resultados = [c for c in resultados if c["ciudad"] == ciudad]

    # Buscar en nombre o email
    if buscar:
        buscar_lower = buscar.lower()
        resultados = [
            c for c in resultados
            if buscar_lower in c["nombre"].lower()
            or buscar_lower in c["email"].lower()
        ]

    # Ordenar
    resultados.sort(key=lambda c: c[sort_by], reverse=(order == "desc"))

    # Paginar
    total = len(resultados)
    pages = math.ceil(total / size) if total > 0 else 0
    start = (page - 1) * size

    return {
        "items": resultados[start:start + size],
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }


@app.get(
    "/contactos/{contacto_id}",
    response_model=ContactoResponse,
    tags=["Contactos"]
)
def obtener_contacto(contacto_id: int = Path(ge=1)):
    """Obtener contacto por ID."""
    if contacto_id not in contactos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contacto con ID {contacto_id} no encontrado"
        )
    return contactos_db[contacto_id]


@app.post(
    "/contactos",
    response_model=ContactoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Contactos"]
)
def crear_contacto(contacto: ContactoCrear):
    """Crear contacto. Retorna 409 si el email ya existe."""
    # Validar email único
    for c in contactos_db.values():
        if c["email"] == contacto.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un contacto con email '{contacto.email}'"
            )

    nuevo_id = siguiente_id()
    nuevo = {"id": nuevo_id, **contacto.model_dump()}
    contactos_db[nuevo_id] = nuevo
    return nuevo


@app.put(
    "/contactos/{contacto_id}",
    response_model=ContactoResponse,
    tags=["Contactos"]
)
def actualizar_contacto(
    contacto_id: int = Path(ge=1),
    contacto: ContactoActualizar = ...
):
    """Actualizar contacto. Solo se modifican los campos enviados."""
    if contacto_id not in contactos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contacto con ID {contacto_id} no encontrado"
        )

    # Validar email único si se está actualizando
    datos = contacto.model_dump(exclude_none=True)
    if "email" in datos:
        for cid, c in contactos_db.items():
            if c["email"] == datos["email"] and cid != contacto_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe un contacto con email '{datos['email']}'"
                )

    actual = contactos_db[contacto_id]
    for campo, valor in datos.items():
        actual[campo] = valor

    return actual


@app.delete(
    "/contactos/{contacto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Contactos"]
)
def eliminar_contacto(contacto_id: int = Path(ge=1)):
    """Eliminar contacto."""
    if contacto_id not in contactos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contacto con ID {contacto_id} no encontrado"
        )
    del contactos_db[contacto_id]
    return None


@app.get("/estadisticas", summary="Estadísticas", tags=["Utilidades"])
def estadisticas():
    """Estadísticas generales de contactos."""
    contactos = list(contactos_db.values())
    ciudades: dict[str, int] = {}
    for c in contactos:
        ciudades[c["ciudad"]] = ciudades.get(c["ciudad"], 0) + 1

    return {
        "total_contactos": len(contactos),
        "con_telefono": sum(1 for c in contactos if c["telefono"]),
        "ciudades": ciudades
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
