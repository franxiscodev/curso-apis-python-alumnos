"""
Solución Ejercicio 03: Sistema de Pedidos con Modelos Anidados
==============================================================
"""

from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator


class Direccion(BaseModel):
    """Dirección de envío o facturación."""
    calle: str
    ciudad: str
    codigo_postal: str = Field(min_length=5, max_length=5)
    pais: str = "España"

    @field_validator("codigo_postal")
    @classmethod
    def validar_codigo_postal(cls, v: str) -> str:
        """Valida que sea 5 dígitos."""
        if not v.isdigit():
            raise ValueError("Código postal debe contener solo dígitos")
        return v


class Cliente(BaseModel):
    """Cliente que realiza el pedido."""
    id: int
    nombre: str
    email: EmailStr
    direccion: Direccion


class ProductoPedido(BaseModel):
    """Producto dentro de un pedido."""
    producto_id: int
    nombre: str
    precio_unitario: float = Field(gt=0)
    cantidad: int = Field(ge=1, default=1)

    @property
    def subtotal(self) -> float:
        """Calcula subtotal del producto."""
        return self.precio_unitario * self.cantidad


class Pedido(BaseModel):
    """Pedido completo con cliente y productos."""
    id: int | None = None
    cliente: Cliente
    productos: list[ProductoPedido] = Field(min_length=1)
    direccion_envio: Direccion | None = None
    notas: str | None = None

    @model_validator(mode="after")
    def establecer_direccion_envio(self) -> "Pedido":
        """Si no hay dirección de envío, usar la del cliente."""
        if self.direccion_envio is None:
            # Crear copia de la dirección del cliente
            self.direccion_envio = Direccion.model_validate(
                self.cliente.direccion.model_dump()
            )
        return self

    @property
    def total(self) -> float:
        """Calcula total del pedido."""
        return sum(p.subtotal for p in self.productos)


# =============================================================================
# DTOs
# =============================================================================


class PedidoCrear(BaseModel):
    """DTO para crear pedido (sin id)."""
    cliente: Cliente
    productos: list[ProductoPedido] = Field(min_length=1)
    direccion_envio: Direccion | None = None
    notas: str | None = None


class PedidoResponse(BaseModel):
    """DTO para respuesta de pedido."""
    id: int
    cliente: Cliente
    productos: list[ProductoPedido]
    direccion_envio: Direccion
    notas: str | None
    total: float

    @classmethod
    def from_pedido(cls, pedido: Pedido) -> "PedidoResponse":
        """Crea response desde un Pedido."""
        return cls(
            id=pedido.id or 0,
            cliente=pedido.cliente,
            productos=pedido.productos,
            direccion_envio=pedido.direccion_envio,  # type: ignore
            notas=pedido.notas,
            total=pedido.total
        )


# =============================================================================
# VERIFICACIÓN
# =============================================================================

if __name__ == "__main__":
    from pydantic import ValidationError
    import json

    print("=" * 60)
    print("Solución Ejercicio 03: Sistema de Pedidos")
    print("=" * 60)

    # Datos de prueba
    datos_pedido = {
        "cliente": {
            "id": 1,
            "nombre": "Ana García",
            "email": "ana@ejemplo.com",
            "direccion": {
                "calle": "Gran Vía 123",
                "ciudad": "Madrid",
                "codigo_postal": "28001"
            }
        },
        "productos": [
            {"producto_id": 1, "nombre": "Laptop", "precio_unitario": 999.99, "cantidad": 1},
            {"producto_id": 2, "nombre": "Mouse", "precio_unitario": 29.99, "cantidad": 2}
        ]
    }

    # Crear pedido
    print("\n--- Crear pedido ---")
    pedido = Pedido.model_validate(datos_pedido)
    print(f"Pedido creado para: {pedido.cliente.nombre}")

    # Acceso anidado
    print("\n--- Acceso a modelos anidados ---")
    print(f"Email cliente: {pedido.cliente.email}")
    print(f"Ciudad cliente: {pedido.cliente.direccion.ciudad}")

    # Subtotales
    print("\n--- Subtotales ---")
    for p in pedido.productos:
        print(f"  {p.nombre}: ${p.precio_unitario} x {p.cantidad} = ${p.subtotal}")

    # Total
    print(f"\nTotal del pedido: ${pedido.total:.2f}")

    # Dirección de envío
    print("\n--- Dirección de envío ---")
    print(f"Copiada del cliente: {pedido.direccion_envio.ciudad}")

    # Con dirección diferente
    print("\n--- Dirección de envío diferente ---")
    datos_con_envio = {
        **datos_pedido,
        "direccion_envio": {
            "calle": "Diagonal 456",
            "ciudad": "Barcelona",
            "codigo_postal": "08001"
        }
    }
    pedido2 = Pedido.model_validate(datos_con_envio)
    print(f"Envío a: {pedido2.direccion_envio.ciudad}")

    # Validaciones
    print("\n--- Validaciones ---")

    # Código postal inválido
    try:
        Direccion(calle="Test", ciudad="Test", codigo_postal="123")
    except ValidationError as e:
        print(f"Código postal inválido: OK")

    # Pedido sin productos
    try:
        Pedido.model_validate({**datos_pedido, "productos": []})
    except ValidationError:
        print("Pedido sin productos: Rechazado OK")

    # Serialización
    print("\n--- Serialización ---")
    data = pedido.model_dump()
    print(f"Claves: {list(data.keys())}")

    # DTO Response
    print("\n--- DTO Response ---")
    pedido.id = 1000
    response = PedidoResponse.from_pedido(pedido)
    print(f"Response ID: {response.id}")
    print(f"Response Total: ${response.total:.2f}")

    # JSON completo
    print("\n--- JSON completo ---")
    print(pedido.model_dump_json(indent=2)[:400] + "...")

    print("\n✓ Solución completada")
