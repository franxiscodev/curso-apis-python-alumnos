"""
Ejemplo 01: Pydantic Básico
===========================
BaseModel, tipos de datos, Field, y serialización.
"""

from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


# =============================================================================
# MODELO BÁSICO
# =============================================================================


class Usuario(BaseModel):
    """Modelo básico de usuario."""
    nombre: str
    email: str
    edad: int
    activo: bool = True  # Valor por defecto


# =============================================================================
# TIPOS ESPECIALES DE PYDANTIC
# =============================================================================


class UsuarioCompleto(BaseModel):
    """Usuario con tipos especiales de Pydantic."""
    nombre: str
    email: EmailStr          # Valida formato de email
    edad: int | None = None  # Opcional (puede ser None)
    creado_en: datetime = Field(default_factory=datetime.now)


# =============================================================================
# FIELD: CONFIGURACIÓN DE CAMPOS
# =============================================================================


class Producto(BaseModel):
    """Producto con validaciones usando Field."""
    id: int
    nombre: str = Field(min_length=1, max_length=100)
    precio: float = Field(gt=0, description="Precio debe ser mayor a 0")
    stock: int = Field(default=0, ge=0, description="Stock no negativo")
    descripcion: str | None = Field(default=None, max_length=500)


# =============================================================================
# SERIALIZACIÓN
# =============================================================================


def demo_serializacion():
    """Demuestra serialización con model_dump()."""
    print("\n--- Serialización ---")

    usuario = UsuarioCompleto(
        nombre="Ana García",
        email="ana@ejemplo.com",
        edad=28
    )

    # model_dump() - a diccionario
    data = usuario.model_dump()
    print(f"model_dump(): {data}")

    # Excluir campos
    data_sin_email = usuario.model_dump(exclude={"email"})
    print(f"exclude email: {data_sin_email}")

    # Solo algunos campos
    data_parcial = usuario.model_dump(include={"nombre", "email"})
    print(f"include nombre,email: {data_parcial}")

    # Excluir None
    usuario_sin_edad = UsuarioCompleto(nombre="Test", email="test@test.com")
    data_sin_none = usuario_sin_edad.model_dump(exclude_none=True)
    print(f"exclude_none: {data_sin_none}")

    # A JSON string
    json_str = usuario.model_dump_json(indent=2)
    print(f"model_dump_json():\n{json_str}")


# =============================================================================
# DESERIALIZACIÓN
# =============================================================================


def demo_deserializacion():
    """Demuestra deserialización con model_validate()."""
    print("\n--- Deserialización ---")

    # Desde diccionario
    data = {
        "nombre": "Carlos López",
        "email": "carlos@ejemplo.com",
        "edad": 35
    }
    usuario = UsuarioCompleto.model_validate(data)
    print(f"Desde dict: {usuario}")

    # Desde JSON string
    json_str = '{"nombre": "María", "email": "maria@test.com"}'
    usuario2 = UsuarioCompleto.model_validate_json(json_str)
    print(f"Desde JSON: {usuario2}")


# =============================================================================
# VALIDACIÓN AUTOMÁTICA
# =============================================================================


def demo_validacion():
    """Demuestra la validación automática."""
    print("\n--- Validación Automática ---")

    from pydantic import ValidationError

    # Tipo incorrecto - Pydantic intenta convertir
    usuario = Usuario(nombre="Ana", email="ana@test.com", edad="25")
    print(f"edad='25' convertido a: {usuario.edad} (tipo: {type(usuario.edad).__name__})")

    # Error de validación
    print("\nIntentando crear Producto con precio negativo...")
    try:
        producto = Producto(id=1, nombre="Test", precio=-10)
    except ValidationError as e:
        print(f"ValidationError capturado:")
        for error in e.errors():
            print(f"  - Campo: {error['loc']}")
            print(f"    Mensaje: {error['msg']}")

    # Email inválido
    print("\nIntentando crear Usuario con email inválido...")
    try:
        usuario = UsuarioCompleto(nombre="Test", email="no-es-email")
    except ValidationError as e:
        print(f"ValidationError: {e.errors()[0]['msg']}")


# =============================================================================
# DEMOSTRACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Pydantic Básico")
    print("=" * 60)

    # Crear modelo básico
    print("\n--- Modelo Básico ---")
    usuario = Usuario(
        nombre="Ana García",
        email="ana@ejemplo.com",
        edad=28
    )
    print(f"Usuario: {usuario}")
    print(f"Nombre: {usuario.nombre}")
    print(f"Activo (default): {usuario.activo}")

    # Modelo con tipos especiales
    print("\n--- Tipos Especiales ---")
    usuario_completo = UsuarioCompleto(
        nombre="Carlos",
        email="carlos@ejemplo.com"
    )
    print(f"Usuario: {usuario_completo}")
    print(f"creado_en (auto): {usuario_completo.creado_en}")

    # Field con restricciones
    print("\n--- Field con Restricciones ---")
    producto = Producto(
        id=1,
        nombre="Laptop Gaming",
        precio=1299.99,
        stock=10
    )
    print(f"Producto: {producto}")

    # Serialización y deserialización
    demo_serializacion()
    demo_deserializacion()
    demo_validacion()

    print("\n✓ Ejemplo completado")
