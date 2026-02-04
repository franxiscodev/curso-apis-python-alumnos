"""
Ejercicio 02: Mapear Operaciones a Métodos HTTP
===============================================

Objetivo:
Para cada escenario, determinar:
1. El método HTTP correcto
2. La URI apropiada
3. El código de estado esperado

Instrucciones:
Completa las funciones retornando un diccionario con:
- "metodo": GET, POST, PUT, PATCH, DELETE
- "uri": La URI RESTful
- "status_exito": Código de estado si tiene éxito
- "status_error": Código de estado más probable en caso de error
"""

from typing import TypedDict


class EndpointSpec(TypedDict):
    """Especificación de un endpoint."""
    metodo: str
    uri: str
    status_exito: int
    status_error: int


# =============================================================================
# TU CÓDIGO AQUÍ
# =============================================================================


def escenario_1() -> EndpointSpec:
    """
    Escenario: Un cliente quiere ver la lista de todos los productos
    disponibles en la tienda.
    """
    return {
        "metodo": "TODO",
        "uri": "TODO",
        "status_exito": 0,
        "status_error": 0,
    }


def escenario_2() -> EndpointSpec:
    """
    Escenario: Un administrador quiere agregar un nuevo producto
    al catálogo de la tienda.
    """
    return {
        "metodo": "TODO",
        "uri": "TODO",
        "status_exito": 0,
        "status_error": 0,
    }


def escenario_3() -> EndpointSpec:
    """
    Escenario: Un cliente quiere ver los detalles de un producto
    específico con ID 42.
    """
    return {
        "metodo": "TODO",
        "uri": "TODO",
        "status_exito": 0,
        "status_error": 0,
    }


def escenario_4() -> EndpointSpec:
    """
    Escenario: Un administrador necesita cambiar SOLO el precio
    del producto 42, sin modificar otros campos.
    """
    return {
        "metodo": "TODO",
        "uri": "TODO",
        "status_exito": 0,
        "status_error": 0,
    }


def escenario_5() -> EndpointSpec:
    """
    Escenario: Un administrador quiere reemplazar TODA la información
    del producto 42 con nuevos datos.
    """
    return {
        "metodo": "TODO",
        "uri": "TODO",
        "status_exito": 0,
        "status_error": 0,
    }


def escenario_6() -> EndpointSpec:
    """
    Escenario: Un administrador necesita eliminar el producto 42
    del catálogo.
    """
    return {
        "metodo": "TODO",
        "uri": "TODO",
        "status_exito": 0,
        "status_error": 0,
    }


def escenario_7() -> EndpointSpec:
    """
    Escenario: Un cliente quiere ver todos sus pedidos anteriores.
    El ID del cliente es 15.
    """
    return {
        "metodo": "TODO",
        "uri": "TODO",
        "status_exito": 0,
        "status_error": 0,
    }


def escenario_8() -> EndpointSpec:
    """
    Escenario: Un cliente quiere crear un nuevo pedido.
    El ID del cliente es 15.
    """
    return {
        "metodo": "TODO",
        "uri": "TODO",
        "status_exito": 0,
        "status_error": 0,
    }


def escenario_9() -> EndpointSpec:
    """
    Escenario: Un cliente quiere filtrar productos por categoría
    "electronica" y precio máximo de 500.
    """
    return {
        "metodo": "TODO",
        "uri": "TODO",
        "status_exito": 0,
        "status_error": 0,
    }


def escenario_10() -> EndpointSpec:
    """
    Escenario: El sistema necesita marcar el pedido 789 como "enviado".
    Solo cambia el campo estado.
    """
    return {
        "metodo": "TODO",
        "uri": "TODO",
        "status_exito": 0,
        "status_error": 0,
    }


# =============================================================================
# VERIFICACIÓN
# =============================================================================

RESPUESTAS_ESPERADAS = {
    "escenario_1": {"metodo": "GET", "uri": "/productos", "status_exito": 200},
    "escenario_2": {"metodo": "POST", "uri": "/productos", "status_exito": 201},
    "escenario_3": {"metodo": "GET", "uri": "/productos/42", "status_exito": 200, "status_error": 404},
    "escenario_4": {"metodo": "PATCH", "uri": "/productos/42", "status_exito": 200},
    "escenario_5": {"metodo": "PUT", "uri": "/productos/42", "status_exito": 200},
    "escenario_6": {"metodo": "DELETE", "uri": "/productos/42", "status_exito": 204},
    "escenario_7": {"metodo": "GET", "status_exito": 200},  # URI flexible
    "escenario_8": {"metodo": "POST", "status_exito": 201},  # URI flexible
    "escenario_9": {"metodo": "GET", "status_exito": 200},  # Query params
    "escenario_10": {"metodo": "PATCH", "status_exito": 200},
}


if __name__ == "__main__":
    print("=" * 60)
    print("Verificando Ejercicio 02: Métodos HTTP")
    print("=" * 60)

    escenarios = [
        ("escenario_1", escenario_1),
        ("escenario_2", escenario_2),
        ("escenario_3", escenario_3),
        ("escenario_4", escenario_4),
        ("escenario_5", escenario_5),
        ("escenario_6", escenario_6),
        ("escenario_7", escenario_7),
        ("escenario_8", escenario_8),
        ("escenario_9", escenario_9),
        ("escenario_10", escenario_10),
    ]

    correctos = 0

    for nombre, func in escenarios:
        resultado = func()
        esperado = RESPUESTAS_ESPERADAS[nombre]

        # Verificar método
        metodo_ok = resultado["metodo"] == esperado["metodo"]

        # Verificar status de éxito
        status_ok = resultado["status_exito"] == esperado["status_exito"]

        if metodo_ok and status_ok:
            print(f"\n✓ {nombre}")
            print(f"  {resultado['metodo']} {resultado['uri']} → {resultado['status_exito']}")
            correctos += 1
        else:
            print(f"\n✗ {nombre}")
            print(f"  Tu respuesta: {resultado['metodo']} {resultado['uri']} → {resultado['status_exito']}")
            if not metodo_ok:
                print(f"  Método esperado: {esperado['metodo']}")
            if not status_ok:
                print(f"  Status esperado: {esperado['status_exito']}")

    print(f"\n{'=' * 60}")
    print(f"Resultado: {correctos}/10 escenarios correctos")
    print("=" * 60)
    print("\nEjecuta la solución con:")
    print("  python ejercicios/soluciones/ejercicio_02_solucion.py")
