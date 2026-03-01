"""
Solución Ejercicio 01: Modelo Usuario con Validación
=====================================================
"""

from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict


class Usuario(BaseModel):
    """Modelo de usuario con validación completa."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    id: int | None = None
    nombre: str = Field(min_length=1, max_length=50)
    email: EmailStr
    edad: int = Field(ge=18, le=120)
    activo: bool = True

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        """Valida y normaliza el nombre."""
        # Strip ya se hace por str_strip_whitespace
        if not v or not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.title()

    @field_validator("edad")
    @classmethod
    def validar_edad(cls, v: int) -> int:
        """Validación adicional de edad (ya cubierta por Field, pero explícita)."""
        if v < 18:
            raise ValueError("Debe ser mayor de 18 años")
        if v > 120:
            raise ValueError("Edad no puede superar 120 años")
        return v


# =============================================================================
# VERIFICACIÓN
# =============================================================================

if __name__ == "__main__":
    from pydantic import ValidationError

    print("=" * 60)
    print("Solución Ejercicio 01: Modelo Usuario")
    print("=" * 60)

    # Creación exitosa
    print("\n--- Creación exitosa ---")
    usuario = Usuario(
        nombre="  ana garcía  ",
        email="ana@ejemplo.com",
        edad=28
    )
    print(f"Usuario: {usuario}")
    print(f"Nombre normalizado: '{usuario.nombre}'")
    print(f"id (default): {usuario.id}")
    print(f"activo (default): {usuario.activo}")

    # Serialización
    print("\n--- Serialización ---")
    print(f"model_dump(): {usuario.model_dump()}")

    # Validaciones
    print("\n--- Validaciones ---")

    # Email inválido
    try:
        Usuario(nombre="Test", email="invalido", edad=25)
    except ValidationError as e:
        print(f"Email inválido: {e.errors()[0]['msg']}")

    # Edad fuera de rango
    try:
        Usuario(nombre="Test", email="t@t.com", edad=15)
    except ValidationError as e:
        print(f"Edad < 18: {e.errors()[0]['msg']}")

    # Campo extra
    try:
        Usuario(nombre="Test", email="t@t.com", edad=25, extra="valor")
    except ValidationError as e:
        print(f"Campo extra: {e.errors()[0]['msg']}")

    # Nombre vacío
    try:
        Usuario(nombre="   ", email="t@t.com", edad=25)
    except ValidationError as e:
        print(f"Nombre vacío: {e.errors()[0]['msg']}")

    print("\n✓ Solución completada")
