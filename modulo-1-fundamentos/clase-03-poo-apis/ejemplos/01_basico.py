"""
Ejemplo 01: Clases Básicas para APIs
====================================
Clases que representan recursos, @property, y métodos especiales.
"""


class Usuario:
    """Representa un usuario del sistema (recurso de API)."""

    def __init__(self, nombre: str, email: str, id: int | None = None):
        """
        Inicializa un usuario.

        Args:
            nombre: Nombre del usuario
            email: Correo electrónico
            id: Identificador único (None si es nuevo)
        """
        self.id = id
        self.nombre = nombre
        self._email = email  # Atributo "privado" para usar con @property

    @property
    def email(self) -> str:
        """Getter para email."""
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        """Setter con validación básica."""
        if "@" not in valor:
            raise ValueError(f"Email inválido: {valor}")
        self._email = valor

    def to_dict(self) -> dict:
        """Serializa a diccionario (para JSON response)."""
        return {"id": self.id, "nombre": self.nombre, "email": self.email}

    @classmethod
    def from_dict(cls, data: dict) -> "Usuario":
        """Deserializa desde diccionario (desde JSON request)."""
        return cls(
            id=data.get("id"),
            nombre=data["nombre"],
            email=data["email"]
        )

    def __repr__(self) -> str:
        """Representación para debugging."""
        return f"Usuario(id={self.id}, nombre='{self.nombre}')"

    def __str__(self) -> str:
        """Representación para usuarios."""
        return f"{self.nombre} <{self.email}>"

    def __eq__(self, other: object) -> bool:
        """Comparación por igualdad (basada en id)."""
        if not isinstance(other, Usuario):
            return False
        return self.id == other.id


# =============================================================================
# CLASE CON PROPIEDADES CALCULADAS
# =============================================================================


class Producto:
    """Producto con precio y descuento."""

    def __init__(self, nombre: str, precio: float, descuento: float = 0):
        self.nombre = nombre
        self._precio = precio
        self._descuento = descuento

    @property
    def precio(self) -> float:
        """Precio base del producto."""
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        """Setter con validación."""
        if valor < 0:
            raise ValueError("El precio no puede ser negativo")
        self._precio = valor

    @property
    def descuento(self) -> float:
        """Porcentaje de descuento (0-100)."""
        return self._descuento

    @descuento.setter
    def descuento(self, valor: float) -> None:
        """Setter con validación de rango."""
        if not 0 <= valor <= 100:
            raise ValueError("Descuento debe estar entre 0 y 100")
        self._descuento = valor

    @property
    def precio_final(self) -> float:
        """Precio con descuento aplicado (propiedad calculada)."""
        return self._precio * (1 - self._descuento / 100)

    def to_dict(self) -> dict:
        """Serializa incluyendo precio calculado."""
        return {
            "nombre": self.nombre,
            "precio": self.precio,
            "descuento": self.descuento,
            "precio_final": self.precio_final
        }


# =============================================================================
# DEMOSTRACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Demostración: Clases Básicas para APIs")
    print("=" * 60)

    # --- Usuario ---
    print("\n--- Clase Usuario ---")

    # Crear desde constructor
    usuario1 = Usuario(nombre="Ana García", email="ana@ejemplo.com", id=1)
    print(f"repr: {repr(usuario1)}")
    print(f"str:  {usuario1}")

    # Crear desde diccionario (como llegaría de JSON)
    datos_json = {"nombre": "Carlos López", "email": "carlos@ejemplo.com"}
    usuario2 = Usuario.from_dict(datos_json)
    print(f"\nDesde dict: {usuario2}")

    # Serializar a diccionario (para respuesta JSON)
    print(f"to_dict(): {usuario1.to_dict()}")

    # Comparación
    usuario3 = Usuario(nombre="Ana García", email="otro@email.com", id=1)
    print(f"\nusuario1 == usuario3 (mismo id): {usuario1 == usuario3}")

    # Validación en setter
    print("\n--- Validación con @property ---")
    try:
        usuario1.email = "email-invalido"
    except ValueError as e:
        print(f"Error capturado: {e}")

    # --- Producto ---
    print("\n--- Clase Producto ---")
    producto = Producto(nombre="Laptop", precio=1000, descuento=20)
    print(f"Precio base: ${producto.precio}")
    print(f"Descuento: {producto.descuento}%")
    print(f"Precio final: ${producto.precio_final}")
    print(f"to_dict(): {producto.to_dict()}")

    # Validación
    print("\n--- Validación de precio ---")
    try:
        producto.precio = -100
    except ValueError as e:
        print(f"Error capturado: {e}")

    print("\n✓ Ejemplo completado")
