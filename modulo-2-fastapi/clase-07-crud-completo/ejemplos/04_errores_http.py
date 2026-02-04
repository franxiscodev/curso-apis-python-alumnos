"""
Manejo de Errores HTTP
=======================
Errores HTTP consistentes y validación de negocio.

Ejecutar:
    uvicorn ejemplos.04_errores_http:app --reload

Conceptos:
    - HTTPException con diferentes status codes
    - Validación de negocio (no solo de tipos)
    - Respuestas de error consistentes
    - Diferencia entre errores de validación y de negocio
"""

from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel, Field

app = FastAPI(title="Errores HTTP", version="1.0.0")


# =============================================================================
# MODELOS
# =============================================================================


class UsuarioCrear(BaseModel):
    """Modelo para crear usuario."""
    nombre: str = Field(min_length=2, max_length=50)
    email: str = Field(min_length=5, max_length=100)
    edad: int = Field(ge=0, le=150)


class UsuarioResponse(BaseModel):
    """Modelo de respuesta."""
    id: int
    nombre: str
    email: str
    edad: int


# =============================================================================
# "BASE DE DATOS"
# =============================================================================


usuarios_db: dict[int, dict] = {
    1: {"id": 1, "nombre": "Ana García", "email": "ana@ejemplo.com", "edad": 28},
    2: {"id": 2, "nombre": "Luis Pérez", "email": "luis@ejemplo.com", "edad": 35},
}
contador_id = 2


# =============================================================================
# ENDPOINTS CON MANEJO DE ERRORES
# =============================================================================


@app.post(
    "/usuarios",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Usuarios"]
)
def crear_usuario(usuario: UsuarioCrear):
    """
    Crear usuario con validación de negocio.

    Errores posibles:
    - 409: Email duplicado
    - 422: Error de validación de tipos (automático)
    """
    global contador_id

    # Validación de negocio: email único
    for u in usuarios_db.values():
        if u["email"] == usuario.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un usuario con email '{usuario.email}'"
            )

    contador_id += 1
    nuevo = {"id": contador_id, **usuario.model_dump()}
    usuarios_db[contador_id] = nuevo
    return nuevo


@app.get("/usuarios/{usuario_id}", response_model=UsuarioResponse, tags=["Usuarios"])
def obtener_usuario(usuario_id: int = Path(ge=1)):
    """
    Obtener usuario por ID.

    Errores posibles:
    - 404: Usuario no encontrado
    """
    if usuario_id not in usuarios_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado"
        )
    return usuarios_db[usuario_id]


@app.delete(
    "/usuarios/{usuario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Usuarios"]
)
def eliminar_usuario(usuario_id: int = Path(ge=1)):
    """
    Eliminar usuario con validación de negocio.

    Errores posibles:
    - 404: Usuario no encontrado
    - 400: No se puede eliminar (regla de negocio)
    """
    if usuario_id not in usuarios_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado"
        )

    # Regla de negocio: no eliminar usuario con ID 1 (admin)
    if usuario_id == 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el usuario administrador"
        )

    del usuarios_db[usuario_id]
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
