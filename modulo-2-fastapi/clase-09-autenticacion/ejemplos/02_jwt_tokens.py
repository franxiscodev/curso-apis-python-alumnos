"""
Tokens JWT (JSON Web Tokens)
==============================
Crear, decodificar y validar tokens JWT.

Ejecutar:
    python ejemplos/02_jwt_tokens.py

Conceptos:
    - Crear token con jose.jwt.encode
    - Decodificar con jose.jwt.decode
    - Expiración con campo "exp"
    - Estructura: header.payload.firma
"""

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt


# =============================================================================
# CONFIGURACIÓN
# =============================================================================


# En producción: usar variable de entorno, nunca hardcodear
SECRET_KEY = "mi-clave-secreta-de-desarrollo-cambiar-en-produccion"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30


# =============================================================================
# FUNCIONES JWT
# =============================================================================


def crear_token(datos: dict, expira_en: timedelta | None = None) -> str:
    """Crea un token JWT con los datos proporcionados."""
    payload = datos.copy()
    if expira_en:
        expiracion = datetime.now(timezone.utc) + expira_en
    else:
        expiracion = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload["exp"] = expiracion
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decodificar_token(token: str) -> dict | None:
    """Decodifica un token JWT. Retorna None si es inválido."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


# =============================================================================
# DEMOSTRACIÓN
# =============================================================================


if __name__ == "__main__":
    # Crear token para un usuario
    print("=== Crear Token ===")
    token = crear_token(
        datos={"sub": "usuario1", "rol": "admin"},
        expira_en=timedelta(hours=1)
    )
    print(f"Token: {token[:50]}...")
    print(f"Partes: {len(token.split('.'))} (header.payload.firma)")

    # Decodificar token
    print("\n=== Decodificar Token ===")
    payload = decodificar_token(token)
    print(f"Payload: {payload}")
    print(f"Usuario: {payload['sub']}")
    print(f"Rol: {payload['rol']}")

    # Token expirado
    print("\n=== Token Expirado ===")
    token_expirado = crear_token(
        datos={"sub": "usuario2"},
        expira_en=timedelta(seconds=-1)  # Ya expirado
    )
    resultado = decodificar_token(token_expirado)
    print(f"Token expirado decodificado: {resultado}")  # None

    # Token manipulado
    print("\n=== Token Manipulado ===")
    token_falso = token[:-5] + "XXXXX"  # Alterar la firma
    resultado = decodificar_token(token_falso)
    print(f"Token manipulado decodificado: {resultado}")  # None
