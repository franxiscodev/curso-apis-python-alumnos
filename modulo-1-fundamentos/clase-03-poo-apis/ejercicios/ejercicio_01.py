"""
Ejercicio 01: Clase Producto con Validación
============================================

Objetivo:
Crear una clase Producto que represente un producto de API con:
- Validación de datos usando @property
- Métodos de serialización (to_dict, from_dict)
- Métodos especiales (__repr__, __eq__)

Requisitos:
1. Atributos: id, nombre, precio, stock
2. Validaciones:
   - nombre: no puede estar vacío
   - precio: debe ser >= 0
   - stock: debe ser >= 0 (entero)
3. Propiedad calculada: disponible (True si stock > 0)
4. to_dict() y from_dict() para JSON
5. __repr__ para debugging
6. __eq__ comparando por id
"""


class Producto:
    """
    Representa un producto del catálogo.

    TODO: Implementar la clase completa.
    """

    def __init__(
        self,
        nombre: str,
        precio: float,
        stock: int = 0,
        id: int | None = None
    ):
        # TODO: Implementar inicialización con validación
        pass

    # TODO: Implementar @property y setters para nombre, precio, stock

    # TODO: Implementar @property disponible (calculada)

    # TODO: Implementar to_dict()

    # TODO: Implementar from_dict() como @classmethod

    # TODO: Implementar __repr__

    # TODO: Implementar __eq__


# =============================================================================
# VERIFICACIÓN (No modificar)
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Verificando Ejercicio 01: Clase Producto")
    print("=" * 60)

    # Test 1: Creación básica
    print("\n--- Test 1: Creación básica ---")
    try:
        p = Producto(nombre="Laptop", precio=999.99, stock=10, id=1)
        print(f"  ✓ Producto creado: {p}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 2: Validación de nombre
    print("\n--- Test 2: Validación de nombre ---")
    try:
        p_malo = Producto(nombre="", precio=100)
        print("  ✗ Debería lanzar ValueError para nombre vacío")
    except ValueError:
        print("  ✓ ValueError lanzado correctamente")

    # Test 3: Validación de precio
    print("\n--- Test 3: Validación de precio ---")
    try:
        p_malo = Producto(nombre="Test", precio=-50)
        print("  ✗ Debería lanzar ValueError para precio negativo")
    except ValueError:
        print("  ✓ ValueError lanzado correctamente")

    # Test 4: Propiedad disponible
    print("\n--- Test 4: Propiedad disponible ---")
    p_stock = Producto(nombre="Con Stock", precio=50, stock=5)
    p_sin_stock = Producto(nombre="Sin Stock", precio=50, stock=0)
    if p_stock.disponible and not p_sin_stock.disponible:
        print("  ✓ Propiedad disponible funciona")
    else:
        print("  ✗ Propiedad disponible incorrecta")

    # Test 5: Serialización
    print("\n--- Test 5: Serialización ---")
    p = Producto(nombre="Mouse", precio=29.99, stock=100, id=2)
    d = p.to_dict()
    if all(k in d for k in ["id", "nombre", "precio", "stock", "disponible"]):
        print(f"  ✓ to_dict(): {d}")
    else:
        print("  ✗ to_dict() incompleto")

    # Test 6: Deserialización
    print("\n--- Test 6: Deserialización ---")
    datos = {"id": 3, "nombre": "Teclado", "precio": 79.99, "stock": 50}
    p_from = Producto.from_dict(datos)
    if p_from.nombre == "Teclado" and p_from.precio == 79.99:
        print(f"  ✓ from_dict(): {p_from}")
    else:
        print("  ✗ from_dict() incorrecto")

    # Test 7: Igualdad
    print("\n--- Test 7: Igualdad (por id) ---")
    p1 = Producto(nombre="A", precio=10, id=1)
    p2 = Producto(nombre="B", precio=20, id=1)
    p3 = Producto(nombre="A", precio=10, id=2)
    if p1 == p2 and p1 != p3:
        print("  ✓ __eq__ compara por id")
    else:
        print("  ✗ __eq__ incorrecto")

    print("\n" + "=" * 60)
    print("Ejecuta las soluciones con:")
    print("  python ejercicios/soluciones/ejercicio_01_solucion.py")
