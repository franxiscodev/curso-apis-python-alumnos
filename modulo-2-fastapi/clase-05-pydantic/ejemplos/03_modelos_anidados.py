"""
Ejemplo 03: Modelos Anidados y Herencia
=======================================
Composición de modelos, herencia, y patrones DTO.
"""

from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


# =============================================================================
# MODELOS ANIDADOS (COMPOSICIÓN)
# =============================================================================


class Direccion(BaseModel):
    """Modelo de dirección."""
    calle: str
    numero: str
    ciudad: str
    codigo_postal: str
    pais: str = "España"


class Contacto(BaseModel):
    """Información de contacto."""
    email: EmailStr
    telefono: str | None = None


class Usuario(BaseModel):
    """Usuario con modelos anidados."""
    id: int
    nombre: str
    contacto: Contacto          # Modelo anidado
    direccion: Direccion | None = None  # Opcional


# =============================================================================
# LISTAS DE MODELOS ANIDADOS
# =============================================================================


class ProductoItem(BaseModel):
    """Producto en un pedido."""
    producto_id: int
    nombre: str
    precio: float
    cantidad: int = 1

    @property
    def subtotal(self) -> float:
        return self.precio * self.cantidad


class Pedido(BaseModel):
    """Pedido con lista de productos."""
    id: int
    usuario_id: int
    productos: list[ProductoItem]  # Lista de modelos
    direccion_envio: Direccion
    notas: str | None = None

    @property
    def total(self) -> float:
        return sum(p.subtotal for p in self.productos)


# =============================================================================
# HERENCIA DE MODELOS
# =============================================================================


class ModeloBase(BaseModel):
    """Clase base con campos comunes."""
    id: int | None = None
    creado_en: datetime = Field(default_factory=datetime.now)
    actualizado_en: datetime | None = None


class UsuarioBase(BaseModel):
    """Campos comunes de usuario."""
    nombre: str
    email: EmailStr


class UsuarioCrear(UsuarioBase):
    """DTO para crear usuario (incluye password)."""
    password: str


class UsuarioActualizar(BaseModel):
    """DTO para actualizar (todos opcionales)."""
    nombre: str | None = None
    email: EmailStr | None = None


class UsuarioResponse(UsuarioBase):
    """DTO para respuesta (incluye id, sin password)."""
    id: int
    activo: bool = True


class UsuarioEnDB(UsuarioBase, ModeloBase):
    """Representación en base de datos."""
    hashed_password: str
    activo: bool = True


# =============================================================================
# PATRÓN COMPLETO: ENTIDAD CON DTOs
# =============================================================================


class ProductoBase(BaseModel):
    """Campos comunes del producto."""
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str | None = None
    precio: float = Field(gt=0)
    categoria: str


class ProductoCrear(ProductoBase):
    """Para crear producto."""
    stock: int = Field(default=0, ge=0)


class ProductoActualizar(BaseModel):
    """Para actualizar (todo opcional)."""
    nombre: str | None = None
    descripcion: str | None = None
    precio: float | None = Field(default=None, gt=0)
    categoria: str | None = None
    stock: int | None = Field(default=None, ge=0)


class ProductoResponse(ProductoBase):
    """Para respuesta."""
    id: int
    stock: int
    disponible: bool = True


class ProductoEnDB(ProductoBase, ModeloBase):
    """En base de datos."""
    stock: int = 0
    activo: bool = True


# =============================================================================
# DEMOSTRACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Modelos Anidados y Herencia")
    print("=" * 60)

    # --- Modelos Anidados ---
    print("\n--- Modelos Anidados ---")

    # Pydantic convierte dicts a modelos automáticamente
    usuario = Usuario(
        id=1,
        nombre="Ana García",
        contacto={
            "email": "ana@ejemplo.com",
            "telefono": "+34600000000"
        },
        direccion={
            "calle": "Gran Vía",
            "numero": "123",
            "ciudad": "Madrid",
            "codigo_postal": "28001"
        }
    )

    print(f"Usuario: {usuario.nombre}")
    print(f"Email (anidado): {usuario.contacto.email}")
    print(f"Ciudad (anidado): {usuario.direccion.ciudad}")

    # --- Lista de Modelos ---
    print("\n--- Lista de Modelos Anidados ---")

    pedido = Pedido(
        id=1000,
        usuario_id=1,
        productos=[
            {"producto_id": 1, "nombre": "Laptop", "precio": 999.99, "cantidad": 1},
            {"producto_id": 2, "nombre": "Mouse", "precio": 29.99, "cantidad": 2},
            {"producto_id": 3, "nombre": "Teclado", "precio": 79.99, "cantidad": 1}
        ],
        direccion_envio={
            "calle": "Calle Mayor",
            "numero": "10",
            "ciudad": "Barcelona",
            "codigo_postal": "08001"
        }
    )

    print(f"Pedido #{pedido.id}")
    print(f"Productos: {len(pedido.productos)}")
    for p in pedido.productos:
        print(f"  - {p.nombre}: ${p.precio} x {p.cantidad} = ${p.subtotal}")
    print(f"Total: ${pedido.total:.2f}")

    # --- Herencia: DTOs ---
    print("\n--- Herencia: Patrón DTO ---")

    # Crear usuario (desde request)
    datos_crear = UsuarioCrear(
        nombre="Carlos López",
        email="carlos@ejemplo.com",
        password="MiPassword123"
    )
    print(f"DTO Crear: {datos_crear.model_dump()}")

    # Simular guardado en DB
    usuario_db = UsuarioEnDB(
        id=2,
        nombre=datos_crear.nombre,
        email=datos_crear.email,
        hashed_password="hashed_" + datos_crear.password
    )
    print(f"En DB: id={usuario_db.id}, creado_en={usuario_db.creado_en}")

    # Response (sin password)
    response = UsuarioResponse(
        id=usuario_db.id,
        nombre=usuario_db.nombre,
        email=usuario_db.email,
        activo=usuario_db.activo
    )
    print(f"Response: {response.model_dump()}")

    # --- Actualización parcial ---
    print("\n--- Actualización Parcial ---")

    actualizacion = UsuarioActualizar(nombre="Carlos López García")
    print(f"Solo actualizar: {actualizacion.model_dump(exclude_none=True)}")

    # --- Serialización de modelos anidados ---
    print("\n--- Serialización Completa ---")

    import json
    pedido_json = pedido.model_dump_json(indent=2)
    print(f"Pedido como JSON:\n{pedido_json[:500]}...")

    print("\n✓ Ejemplo completado")
