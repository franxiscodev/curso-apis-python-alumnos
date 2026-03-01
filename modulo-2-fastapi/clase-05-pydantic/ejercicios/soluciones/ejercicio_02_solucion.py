"""
Solución Ejercicio 02: Modelo Producto con Validadores Custom
=============================================================
"""

import re
from pydantic import BaseModel, Field, field_validator, model_validator


class Producto(BaseModel):
    """Modelo de producto con validadores personalizados."""

    id: int | None = None
    nombre: str = Field(min_length=1, max_length=100)
    precio: float = Field(gt=0)
    precio_oferta: float | None = None
    stock: int = Field(default=0, ge=0)
    sku: str

    @field_validator("sku")
    @classmethod
    def normalizar_sku(cls, v: str) -> str:
        """Normaliza SKU a formato ABC-123."""
        # Convertir a mayúsculas y limpiar
        v = v.upper().strip()

        # Si no tiene guión, intentar agregar uno
        if "-" not in v:
            # Buscar punto donde letras terminan y números empiezan
            match = re.match(r"([A-Z]+)(\d+)", v)
            if match:
                v = f"{match.group(1)}-{match.group(2)}"

        return v

    @field_validator("precio", mode="before")
    @classmethod
    def limpiar_precio(cls, v):
        """Limpia precio de strings como '$1,299.99'."""
        if isinstance(v, str):
            # Remover símbolos de moneda y separadores
            v = v.replace("$", "").replace("€", "").replace(",", "")
            v = v.strip()
        return v

    @model_validator(mode="after")
    def validar_precio_oferta(self) -> "Producto":
        """Valida que precio_oferta < precio."""
        if self.precio_oferta is not None:
            if self.precio_oferta >= self.precio:
                raise ValueError(
                    f"precio_oferta ({self.precio_oferta}) debe ser menor "
                    f"que precio ({self.precio})"
                )
        return self

    @property
    def disponible(self) -> bool:
        """True si hay stock disponible."""
        return self.stock > 0

    @property
    def precio_final(self) -> float:
        """Retorna precio_oferta si existe, sino precio."""
        return self.precio_oferta if self.precio_oferta is not None else self.precio


# =============================================================================
# VERIFICACIÓN
# =============================================================================

if __name__ == "__main__":
    from pydantic import ValidationError

    print("=" * 60)
    print("Solución Ejercicio 02: Modelo Producto")
    print("=" * 60)

    # Creación básica
    print("\n--- Creación básica ---")
    producto = Producto(
        nombre="Laptop Gaming",
        precio=999.99,
        stock=10,
        sku="lap123"
    )
    print(f"Producto: {producto.nombre}")
    print(f"SKU normalizado: {producto.sku}")

    # SKU normalización
    print("\n--- SKU normalización ---")
    skus = ["abc123", "xyz-456", "PROD001", "item-999"]
    for sku in skus:
        p = Producto(nombre="Test", precio=100, sku=sku)
        print(f"  '{sku}' → '{p.sku}'")

    # Precio desde string
    print("\n--- Precio desde string ---")
    precios = ["$99.99", "$1,299.99", "€500", "199.99"]
    for precio in precios:
        p = Producto(nombre="Test", precio=precio, sku="T-001")
        print(f"  '{precio}' → {p.precio}")

    # precio_oferta válido
    print("\n--- precio_oferta válido ---")
    p = Producto(
        nombre="Oferta",
        precio=100,
        precio_oferta=80,
        sku="OFE-001"
    )
    print(f"  precio: {p.precio}, oferta: {p.precio_oferta}")
    print(f"  precio_final: {p.precio_final}")

    # precio_oferta inválido
    print("\n--- precio_oferta inválido ---")
    try:
        Producto(
            nombre="Test",
            precio=100,
            precio_oferta=150,
            sku="T-001"
        )
    except ValidationError as e:
        print(f"  Error: {e.errors()[0]['msg']}")

    # Propiedades
    print("\n--- Propiedades calculadas ---")
    p_con = Producto(nombre="A", precio=100, stock=10, sku="A-001")
    p_sin = Producto(nombre="B", precio=100, stock=0, sku="B-001")
    p_ofe = Producto(nombre="C", precio=100, precio_oferta=75, sku="C-001")

    print(f"  Con stock: disponible={p_con.disponible}")
    print(f"  Sin stock: disponible={p_sin.disponible}")
    print(f"  Sin oferta: precio_final={p_con.precio_final}")
    print(f"  Con oferta: precio_final={p_ofe.precio_final}")

    # Precio negativo
    print("\n--- Validaciones ---")
    try:
        Producto(nombre="Test", precio=-10, sku="T-001")
    except ValidationError as e:
        print(f"  Precio negativo: {e.errors()[0]['msg']}")

    print("\n✓ Solución completada")
