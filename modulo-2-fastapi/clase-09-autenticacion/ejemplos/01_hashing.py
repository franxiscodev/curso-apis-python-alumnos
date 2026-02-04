"""
Hashing de Contraseñas con bcrypt
==================================
Nunca guardar contraseñas en texto plano.

Ejecutar:
    python ejemplos/01_hashing.py

Conceptos:
    - passlib con bcrypt
    - hash() para crear hash
    - verify() para comparar
    - Salt automático (cada hash es diferente)
"""

from passlib.context import CryptContext


# =============================================================================
# CONFIGURACIÓN
# =============================================================================


# Contexto de hashing: bcrypt es el estándar recomendado
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# =============================================================================
# FUNCIONES DE HASHING
# =============================================================================


def hashear_password(password: str) -> str:
    """Crea un hash seguro de la contraseña."""
    return pwd_context.hash(password)


def verificar_password(password_plano: str, password_hash: str) -> bool:
    """Verifica si la contraseña coincide con el hash."""
    return pwd_context.verify(password_plano, password_hash)


# =============================================================================
# DEMOSTRACIÓN
# =============================================================================


if __name__ == "__main__":
    contraseña = "mi_contraseña_segura"

    # Crear hash
    hash1 = hashear_password(contraseña)
    hash2 = hashear_password(contraseña)  # Mismo password, hash diferente

    print("=== Hashing ===")
    print(f"Contraseña: {contraseña}")
    print(f"Hash 1: {hash1}")
    print(f"Hash 2: {hash2}")
    print(f"¿Son iguales? {hash1 == hash2}")  # False (salt diferente)

    # Verificar
    print("\n=== Verificación ===")
    print(f"Correcta vs Hash 1: {verificar_password(contraseña, hash1)}")
    print(f"Correcta vs Hash 2: {verificar_password(contraseña, hash2)}")
    print(f"Incorrecta vs Hash 1: {verificar_password('otra', hash1)}")

    # Ejemplo práctico: simular registro y login
    print("\n=== Simulación Registro/Login ===")
    usuarios_db = {}

    # Registro
    email = "ana@ejemplo.com"
    password_registro = "secreto123"
    usuarios_db[email] = {
        "email": email,
        "password_hash": hashear_password(password_registro)
    }
    print(f"Registrado: {email}")

    # Login correcto
    password_login = "secreto123"
    usuario = usuarios_db[email]
    if verificar_password(password_login, usuario["password_hash"]):
        print(f"Login exitoso para {email}")
    else:
        print("Login fallido")

    # Login incorrecto
    password_mal = "contraseña_incorrecta"
    if verificar_password(password_mal, usuario["password_hash"]):
        print("Login exitoso")
    else:
        print(f"Login fallido con '{password_mal}'")
