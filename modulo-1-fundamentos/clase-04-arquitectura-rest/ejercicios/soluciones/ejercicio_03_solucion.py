"""
Solución Ejercicio 03: Diseño de Respuestas y Manejo de Errores
===============================================================
"""

from dataclasses import dataclass, asdict
import json


@dataclass
class Producto:
    """Modelo de producto."""
    id: int
    nombre: str
    precio: float
    categoria: str


def response_producto(producto: Producto) -> dict:
    """Genera respuesta para un producto individual."""
    return asdict(producto)


def response_lista_productos(
    productos: list[Producto],
    total: int,
    page: int,
    per_page: int
) -> dict:
    """Genera respuesta para lista de productos con paginación."""
    # Calcular total de páginas
    total_pages = (total + per_page - 1) // per_page

    # Construir links de navegación
    base_url = "/productos"
    links = {
        "self": f"{base_url}?page={page}&per_page={per_page}",
        "first": f"{base_url}?page=1&per_page={per_page}",
        "last": f"{base_url}?page={total_pages}&per_page={per_page}",
    }

    # Link anterior (solo si no es primera página)
    if page > 1:
        links["prev"] = f"{base_url}?page={page - 1}&per_page={per_page}"

    # Link siguiente (solo si no es última página)
    if page < total_pages:
        links["next"] = f"{base_url}?page={page + 1}&per_page={per_page}"

    return {
        "data": [asdict(p) for p in productos],
        "meta": {
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages
        },
        "links": links
    }


def response_error_validacion(errores: list[dict]) -> dict:
    """Genera respuesta de error de validación (422)."""
    details = [
        {"field": e["campo"], "message": e["mensaje"]}
        for e in errores
    ]

    return {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Los datos proporcionados no son válidos",
            "details": details
        }
    }


def response_error_not_found(recurso: str, id: int) -> dict:
    """Genera respuesta de error 404."""
    return {
        "error": {
            "code": "NOT_FOUND",
            "message": f"{recurso} con ID {id} no encontrado"
        }
    }


def response_error_no_autorizado() -> dict:
    """Genera respuesta de error 401."""
    return {
        "error": {
            "code": "UNAUTHORIZED",
            "message": "Token de autenticación requerido"
        }
    }


def response_error_sin_permisos(accion: str) -> dict:
    """Genera respuesta de error 403."""
    return {
        "error": {
            "code": "FORBIDDEN",
            "message": f"No tienes permisos para {accion}"
        }
    }


def response_creado(producto: Producto) -> tuple[dict, dict]:
    """Genera respuesta para recurso creado (201)."""
    body = asdict(producto)
    headers = {"Location": f"/productos/{producto.id}"}
    return body, headers


# =============================================================================
# FUNCIONES ADICIONALES ÚTILES
# =============================================================================


def response_error_conflicto(mensaje: str) -> dict:
    """Genera respuesta de error 409 (conflicto)."""
    return {
        "error": {
            "code": "CONFLICT",
            "message": mensaje
        }
    }


def response_error_rate_limit(limite: int, retry_after: int) -> dict:
    """Genera respuesta de error 429 (rate limit)."""
    return {
        "error": {
            "code": "RATE_LIMIT_EXCEEDED",
            "message": f"Has excedido el límite de {limite} requests",
            "retry_after": retry_after
        }
    }


def response_error_interno(request_id: str | None = None) -> dict:
    """Genera respuesta de error 500."""
    error = {
        "error": {
            "code": "INTERNAL_ERROR",
            "message": "Ha ocurrido un error interno. Por favor, intenta más tarde."
        }
    }
    if request_id:
        error["error"]["request_id"] = request_id
    return error


# =============================================================================
# DEMOSTRACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Solución Ejercicio 03: Respuestas y Errores")
    print("=" * 60)

    # Datos de prueba
    producto = Producto(id=1, nombre="Laptop", precio=999.99, categoria="electronica")
    productos = [
        Producto(id=1, nombre="Laptop", precio=999.99, categoria="electronica"),
        Producto(id=2, nombre="Mouse", precio=29.99, categoria="accesorios"),
    ]

    # Response individual
    print("\n--- GET /productos/1 → 200 OK ---")
    print(json.dumps(response_producto(producto), indent=2))

    # Response lista paginada
    print("\n--- GET /productos?page=1 → 200 OK ---")
    print(json.dumps(response_lista_productos(productos, 50, 1, 10), indent=2))

    # Error validación
    print("\n--- POST /productos (inválido) → 422 ---")
    print(json.dumps(response_error_validacion([
        {"campo": "email", "mensaje": "Formato inválido"},
        {"campo": "precio", "mensaje": "Debe ser mayor a 0"}
    ]), indent=2))

    # Error not found
    print("\n--- GET /productos/999 → 404 ---")
    print(json.dumps(response_error_not_found("Producto", 999), indent=2))

    # Error no autorizado
    print("\n--- GET /admin (sin token) → 401 ---")
    print(json.dumps(response_error_no_autorizado(), indent=2))

    # Error sin permisos
    print("\n--- DELETE /productos/1 (sin permisos) → 403 ---")
    print(json.dumps(response_error_sin_permisos("eliminar productos"), indent=2))

    # Response creado
    print("\n--- POST /productos → 201 Created ---")
    body, headers = response_creado(producto)
    print(f"Body: {json.dumps(body, indent=2)}")
    print(f"Headers: {headers}")

    # Errores adicionales
    print("\n--- Errores Adicionales ---")
    print("\n409 Conflict:")
    print(json.dumps(response_error_conflicto("El email ya está registrado"), indent=2))

    print("\n429 Rate Limit:")
    print(json.dumps(response_error_rate_limit(100, 60), indent=2))

    print("\n500 Internal Error:")
    print(json.dumps(response_error_interno("req-abc123"), indent=2))

    print("\n✓ Solución completada")
