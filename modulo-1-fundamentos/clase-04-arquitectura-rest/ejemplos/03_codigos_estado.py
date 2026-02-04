"""
Ejemplo 03: Códigos de Estado HTTP
==================================
Cuándo usar cada código de estado y ejemplos prácticos.
"""

from dataclasses import dataclass
from enum import IntEnum


# =============================================================================
# CÓDIGOS DE ESTADO COMUNES
# =============================================================================


class CodigoHTTP(IntEnum):
    """Códigos de estado HTTP más usados en APIs."""

    # 2xx - Éxito
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204

    # 3xx - Redirección
    MOVED_PERMANENTLY = 301
    FOUND = 302
    NOT_MODIFIED = 304

    # 4xx - Error del Cliente
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    TOO_MANY_REQUESTS = 429

    # 5xx - Error del Servidor
    INTERNAL_SERVER_ERROR = 500
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503


# =============================================================================
# INFORMACIÓN DE CÓDIGOS
# =============================================================================


@dataclass
class InfoCodigo:
    """Información sobre un código de estado."""
    codigo: int
    nombre: str
    descripcion: str
    ejemplo_uso: str


CODIGOS_INFO: dict[int, InfoCodigo] = {
    # 2xx
    200: InfoCodigo(
        codigo=200,
        nombre="OK",
        descripcion="Request exitoso. Retorna datos solicitados.",
        ejemplo_uso="GET /usuarios/123 → Retorna datos del usuario"
    ),
    201: InfoCodigo(
        codigo=201,
        nombre="Created",
        descripcion="Recurso creado exitosamente.",
        ejemplo_uso="POST /usuarios → Usuario creado, retorna ID y Location header"
    ),
    204: InfoCodigo(
        codigo=204,
        nombre="No Content",
        descripcion="Éxito pero sin contenido para retornar.",
        ejemplo_uso="DELETE /usuarios/123 → Eliminado, sin body en response"
    ),

    # 4xx
    400: InfoCodigo(
        codigo=400,
        nombre="Bad Request",
        descripcion="Request malformado o inválido.",
        ejemplo_uso="POST /usuarios con JSON mal formado"
    ),
    401: InfoCodigo(
        codigo=401,
        nombre="Unauthorized",
        descripcion="No autenticado. Falta token o es inválido.",
        ejemplo_uso="GET /admin sin Authorization header"
    ),
    403: InfoCodigo(
        codigo=403,
        nombre="Forbidden",
        descripcion="Autenticado pero sin permisos.",
        ejemplo_uso="Usuario normal intenta DELETE /admin/config"
    ),
    404: InfoCodigo(
        codigo=404,
        nombre="Not Found",
        descripcion="Recurso no existe.",
        ejemplo_uso="GET /usuarios/99999 donde ID no existe"
    ),
    409: InfoCodigo(
        codigo=409,
        nombre="Conflict",
        descripcion="Conflicto con el estado actual del recurso.",
        ejemplo_uso="POST /usuarios con email que ya existe"
    ),
    422: InfoCodigo(
        codigo=422,
        nombre="Unprocessable Entity",
        descripcion="Datos sintácticamente correctos pero semánticamente inválidos.",
        ejemplo_uso="POST /usuarios con email='no-es-email'"
    ),
    429: InfoCodigo(
        codigo=429,
        nombre="Too Many Requests",
        descripcion="Rate limit excedido.",
        ejemplo_uso="Cliente hace más de 100 requests/minuto"
    ),

    # 5xx
    500: InfoCodigo(
        codigo=500,
        nombre="Internal Server Error",
        descripcion="Error inesperado en el servidor.",
        ejemplo_uso="Error en base de datos, excepción no manejada"
    ),
    503: InfoCodigo(
        codigo=503,
        nombre="Service Unavailable",
        descripcion="Servicio temporalmente no disponible.",
        ejemplo_uso="Servidor en mantenimiento"
    ),
}


# =============================================================================
# SIMULACIÓN DE RESPUESTAS
# =============================================================================


@dataclass
class Response:
    """Simula una respuesta HTTP."""
    status_code: int
    body: dict | None = None
    headers: dict | None = None

    def __str__(self) -> str:
        info = CODIGOS_INFO.get(self.status_code)
        nombre = info.nombre if info else "Unknown"
        return f"HTTP {self.status_code} {nombre}"


