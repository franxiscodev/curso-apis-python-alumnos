"""
Ejemplo 03: Decoradores Prácticos para APIs
===========================================
Decoradores que usarás al desarrollar APIs con FastAPI.

Objetivo: Crear decoradores reutilizables para logging, timing, auth y caché.
"""

from functools import wraps, lru_cache
from datetime import datetime
import time
from typing import Callable, Any

# =============================================================================
# DECORADOR: Logging de requests (simulado)
# =============================================================================


def log_request(func: Callable) -> Callable:
    """
    Decorador que simula el logging de una petición HTTP.

    En FastAPI real, esto se haría con middleware, pero el concepto es similar.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] REQUEST → {func.__name__}")

        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        duracion = time.perf_counter() - inicio

        status = "200 OK" if resultado else "404 Not Found"
        print(f"[{timestamp}] RESPONSE ← {status} ({duracion:.3f}s)")

        return resultado

    return wrapper


# =============================================================================
# DECORADOR: Validación simple (preview de lo que hace Pydantic)
# =============================================================================


def validar_positivo(param_name: str):
    """
    Decorador que valida que un parámetro sea positivo.

    Args:
        param_name: Nombre del parámetro a validar
    """
    def decorador(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Buscar el parámetro en kwargs
            if param_name in kwargs:
                valor = kwargs[param_name]
            else:
                # Buscar por posición usando __code__
                param_names = func.__code__.co_varnames[:func.__code__.co_argcount]
                if param_name in param_names:
                    idx = param_names.index(param_name)
                    if idx < len(args):
                        valor = args[idx]
                    else:
                        valor = None
                else:
                    valor = None

            if valor is not None and valor <= 0:
                raise ValueError(f"{param_name} debe ser positivo, recibido: {valor}")

            return func(*args, **kwargs)
        return wrapper
    return decorador


# =============================================================================
# DECORADOR: Autenticación simulada
# =============================================================================

# Simulamos tokens válidos
_tokens_validos = {"token-abc-123", "token-xyz-789", "admin-token"}


def requiere_auth(func: Callable) -> Callable:
    """
    Decorador que requiere autenticación.

    En FastAPI real, usarías Depends() con OAuth2, pero el concepto es similar.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Buscar token en kwargs
        token = kwargs.get("token") or (args[0] if args else None)

        if not token:
            return {"error": "Token requerido", "status": 401}

        if token not in _tokens_validos:
            return {"error": "Token inválido", "status": 403}

        # Token válido, ejecutar función
        return func(*args, **kwargs)

    return wrapper


