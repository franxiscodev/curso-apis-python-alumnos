"""
Solución Ejercicio 01: Clase Producto con Validación
=====================================================
"""


class Producto:
    """Representa un producto del catálogo con validación."""

    def __init__(
        self,
        nombre: str,
        precio: float,
        stock: int = 0,
        id: int | None = None
    ):
        """
        Inicializa un producto.

        Args:
            nombre: Nombre del producto (no vacío)
            precio: Precio del producto (>= 0)
            stock: Cantidad en inventario (>= 0)
            id: Identificador único
        """
        self.id = id
        self.nombre = nombre  # Usa setter con validación
        self.precio = precio  # Usa setter con validación
        self.stock = stock    # Usa setter con validación

    # --- Nombre ---
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = valor.strip()

    # --- Precio ---
    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        if valor < 0:
            raise ValueError(f"El precio no puede ser negativo: {valor}")
        self._precio = valor

    # --- Stock ---
    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int) -> None:
        if valor < 0:
            raise ValueError(f"El stock no puede ser negativo: {valor}")
        self._stock = int(valor)

    # --- Propiedad calculada ---
    @property
    def disponible(self) -> bool:
        """True si hay stock disponible."""
        return self._stock > 0

    # --- Serialización ---
    def to_dict(self) -> dict:
        """Serializa a diccionario para JSON response."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
            "disponible": self.disponible
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Producto":
        """Deserializa desde diccionario (JSON request)."""
        return cls(
            id=data.get("id"),
            nombre=data["nombre"],
            precio=data["precio"],
            stock=data.get("stock", 0)
        )

    # --- Métodos especiales ---
    def __repr__(self) -> str:
        return f"Producto(id={self.id}, nombre='{self.nombre}', precio={self.precio})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Producto):
            return False
        return self.id == other.id


# =============================================================================
# VERIFICACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Solución Ejercicio 01: Clase Producto")
    print("=" * 60)

    # Test 1: Creación básica
    print("\n--- Test 1: Creación básica ---")
    p = Producto(nombre="Laptop", precio=999.99, stock=10, id=1)
    print(f"  ✓ Producto creado: {p}")

    # Test 2: Validación de nombre
    print("\n--- Test 2: Validación de nombre ---")
    try:
        Producto(nombre="", precio=100)
    except ValueError:
        print("  ✓ ValueError para nombre vacío")

    # Test 3: Validación de precio
    print("\n--- Test 3: Validación de precio ---")
    try:
        Producto(nombre="Test", precio=-50)
    except ValueError:
        print("  ✓ ValueError para precio negativo")

    # Test 4: Propiedad disponible
    print("\n--- Test 4: Propiedad disponible ---")
    p_stock = Producto(nombre="Con Stock", precio=50, stock=5)
    p_sin = Producto(nombre="Sin Stock", precio=50, stock=0)
    print(f"  ✓ Con stock: disponible={p_stock.disponible}")
    print(f"  ✓ Sin stock: disponible={p_sin.disponible}")

    # Test 5: Serialización
    print("\n--- Test 5: to_dict() ---")
    print(f"  ✓ {p.to_dict()}")

    # Test 6: Deserialización
    print("\n--- Test 6: from_dict() ---")
    datos = {"id": 3, "nombre": "Teclado", "precio": 79.99, "stock": 50}
    p_from = Producto.from_dict(datos)
    print(f"  ✓ {p_from}")

    # Test 7: Igualdad
    print("\n--- Test 7: __eq__ ---")
    p1 = Producto(nombre="A", precio=10, id=1)
    p2 = Producto(nombre="B", precio=20, id=1)
    print(f"  ✓ p1 == p2 (mismo id): {p1 == p2}")

    print("\n✓ Solución completada")
