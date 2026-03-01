"""
Solución Ejercicio 03: Repository de Pedidos
=============================================
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime


# =============================================================================
# ENTIDADES
# =============================================================================


@dataclass
class Producto:
    """Producto en un pedido."""
    nombre: str
    precio: float
    cantidad: int = 1

    @property
    def subtotal(self) -> float:
        return self.precio * self.cantidad


@dataclass
class Pedido:
    """Pedido de un cliente."""
    cliente_id: int
    productos: list[Producto] = field(default_factory=list)
    id: int | None = None
    fecha: datetime = field(default_factory=datetime.now)

    @property
    def total(self) -> float:
        return sum(p.subtotal for p in self.productos)

    def agregar_producto(self, producto: Producto) -> None:
        self.productos.append(producto)


# =============================================================================
# PATRÓN REPOSITORY
# =============================================================================


class PedidoRepository(ABC):
    """Interfaz abstracta para Repository de Pedidos."""

    @abstractmethod
    def obtener(self, id: int) -> Pedido | None:
        """Obtiene pedido por ID."""
        pass

    @abstractmethod
    def guardar(self, pedido: Pedido) -> Pedido:
        """Guarda pedido (crea si no tiene ID, actualiza si tiene)."""
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina pedido. Retorna True si existía."""
        pass

    @abstractmethod
    def listar(self) -> list[Pedido]:
        """Lista todos los pedidos."""
        pass

    @abstractmethod
    def listar_por_cliente(self, cliente_id: int) -> list[Pedido]:
        """Lista pedidos de un cliente específico."""
        pass


class PedidoMemoryRepository(PedidoRepository):
    """Implementación en memoria del Repository de Pedidos."""

    def __init__(self):
        self._pedidos: dict[int, Pedido] = {}
        self._next_id = 1

    def obtener(self, id: int) -> Pedido | None:
        """Obtiene pedido por ID."""
        return self._pedidos.get(id)

    def guardar(self, pedido: Pedido) -> Pedido:
        """Guarda pedido con auto-incremento de ID."""
        if pedido.id is None:
            pedido.id = self._next_id
            self._next_id += 1
        self._pedidos[pedido.id] = pedido
        return pedido

    def eliminar(self, id: int) -> bool:
        """Elimina pedido si existe."""
        if id in self._pedidos:
            del self._pedidos[id]
            return True
        return False

    def listar(self) -> list[Pedido]:
        """Lista todos los pedidos."""
        return list(self._pedidos.values())

    def listar_por_cliente(self, cliente_id: int) -> list[Pedido]:
        """Filtra pedidos por cliente_id."""
        return [p for p in self._pedidos.values() if p.cliente_id == cliente_id]

    def contar(self) -> int:
        """Retorna cantidad de pedidos (método adicional útil)."""
        return len(self._pedidos)

    def total_ventas(self) -> float:
        """Calcula total de todas las ventas (método adicional)."""
        return sum(p.total for p in self._pedidos.values())


# =============================================================================
# VERIFICACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Solución Ejercicio 03: Repository de Pedidos")
    print("=" * 60)

    repo = PedidoMemoryRepository()

    # Test 1: Guardar pedido
    print("\n--- Test 1: Guardar pedido ---")
    pedido1 = Pedido(cliente_id=1)
    pedido1.agregar_producto(Producto("Laptop", 999.99))
    pedido1.agregar_producto(Producto("Mouse", 29.99, cantidad=2))
    pedido_guardado = repo.guardar(pedido1)
    print(f"  ✓ Pedido guardado: ID={pedido_guardado.id}, Total=${pedido_guardado.total:.2f}")

    # Test 2: Obtener pedido
    print("\n--- Test 2: Obtener pedido ---")
    obtenido = repo.obtener(1)
    print(f"  ✓ Obtenido: {obtenido}")
    print(f"  ✓ Inexistente: {repo.obtener(999)}")

    # Test 3: Múltiples pedidos
    print("\n--- Test 3: Múltiples pedidos ---")
    pedido2 = Pedido(cliente_id=1)
    pedido2.agregar_producto(Producto("Teclado", 79.99))
    repo.guardar(pedido2)

    pedido3 = Pedido(cliente_id=2)
    pedido3.agregar_producto(Producto("Monitor", 299.99))
    repo.guardar(pedido3)
    print(f"  ✓ Total pedidos: {repo.contar()}")

    # Test 4: Listar todos
    print("\n--- Test 4: Listar todos ---")
    for p in repo.listar():
        print(f"  - ID={p.id}, Cliente={p.cliente_id}, Total=${p.total:.2f}")

    # Test 5: Listar por cliente
    print("\n--- Test 5: Listar por cliente ---")
    print(f"  ✓ Cliente 1: {len(repo.listar_por_cliente(1))} pedidos")
    print(f"  ✓ Cliente 2: {len(repo.listar_por_cliente(2))} pedidos")

    # Test 6: Eliminar
    print("\n--- Test 6: Eliminar pedido ---")
    print(f"  ✓ Eliminar ID=2: {repo.eliminar(2)}")
    print(f"  ✓ Eliminar ID=999: {repo.eliminar(999)}")
    print(f"  ✓ Pedidos restantes: {repo.contar()}")

    # Test 7: Estadísticas
    print("\n--- Test 7: Estadísticas ---")
    print(f"  ✓ Total ventas: ${repo.total_ventas():.2f}")

    # Test 8: ABC no instanciable
    print("\n--- Test 8: ABC ---")
    try:
        PedidoRepository()  # type: ignore
    except TypeError:
        print("  ✓ PedidoRepository no es instanciable (ABC)")

    print("\n✓ Solución completada")
