"""
Ejercicio 03: Sistema de Pedidos con Modelos Anidados
=====================================================

Objetivo:
Crear un sistema de modelos Pydantic para gestionar pedidos.

Requisitos:

1. Modelo Direccion:
   - calle: str
   - ciudad: str
   - codigo_postal: str (5 dígitos)
   - pais: str (default "España")

2. Modelo Cliente:
   - id: int
   - nombre: str
   - email: EmailStr
   - direccion: Direccion (anidado)

3. Modelo ProductoPedido:
   - producto_id: int
   - nombre: str
   - precio_unitario: float (> 0)
   - cantidad: int (>= 1)
   - Propiedad: subtotal (precio_unitario * cantidad)

4. Modelo Pedido:
   - id: int | None
   - cliente: Cliente (anidado)
   - productos: list[ProductoPedido] (mínimo 1)
   - direccion_envio: Direccion | None (si None, usar direccion del cliente)
   - notas: str | None
   - Propiedad: total (suma de subtotales)
   - @model_validator: si direccion_envio es None, copiar de cliente

5. DTOs:
   - PedidoCrear: para crear pedido (sin id)
   - PedidoResponse: para respuesta (con id, total calculado)
"""

from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator


# =============================================================================
# TU CÓDIGO AQUÍ
# =============================================================================


class Direccion(BaseModel):
    """Dirección de envío o facturación."""
    pass


class Cliente(BaseModel):
    """Cliente que realiza el pedido."""
    pass


class ProductoPedido(BaseModel):
    """Producto dentro de un pedido."""
    pass


class Pedido(BaseModel):
    """Pedido completo con cliente y productos."""
    pass


# DTOs (opcional)
class PedidoCrear(BaseModel):
    """DTO para crear pedido."""
    pass


class PedidoResponse(BaseModel):
    """DTO para respuesta de pedido."""
    pass


# =============================================================================
# VERIFICACIÓN (No modificar)
# =============================================================================

if __name__ == "__main__":
    from pydantic import ValidationError

    print("=" * 60)
    print("Verificando Ejercicio 03: Sistema de Pedidos")
    print("=" * 60)

    # Datos de prueba
    datos_pedido = {
        "cliente": {
            "id": 1,
            "nombre": "Ana García",
            "email": "ana@ejemplo.com",
            "direccion": {
                "calle": "Gran Vía 123",
                "ciudad": "Madrid",
                "codigo_postal": "28001"
            }
        },
        "productos": [
            {"producto_id": 1, "nombre": "Laptop", "precio_unitario": 999.99, "cantidad": 1},
            {"producto_id": 2, "nombre": "Mouse", "precio_unitario": 29.99, "cantidad": 2}
        ]
    }

    # Test 1: Crear pedido completo
    print("\n--- Test 1: Crear pedido completo ---")
    try:
        pedido = Pedido.model_validate(datos_pedido)
        print(f"  ✓ Pedido creado")
        print(f"    Cliente: {pedido.cliente.nombre}")
        print(f"    Productos: {len(pedido.productos)}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 2: Acceso a modelos anidados
    print("\n--- Test 2: Modelos anidados ---")
    try:
        pedido = Pedido.model_validate(datos_pedido)
        print(f"  ✓ Cliente email: {pedido.cliente.email}")
        print(f"  ✓ Cliente ciudad: {pedido.cliente.direccion.ciudad}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 3: Subtotal de productos
    print("\n--- Test 3: Subtotal de productos ---")
    try:
        pedido = Pedido.model_validate(datos_pedido)
        for p in pedido.productos:
            if hasattr(p, 'subtotal'):
                print(f"  ✓ {p.nombre}: ${p.precio_unitario} x {p.cantidad} = ${p.subtotal}")
            else:
                print(f"  ✗ Falta propiedad 'subtotal' en ProductoPedido")
                break
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 4: Total del pedido
    print("\n--- Test 4: Total del pedido ---")
    try:
        pedido = Pedido.model_validate(datos_pedido)
        if hasattr(pedido, 'total'):
            # 999.99 + (29.99 * 2) = 1059.97
            esperado = 1059.97
            if abs(pedido.total - esperado) < 0.01:
                print(f"  ✓ Total: ${pedido.total:.2f}")
            else:
                print(f"  ✗ Total incorrecto: ${pedido.total} (esperado: ${esperado})")
        else:
            print("  ✗ Falta propiedad 'total' en Pedido")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 5: Dirección de envío por defecto
    print("\n--- Test 5: Dirección envío por defecto ---")
    try:
        pedido = Pedido.model_validate(datos_pedido)
        if pedido.direccion_envio is not None:
            if pedido.direccion_envio.ciudad == "Madrid":
                print(f"  ✓ Dirección copiada del cliente: {pedido.direccion_envio.ciudad}")
            else:
                print(f"  ✗ Dirección incorrecta")
        else:
            print("  ⚠ direccion_envio es None (debería copiarse del cliente)")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 6: Dirección de envío diferente
    print("\n--- Test 6: Dirección envío diferente ---")
    try:
        datos_con_envio = {
            **datos_pedido,
            "direccion_envio": {
                "calle": "Calle Nueva 456",
                "ciudad": "Barcelona",
                "codigo_postal": "08001"
            }
        }
        pedido = Pedido.model_validate(datos_con_envio)
        if pedido.direccion_envio.ciudad == "Barcelona":
            print(f"  ✓ Dirección envío diferente: {pedido.direccion_envio.ciudad}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 7: Validación código postal
    print("\n--- Test 7: Validación código postal ---")
    try:
        datos_invalidos = {
            **datos_pedido,
            "cliente": {
                **datos_pedido["cliente"],
                "direccion": {
                    "calle": "Test",
                    "ciudad": "Test",
                    "codigo_postal": "123"  # Solo 3 dígitos
                }
            }
        }
        Pedido.model_validate(datos_invalidos)
        print("  ✗ Debería rechazar código postal inválido")
    except ValidationError:
        print("  ✓ Código postal inválido rechazado")

    # Test 8: Pedido sin productos
    print("\n--- Test 8: Pedido sin productos ---")
    try:
        datos_sin_productos = {
            **datos_pedido,
            "productos": []
        }
        Pedido.model_validate(datos_sin_productos)
        print("  ✗ Debería rechazar pedido sin productos")
    except ValidationError:
        print("  ✓ Pedido sin productos rechazado")

    # Test 9: Serialización
    print("\n--- Test 9: Serialización ---")
    try:
        pedido = Pedido.model_validate(datos_pedido)
        data = pedido.model_dump()
        if "cliente" in data and "productos" in data:
            print(f"  ✓ Serialización correcta")
            print(f"    Claves: {list(data.keys())}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    print("\n" + "=" * 60)
    print("Ejecuta la solución con:")
    print("  python ejercicios/soluciones/ejercicio_03_solucion.py")
