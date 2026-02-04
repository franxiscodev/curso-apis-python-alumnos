"""
Ejemplo 04: Configuración Avanzada
==================================
model_config, alias, serialización avanzada.
"""

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, AliasChoices, AliasPath


# =============================================================================
# model_config BÁSICO
# =============================================================================


class UsuarioEstricto(BaseModel):
    """Modelo con configuración estricta."""

    model_config = ConfigDict(
        str_strip_whitespace=True,  # Elimina espacios en strings
        extra="forbid",             # Rechaza campos extra
    )

    nombre: str
    email: str


class UsuarioFlexible(BaseModel):
    """Modelo que ignora campos extra."""

    model_config = ConfigDict(
        extra="ignore",  # Ignora campos extra silenciosamente
    )

    nombre: str
    email: str


# =============================================================================
# MODELO INMUTABLE (frozen)
# =============================================================================


class ConfiguracionApp(BaseModel):
    """Configuración inmutable."""

    model_config = ConfigDict(
        frozen=True,  # No se puede modificar después de crear
    )

    database_url: str
    debug: bool = False
    max_connections: int = 10


# =============================================================================
# VALIDACIÓN EN ASIGNACIÓN
# =============================================================================


class Producto(BaseModel):
    """Producto que valida al asignar."""

    model_config = ConfigDict(
        validate_assignment=True,  # Valida al hacer producto.precio = x
    )

    nombre: str
    precio: float = Field(gt=0)


# =============================================================================
# ALIAS: NOMBRES ALTERNATIVOS
# =============================================================================


class UsuarioAPI(BaseModel):
    """Usuario con alias para compatibilidad con API externa."""

    model_config = ConfigDict(
        populate_by_name=True,  # Acepta tanto alias como nombre real
    )

    id: int
    nombre_completo: str = Field(alias="fullName")
    correo: str = Field(alias="email")
    fecha_registro: datetime = Field(alias="createdAt")


class DatosExternos(BaseModel):
    """Modelo con múltiples alias posibles."""

    # AliasChoices permite múltiples nombres para el mismo campo
    usuario_id: int = Field(
        validation_alias=AliasChoices("user_id", "userId", "id")
    )
    nombre: str = Field(
        validation_alias=AliasChoices("name", "nombre", "fullName")
    )


# =============================================================================
# SERIALIZACIÓN PERSONALIZADA
# =============================================================================


class ArticuloBlog(BaseModel):
    """Artículo con serialización personalizada."""

    model_config = ConfigDict(
        populate_by_name=True,
    )

    id: int
    titulo: str = Field(serialization_alias="title")
    contenido: str = Field(serialization_alias="content")
    autor: str = Field(serialization_alias="author")
    publicado_en: datetime = Field(
        serialization_alias="publishedAt",
        default_factory=datetime.now
    )


# =============================================================================
# EJEMPLO COMPLETO: API RESPONSE
# =============================================================================


class APIResponse(BaseModel):
    """Response wrapper estándar."""

    model_config = ConfigDict(
        populate_by_name=True,
    )

    exito: bool = Field(alias="success", default=True)
    datos: dict | list | None = Field(alias="data", default=None)
    error: str | None = None
    timestamp: datetime = Field(default_factory=datetime.now)

    def model_dump_api(self) -> dict:
        """Serializa para API (usa alias, excluye None)."""
        return self.model_dump(
            by_alias=True,
            exclude_none=True
        )


# =============================================================================
# DEMOSTRACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Configuración Avanzada de Pydantic")
    print("=" * 60)

    from pydantic import ValidationError

    # --- extra="forbid" vs extra="ignore" ---
    print("\n--- extra='forbid' vs extra='ignore' ---")

    # Estricto: rechaza campos extra
    print("\nModelo estricto (extra='forbid'):")
    try:
        UsuarioEstricto(
            nombre="Ana",
            email="ana@test.com",
            campo_extra="valor"  # Error!
        )
    except ValidationError as e:
        print(f"  Error: {e.errors()[0]['msg']}")

    # Flexible: ignora campos extra
    print("\nModelo flexible (extra='ignore'):")
    usuario = UsuarioFlexible(
        nombre="Ana",
        email="ana@test.com",
        campo_extra="valor"  # Se ignora
    )
    print(f"  Creado: {usuario.model_dump()}")

    # --- frozen (inmutable) ---
    print("\n--- Modelo Inmutable (frozen) ---")
    config = ConfiguracionApp(
        database_url="postgresql://localhost/db",
        debug=True
    )
    print(f"Config: {config}")

    print("Intentando modificar:")
    try:
        config.debug = False  # Error!
    except ValidationError as e:
        print(f"  Error: Instance is frozen")

    # --- validate_assignment ---
    print("\n--- Validación en Asignación ---")
    producto = Producto(nombre="Laptop", precio=999.99)
    print(f"Precio original: {producto.precio}")

    print("Intentando asignar precio negativo:")
    try:
        producto.precio = -100  # Error por validate_assignment
    except ValidationError as e:
        print(f"  Error: {e.errors()[0]['msg']}")

    producto.precio = 899.99  # OK
    print(f"Nuevo precio válido: {producto.precio}")

    # --- Alias ---
    print("\n--- Alias ---")

    # Datos que vienen de API externa (usan camelCase)
    datos_api = {
        "id": 1,
        "fullName": "Ana García",
        "email": "ana@api.com",
        "createdAt": "2024-01-15T10:30:00"
    }

    usuario_api = UsuarioAPI.model_validate(datos_api)
    print(f"Nombre interno: usuario_api.nombre_completo = '{usuario_api.nombre_completo}'")

    # Serializar con alias (para responder a API)
    print(f"Con alias: {usuario_api.model_dump(by_alias=True)}")

    # Sin alias (nombres Python)
    print(f"Sin alias: {usuario_api.model_dump()}")

    # --- Múltiples alias ---
    print("\n--- Múltiples Alias (AliasChoices) ---")

    # Acepta diferentes formatos
    datos1 = {"user_id": 1, "name": "Ana"}
    datos2 = {"userId": 2, "fullName": "Carlos"}
    datos3 = {"id": 3, "nombre": "María"}

    for datos in [datos1, datos2, datos3]:
        obj = DatosExternos.model_validate(datos)
        print(f"  {datos} → id={obj.usuario_id}, nombre='{obj.nombre}'")

    # --- Serialización personalizada ---
    print("\n--- Serialización para API ---")

    articulo = ArticuloBlog(
        id=1,
        titulo="Introducción a Pydantic",
        contenido="Pydantic es una librería...",
        autor="Ana García"
    )

    print("Serialización normal:")
    print(f"  {articulo.model_dump()}")

    print("\nSerialización para API (by_alias):")
    print(f"  {articulo.model_dump(by_alias=True)}")

    # --- API Response ---
    print("\n--- API Response Wrapper ---")

    response_exito = APIResponse(
        datos={"usuario": "Ana", "rol": "admin"}
    )
    print(f"Éxito: {response_exito.model_dump_api()}")

    response_error = APIResponse(
        exito=False,
        error="Usuario no encontrado"
    )
    print(f"Error: {response_error.model_dump_api()}")

    print("\n✓ Ejemplo completado")
