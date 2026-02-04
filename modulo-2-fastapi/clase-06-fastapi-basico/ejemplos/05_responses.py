"""
Ejemplo 05: Response Models y Status Codes
==========================================
Controlar las respuestas de la API.

Ejecutar:
    uvicorn 05_responses:app --reload
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr

app = FastAPI(title="Responses")


# =============================================================================
# MODELOS DE REQUEST Y RESPONSE
# =============================================================================


class UsuarioCrear(BaseModel):
    """Modelo para CREAR usuario (incluye password)."""
    nombre: str
    email: EmailStr
    password: str = Field(min_length=8)


class UsuarioResponse(BaseModel):
    """Modelo para RESPUESTA (sin password)."""
    id: int
    nombre: str
    email: EmailStr
    activo: bool = True


class UsuarioEnDB(BaseModel):
    """Modelo interno (con hash de password)."""
    id: int
    nombre: str
    email: EmailStr
    hashed_password: str
    activo: bool = True


# =============================================================================
# RESPONSE MODEL
# =============================================================================


# Simulación de base de datos
usuarios_db: dict[int, UsuarioEnDB] = {}
contador_id = 0


@app.post("/usuarios", response_model=UsuarioResponse, status_code=201)
def crear_usuario(usuario: UsuarioCrear):
    """
    response_model filtra la salida.

    Aunque retornemos el objeto completo con hashed_password,
    FastAPI solo incluye los campos de UsuarioResponse.
    """
    global contador_id
    contador_id += 1

    # Simular hash de password
    usuario_db = UsuarioEnDB(
        id=contador_id,
        nombre=usuario.nombre,
        email=usuario.email,
        hashed_password=f"hashed_{usuario.password}"
    )
    usuarios_db[contador_id] = usuario_db

    # Retornamos todo, pero response_model filtra
    return usuario_db


@app.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int):
    """
    Retorna usuario sin exponer el password hasheado.
    """
    if usuario_id not in usuarios_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario {usuario_id} no encontrado"
        )
    return usuarios_db[usuario_id]


@app.get("/usuarios", response_model=list[UsuarioResponse])
def listar_usuarios():
    """
    Lista de usuarios como response_model.
    """
    return list(usuarios_db.values())


# =============================================================================
# STATUS CODES
# =============================================================================


@app.post("/items", status_code=status.HTTP_201_CREATED)
def crear_item(nombre: str):
    """201 Created para recursos nuevos."""
    return {"id": 1, "nombre": nombre}


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_item(item_id: int):
    """
    204 No Content para DELETE exitoso.

    No debe retornar body.
    """
    # En realidad eliminaríamos el item aquí
    return None


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """200 OK es el default, pero se puede especificar."""
    return {"status": "healthy"}


# =============================================================================
# HTTP EXCEPTIONS
# =============================================================================


items_db = {"laptop": {"nombre": "Laptop", "precio": 999.99}}


@app.get("/items/{item_id}")
def obtener_item(item_id: str):
    """
    HTTPException para errores controlados.
    """
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item '{item_id}' no encontrado"
        )
    return items_db[item_id]


@app.post("/items/{item_id}")
def crear_item_con_id(item_id: str, nombre: str, precio: float):
    """
    409 Conflict si ya existe.
    """
    if item_id in items_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Item '{item_id}' ya existe"
        )
    items_db[item_id] = {"nombre": nombre, "precio": precio}
    return items_db[item_id]


# =============================================================================
# RESPONSE MODEL OPCIONES
# =============================================================================


class ItemCompleto(BaseModel):
    """Item con todos los campos."""
    id: int
    nombre: str
    descripcion: str | None = None
    precio: float
    impuesto: float | None = None
    tags: list[str] = []


@app.get(
    "/items-completos/{item_id}",
    response_model=ItemCompleto,
    response_model_exclude_unset=True  # Excluye campos no establecidos
)
def obtener_item_completo(item_id: int):
    """
    response_model_exclude_unset=True

    Solo incluye campos que fueron explícitamente establecidos.
    """
    return {
        "id": item_id,
        "nombre": "Laptop",
        "precio": 999.99
        # descripcion, impuesto, tags no están → no se incluyen
    }


@app.get(
    "/items-sin-tags/{item_id}",
    response_model=ItemCompleto,
    response_model_exclude={"tags", "impuesto"}  # Excluye campos específicos
)
def obtener_item_sin_tags(item_id: int):
    """
    response_model_exclude excluye campos específicos.
    """
    return {
        "id": item_id,
        "nombre": "Mouse",
        "descripcion": "Mouse inalámbrico",
        "precio": 29.99,
        "impuesto": 5.99,
        "tags": ["periféricos", "wireless"]
    }


# =============================================================================
# MÚLTIPLES RESPONSES
# =============================================================================


class MensajeError(BaseModel):
    """Modelo para errores."""
    detail: str


@app.get(
    "/usuarios-v2/{usuario_id}",
    response_model=UsuarioResponse,
    responses={
        404: {"model": MensajeError, "description": "Usuario no encontrado"},
        500: {"description": "Error interno del servidor"}
    }
)
def obtener_usuario_v2(usuario_id: int):
    """
    Documenta múltiples tipos de response.

    Esto aparece en la documentación Swagger.
    """
    if usuario_id not in usuarios_db:
        raise HTTPException(status_code=404, detail="No encontrado")
    return usuarios_db[usuario_id]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
