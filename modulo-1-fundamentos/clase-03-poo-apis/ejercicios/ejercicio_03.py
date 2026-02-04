"""
Ejercicio 03: Repository de Pedidos
====================================

Objetivo:
Implementar el patrón Repository para gestionar Pedidos.

Clases proporcionadas:
- Producto (entidad)
- Pedido (entidad con composición)

Tu tarea:
1. Crear PedidoRepository (clase abstracta con ABC)
2. Implementar PedidoMemoryRepository

Requisitos del Repository:

1. Métodos abstractos en PedidoRepository:
   - obtener(id: int) -> Pedido | None
   - guardar(pedido: Pedido) -> Pedido
   - eliminar(id: int) -> bool
   - listar() -> list[Pedido]
   - listar_por_cliente(cliente_id: int) -> list[Pedido]

2. PedidoMemoryRepository debe:
   - Almacenar pedidos en un diccionario
   - Auto-incrementar IDs al guardar
   - Implementar todos los métodos abstractos
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime


# =============================================================================
# ENTIDADES (Proporcionadas - No modificar)
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
# TU CÓDIGO AQUÍ
# =============================================================================


class PedidoRepository(ABC):
    """
    Interfaz abstracta para Repository de Pedidos.

    TODO: Definir métodos abstractos.
    """

    @abstractmethod
    def obtener(self, id: int) -> Pedido | None:
        """Obtiene pedido por ID."""
        pass

    # TODO: Agregar los demás métodos abstractos:
    # - guardar(pedido: Pedido) -> Pedido
    # - eliminar(id: int) -> bool
    # - listar() -> list[Pedido]
    # - listar_por_cliente(cliente_id: int) -> list[Pedido]


class PedidoMemoryRepository(PedidoRepository):
    """
    Implementación en memoria del Repository de Pedidos.

    TODO: Implementar todos los métodos.
    """

    def __init__(self):
        # TODO: Inicializar diccionario de pedidos y contador de IDs
        pass

    def obtener(self, id: int) -> Pedido | None:
        # TODO: Implementar
        pass

    # TODO: Implementar los demás métodos


# =============================================================================
# VERIFICACIÓN (No modificar)
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Verificando Ejercicio 03: Repository de Pedidos")
    print("=" * 60)

    # Setup
    repo = PedidoMemoryRepository()

    # Test 1: Guardar pedido
    print("\n--- Test 1: Guardar pedido ---")
    try:
        pedido1 = Pedido(cliente_id=1)
        pedido1.agregar_producto(Producto("Laptop", 999.99))
        pedido1.agregar_producto(Producto("Mouse", 29.99, cantidad=2))

        pedido_guardado = repo.guardar(pedido1)
        if pedido_guardado.id is not None:
            print(f"  ✓ Pedido guardado con ID: {pedido_guardado.id}")
            print(f"    Total: ${pedido_guardado.total:.2f}")
        else:
            print("  ✗ El pedido guardado no tiene ID")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 2: Obtener pedido
    print("\n--- Test 2: Obtener pedido ---")
    try:
        obtenido = repo.obtener(1)
        if obtenido and obtenido.cliente_id == 1:
            print(f"  ✓ Pedido obtenido: ID={obtenido.id}")
        else:
            print("  ✗ No se pudo obtener el pedido")

        no_existe = repo.obtener(999)
        if no_existe is None:
            print("  ✓ Pedido inexistente retorna None")
        else:
            print("  ✗ Debería retornar None para ID inexistente")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 3: Guardar más pedidos
    print("\n--- Test 3: Múltiples pedidos ---")
    try:
        pedido2 = Pedido(cliente_id=1)
        pedido2.agregar_producto(Producto("Teclado", 79.99))
        repo.guardar(pedido2)

        pedido3 = Pedido(cliente_id=2)
        pedido3.agregar_producto(Producto("Monitor", 299.99))
        repo.guardar(pedido3)

        print(f"  ✓ Total pedidos guardados: 3")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 4: Listar todos
    print("\n--- Test 4: Listar todos ---")
    try:
        todos = repo.listar()
        if len(todos) == 3:
            print(f"  ✓ Listados {len(todos)} pedidos")
            for p in todos:
                print(f"    - ID={p.id}, Cliente={p.cliente_id}, Total=${p.total:.2f}")
        else:
            print(f"  ✗ Se esperaban 3 pedidos, hay {len(todos)}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 5: Listar por cliente
    print("\n--- Test 5: Listar por cliente ---")
    try:
        pedidos_cliente1 = repo.listar_por_cliente(1)
        pedidos_cliente2 = repo.listar_por_cliente(2)

        if len(pedidos_cliente1) == 2 and len(pedidos_cliente2) == 1:
            print(f"  ✓ Cliente 1: {len(pedidos_cliente1)} pedidos")
            print(f"  ✓ Cliente 2: {len(pedidos_cliente2)} pedidos")
        else:
            print("  ✗ Filtro por cliente incorrecto")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 6: Eliminar pedido
    print("\n--- Test 6: Eliminar pedido ---")
    try:
        eliminado = repo.eliminar(2)
        if eliminado:
            print("  ✓ Pedido 2 eliminado")
        else:
            print("  ✗ No se pudo eliminar")

        if repo.obtener(2) is None:
            print("  ✓ Pedido ya no existe")
        else:
            print("  ✗ Pedido aún existe después de eliminar")

        no_eliminado = repo.eliminar(999)
        if not no_eliminado:
            print("  ✓ Eliminar ID inexistente retorna False")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 7: Verificar ABC
    print("\n--- Test 7: PedidoRepository es ABC ---")
    try:
        repo_abstracto = PedidoRepository()  # type: ignore
        print("  ✗ No debería poder instanciar ABC")
    except TypeError:
        print("  ✓ PedidoRepository es abstracta (no instanciable)")

    print("\n" + "=" * 60)
    print("Ejecuta las soluciones con:")
    print("  python ejercicios/soluciones/ejercicio_03_solucion.py")
