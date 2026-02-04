"""
Ejemplo 03: Modelando Recursos de API con Tipos
===============================================
TypedDict y dataclasses para definir estructuras de datos de API.

Objetivo: Crear modelos de datos tipados que representen recursos REST.

Nota: Usamos sintaxis moderna Python 3.10+ (str | None en lugar de Optional[str])
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import TypedDict

# =============================================================================
# TYPEDDICT - Diccionarios con estructura definida
# =============================================================================


class UsuarioDict(TypedDict):
    """Estructura de un usuario como diccionario tipado."""
    id: int
    nombre: str
    email: str
    activo: bool


class UsuarioParcialDict(TypedDict, total=False):
    """Usuario con campos opcionales (para actualizaciones parciales PATCH)."""
    nombre: str
    email: str
    activo: bool


def crear_usuario_dict(nombre: str, email: str) -> UsuarioDict:
    """
    Crea un nuevo usuario como TypedDict.

    Args:
        nombre: Nombre completo del usuario
        email: Correo electrónico

    Returns:
        Usuario con ID asignado automáticamente
    """
    return {
        "id": 1,  # En producción vendría de la DB
        "nombre": nombre,
        "email": email,
        "activo": True
    }


# =============================================================================
# DATACLASS - Clases de datos (más potente que TypedDict)
# =============================================================================


@dataclass
class Usuario:
    """
    Modelo de Usuario para API.

    Attributes:
        id: Identificador único (None para usuarios nuevos)
        nombre: Nombre completo
        email: Correo electrónico
        activo: Estado del usuario
        creado_en: Fecha de creación
    """
    nombre: str
    email: str
    id: int | None = None  # Sintaxis moderna para opcional
    activo: bool = True
    creado_en: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict[str, str | int | bool]:
        """Convierte el usuario a diccionario (para respuesta JSON)."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "activo": self.activo,
            "creado_en": self.creado_en.isoformat()
        }


@dataclass
class Producto:
    """Modelo de Producto para API de e-commerce."""
    nombre: str
    precio: float
    id: int | None = None
    stock: int = 0
    categorias: list[str] = field(default_factory=list)

    def aplicar_descuento(self, porcentaje: float) -> float:
        """Calcula precio con descuento sin modificar el original."""
        return self.precio * (1 - porcentaje / 100)


# =============================================================================
# SIMULACIÓN DE OPERACIONES CRUD
# =============================================================================


def listar_usuarios() -> list[Usuario]:
    """Simula GET /usuarios - Lista todos los usuarios."""
    return [
        Usuario(id=1, nombre="Ana García", email="ana@ejemplo.com"),
        Usuario(id=2, nombre="Carlos López", email="carlos@ejemplo.com"),
    ]


def obtener_usuario(user_id: int) -> Usuario | None:
    """Simula GET /usuarios/{id} - Obtiene un usuario por ID."""
    usuarios = {u.id: u for u in listar_usuarios()}
    return usuarios.get(user_id)


def crear_usuario(nombre: str, email: str) -> Usuario:
    """Simula POST /usuarios - Crea un nuevo usuario."""
    return Usuario(id=3, nombre=nombre, email=email)


# =============================================================================
# EJECUCIÓN DE EJEMPLOS
# =============================================================================

if __name__ == "__main__":
    # TypedDict
    usuario_dict = crear_usuario_dict("María", "maria@ejemplo.com")
    print(f"TypedDict: {usuario_dict}")

    # Dataclass - crear usuario
    usuario = Usuario(nombre="Pedro Ruiz", email="pedro@ejemplo.com")
    print(f"\nDataclass: {usuario}")
    print(f"Como dict: {usuario.to_dict()}")

    # Dataclass - producto con métodos
    producto = Producto(
        nombre="Laptop",
        precio=1200.00,
        stock=10,
        categorias=["electrónica", "computación"]
    )
    print(f"\nProducto: {producto}")
    print(f"Precio con 20% descuento: ${producto.aplicar_descuento(20):.2f}")

    # Simular API
    print("\n--- Simulación API ---")
    print(f"GET /usuarios: {[u.nombre for u in listar_usuarios()]}")
    print(f"GET /usuarios/1: {obtener_usuario(1)}")
    print(f"GET /usuarios/99: {obtener_usuario(99)}")
    print(f"POST /usuarios: {crear_usuario('Nuevo', 'nuevo@ejemplo.com')}")
