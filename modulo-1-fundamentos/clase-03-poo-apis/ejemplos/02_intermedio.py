"""
Ejemplo 02: Herencia y Composición
==================================
Herencia con ModeloBase, composición, y clases abstractas.
"""

from abc import ABC, abstractmethod
from datetime import datetime


# =============================================================================
# HERENCIA: MODELO BASE
# =============================================================================


class ModeloBase:
    """Clase base para todos los modelos de API."""

    def __init__(self):
        self.id: int | None = None
        self.creado_en: datetime = datetime.now()
        self.actualizado_en: datetime = datetime.now()

    def to_dict(self) -> dict:
        """Serialización base con campos comunes."""
        return {
            "id": self.id,
            "creado_en": self.creado_en.isoformat(),
            "actualizado_en": self.actualizado_en.isoformat(),
        }

    def actualizar(self) -> None:
        """Marca el modelo como actualizado."""
        self.actualizado_en = datetime.now()


class Usuario(ModeloBase):
    """Usuario hereda campos comunes de ModeloBase."""

    def __init__(self, nombre: str, email: str):
        super().__init__()  # Llama al __init__ del padre
        self.nombre = nombre
        self.email = email

    def to_dict(self) -> dict:
        """Extiende serialización base."""
        base = super().to_dict()
        base.update({"nombre": self.nombre, "email": self.email})
        return base


class Producto(ModeloBase):
    """Producto también hereda de ModeloBase."""

    def __init__(self, nombre: str, precio: float):
        super().__init__()
        self.nombre = nombre
        self.precio = precio

    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({"nombre": self.nombre, "precio": self.precio})
        return base


# =============================================================================
# COMPOSICIÓN: "TIENE UN" VS "ES UN"
# =============================================================================


class Direccion:
    """Clase para composición (no herencia)."""

    def __init__(self, calle: str, ciudad: str, codigo_postal: str):
        self.calle = calle
        self.ciudad = ciudad
        self.codigo_postal = codigo_postal

    def to_dict(self) -> dict:
        return {
            "calle": self.calle,
            "ciudad": self.ciudad,
            "codigo_postal": self.codigo_postal
        }


class Pedido(ModeloBase):
    """
    Pedido usa COMPOSICIÓN.

    - Pedido TIENE UN usuario (no ES UN usuario)
    - Pedido TIENE productos (no ES UN producto)
    - Pedido TIENE UNA dirección de envío
    """

    def __init__(
        self,
        usuario: Usuario,
        productos: list[Producto],
        direccion_envio: Direccion
    ):
        super().__init__()
        self.usuario = usuario          # Composición
        self.productos = productos      # Composición
        self.direccion_envio = direccion_envio

    @property
    def total(self) -> float:
        """Calcula total del pedido."""
        return sum(p.precio for p in self.productos)

    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({
            "usuario": self.usuario.to_dict(),
            "productos": [p.to_dict() for p in self.productos],
            "direccion_envio": self.direccion_envio.to_dict(),
            "total": self.total
        })
        return base


# =============================================================================
# CLASES ABSTRACTAS (ABC)
# =============================================================================


class Notificador(ABC):
    """Interfaz abstracta para envío de notificaciones."""

    @abstractmethod
    def enviar(self, destinatario: str, mensaje: str) -> bool:
        """Envía una notificación. Debe ser implementado."""
        pass

    @abstractmethod
    def validar_destinatario(self, destinatario: str) -> bool:
        """Valida el destinatario. Debe ser implementado."""
        pass


class NotificadorEmail(Notificador):
    """Implementación concreta para email."""

    def enviar(self, destinatario: str, mensaje: str) -> bool:
        print(f"[EMAIL] Enviando a {destinatario}: {mensaje}")
        return True

    def validar_destinatario(self, destinatario: str) -> bool:
        return "@" in destinatario


class NotificadorSMS(Notificador):
    """Implementación concreta para SMS."""

    def enviar(self, destinatario: str, mensaje: str) -> bool:
        print(f"[SMS] Enviando a {destinatario}: {mensaje[:160]}")
        return True

    def validar_destinatario(self, destinatario: str) -> bool:
        return destinatario.startswith("+") and len(destinatario) >= 10


# =============================================================================
# DEMOSTRACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Demostración: Herencia y Composición")
    print("=" * 60)

    # --- Herencia ---
    print("\n--- Herencia: ModeloBase ---")
    usuario = Usuario(nombre="Ana", email="ana@ejemplo.com")
    usuario.id = 1
    print(f"Usuario hereda de ModeloBase:")
    print(f"  {usuario.to_dict()}")

    producto = Producto(nombre="Laptop", precio=999.99)
    producto.id = 100
    print(f"\nProducto también hereda:")
    print(f"  {producto.to_dict()}")

    # --- Composición ---
    print("\n--- Composición: Pedido ---")
    productos = [
        Producto("Laptop", 999.99),
        Producto("Mouse", 29.99),
    ]
    for i, p in enumerate(productos, 1):
        p.id = i

    direccion = Direccion(
        calle="Calle Principal 123",
        ciudad="Madrid",
        codigo_postal="28001"
    )

    pedido = Pedido(
        usuario=usuario,
        productos=productos,
        direccion_envio=direccion
    )
    pedido.id = 1000

    print("Pedido compuesto por:")
    print(f"  Usuario: {usuario.nombre}")
    print(f"  Productos: {len(productos)}")
    print(f"  Total: ${pedido.total}")
    print(f"\nto_dict() completo:")
    import json
    print(json.dumps(pedido.to_dict(), indent=2, default=str))

    # --- ABC ---
    print("\n--- Clases Abstractas ---")

    # No se puede instanciar ABC directamente
    # notificador = Notificador()  # TypeError!

    email = NotificadorEmail()
    sms = NotificadorSMS()

    # Polimorfismo: misma interfaz, diferente implementación
    notificadores: list[Notificador] = [email, sms]

    for n in notificadores:
        tipo = n.__class__.__name__
        print(f"\n{tipo}:")
        print(f"  Válido 'ana@email.com': {n.validar_destinatario('ana@email.com')}")
        print(f"  Válido '+34600000000': {n.validar_destinatario('+34600000000')}")

    print("\n✓ Ejemplo completado")
