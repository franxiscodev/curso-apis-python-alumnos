"""
Solución Ejercicio 02: Herencia - Usuario, Admin, Cliente
==========================================================
"""


class Usuario:
    """Clase base para usuarios del sistema."""

    def __init__(self, nombre: str, email: str, id: int | None = None):
        self.id = id
        self.nombre = nombre
        self.email = email

    def to_dict(self) -> dict:
        """Serializa a diccionario."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email
        }

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, nombre='{self.nombre}')"


class Admin(Usuario):
    """Usuario administrador con permisos."""

    def __init__(
        self,
        nombre: str,
        email: str,
        permisos: list[str] | None = None,
        id: int | None = None
    ):
        super().__init__(nombre, email, id)  # Llamar al padre
        self.permisos = permisos if permisos is not None else []

    def tiene_permiso(self, permiso: str) -> bool:
        """Verifica si el admin tiene un permiso específico."""
        return permiso in self.permisos

    def agregar_permiso(self, permiso: str) -> None:
        """Agrega un permiso si no existe."""
        if permiso not in self.permisos:
            self.permisos.append(permiso)

    def to_dict(self) -> dict:
        """Extiende to_dict() del padre con permisos."""
        base = super().to_dict()
        base["permisos"] = self.permisos
        base["tipo"] = "admin"
        return base


class Cliente(Usuario):
    """Usuario cliente con crédito."""

    def __init__(
        self,
        nombre: str,
        email: str,
        credito: float = 0,
        id: int | None = None
    ):
        super().__init__(nombre, email, id)
        self._credito = credito

    @property
    def credito(self) -> float:
        """Crédito disponible del cliente."""
        return self._credito

    def agregar_credito(self, monto: float) -> None:
        """Agrega crédito al cliente."""
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        self._credito += monto

    def usar_credito(self, monto: float) -> bool:
        """Usa crédito si hay suficiente. Retorna True si tuvo éxito."""
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        if monto > self._credito:
            return False
        self._credito -= monto
        return True

    @property
    def es_premium(self) -> bool:
        """True si el cliente tiene crédito >= 1000."""
        return self._credito >= 1000

    def to_dict(self) -> dict:
        """Extiende to_dict() del padre con crédito."""
        base = super().to_dict()
        base["credito"] = self.credito
        base["es_premium"] = self.es_premium
        base["tipo"] = "cliente"
        return base


# =============================================================================
# VERIFICACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Solución Ejercicio 02: Herencia")
    print("=" * 60)

    # Test 1: Usuario base
    print("\n--- Test 1: Usuario base ---")
    u = Usuario(nombre="Ana", email="ana@test.com", id=1)
    print(f"  ✓ Usuario: {u}")
    print(f"  ✓ to_dict: {u.to_dict()}")

    # Test 2: Admin
    print("\n--- Test 2: Admin ---")
    admin = Admin(
        nombre="Carlos",
        email="carlos@admin.com",
        permisos=["leer", "escribir", "eliminar"],
        id=2
    )
    print(f"  ✓ Admin: {admin}")
    print(f"  ✓ Tiene 'escribir': {admin.tiene_permiso('escribir')}")
    print(f"  ✓ Tiene 'sudo': {admin.tiene_permiso('sudo')}")

    # Test 3: Admin hereda de Usuario
    print("\n--- Test 3: Herencia ---")
    print(f"  ✓ Admin es Usuario: {isinstance(admin, Usuario)}")

    # Test 4: Admin to_dict
    print("\n--- Test 4: Admin to_dict ---")
    print(f"  ✓ {admin.to_dict()}")

    # Test 5: Cliente
    print("\n--- Test 5: Cliente ---")
    cliente = Cliente(
        nombre="María",
        email="maria@cliente.com",
        credito=500,
        id=3
    )
    print(f"  ✓ Cliente: {cliente}")
    print(f"  ✓ Crédito: ${cliente.credito}")

    # Test 6: Cliente agregar_credito
    print("\n--- Test 6: agregar_credito ---")
    cliente.agregar_credito(600)
    print(f"  ✓ Crédito después de agregar 600: ${cliente.credito}")

    # Test 7: Cliente es_premium
    print("\n--- Test 7: es_premium ---")
    cliente_normal = Cliente(nombre="Juan", email="juan@test.com", credito=100)
    print(f"  ✓ María es premium (${cliente.credito}): {cliente.es_premium}")
    print(f"  ✓ Juan NO es premium (${cliente_normal.credito}): {cliente_normal.es_premium}")

    # Test 8: Cliente to_dict
    print("\n--- Test 8: Cliente to_dict ---")
    print(f"  ✓ {cliente.to_dict()}")

    # Test 9: Polimorfismo
    print("\n--- Test 9: Polimorfismo ---")
    usuarios: list[Usuario] = [u, admin, cliente]
    print("  Procesando lista de usuarios:")
    for usuario in usuarios:
        print(f"    - {usuario.__class__.__name__}: {usuario.nombre}")

    print("\n✓ Solución completada")
