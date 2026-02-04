"""
Ejercicio 03: Diseño de Respuestas y Manejo de Errores
======================================================

Objetivo:
Implementar funciones que generen respuestas JSON estándar para:
1. Respuestas exitosas (individual y colección)
2. Respuestas de error
3. Paginación

Requisitos:
- Las respuestas deben seguir una estructura consistente
- Los errores deben incluir código, mensaje y detalles
- La paginación debe incluir meta y links
"""

from dataclasses import dataclass
from datetime import datetime


# =============================================================================
# MODELOS (Proporcionados)
# =============================================================================


@dataclass
class Producto:
    """Modelo de producto."""
    id: int
    nombre: str
    precio: float
    categoria: str


# =============================================================================
# TU CÓDIGO AQUÍ
# =============================================================================


def response_producto(producto: Producto) -> dict:
    """
    Genera respuesta para un producto individual.

    Ejemplo de salida esperada:
    {
        "id": 1,
        "nombre": "Laptop",
        "precio": 999.99,
        "categoria": "electronica"
    }
    """
    # TODO: Implementar
    pass


def response_lista_productos(
    productos: list[Producto],
    total: int,
    page: int,
    per_page: int
) -> dict:
    """
    Genera respuesta para lista de productos con paginación.

    Ejemplo de salida esperada:
    {
        "data": [...],
        "meta": {
            "total": 100,
            "page": 1,
            "per_page": 10,
            "total_pages": 10
        },
        "links": {
            "self": "/productos?page=1&per_page=10",
            "next": "/productos?page=2&per_page=10",
            "last": "/productos?page=10&per_page=10"
        }
    }
    """
    # TODO: Implementar
    pass


def response_error_validacion(errores: list[dict]) -> dict:
    """
    Genera respuesta de error de validación (422).

    Args:
        errores: Lista de errores, cada uno con "campo" y "mensaje"

    Ejemplo de entrada:
        [{"campo": "email", "mensaje": "Formato inválido"}]

    Ejemplo de salida esperada:
    {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Los datos proporcionados no son válidos",
            "details": [
                {"field": "email", "message": "Formato inválido"}
            ]
        }
    }
    """
    # TODO: Implementar
    pass


def response_error_not_found(recurso: str, id: int) -> dict:
    """
    Genera respuesta de error 404.

    Ejemplo de salida para recurso="Producto", id=999:
    {
        "error": {
            "code": "NOT_FOUND",
            "message": "Producto con ID 999 no encontrado"
        }
    }
    """
    # TODO: Implementar
    pass


def response_error_no_autorizado() -> dict:
    """
    Genera respuesta de error 401.

    Ejemplo de salida:
    {
        "error": {
            "code": "UNAUTHORIZED",
            "message": "Token de autenticación requerido"
        }
    }
    """
    # TODO: Implementar
    pass


def response_error_sin_permisos(accion: str) -> dict:
    """
    Genera respuesta de error 403.

    Ejemplo de salida para accion="eliminar productos":
    {
        "error": {
            "code": "FORBIDDEN",
            "message": "No tienes permisos para eliminar productos"
        }
    }
    """
    # TODO: Implementar
    pass


def response_creado(producto: Producto) -> tuple[dict, dict]:
    """
    Genera respuesta para recurso creado (201).

    Returns:
        Tupla de (body, headers)

    Ejemplo:
        body: {"id": 1, "nombre": "Laptop", ...}
        headers: {"Location": "/productos/1"}
    """
    # TODO: Implementar
    pass


# =============================================================================
# VERIFICACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Verificando Ejercicio 03: Respuestas y Errores")
    print("=" * 60)

    # Datos de prueba
    producto = Producto(id=1, nombre="Laptop", precio=999.99, categoria="electronica")
    productos = [
        Producto(id=1, nombre="Laptop", precio=999.99, categoria="electronica"),
        Producto(id=2, nombre="Mouse", precio=29.99, categoria="accesorios"),
    ]

    # Test 1: Response individual
    print("\n--- Test 1: Response Individual ---")
    try:
        resp = response_producto(producto)
        if resp and "id" in resp and "nombre" in resp:
            print(f"  ✓ Respuesta: {resp}")
        else:
            print("  ✗ Falta implementar o estructura incorrecta")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 2: Response lista con paginación
    print("\n--- Test 2: Response Lista Paginada ---")
    try:
        resp = response_lista_productos(productos, total=50, page=1, per_page=10)
        if resp and "data" in resp and "meta" in resp and "links" in resp:
            print(f"  ✓ Tiene data, meta, links")
            if resp["meta"].get("total_pages") == 5:
                print(f"  ✓ total_pages calculado correctamente")
            else:
                print(f"  ✗ total_pages incorrecto: {resp['meta'].get('total_pages')}")
        else:
            print("  ✗ Falta implementar o estructura incorrecta")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 3: Error de validación
    print("\n--- Test 3: Error Validación ---")
    try:
        resp = response_error_validacion([
            {"campo": "email", "mensaje": "Formato inválido"},
            {"campo": "precio", "mensaje": "Debe ser mayor a 0"}
        ])
        if resp and "error" in resp:
            err = resp["error"]
            if err.get("code") == "VALIDATION_ERROR" and "details" in err:
                print(f"  ✓ Estructura correcta con {len(err['details'])} detalles")
            else:
                print("  ✗ Falta code o details")
        else:
            print("  ✗ Falta implementar")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 4: Error not found
    print("\n--- Test 4: Error Not Found ---")
    try:
        resp = response_error_not_found("Producto", 999)
        if resp and resp.get("error", {}).get("code") == "NOT_FOUND":
            print(f"  ✓ {resp}")
        else:
            print("  ✗ Falta implementar o code incorrecto")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 5: Error no autorizado
    print("\n--- Test 5: Error No Autorizado ---")
    try:
        resp = response_error_no_autorizado()
        if resp and resp.get("error", {}).get("code") == "UNAUTHORIZED":
            print(f"  ✓ {resp}")
        else:
            print("  ✗ Falta implementar o code incorrecto")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 6: Error sin permisos
    print("\n--- Test 6: Error Sin Permisos ---")
    try:
        resp = response_error_sin_permisos("eliminar productos")
        if resp and resp.get("error", {}).get("code") == "FORBIDDEN":
            print(f"  ✓ {resp}")
        else:
            print("  ✗ Falta implementar o code incorrecto")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 7: Response creado
    print("\n--- Test 7: Response Creado ---")
    try:
        body, headers = response_creado(producto)
        if body and "id" in body and headers.get("Location"):
            print(f"  ✓ Body: {body}")
            print(f"  ✓ Headers: {headers}")
        else:
            print("  ✗ Falta implementar o estructura incorrecta")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    print("\n" + "=" * 60)
    print("Ejecuta la solución con:")
    print("  python ejercicios/soluciones/ejercicio_03_solucion.py")
