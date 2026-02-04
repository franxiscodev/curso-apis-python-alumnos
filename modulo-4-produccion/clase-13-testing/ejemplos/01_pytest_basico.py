"""
Ejemplo 01: pytest Básico
===========================
Tests unitarios de funciones y modelos Pydantic.

Ejecutar:
    pytest ejemplos/01_pytest_basico.py -v
"""

from pydantic import BaseModel, ValidationError


# === CÓDIGO A TESTEAR ===


class Producto(BaseModel):
    nombre: str
    precio: float
    stock: int = 0


def calcular_total(precio: float, cantidad: int, descuento: float = 0) -> float:
    """Calcula el total con descuento opcional."""
    subtotal = precio * cantidad
    return round(subtotal * (1 - descuento), 2)


def aplicar_impuesto(monto: float, tasa: float = 0.21) -> float:
    """Aplica impuesto al monto."""
    return round(monto * (1 + tasa), 2)


def validar_stock(stock: int, cantidad: int) -> bool:
    """Verifica si hay stock suficiente."""
    return stock >= cantidad


# === TESTS ===


def test_calcular_total_basico():
    assert calcular_total(10.0, 3) == 30.0


def test_calcular_total_con_descuento():
    assert calcular_total(100.0, 2, descuento=0.1) == 180.0


def test_calcular_total_sin_cantidad():
    assert calcular_total(50.0, 0) == 0.0


def test_aplicar_impuesto():
    assert aplicar_impuesto(100.0) == 121.0


def test_aplicar_impuesto_tasa_custom():
    assert aplicar_impuesto(100.0, tasa=0.10) == 110.0


def test_validar_stock_suficiente():
    assert validar_stock(10, 5) is True


def test_validar_stock_insuficiente():
    assert validar_stock(3, 5) is False


def test_validar_stock_exacto():
    assert validar_stock(5, 5) is True


# === TESTS DE MODELOS PYDANTIC ===


def test_producto_valido():
    producto = Producto(nombre="Laptop", precio=999.99, stock=10)
    assert producto.nombre == "Laptop"
    assert producto.precio == 999.99
    assert producto.stock == 10


def test_producto_stock_default():
    producto = Producto(nombre="Mouse", precio=29.99)
    assert producto.stock == 0


def test_producto_invalido():
    try:
        Producto(nombre="Test", precio="no_es_numero")
        assert False, "Debería haber fallado"
    except ValidationError:
        pass  # Esperado


def test_producto_model_dump():
    producto = Producto(nombre="Teclado", precio=49.99, stock=5)
    datos = producto.model_dump()
    assert datos == {"nombre": "Teclado", "precio": 49.99, "stock": 5}
