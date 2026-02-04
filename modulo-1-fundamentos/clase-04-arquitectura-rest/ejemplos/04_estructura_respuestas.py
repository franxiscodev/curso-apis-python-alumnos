"""
Ejemplo 04: Estructura de Respuestas JSON
=========================================
Formatos estándar para responses, paginación y errores.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any
import json


# =============================================================================
# RESPUESTA INDIVIDUAL
# =============================================================================


@dataclass
class Usuario:
    """Modelo de usuario."""
    id: int
    nombre: str
    email: str
    creado_en: str = field(default_factory=lambda: datetime.now().isoformat())


def response_individual(usuario: Usuario) -> dict:
    """
    Response para recurso individual.

    GET /usuarios/123 → 200 OK
    """
    return asdict(usuario)


# =============================================================================
# RESPUESTA DE COLECCIÓN CON PAGINACIÓN
# =============================================================================


@dataclass
class MetaPaginacion:
    """Metadatos de paginación."""
    total: int
    page: int
    per_page: int
    total_pages: int


@dataclass
class LinksPaginacion:
    """Links de navegación HATEOAS."""
    self_link: str
    first: str | None = None
    prev: str | None = None
    next: str | None = None
    last: str | None = None


def response_coleccion_paginada(
    items: list[dict],
    total: int,
    page: int = 1,
    per_page: int = 10,
    base_url: str = "/api/v1/usuarios"
) -> dict:
    """
    Response para colección con paginación.

    GET /usuarios?page=2&per_page=10 → 200 OK
    """
    total_pages = (total + per_page - 1) // per_page

    # Construir links
    links = {
        "self": f"{base_url}?page={page}&per_page={per_page}",
        "first": f"{base_url}?page=1&per_page={per_page}",
        "last": f"{base_url}?page={total_pages}&per_page={per_page}",
    }

    if page > 1:
        links["prev"] = f"{base_url}?page={page-1}&per_page={per_page}"
    if page < total_pages:
        links["next"] = f"{base_url}?page={page+1}&per_page={per_page}"

    return {
        "data": items,
        "meta": {
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages
        },
        "links": links
    }


# =============================================================================
# RESPUESTA DE ERROR
# =============================================================================


@dataclass
class DetalleError:
    """Detalle de un error de validación."""
    field: str
    message: str
    code: str | None = None


@dataclass
class ErrorResponse:
    """Estructura estándar de error."""
    code: str
    message: str
    details: list[DetalleError] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": [asdict(d) for d in self.details] if self.details else None
            }
        }


def response_error_validacion(errores: list[tuple[str, str]]) -> dict:
    """
    Response para error de validación.

    POST /usuarios con datos inválidos → 422
    """
    detalles = [DetalleError(field=campo, message=msg) for campo, msg in errores]
    error = ErrorResponse(
        code="VALIDATION_ERROR",
        message="Los datos proporcionados no son válidos",
        details=detalles
    )
    return error.to_dict()


def response_error_not_found(recurso: str, id: Any) -> dict:
    """
    Response para recurso no encontrado.

    GET /usuarios/999 → 404
    """
    error = ErrorResponse(
        code="NOT_FOUND",
        message=f"{recurso} con ID {id} no encontrado"
    )
    return error.to_dict()


def response_error_conflicto(mensaje: str) -> dict:
    """
    Response para conflicto.

    POST /usuarios con email duplicado → 409
    """
    error = ErrorResponse(
        code="CONFLICT",
        message=mensaje
    )
    return error.to_dict()


# =============================================================================
# RESPUESTA ENVOLVENTE (WRAPPER)
# =============================================================================


def response_wrapper(
    data: Any = None,
    error: dict | None = None,
    meta: dict | None = None
) -> dict:
    """
    Estructura envolvente consistente para todas las respuestas.

    Siempre retorna:
    {
        "success": bool,
        "data": ... (solo si éxito),
        "error": ... (solo si error),
        "meta": ... (opcional, timestamps, etc.)
    }
    """
    response = {
        "success": error is None,
        "timestamp": datetime.now().isoformat()
    }

    if error is None:
        response["data"] = data
    else:
        response["error"] = error.get("error", error)

    if meta:
        response["meta"] = meta

    return response


# =============================================================================
# RESPUESTA POST CREACIÓN
# =============================================================================


def response_created(recurso: dict, location: str) -> tuple[dict, dict]:
    """
    Response para recurso creado.

    POST /usuarios → 201 Created

    Returns:
        Tuple de (body, headers)
    """
    body = recurso
    headers = {"Location": location}
    return body, headers


# =============================================================================
# DEMOSTRACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Estructura de Respuestas JSON")
    print("=" * 60)

    # --- Recurso individual ---
    print("\n--- GET /usuarios/1 → 200 OK ---")
    usuario = Usuario(id=1, nombre="Ana García", email="ana@ejemplo.com")
    response = response_individual(usuario)
    print(json.dumps(response, indent=2, ensure_ascii=False))

    # --- Colección paginada ---
    print("\n--- GET /usuarios?page=2 → 200 OK ---")
    usuarios = [
        {"id": 11, "nombre": "Usuario 11", "email": "u11@test.com"},
        {"id": 12, "nombre": "Usuario 12", "email": "u12@test.com"},
        {"id": 13, "nombre": "Usuario 13", "email": "u13@test.com"},
    ]
    response = response_coleccion_paginada(
        items=usuarios,
        total=45,
        page=2,
        per_page=10
    )
    print(json.dumps(response, indent=2, ensure_ascii=False))

    # --- Error de validación ---
    print("\n--- POST /usuarios (inválido) → 422 ---")
    response = response_error_validacion([
        ("email", "Formato de email inválido"),
        ("nombre", "El nombre es requerido")
    ])
    print(json.dumps(response, indent=2, ensure_ascii=False))

    # --- Error not found ---
    print("\n--- GET /usuarios/999 → 404 ---")
    response = response_error_not_found("Usuario", 999)
    print(json.dumps(response, indent=2, ensure_ascii=False))

    # --- Error conflicto ---
    print("\n--- POST /usuarios (duplicado) → 409 ---")
    response = response_error_conflicto("El email ana@ejemplo.com ya está registrado")
    print(json.dumps(response, indent=2, ensure_ascii=False))

    # --- Respuesta creación ---
    print("\n--- POST /usuarios → 201 Created ---")
    nuevo_usuario = {"id": 100, "nombre": "Nuevo", "email": "nuevo@test.com"}
    body, headers = response_created(nuevo_usuario, "/api/v1/usuarios/100")
    print(f"Body: {json.dumps(body, indent=2)}")
    print(f"Headers: {headers}")

    # --- Wrapper consistente ---
    print("\n--- Wrapper Consistente ---")
    print("\nÉxito:")
    print(json.dumps(
        response_wrapper(data={"id": 1, "nombre": "Ana"}),
        indent=2
    ))

    print("\nError:")
    print(json.dumps(
        response_wrapper(error=response_error_not_found("Usuario", 999)),
        indent=2
    ))

    print("\n✓ Ejemplo completado")