def requiere_rol(rol_requerido: str):
    """
    Decorador que requiere un rol específico.

    Args:
        rol_requerido: Rol necesario para acceder
    """
    # Simulamos roles por token
    _roles = {
        "admin-token": ["admin", "user"],
        "token-abc-123": ["user"],
        "token-xyz-789": ["user", "editor"],
    }

    def decorador(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = kwargs.get("token")

            if not token or token not in _tokens_validos:
                return {"error": "No autenticado", "status": 401}

            roles_usuario = _roles.get(token, [])

            if rol_requerido not in roles_usuario:
                return {"error": f"Requiere rol: {rol_requerido}", "status": 403}

            return func(*args, **kwargs)

        return wrapper
    return decorador


# =============================================================================
# DECORADOR: Caché simple (similar a lru_cache pero para APIs)
# =============================================================================


def cache_resultado(ttl_segundos: int = 60):
    """
    Decorador que cachea resultados por un tiempo determinado.

    Args:
        ttl_segundos: Tiempo de vida del caché en segundos
    """
    cache: dict[str, tuple[Any, float]] = {}

    def decorador(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Crear clave única basada en argumentos
            cache_key = f"{func.__name__}:{args}:{kwargs}"

            # Verificar si existe en caché y no expiró
            if cache_key in cache:
                resultado, timestamp = cache[cache_key]
                edad = time.time() - timestamp
                if edad < ttl_segundos:
                    print(f"  [CACHE HIT] {func.__name__} (edad: {edad:.1f}s)")
                    return resultado
                else:
                    print(f"  [CACHE EXPIRED] {func.__name__}")

            # Ejecutar función y guardar en caché
            print(f"  [CACHE MISS] {func.__name__} - ejecutando...")
            resultado = func(*args, **kwargs)
            cache[cache_key] = (resultado, time.time())

            return resultado

        # Exponer función para limpiar caché
        wrapper.limpiar_cache = lambda: cache.clear()

        return wrapper
    return decorador


# =============================================================================
# SIMULACIÓN DE ENDPOINTS DE API
# =============================================================================


@log_request
@validar_positivo("user_id")
def obtener_usuario(user_id: int) -> dict | None:
    """GET /usuarios/{user_id}"""
    # Simular base de datos
    usuarios = {
        1: {"id": 1, "nombre": "Ana García", "email": "ana@ejemplo.com"},
        2: {"id": 2, "nombre": "Carlos López", "email": "carlos@ejemplo.com"},
    }
    time.sleep(0.1)  # Simular latencia
    return usuarios.get(user_id)


@log_request
@requiere_auth
def listar_usuarios_protegido(token: str) -> list[dict]:
    """GET /admin/usuarios - Requiere autenticación"""
    return [
        {"id": 1, "nombre": "Ana"},
        {"id": 2, "nombre": "Carlos"},
    ]


@requiere_rol("admin")
def eliminar_usuario(token: str, user_id: int) -> dict:
    """DELETE /admin/usuarios/{id} - Solo admins"""
    return {"mensaje": f"Usuario {user_id} eliminado", "status": 200}


@cache_resultado(ttl_segundos=5)
def consulta_lenta(query: str) -> list[dict]:
    """Simula una consulta costosa a base de datos."""
    time.sleep(1)  # Simular consulta lenta
    return [{"resultado": query, "timestamp": datetime.now().isoformat()}]


# =============================================================================
# PREVIEW: Así se ve en FastAPI (no ejecutable aún)
# =============================================================================

"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# En FastAPI, los decoradores definen rutas:
@app.get("/usuarios/{user_id}")
async def obtener_usuario(user_id: int):
    # Pydantic valida automáticamente que user_id sea int
    return {"id": user_id}

# La autenticación se maneja con Depends:
@app.get("/admin/usuarios")
async def listar_usuarios(token: str = Depends(oauth2_scheme)):
    # FastAPI inyecta el token automáticamente
    return [{"id": 1}]
"""


# =============================================================================
# EJECUCIÓN DE EJEMPLOS
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DECORADOR @log_request + @validar_positivo")
    print("=" * 60)

    print("\nBuscando usuario 1:")
    print(f"Resultado: {obtener_usuario(user_id=1)}")

    print("\nBuscando usuario 99 (no existe):")
    print(f"Resultado: {obtener_usuario(user_id=99)}")

    print("\nBuscando usuario -1 (inválido):")
    try:
        obtener_usuario(user_id=-1)
    except ValueError as e:
        print(f"Error: {e}")

    print("\n" + "=" * 60)
    print("DECORADOR @requiere_auth")
    print("=" * 60)

    print("\nSin token:")
    print(listar_usuarios_protegido(token=""))

    print("\nToken inválido:")
    print(listar_usuarios_protegido(token="token-falso"))

    print("\nToken válido:")
    print(listar_usuarios_protegido(token="token-abc-123"))

    print("\n" + "=" * 60)
    print("DECORADOR @requiere_rol('admin')")
    print("=" * 60)

    print("\nUsuario normal intentando eliminar:")
    print(eliminar_usuario(token="token-abc-123", user_id=1))

    print("\nAdmin eliminando:")
    print(eliminar_usuario(token="admin-token", user_id=1))

    print("\n" + "=" * 60)
    print("DECORADOR @cache_resultado")
    print("=" * 60)

    print("\nPrimera llamada (MISS - tarda 1s):")
    print(consulta_lenta("SELECT * FROM usuarios"))

    print("\nSegunda llamada inmediata (HIT - instantánea):")
    print(consulta_lenta("SELECT * FROM usuarios"))

    print("\nLlamada con query diferente (MISS):")
    print(consulta_lenta("SELECT * FROM productos"))
