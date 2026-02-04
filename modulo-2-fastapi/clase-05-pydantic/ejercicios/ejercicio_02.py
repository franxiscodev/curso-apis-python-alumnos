"""
Ejercicio 02: Modelo Producto con Validadores Custom
====================================================

Objetivo:
Crear un modelo Pydantic para Producto con validadores personalizados.

Requisitos:
1. Campos:
   - id: int | None
   - nombre: str (1-100 caracteres)
   - precio: float (> 0)
   - precio_oferta: float | None (opcional)
   - stock: int (>= 0, default 0)
   - sku: str (código de producto)

2. Validadores:
   - @field_validator para sku:
     * Convertir a mayúsculas
     * Formato: letras-números (ej: "ABC-123")
     * Si no tiene guión, agregar uno (ej: "ABC123" → "ABC-123")

   - @field_validator para precio (mode="before"):
     * Aceptar strings como "$99.99" o "99,99"
     * Limpiar y convertir a float

   - @model_validator para precio_oferta:
     * Si existe, debe ser menor que precio
     * Raise ValueError si precio_oferta >= precio

3. Propiedad calculada:
   - disponible: bool (True si stock > 0)
   - precio_final: float (precio_oferta si existe, sino precio)
"""

from pydantic import BaseModel, Field, field_validator, model_validator


# =============================================================================
# TU CÓDIGO AQUÍ
# =============================================================================


class Producto(BaseModel):
    """
    Modelo de producto con validadores personalizados.

    TODO: Implementar según los requisitos.
    """
    pass


# =============================================================================
# VERIFICACIÓN (No modificar)
# =============================================================================

if __name__ == "__main__":
    from pydantic import ValidationError

    print("=" * 60)
    print("Verificando Ejercicio 02: Modelo Producto")
    print("=" * 60)

    # Test 1: Creación básica
    print("\n--- Test 1: Creación básica ---")
    try:
        producto = Producto(
            nombre="Laptop Gaming",
            precio=999.99,
            sku="lap123"
        )
        print(f"  ✓ Producto creado: {producto.nombre}")
        print(f"  ✓ SKU normalizado: {producto.sku}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 2: SKU normalización
    print("\n--- Test 2: SKU normalización ---")
    try:
        p1 = Producto(nombre="Test", precio=100, sku="abc123")
        p2 = Producto(nombre="Test", precio=100, sku="xyz-456")

        if p1.sku == "ABC-123":
            print(f"  ✓ 'abc123' → '{p1.sku}'")
        else:
            print(f"  ✗ SKU incorrecto: '{p1.sku}' (esperado: 'ABC-123')")

        if p2.sku == "XYZ-456":
            print(f"  ✓ 'xyz-456' → '{p2.sku}'")
        else:
            print(f"  ✗ SKU incorrecto: '{p2.sku}'")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 3: Precio desde string
    print("\n--- Test 3: Precio desde string ---")
    try:
        p = Producto(nombre="Test", precio="$1,299.99", sku="TST-001")
        if p.precio == 1299.99:
            print(f"  ✓ '$1,299.99' → {p.precio}")
        else:
            print(f"  ✗ Precio incorrecto: {p.precio}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 4: Precio inválido
    print("\n--- Test 4: Precio inválido ---")
    try:
        Producto(nombre="Test", precio=-10, sku="TST-001")
        print("  ✗ Debería rechazar precio negativo")
    except ValidationError:
        print("  ✓ Precio negativo rechazado")

    # Test 5: precio_oferta válido
    print("\n--- Test 5: precio_oferta válido ---")
    try:
        p = Producto(
            nombre="Test",
            precio=100,
            precio_oferta=80,
            sku="TST-001"
        )
        print(f"  ✓ precio_oferta < precio: {p.precio_oferta} < {p.precio}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 6: precio_oferta inválido
    print("\n--- Test 6: precio_oferta inválido ---")
    try:
        Producto(
            nombre="Test",
            precio=100,
            precio_oferta=150,  # Mayor que precio!
            sku="TST-001"
        )
        print("  ✗ Debería rechazar precio_oferta >= precio")
    except ValidationError:
        print("  ✓ precio_oferta >= precio rechazado")

    # Test 7: Propiedades calculadas
    print("\n--- Test 7: Propiedades calculadas ---")
    try:
        p_con_stock = Producto(nombre="A", precio=100, stock=10, sku="A-001")
        p_sin_stock = Producto(nombre="B", precio=100, stock=0, sku="B-001")
        p_con_oferta = Producto(
            nombre="C", precio=100, precio_oferta=80, sku="C-001"
        )

        # disponible
        if hasattr(p_con_stock, 'disponible'):
            if p_con_stock.disponible and not p_sin_stock.disponible:
                print("  ✓ disponible funciona correctamente")
            else:
                print("  ✗ disponible incorrecto")
        else:
            print("  ✗ Falta propiedad 'disponible'")

        # precio_final
        if hasattr(p_con_oferta, 'precio_final'):
            if p_con_oferta.precio_final == 80:
                print(f"  ✓ precio_final con oferta: {p_con_oferta.precio_final}")
            else:
                print(f"  ✗ precio_final incorrecto: {p_con_oferta.precio_final}")

            if p_con_stock.precio_final == 100:
                print(f"  ✓ precio_final sin oferta: {p_con_stock.precio_final}")
        else:
            print("  ✗ Falta propiedad 'precio_final'")

    except Exception as e:
        print(f"  ✗ Error: {e}")

    print("\n" + "=" * 60)
    print("Ejecuta la solución con:")
    print("  python ejercicios/soluciones/ejercicio_02_solucion.py")
