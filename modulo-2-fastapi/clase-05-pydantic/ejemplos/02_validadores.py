"""
Ejemplo 02: Validadores Personalizados
======================================
@field_validator, @model_validator, y validación avanzada.
"""

from pydantic import BaseModel, Field, field_validator, model_validator, ValidationError
from datetime import date

# =============================================================================
# @field_validator BÁSICO
# =============================================================================


class Usuario(BaseModel):
    """Usuario con validadores de campo."""
    nombre: str
    email: str
    edad: int

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, v: str) -> str:
        """Valida que el nombre no esté vacío y lo normaliza."""
        if not v or not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip().title()  # Capitaliza

    @field_validator("email")
    @classmethod
    def email_valido(cls, v: str) -> str:
        """Validación básica de email."""
        if "@" not in v:
            raise ValueError("Email debe contener @")
        if "." not in v.split("@")[1]:
            raise ValueError("Email debe tener dominio válido")
        return v.lower()

    @field_validator("edad")
    @classmethod
    def edad_razonable(cls, v: int) -> int:
        """Valida rango de edad."""
        if v < 0:
            raise ValueError("La edad no puede ser negativa")
        if v > 150:
            raise ValueError("La edad no puede ser mayor a 150")
        return v


# =============================================================================
# @field_validator con mode="before"
# =============================================================================


class Producto(BaseModel):
    """Producto con transformación antes de validación."""
    nombre: str
    precio: float
    codigo: str

    @field_validator("precio", mode="before")
    @classmethod
    def limpiar_precio(cls, v):
        """Limpia precio antes de validar tipo."""
        if isinstance(v, str):
            # Remover símbolos de moneda
            v = v.replace("$", "").replace("€", "").replace(",", "")
        return v

    @field_validator("codigo", mode="before")
    @classmethod
    def normalizar_codigo(cls, v):
        """Normaliza código a mayúsculas sin espacios."""
        if isinstance(v, str):
            return v.upper().strip().replace(" ", "-")
        return v


# =============================================================================
# @model_validator
# =============================================================================


class RangoPrecio(BaseModel):
    """Rango de precios con validación cruzada."""
    minimo: float = Field(ge=0)
    maximo: float = Field(ge=0)

    @model_validator(mode="after")
    def validar_rango(self) -> "RangoPrecio":
        """Valida que mínimo <= máximo."""
        if self.minimo > self.maximo:
            raise ValueError(
                f"El precio mínimo ({self.minimo}) no puede ser "
                f"mayor al máximo ({self.maximo})"
            )
        return self


class Reservacion(BaseModel):
    """Reservación con validación de fechas."""

    huesped: str
    fecha_entrada: date
    fecha_salida: date
    habitaciones: int = Field(ge=1)

    @model_validator(mode="after")
    def validar_fechas(self) -> "Reservacion":
        """Valida que las fechas sean coherentes."""
        if self.fecha_salida <= self.fecha_entrada:
            raise ValueError(
                "La fecha de salida debe ser posterior a la entrada")
        return self


# =============================================================================
# VALIDACIÓN CON MÚLTIPLES CAMPOS
# =============================================================================


class CuentaBancaria(BaseModel):
    """Cuenta con validación de password."""
    email: str
    password: str
    confirmar_password: str

    @field_validator("password")
    @classmethod
    def password_fuerte(cls, v: str) -> str:
        """Valida fortaleza de password."""
        if len(v) < 8:
            raise ValueError("Password debe tener al menos 8 caracteres")
        if not any(c.isupper() for c in v):
            raise ValueError("Password debe tener al menos una mayúscula")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password debe tener al menos un número")
        return v

    @model_validator(mode="after")
    def passwords_coinciden(self) -> "CuentaBancaria":
        """Valida que los passwords coincidan."""
        if self.password != self.confirmar_password:
            raise ValueError("Los passwords no coinciden")
        return self


# =============================================================================
# DEMOSTRACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Validadores Personalizados")
    print("=" * 60)

    # --- @field_validator básico ---
    print("\n--- @field_validator básico ---")
    usuario = Usuario(
        nombre="  ana garcía  ",  # Se normaliza
        email="ANA@EJEMPLO.COM",  # Se convierte a minúsculas
        edad=28
    )
    print(f"Nombre normalizado: '{usuario.nombre}'")
    print(f"Email normalizado: '{usuario.email}'")

    # Error de validación
    print("\nValidación de edad:")
    try:
        Usuario(nombre="Test", email="test@test.com", edad=-5)
    except ValidationError as e:
        print(f"  Error: {e.errors()[0]['msg']}")

    # --- mode="before" ---
    print("\n--- @field_validator mode='before' ---")
    producto = Producto(
        nombre="Laptop",
        precio="$1,299.99",  # String con símbolos
        codigo="abc 123"     # Se normaliza a "ABC-123"
    )
    print(f"Precio limpio: {producto.precio}")
    print(f"Código normalizado: {producto.codigo}")

    # --- @model_validator ---
    print("\n--- @model_validator ---")

    # Rango válido
    rango = RangoPrecio(minimo=10, maximo=100)
    print(f"Rango válido: {rango}")

    # Rango inválido
    print("\nRango inválido:")
    try:
        RangoPrecio(minimo=100, maximo=10)
    except ValidationError as e:
        print(f"  Error: {e.errors()[0]['msg']}")

    # --- Reservación ---
    print("\n--- Validación de fechas ---")

    reserva = Reservacion(
        huesped="Ana García",
        fecha_entrada=date(2024, 6, 1),
        fecha_salida=date(2024, 6, 5),
        habitaciones=2
    )
    print(f"Reservación válida: {reserva.huesped}")

    print("\nFechas inválidas:")
    try:
        Reservacion(
            huesped="Test",
            fecha_entrada=date(2024, 6, 10),
            fecha_salida=date(2024, 6, 5)
        )
    except ValidationError as e:
        print(f"  Error: {e.errors()[0]['msg']}")

    # --- Password ---
    print("\n--- Validación de password ---")

    # Password válido
    cuenta = CuentaBancaria(
        email="test@test.com",
        password="MiPassword123",
        confirmar_password="MiPassword123"
    )
    print("Cuenta creada correctamente")

    # Password no coincide
    print("\nPasswords no coinciden:")
    try:
        CuentaBancaria(
            email="test@test.com",
            password="MiPassword123",
            confirmar_password="OtroPassword123"
        )
    except ValidationError as e:
        print(f"  Error: {e.errors()[0]['msg']}")

    # Password débil
    print("\nPassword débil:")
    try:
        CuentaBancaria(
            email="test@test.com",
            password="weak",
            confirmar_password="weak"
        )
    except ValidationError as e:
        print(f"  Error: {e.errors()[0]['msg']}")

    print("\n✓ Ejemplo completado")