class APISimulada:
    """Simula respuestas de una API REST."""

    def __init__(self):
        self._usuarios = {
            1: {"id": 1, "nombre": "Ana", "email": "ana@test.com"},
            2: {"id": 2, "nombre": "Carlos", "email": "carlos@test.com"},
        }
        self._next_id = 3

    def get_usuario(self, id: int, autenticado: bool = True) -> Response:
        """GET /usuarios/{id}"""
        if not autenticado:
            return Response(401, {"error": "Token requerido"})

        if id in self._usuarios:
            return Response(200, self._usuarios[id])
        return Response(404, {"error": f"Usuario {id} no encontrado"})

    def crear_usuario(self, datos: dict) -> Response:
        """POST /usuarios"""
        # Validar JSON
        if not datos:
            return Response(400, {"error": "Body vacío o JSON inválido"})

        # Validar campos requeridos
        if "nombre" not in datos or "email" not in datos:
            return Response(422, {
                "error": "Validación fallida",
                "detalles": ["nombre y email son requeridos"]
            })

        # Validar email único
        for u in self._usuarios.values():
            if u["email"] == datos["email"]:
                return Response(409, {"error": f"Email {datos['email']} ya existe"})

        # Crear usuario
        nuevo = {
            "id": self._next_id,
            "nombre": datos["nombre"],
            "email": datos["email"]
        }
        self._usuarios[self._next_id] = nuevo
        self._next_id += 1

        return Response(
            201,
            nuevo,
            {"Location": f"/usuarios/{nuevo['id']}"}
        )

    def eliminar_usuario(self, id: int, es_admin: bool = False) -> Response:
        """DELETE /usuarios/{id}"""
        if not es_admin:
            return Response(403, {"error": "Solo admins pueden eliminar"})

        if id not in self._usuarios:
            return Response(404, {"error": f"Usuario {id} no encontrado"})

        del self._usuarios[id]
        return Response(204)


# =============================================================================
# GUÍA DE SELECCIÓN DE CÓDIGOS
# =============================================================================


def seleccionar_codigo(
    exito: bool,
    recurso_creado: bool = False,
    tiene_contenido: bool = True,
    tipo_error: str | None = None
) -> int:
    """
    Guía para seleccionar el código de estado correcto.

    Args:
        exito: ¿La operación fue exitosa?
        recurso_creado: ¿Se creó un nuevo recurso?
        tiene_contenido: ¿Hay contenido para retornar?
        tipo_error: Tipo de error si no fue éxito

    Returns:
        Código de estado HTTP recomendado
    """
    if exito:
        if recurso_creado:
            return 201  # Created
        if not tiene_contenido:
            return 204  # No Content
        return 200  # OK

    # Errores del cliente
    errores_cliente = {
        "no_autenticado": 401,
        "sin_permisos": 403,
        "no_encontrado": 404,
        "conflicto": 409,
        "validacion": 422,
        "rate_limit": 429,
        "request_invalido": 400,
    }

    if tipo_error in errores_cliente:
        return errores_cliente[tipo_error]

    # Error del servidor por defecto
    return 500


# =============================================================================
# DEMOSTRACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Códigos de Estado HTTP")
    print("=" * 60)

    # --- Tabla de códigos ---
    print("\n--- Códigos Comunes ---")
    for codigo, info in CODIGOS_INFO.items():
        print(f"\n{codigo} {info.nombre}")
        print(f"  {info.descripcion}")
        print(f"  Ejemplo: {info.ejemplo_uso}")

    # --- Simulación ---
    print("\n" + "=" * 60)
    print("Simulación de Respuestas")
    print("=" * 60)

    api = APISimulada()

    # GET exitoso
    print("\n--- GET /usuarios/1 ---")
    resp = api.get_usuario(1)
    print(f"  {resp}")
    print(f"  Body: {resp.body}")

    # GET no encontrado
    print("\n--- GET /usuarios/999 ---")
    resp = api.get_usuario(999)
    print(f"  {resp}")
    print(f"  Body: {resp.body}")

    # GET sin autenticar
    print("\n--- GET /usuarios/1 (sin auth) ---")
    resp = api.get_usuario(1, autenticado=False)
    print(f"  {resp}")

    # POST exitoso
    print("\n--- POST /usuarios ---")
    resp = api.crear_usuario({"nombre": "María", "email": "maria@test.com"})
    print(f"  {resp}")
    print(f"  Body: {resp.body}")
    print(f"  Headers: {resp.headers}")

    # POST con email duplicado
    print("\n--- POST /usuarios (email duplicado) ---")
    resp = api.crear_usuario({"nombre": "Ana2", "email": "ana@test.com"})
    print(f"  {resp}")
    print(f"  Body: {resp.body}")

    # POST con datos inválidos
    print("\n--- POST /usuarios (sin email) ---")
    resp = api.crear_usuario({"nombre": "Test"})
    print(f"  {resp}")

    # DELETE sin permisos
    print("\n--- DELETE /usuarios/1 (sin ser admin) ---")
    resp = api.eliminar_usuario(1, es_admin=False)
    print(f"  {resp}")

    # DELETE exitoso
    print("\n--- DELETE /usuarios/1 (como admin) ---")
    resp = api.eliminar_usuario(1, es_admin=True)
    print(f"  {resp}")

    # --- Guía de selección ---
    print("\n" + "=" * 60)
    print("Guía de Selección")
    print("=" * 60)
    print(f"\nGET exitoso: {seleccionar_codigo(exito=True)}")
    print(f"POST creó recurso: {seleccionar_codigo(exito=True, recurso_creado=True)}")
    print(f"DELETE exitoso: {seleccionar_codigo(exito=True, tiene_contenido=False)}")
    print(f"Usuario no encontrado: {seleccionar_codigo(exito=False, tipo_error='no_encontrado')}")
    print(f"Error de validación: {seleccionar_codigo(exito=False, tipo_error='validacion')}")

    print("\n✓ Ejemplo completado")
