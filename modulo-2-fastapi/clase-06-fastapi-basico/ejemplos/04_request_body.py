"""
Ejemplo 04: Request Body con Pydantic
=====================================
Enviar datos en el cuerpo de la petición.

Ejecutar:
    uvicorn 04_request_body:app --reload
"""

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field, EmailStr

app = FastAPI(title="Request Body")


# =============================================================================
# MODELOS PYDANTIC PARA REQUEST
# =============================================================================


class ItemCrear(BaseModel):
    """Modelo para crear un item."""
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str | None = None
    precio: float = Field(gt=0)
    cantidad: int = Field(default=1, ge=1)


class ItemActualizar(BaseModel):
    """Modelo para actualizar (todos opcionales)."""
    nombre: str | None = None
    descripcion: str | None = None
    precio: float | None = Field(default=None, gt=0)
    cantidad: int | None = Field(default=None, ge=1)


class Usuario(BaseModel):
    """Modelo de usuario."""
    nombre: str
    email: EmailStr
    edad: int | None = Field(default=None, ge=0, le=150)


# =============================================================================
# REQUEST BODY BÁSICO
# =============================================================================


@app.post("/items")
def crear_item(item: ItemCrear):
    """
    Recibe un item en el body.

    FastAPI:
    1. Lee el body como JSON
    2. Valida con Pydantic
    3. Convierte a objeto ItemCrear

    Request body ejemplo:
    {
        "nombre": "Laptop",
        "descripcion": "Laptop gaming",
        "precio": 999.99,
        "cantidad": 5
    }
    """
    return {
        "mensaje": "Item creado",
        "item": item.model_dump()
    }


# =============================================================================
# BODY + PATH PARAMETERS
# =============================================================================


@app.put("/items/{item_id}")
def actualizar_item(item_id: int, item: ItemActualizar):
    """
    Combina path parameter y request body.

    - item_id: viene de la URL
    - item: viene del body JSON
    """
    # Obtener solo campos con valor
    cambios = item.model_dump(exclude_none=True)

    return {
        "item_id": item_id,
        "cambios": cambios
    }


# =============================================================================
# BODY + PATH + QUERY
# =============================================================================


@app.put("/items/{item_id}/actualizar")
def actualizar_con_notificacion(
    item_id: int = Path(ge=1),              # Path parameter
    item: ItemActualizar = None,             # Request body (opcional)
    notificar: bool = Query(default=False),  # Query parameter
    prioridad: str = Query(default="normal") # Query parameter
):
    """
    Combina todos los tipos de parámetros.

    PUT /items/5/actualizar?notificar=true&prioridad=alta
    Body: {"precio": 899.99}
    """
    resultado = {
        "item_id": item_id,
        "notificar": notificar,
        "prioridad": prioridad
    }

    if item:
        resultado["cambios"] = item.model_dump(exclude_none=True)

    return resultado


# =============================================================================
# MÚLTIPLES BODIES
# =============================================================================


class Direccion(BaseModel):
    """Dirección de envío."""
    calle: str
    ciudad: str
    codigo_postal: str


class PedidoCrear(BaseModel):
    """Pedido con usuario y dirección."""
    usuario: Usuario
    direccion: Direccion
    items: list[ItemCrear]
    notas: str | None = None


@app.post("/pedidos")
def crear_pedido(pedido: PedidoCrear):
    """
    Body con modelos anidados.

    Request body ejemplo:
    {
        "usuario": {
            "nombre": "Ana",
            "email": "ana@test.com"
        },
        "direccion": {
            "calle": "Gran Vía 123",
            "ciudad": "Madrid",
            "codigo_postal": "28001"
        },
        "items": [
            {"nombre": "Laptop", "precio": 999.99},
            {"nombre": "Mouse", "precio": 29.99, "cantidad": 2}
        ]
    }
    """
    total = sum(item.precio * item.cantidad for item in pedido.items)

    return {
        "mensaje": "Pedido creado",
        "cliente": pedido.usuario.nombre,
        "total_items": len(pedido.items),
        "total": total
    }


# =============================================================================
# BODY COMO DICCIONARIO (sin modelo)
# =============================================================================


@app.post("/webhook")
def recibir_webhook(payload: dict):
    """
    Recibe cualquier JSON como dict.

    Útil para webhooks externos donde no conoces la estructura.
    ⚠️ Sin validación automática.
    """
    return {
        "recibido": True,
        "claves": list(payload.keys())
    }


# =============================================================================
# BODY CON CAMPO EMBED
# =============================================================================

from fastapi import Body


@app.post("/items-embed")
def crear_item_embed(
    item: ItemCrear = Body(embed=True)
):
    """
    Con embed=True, el body debe tener la clave del modelo.

    Sin embed:  {"nombre": "...", "precio": ...}
    Con embed:  {"item": {"nombre": "...", "precio": ...}}
    """
    return {"item": item.model_dump()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
