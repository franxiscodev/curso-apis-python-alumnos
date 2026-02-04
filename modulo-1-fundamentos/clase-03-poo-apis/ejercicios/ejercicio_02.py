"""
Ejercicio 02: Herencia - Usuario, Admin, Cliente
=================================================

Objetivo:
Crear una jerarquía de clases con herencia:
- Usuario (clase base)
- Admin (hereda de Usuario)
- Cliente (hereda de Usuario)

Requisitos:

1. Clase Usuario (base):
   - Atributos: id, nombre, email
   - Método: to_dict()
   - Método: __repr__

2. Clase Admin (hereda de Usuario):
   - Atributo adicional: permisos (lista de strings)
   - Método: tiene_permiso(permiso: str) -> bool
   - Sobrescribir to_dict() para incluir permisos

3. Clase Cliente (hereda de Usuario):
   - Atributo adicional: credito (float, default 0)
   - Método: agregar_credito(monto: float)
   - Propiedad: es_premium (True si credito >= 1000)
   - Sobrescribir to_dict() para incluir credito y es_premium
"""


class Usuario:
    """
    Clase base para usuarios del sistema.

    TODO: Implementar clase base.
    """

    def __init__(self, nombre: str, email: str, id: int | None = None):
        # TODO: Implementar
        pass

    def to_dict(self) -> dict:
        # TODO: Implementar
        pass

    def __repr__(self) -> str:
        # TODO: Implementar
        pass


class Admin(Usuario):
    """
    Usuario administrador con permisos.

    TODO: Implementar herencia de Usuario.
    """

    def __init__(
        self,
        nombre: str,
        email: str,
        permisos: list[str] | None = None,
        id: int | None = None
    ):
        # TODO: Llamar super().__init__() y agregar permisos
        pass

    def tiene_permiso(self, permiso: str) -> bool:
        """Verifica si el admin tiene un permiso específico."""
        # TODO: Implementar
        pass

    def to_dict(self) -> dict:
        # TODO: Extender to_dict() del padre
        pass


class Cliente(Usuario):
    """
    Usuario cliente con crédito.

    TODO: Implementar herencia de Usuario.
    """

    def __init__(
        self,
        nombre: str,
        email: str,
        credito: float = 0,
        id: int | None = None
    ):
        # TODO: Llamar super().__init__() y agregar credito
        pass

    def agregar_credito(self, monto: float) -> None:
        """Agrega crédito al cliente."""
        # TODO: Implementar (validar monto > 0)
        pass

    @property
    def es_premium(self) -> bool:
        """True si el cliente tiene crédito >= 1000."""
        # TODO: Implementar
        pass

    def to_dict(self) -> dict:
        # TODO: Extender to_dict() del padre
        pass


# =============================================================================
# VERIFICACIÓN (No modificar)
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Verificando Ejercicio 02: Herencia")
    print("=" * 60)

    # Test 1: Usuario base
    print("\n--- Test 1: Usuario base ---")
    try:
        u = Usuario(nombre="Ana", email="ana@test.com", id=1)
        print(f"  ✓ Usuario: {u}")
        print(f"  ✓ to_dict: {u.to_dict()}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 2: Admin
    print("\n--- Test 2: Admin ---")
    try:
        admin = Admin(
            nombre="Carlos",
            email="carlos@admin.com",
            permisos=["leer", "escribir", "eliminar"],
            id=2
        )
        print(f"  ✓ Admin: {admin}")
        print(f"  ✓ Tiene 'escribir': {admin.tiene_permiso('escribir')}")
        print(f"  ✓ Tiene 'sudo': {admin.tiene_permiso('sudo')}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 3: Admin hereda de Usuario
    print("\n--- Test 3: Admin hereda de Usuario ---")
    if isinstance(admin, Usuario):
        print("  ✓ Admin es instancia de Usuario")
    else:
        print("  ✗ Admin NO hereda de Usuario")

    # Test 4: Admin to_dict incluye permisos
    print("\n--- Test 4: Admin to_dict ---")
    admin_dict = admin.to_dict()
    if "permisos" in admin_dict and "nombre" in admin_dict:
        print(f"  ✓ Admin to_dict: {admin_dict}")
    else:
        print("  ✗ Admin to_dict incompleto")

    # Test 5: Cliente
    print("\n--- Test 5: Cliente ---")
    try:
        cliente = Cliente(
            nombre="María",
            email="maria@cliente.com",
            credito=500,
            id=3
        )
        print(f"  ✓ Cliente: {cliente}")
        print(f"  ✓ Crédito inicial: ${cliente.credito}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 6: Cliente agregar_credito
    print("\n--- Test 6: Cliente agregar_credito ---")
    cliente.agregar_credito(600)
    if cliente.credito == 1100:
        print(f"  ✓ Crédito después de agregar: ${cliente.credito}")
    else:
        print(f"  ✗ Crédito incorrecto: {cliente.credito}")

    # Test 7: Cliente es_premium
    print("\n--- Test 7: Cliente es_premium ---")
    cliente_normal = Cliente(nombre="Juan", email="juan@test.com", credito=100)
    if cliente.es_premium and not cliente_normal.es_premium:
        print(f"  ✓ María es premium: {cliente.es_premium}")
        print(f"  ✓ Juan NO es premium: {cliente_normal.es_premium}")
    else:
        print("  ✗ es_premium incorrecto")

    # Test 8: Cliente to_dict
    print("\n--- Test 8: Cliente to_dict ---")
    cliente_dict = cliente.to_dict()
    if "credito" in cliente_dict and "es_premium" in cliente_dict:
        print(f"  ✓ Cliente to_dict: {cliente_dict}")
    else:
        print("  ✗ Cliente to_dict incompleto")

    print("\n" + "=" * 60)
    print("Ejecuta las soluciones con:")
    print("  python ejercicios/soluciones/ejercicio_02_solucion.py")
