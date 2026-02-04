"""
Errores Comunes en Pydantic
===========================
Errores frecuentes y cómo evitarlos.
"""

from pydantic import BaseModel, Field, field_validator, ValidationError


# =============================================================================
# ERROR 1: Olvidar @classmethod en @field_validator
# =============================================================================

class UsuarioMal1(BaseModel):
    nombre: str

    # ❌ INCORRECTO: Falta @classmethod
    # @field_validator("nombre")
    # def validar_nombre(cls, v):  # Esto fallará
    #     return v.strip()


class UsuarioBien1(BaseModel):
    nombre: str

    # ✅ CORRECTO: Con @classmethod
    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        return v.strip()


# =============================================================================
# ERROR 2: Usar .dict() en lugar de .model_dump() (Pydantic v2)
# =============================================================================

class Usuario(BaseModel):
    nombre: str


def demo_error_2():
    """En Pydantic v2, usar model_dump() no dict()."""
    usuario = Usuario(nombre="Ana")

    # ❌ Pydantic v1 (deprecated en v2)
    # data = usuario.dict()

    # ✅ Pydantic v2
    data = usuario.model_dump()
    print(f"  Correcto: usuario.model_dump() → {data}")


# =============================================================================
# ERROR 3: Mutable default en Field
# =============================================================================

# ❌ INCORRECTO: Lista mutable como default
# class PedidoMal(BaseModel):
#     productos: list = []  # ¡Peligroso! Compartido entre instancias


# ✅ CORRECTO: Usar default_factory
class PedidoBien(BaseModel):
    productos: list[str] = Field(default_factory=list)


# =============================================================================
# ERROR 4: Confundir validation_alias y serialization_alias
# =============================================================================

class ProductoAliases(BaseModel):
    # validation_alias: para ENTRADA (deserialización)
    # serialization_alias: para SALIDA (serialización)

    nombre: str = Field(
        validation_alias="name",       # Acepta "name" en input
        serialization_alias="title"    # Serializa como "title"
    )


def demo_error_4():
    """Diferencia entre validation_alias y serialization_alias."""
    # Input usa validation_alias
    producto = ProductoAliases.model_validate({"name": "Laptop"})
    print(f"  Entrada con 'name': {producto.nombre}")

    # Output usa serialization_alias
    print(f"  Salida con alias: {producto.model_dump(by_alias=True)}")


# =============================================================================
# ERROR 5: No manejar ValidationError
# =============================================================================

class Producto(BaseModel):
    precio: float = Field(gt=0)


def demo_error_5():
    """Siempre manejar ValidationError en código de producción."""
    datos = {"precio": -10}

    # ❌ Sin manejo de error
    # producto = Producto(**datos)  # Crash!

    # ✅ Con manejo de error
    try:
        producto = Producto(**datos)
    except ValidationError as e:
        print("  ValidationError capturado:")
        for error in e.errors():
            print(f"    - {error['loc'][0]}: {error['msg']}")


# =============================================================================
# ERROR 6: Esperar que Optional valide None automáticamente
# =============================================================================

class ConfigMal(BaseModel):
    # ❌ Esto NO permite None, solo hace el campo opcional con default None
    # valor: str = None  # Error si se pasa None explícitamente


class ConfigBien(BaseModel):
    # ✅ Usa str | None para permitir None
    valor: str | None = None


def demo_error_6():
    """Diferencia entre default None y tipo Optional."""
    # Con str | None, acepta None explícito
    config = ConfigBien(valor=None)
    print(f"  valor=None permitido: {config.valor}")


# =============================================================================
# ERROR 7: Usar model_validate con objeto, no dict
# =============================================================================

class UsuarioInput(BaseModel):
    nombre: str


class UsuarioOutput(BaseModel):
    nombre: str
    id: int = 1


def demo_error_7():
    """model_validate espera dict, no objeto Pydantic."""
    input_data = UsuarioInput(nombre="Ana")

    # ❌ Esto puede causar problemas
    # output = UsuarioOutput.model_validate(input_data)

    # ✅ Convertir a dict primero
    output = UsuarioOutput.model_validate(input_data.model_dump())
    print(f"  Conversión correcta: {output}")

    # ✅ O usar model_validate con from_attributes=True
    # (requiere configurar model_config)


# =============================================================================
# ERROR 8: Olvidar mode en @field_validator
# =============================================================================

class PrecioProducto(BaseModel):
    precio: float

    # mode="before": se ejecuta ANTES de la conversión de tipo
    # mode="after": se ejecuta DESPUÉS (default)

    @field_validator("precio", mode="before")
    @classmethod
    def limpiar_precio(cls, v):
        """Limpia strings como '$100' antes de convertir a float."""
        if isinstance(v, str):
            v = v.replace("$", "").replace(",", "")
        return v


def demo_error_8():
    """mode='before' permite transformar antes de validar tipo."""
    producto = PrecioProducto(precio="$1,299.99")
    print(f"  Precio limpio: {producto.precio}")


# =============================================================================
# DEMOSTRACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Errores Comunes en Pydantic")
    print("=" * 60)

    print("\n--- Error 1: @classmethod en @field_validator ---")
    print("  Siempre usar @classmethod después de @field_validator")

    print("\n--- Error 2: .dict() vs .model_dump() ---")
    demo_error_2()

    print("\n--- Error 3: Mutable defaults ---")
    p1 = PedidoBien()
    p2 = PedidoBien()
    p1.productos.append("Laptop")
    print(f"  p1.productos: {p1.productos}")
    print(f"  p2.productos: {p2.productos}")  # Vacío, no compartido

    print("\n--- Error 4: validation_alias vs serialization_alias ---")
    demo_error_4()

    print("\n--- Error 5: Manejar ValidationError ---")
    demo_error_5()

    print("\n--- Error 6: str | None vs default None ---")
    demo_error_6()

    print("\n--- Error 7: model_validate con dict ---")
    demo_error_7()

    print("\n--- Error 8: mode='before' en @field_validator ---")
    demo_error_8()

    print("\n--- Resumen ---")
    print("""
    1. @field_validator necesita @classmethod
    2. Usar model_dump() no dict() (Pydantic v2)
    3. Usar default_factory para mutables
    4. validation_alias ≠ serialization_alias
    5. Siempre manejar ValidationError
    6. str | None para permitir None
    7. model_validate espera dict
    8. mode='before' para transformar antes de validar tipo
    """)

    print("✓ Demostración completada")
