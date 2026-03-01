"""
Solución Ejercicio 02: Mapear Operaciones a Métodos HTTP
========================================================
"""

from typing import TypedDict


class EndpointSpec(TypedDict):
    """Especificación de un endpoint."""
    metodo: str
    uri: str
    status_exito: int
    status_error: int


def escenario_1() -> EndpointSpec:
    """
    Escenario: Un cliente quiere ver la lista de todos los productos
    disponibles en la tienda.

    Análisis:
    - Leer datos → GET
    - Colección de recursos → /productos
    - Éxito retorna lista → 200 OK
    """
    return {
        "metodo": "GET",
        "uri": "/productos",
        "status_exito": 200,
        "status_error": 500,  # Error de servidor si falla
    }


def escenario_2() -> EndpointSpec:
    """
    Escenario: Un administrador quiere agregar un nuevo producto
    al catálogo de la tienda.

    Análisis:
    - Crear nuevo recurso → POST
    - Enviar a la colección → /productos
    - Recurso creado → 201 Created
    """
    return {
        "metodo": "POST",
        "uri": "/productos",
        "status_exito": 201,
        "status_error": 422,  # Validación fallida
    }


def escenario_3() -> EndpointSpec:
    """
    Escenario: Un cliente quiere ver los detalles de un producto
    específico con ID 42.

    Análisis:
    - Leer un recurso específico → GET
    - Recurso individual → /productos/{id}
    - Éxito → 200, No existe → 404
    """
    return {
        "metodo": "GET",
        "uri": "/productos/42",
        "status_exito": 200,
        "status_error": 404,
    }


def escenario_4() -> EndpointSpec:
    """
    Escenario: Un administrador necesita cambiar SOLO el precio
    del producto 42, sin modificar otros campos.

    Análisis:
    - Actualización parcial → PATCH
    - Body: {"precio": 99.99}
    - Solo modifica lo enviado
    """
    return {
        "metodo": "PATCH",
        "uri": "/productos/42",
        "status_exito": 200,
        "status_error": 404,
    }


def escenario_5() -> EndpointSpec:
    """
    Escenario: Un administrador quiere reemplazar TODA la información
    del producto 42 con nuevos datos.

    Análisis:
    - Reemplazo completo → PUT
    - Body contiene TODOS los campos
    - Campos omitidos se pierden o usan default
    """
    return {
        "metodo": "PUT",
        "uri": "/productos/42",
        "status_exito": 200,
        "status_error": 404,
    }


def escenario_6() -> EndpointSpec:
    """
    Escenario: Un administrador necesita eliminar el producto 42
    del catálogo.

    Análisis:
    - Eliminar → DELETE
    - Éxito sin contenido → 204 No Content
    """
    return {
        "metodo": "DELETE",
        "uri": "/productos/42",
        "status_exito": 204,
        "status_error": 404,
    }


def escenario_7() -> EndpointSpec:
    """
    Escenario: Un cliente quiere ver todos sus pedidos anteriores.
    El ID del cliente es 15.

    Análisis:
    - Leer colección → GET
    - Relación jerárquica → /usuarios/{id}/pedidos
    - Alternativa válida: /pedidos?usuario_id=15
    """
    return {
        "metodo": "GET",
        "uri": "/usuarios/15/pedidos",
        "status_exito": 200,
        "status_error": 404,  # Usuario no existe
    }


def escenario_8() -> EndpointSpec:
    """
    Escenario: Un cliente quiere crear un nuevo pedido.
    El ID del cliente es 15.

    Análisis:
    - Crear recurso → POST
    - Puede ser /pedidos (con usuario_id en body)
    - O /usuarios/15/pedidos (jerárquico)
    """
    return {
        "metodo": "POST",
        "uri": "/usuarios/15/pedidos",  # o "/pedidos"
        "status_exito": 201,
        "status_error": 422,
    }


def escenario_9() -> EndpointSpec:
    """
    Escenario: Un cliente quiere filtrar productos por categoría
    "electronica" y precio máximo de 500.

    Análisis:
    - Leer con filtros → GET
    - Filtros como query params
    """
    return {
        "metodo": "GET",
        "uri": "/productos?categoria=electronica&precio_max=500",
        "status_exito": 200,
        "status_error": 400,  # Parámetros inválidos
    }


def escenario_10() -> EndpointSpec:
    """
    Escenario: El sistema necesita marcar el pedido 789 como "enviado".
    Solo cambia el campo estado.

    Análisis:
    - Cambio parcial → PATCH
    - Body: {"estado": "enviado"}
    """
    return {
        "metodo": "PATCH",
        "uri": "/pedidos/789",
        "status_exito": 200,
        "status_error": 404,
    }


# =============================================================================
# DEMOSTRACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Solución Ejercicio 02: Métodos HTTP")
    print("=" * 60)

    escenarios = [
        ("Ver lista de productos", escenario_1),
        ("Agregar nuevo producto", escenario_2),
        ("Ver detalles producto 42", escenario_3),
        ("Cambiar solo precio", escenario_4),
        ("Reemplazar producto completo", escenario_5),
        ("Eliminar producto", escenario_6),
        ("Ver pedidos del cliente 15", escenario_7),
        ("Crear pedido para cliente 15", escenario_8),
        ("Filtrar productos", escenario_9),
        ("Marcar pedido como enviado", escenario_10),
    ]

    print("\n--- Escenarios y Soluciones ---\n")
    for desc, func in escenarios:
        result = func()
        print(f"📋 {desc}")
        print(f"   {result['metodo']:6} {result['uri']}")
        print(f"   Éxito: {result['status_exito']}, Error: {result['status_error']}\n")

    print("--- Resumen de Métodos ---")
    print("""
    GET    → Leer (seguro, idempotente)
    POST   → Crear (no idempotente, retorna 201)
    PUT    → Reemplazar todo (idempotente)
    PATCH  → Actualizar parcial (idempotente)
    DELETE → Eliminar (idempotente, retorna 204)
    """)

    print("✓ Solución completada")
