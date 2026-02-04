"""
Errores Comunes en POO para APIs
================================
Errores frecuentes y cómo evitarlos.
"""


# =============================================================================
# ERROR 1: Olvidar super().__init__()
# =============================================================================

class ModeloBase:
    def __init__(self):
        self.id: int | None = None


# ❌ INCORRECTO: No llama a super().__init__()
class UsuarioMal(ModeloBase):
    def __init__(self, nombre: str):
        # Falta: super().__init__()
        self.nombre = nombre


# ✅ CORRECTO: Siempre llamar super().__init__()
class UsuarioBien(ModeloBase):
    def __init__(self, nombre: str):
        super().__init__()  # ← Importante!
        self.nombre = nombre


# Demostración
def demo_error_1():
    print("--- Error 1: Olvidar super().__init__() ---")
    mal = UsuarioMal("Ana")
    print(f"  UsuarioMal - tiene 'id'? {hasattr(mal, 'id')}")  # False!

    bien = UsuarioBien("Ana")
    print(f"  UsuarioBien - tiene 'id'? {hasattr(bien, 'id')}")  # True


# =============================================================================
# ERROR 2: Mutar argumentos por defecto mutables
# =============================================================================

# ❌ INCORRECTO: Lista mutable como default
class PedidoMal:
    def __init__(self, productos: list = []):  # ← Peligroso!
        self.productos = productos


# ✅ CORRECTO: Usar None y crear lista nueva
class PedidoBien:
    def __init__(self, productos: list | None = None):
        self.productos = productos if productos is not None else []


def demo_error_2():
    print("\n--- Error 2: Argumentos mutables por defecto ---")
    p1_mal = PedidoMal()
    p2_mal = PedidoMal()
    p1_mal.productos.append("Laptop")
    print(f"  PedidoMal - p2.productos: {p2_mal.productos}")  # ['Laptop']!

    p1_bien = PedidoBien()
    p2_bien = PedidoBien()
    p1_bien.productos.append("Laptop")
    print(f"  PedidoBien - p2.productos: {p2_bien.productos}")  # []


# =============================================================================
# ERROR 3: Herencia incorrecta (ES UN vs TIENE UN)
# =============================================================================

class Usuario:
    def __init__(self, nombre: str):
        self.nombre = nombre


# ❌ INCORRECTO: Pedido NO ES UN Usuario
class PedidoHeredaMal(Usuario):  # ← Incorrecto!
    def __init__(self, nombre: str, total: float):
        super().__init__(nombre)
        self.total = total


# ✅ CORRECTO: Pedido TIENE UN Usuario
class PedidoComposicion:
    def __init__(self, usuario: Usuario, total: float):
        self.usuario = usuario  # ← Composición
        self.total = total


def demo_error_3():
    print("\n--- Error 3: Herencia vs Composición ---")
    print("  ❌ Herencia: 'Pedido ES UN Usuario' - No tiene sentido")
    print("  ✅ Composición: 'Pedido TIENE UN Usuario' - Correcto")


# =============================================================================
# ERROR 4: @property sin @X.setter cuando se necesita
# =============================================================================

class ProductoSoloLectura:
    def __init__(self, precio: float):
        self._precio = precio

    @property
    def precio(self) -> float:
        return self._precio
    # Sin setter - es solo lectura


def demo_error_4():
    print("\n--- Error 4: @property sin setter ---")
    p = ProductoSoloLectura(100)
    print(f"  Precio: {p.precio}")
    try:
        p.precio = 200  # AttributeError!
    except AttributeError as e:
        print(f"  Error al asignar: property 'precio' no tiene setter")
    print("  Solución: Agregar @precio.setter si necesitas modificarlo")


# =============================================================================
# ERROR 5: __eq__ sin __hash__
# =============================================================================

# ❌ INCORRECTO: __eq__ sin __hash__
class UsuarioSinHash:
    def __init__(self, id: int):
        self.id = id

    def __eq__(self, other):
        if not isinstance(other, UsuarioSinHash):
            return False
        return self.id == other.id
    # Falta __hash__!


# ✅ CORRECTO: __eq__ con __hash__
class UsuarioConHash:
    def __init__(self, id: int):
        self.id = id

    def __eq__(self, other):
        if not isinstance(other, UsuarioConHash):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


def demo_error_5():
    print("\n--- Error 5: __eq__ sin __hash__ ---")
    u1 = UsuarioSinHash(1)
    try:
        conjunto = {u1}  # TypeError en Python!
    except TypeError:
        print("  UsuarioSinHash no se puede usar en set/dict key")

    u2 = UsuarioConHash(1)
    conjunto = {u2}  # OK
    print(f"  UsuarioConHash en set: {len(conjunto)} elementos")


# =============================================================================
# ERROR 6: Usar isinstance incorrectamente
# =============================================================================

# ❌ INCORRECTO: Comparar con type()
def procesar_mal(valor):
    if type(valor) == list:  # No detecta subclases
        return "es lista"


# ✅ CORRECTO: Usar isinstance()
def procesar_bien(valor):
    if isinstance(valor, list):  # Detecta list y subclases
        return "es lista o subclase"


def demo_error_6():
    print("\n--- Error 6: type() vs isinstance() ---")
    from collections import UserList
    mi_lista = UserList([1, 2, 3])  # Subclase de list conceptualmente
    print(f"  type() == list: {type([]) == list}")  # True
    print(f"  isinstance(UserList, list): {isinstance(mi_lista, list)}")  # False
    print("  Usar isinstance() para compatibilidad con subclases")


# =============================================================================
# EJECUCIÓN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Errores Comunes en POO para APIs")
    print("=" * 60)

    demo_error_1()
    demo_error_2()
    demo_error_3()
    demo_error_4()
    demo_error_5()
    demo_error_6()

    print("\n✓ Demostración completada")
