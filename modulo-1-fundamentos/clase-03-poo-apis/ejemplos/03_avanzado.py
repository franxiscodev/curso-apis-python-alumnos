"""
Ejemplo 03: Patrones para APIs
==============================
Repository, DTO, y Factory patterns.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime


# =============================================================================
# MODELO DE DOMINIO
# =============================================================================


@dataclass
class Usuario:
    """Entidad de dominio Usuario."""
    nombre: str
    email: str
    id: int | None = None
    creado_en: datetime = field(default_factory=datetime.now)


# =============================================================================
# PATRÓN DTO (DATA TRANSFER OBJECT)
# =============================================================================


@dataclass
class UsuarioCrearDTO:
    """DTO para crear usuario (request body)."""
    nombre: str
    email: str


@dataclass
class UsuarioActualizarDTO:
    """DTO para actualizar usuario (campos opcionales)."""
    nombre: str | None = None
    email: str | None = None


@dataclass
class UsuarioResponseDTO:
    """DTO para respuesta (incluye campos calculados/internos)."""
    id: int
    nombre: str
    email: str
    creado_en: str

    @classmethod
    def from_entidad(cls, usuario: Usuario) -> "UsuarioResponseDTO":
        """Convierte entidad a DTO de respuesta."""
        return cls(
            id=usuario.id,  # type: ignore
            nombre=usuario.nombre,
            email=usuario.email,
            creado_en=usuario.creado_en.isoformat()
        )


# =============================================================================
# PATRÓN REPOSITORY
# =============================================================================


class UsuarioRepository(ABC):
    """Interfaz abstracta para acceso a datos de Usuario."""

    @abstractmethod
    def obtener(self, id: int) -> Usuario | None:
        """Obtiene usuario por ID."""
        pass

    @abstractmethod
    def obtener_por_email(self, email: str) -> Usuario | None:
        """Obtiene usuario por email."""
        pass

    @abstractmethod
    def guardar(self, usuario: Usuario) -> Usuario:
        """Guarda usuario (crea o actualiza)."""
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina usuario por ID."""
        pass

    @abstractmethod
    def listar(self, limite: int = 100) -> list[Usuario]:
        """Lista usuarios con límite."""
        pass


class UsuarioMemoryRepository(UsuarioRepository):
    """Implementación en memoria (para testing/desarrollo)."""

    def __init__(self):
        self._usuarios: dict[int, Usuario] = {}
        self._next_id = 1

    def obtener(self, id: int) -> Usuario | None:
        return self._usuarios.get(id)

    def obtener_por_email(self, email: str) -> Usuario | None:
        for usuario in self._usuarios.values():
            if usuario.email == email:
                return usuario
        return None

    def guardar(self, usuario: Usuario) -> Usuario:
        if usuario.id is None:
            usuario.id = self._next_id
            self._next_id += 1
        self._usuarios[usuario.id] = usuario
        return usuario

    def eliminar(self, id: int) -> bool:
        if id in self._usuarios:
            del self._usuarios[id]
            return True
        return False

    def listar(self, limite: int = 100) -> list[Usuario]:
        return list(self._usuarios.values())[:limite]


# =============================================================================
# PATRÓN FACTORY
# =============================================================================


class UsuarioFactory:
    """Factory para crear usuarios con lógica de negocio."""

    @staticmethod
    def crear_desde_dto(dto: UsuarioCrearDTO) -> Usuario:
        """Crea usuario desde DTO de creación."""
        return Usuario(nombre=dto.nombre, email=dto.email)

    @staticmethod
    def crear_admin(nombre: str, email: str) -> Usuario:
        """Crea usuario con prefijo de admin."""
        return Usuario(nombre=f"[ADMIN] {nombre}", email=email)

    @staticmethod
    def crear_anonimo() -> Usuario:
        """Crea usuario anónimo."""
        return Usuario(nombre="Anónimo", email="anonimo@sistema.local")


# =============================================================================
# SERVICIO (CAPA DE NEGOCIO)
# =============================================================================


class UsuarioService:
    """Servicio que orquesta lógica de negocio."""

    def __init__(self, repository: UsuarioRepository):
        self._repo = repository

    def crear_usuario(self, dto: UsuarioCrearDTO) -> UsuarioResponseDTO:
        """Crea usuario y retorna DTO de respuesta."""
        # Validar email único
        if self._repo.obtener_por_email(dto.email):
            raise ValueError(f"Email ya existe: {dto.email}")

        # Crear y guardar
        usuario = UsuarioFactory.crear_desde_dto(dto)
        usuario = self._repo.guardar(usuario)

        return UsuarioResponseDTO.from_entidad(usuario)

    def obtener_usuario(self, id: int) -> UsuarioResponseDTO | None:
        """Obtiene usuario por ID."""
        usuario = self._repo.obtener(id)
        if usuario:
            return UsuarioResponseDTO.from_entidad(usuario)
        return None

    def listar_usuarios(self, limite: int = 100) -> list[UsuarioResponseDTO]:
        """Lista usuarios como DTOs de respuesta."""
        usuarios = self._repo.listar(limite)
        return [UsuarioResponseDTO.from_entidad(u) for u in usuarios]


# =============================================================================
# DEMOSTRACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Demostración: Patrones para APIs")
    print("=" * 60)

    # --- Setup ---
    repo = UsuarioMemoryRepository()
    service = UsuarioService(repo)

    # --- DTOs ---
    print("\n--- Patrón DTO ---")
    dto_crear = UsuarioCrearDTO(nombre="Ana García", email="ana@ejemplo.com")
    print(f"DTO para crear: {dto_crear}")

    # --- Service + Repository ---
    print("\n--- Service + Repository ---")

    # Crear usuarios
    usuario1 = service.crear_usuario(dto_crear)
    print(f"Usuario creado: {usuario1}")

    usuario2 = service.crear_usuario(
        UsuarioCrearDTO(nombre="Carlos López", email="carlos@ejemplo.com")
    )
    print(f"Usuario creado: {usuario2}")

    # Listar
    print("\n--- Listar usuarios ---")
    for u in service.listar_usuarios():
        print(f"  {u.id}: {u.nombre} ({u.email})")

    # Obtener por ID
    print("\n--- Obtener por ID ---")
    encontrado = service.obtener_usuario(1)
    print(f"Usuario 1: {encontrado}")

    no_encontrado = service.obtener_usuario(999)
    print(f"Usuario 999: {no_encontrado}")

    # --- Validación de email único ---
    print("\n--- Validación en Service ---")
    try:
        service.crear_usuario(
            UsuarioCrearDTO(nombre="Otro", email="ana@ejemplo.com")
        )
    except ValueError as e:
        print(f"Error capturado: {e}")

    # --- Factory ---
    print("\n--- Patrón Factory ---")
    admin = UsuarioFactory.crear_admin("Super Admin", "admin@sistema.com")
    print(f"Admin: {admin.nombre}")

    anonimo = UsuarioFactory.crear_anonimo()
    print(f"Anónimo: {anonimo.nombre}, {anonimo.email}")

    print("\n✓ Ejemplo completado")
