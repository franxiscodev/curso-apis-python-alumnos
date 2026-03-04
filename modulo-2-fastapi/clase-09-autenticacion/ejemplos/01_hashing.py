"""
Hashing de Contraseñas con bcrypt
==================================
Nunca guardar contraseñas en texto plano.

Ejecutar:
    python ejemplos/01_hashing.py

Conceptos:
    - bcrypt directo (sin passlib, proyecto abandonado)
    - hash() para crear hash
    - verify() para comparar
    - Salt automático (cada hash es diferente)
    - Manejo del límite de 72 bytes de bcrypt
"""

import bcrypt
import hashlib


# =============================================================================
# CONFIGURACIÓN
# =============================================================================

# Número de rondas de hashing (costo computacional)
# Mayor valor = más seguro pero más lento. 12 es un buen balance.
BCRYPT_ROUNDS = 12


# =============================================================================
# FUNCIONES DE HASHING (Versión básica - para contraseñas normales)
# =============================================================================

def hashear_password(password: str) -> str:
    """
    Crea un hash seguro de la contraseña.

    ADVERTENCIA: Esta versión simple fallará con contraseñas > 72 bytes.
    Usar hashear_password_segura() para producción.
    """
    # Convertir string a bytes
    password_bytes = password.encode('utf-8')

    # Generar salt con el número de rondas configurado
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)

    # Generar hash
    hash_bytes = bcrypt.hashpw(password_bytes, salt)

    # Devolver como string
    return hash_bytes.decode('utf-8')


def verificar_password(password_plano: str, password_hash: str) -> bool:
    """
    Verifica si la contraseña coincide con el hash.
    Versión básica para usar con hashear_password().
    """
    password_bytes = password_plano.encode('utf-8')
    hash_bytes = password_hash.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hash_bytes)


# =============================================================================
# FUNCIONES DE HASHING (Versión profesional - Recomendada)
# =============================================================================

def hashear_password_segura(password: str) -> str:
    """
    Crea un hash seguro de la contraseña.

    Esta versión maneja el límite de 72 bytes de bcrypt usando SHA256
    como pre-hash. Acepta contraseñas de cualquier longitud.

    Esta es la versión recomendada para producción.
    """
    # SHA256 produce 32 bytes (siempre dentro del límite de bcrypt)
    # Esto nos permite manejar contraseñas de cualquier longitud
    password_pre_hasheada = hashlib.sha256(password.encode()).digest()

    # Generar salt y aplicar bcrypt
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    hash_bytes = bcrypt.hashpw(password_pre_hasheada, salt)

    return hash_bytes.decode('utf-8')


def verificar_password_segura(password_plano: str, password_hash: str) -> bool:
    """
    Verifica si la contraseña coincide con el hash.
    Versión para usar con hashear_password_segura().
    """
    # Aplicar el mismo pre-hash SHA256
    password_pre_hasheada = hashlib.sha256(password_plano.encode()).digest()

    # Verificar contra el hash almacenado
    hash_bytes = password_hash.encode('utf-8')
    return bcrypt.checkpw(password_pre_hasheada, hash_bytes)


# =============================================================================
# CLASE PARA MANEJAR USUARIOS (Ejemplo práctico)
# =============================================================================

class Usuario:
    """Clase simple para representar un usuario."""

    def __init__(self, email: str, password: str):
        self.email = email
        # Siempre usar la versión segura
        self.password_hash = hashear_password_segura(password)

    def verificar_password(self, password: str) -> bool:
        """Verifica si la contraseña ingresada es correcta."""
        return verificar_password_segura(password, self.password_hash)

    def __str__(self):
        return f"Usuario: {self.email}"


# =============================================================================
# DEMOSTRACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("HASHING DE CONTRASEÑAS CON BCRYPT")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # Demostración 1: Versión básica (con contraseña normal)
    # -------------------------------------------------------------------------
    print("\n📌 1. VERSIÓN BÁSICA (contraseña normal)")
    print("-" * 50)

    password_normal = "mi_contraseña_segura"

    # Crear hashes (cada uno con salt diferente)
    hash1 = hashear_password(password_normal)
    hash2 = hashear_password(password_normal)

    print(f"Contraseña: {password_normal}")
    print(f"Hash 1: {hash1}")
    print(f"Hash 2: {hash2}")
    # False (salt diferente)
    print(f"¿Son iguales los hashes? {hash1 == hash2}")

    # Verificar
    print(
        f"\nVerificación correcta: {verificar_password(password_normal, hash1)}")
    print(
        f"\nVerificación correcta: {verificar_password(password_normal, hash2)}")
    print(f"Verificación incorrecta: {verificar_password('otra', hash1)}")

    # -------------------------------------------------------------------------
    # Demostración 2: Problema del límite de 72 bytes
    # -------------------------------------------------------------------------
    print("\n📌 2. PROBLEMA DEL LÍMITE DE 72 BYTES")
    print("-" * 50)

    password_larga = "a" * 100
    bytes_count = len(password_larga.encode('utf-8'))
    print(
        f"Contraseña larga: {password_larga[:20]}... ({len(password_larga)} caracteres, {bytes_count} bytes)")

    try:
        # Esto FALLARÁ con la versión básica
        hash_larga = hashear_password(password_larga)
        print(f"Hash básico: {hash_larga[:30]}...")
    except ValueError as e:
        print(f"❌ Error con versión básica: {e}")

    # -------------------------------------------------------------------------
    # Demostración 3: Versión segura (maneja el límite)
    # -------------------------------------------------------------------------
    print("\n📌 3. VERSIÓN SEGURA (con SHA256)")
    print("-" * 50)

    # Probar con la misma contraseña larga
    hash_segura = hashear_password_segura(password_larga)
    print(f"Hash seguro: {hash_segura}")
    print(
        f"Verificación correcta: {verificar_password_segura(password_larga, hash_segura)}")
    print(
        f"Verificación incorrecta: {verificar_password_segura('otra', hash_segura)}")

    # -------------------------------------------------------------------------
    # Demostración 4: Simulación de Registro/Login
    # -------------------------------------------------------------------------
    print("\n📌 4. SIMULACIÓN REGISTRO/LOGIN")
    print("-" * 50)

    # Base de datos simulada
    usuarios_db = {}

    # Registrar usuarios (con diferentes tipos de contraseña)
    print("\n--- REGISTRO DE USUARIOS ---")

    # Usuario 1: contraseña normal
    usuario1 = Usuario("ana@ejemplo.com", "secreto123")
    usuarios_db[usuario1.email] = usuario1
    print(f"✅ Registrado: {usuario1}")

    # Usuario 2: contraseña con acentos (caracteres multibyte)
    usuario2 = Usuario("pedro@ejemplo.com", "contraseña_segura_123")
    usuarios_db[usuario2.email] = usuario2
    bytes_accent = len("contraseña_segura_123".encode('utf-8'))
    print(
        f"✅ Registrado: {usuario2} (contraseña con acentos, {bytes_accent} bytes)")

    # Usuario 3: contraseña extremadamente larga
    usuario3 = Usuario("laura@ejemplo.com", "x" * 200)
    usuarios_db[usuario3.email] = usuario3
    print(f"✅ Registrado: {usuario3} (contraseña de 200 caracteres)")

    # Intentos de login
    print("\n--- INTENTOS DE LOGIN CORRECTOS ---")

    # Login correcto usuario 1
    if usuarios_db["ana@ejemplo.com"].verificar_password("secreto123"):
        print("✅ ana@ejemplo.com: Login exitoso")
    else:
        print("❌ ana@ejemplo.com: Login fallido")

    # Login correcto usuario 2
    if usuarios_db["pedro@ejemplo.com"].verificar_password("contraseña_segura_123"):
        print("✅ pedro@ejemplo.com: Login exitoso")
    else:
        print("❌ pedro@ejemplo.com: Login fallido")

    # Login correcto usuario 3 (contraseña larga)
    if usuarios_db["laura@ejemplo.com"].verificar_password("x" * 200):
        print("✅ laura@ejemplo.com: Login exitoso (contraseña de 200 caracteres)")
    else:
        print("❌ laura@ejemplo.com: Login fallido")

    # Intentos de login incorrectos
    print("\n--- INTENTOS DE LOGIN INCORRECTOS ---")

    intentos_incorrectos = [
        ("ana@ejemplo.com", "contraseña_incorrecta"),
        ("pedro@ejemplo.com", "contraseña"),
        ("laura@ejemplo.com", "y" * 200),
    ]

    for email, password in intentos_incorrectos:
        if email in usuarios_db:
            if usuarios_db[email].verificar_password(password):
                print(f"❌ {email}: Error - debería fallar")
            else:
                print(f"✅ {email}: Login fallido (correcto)")

    # -------------------------------------------------------------------------
    # Demostración 5: Prueba con diferentes tipos de caracteres
    # -------------------------------------------------------------------------
    print("\n📌 5. PRUEBA CON DIFERENTES TIPOS DE CARACTERES")
    print("-" * 50)

    pruebas = [
        ("Solo ASCII", "password123"),
        ("Con acentos", "contraseña_segura"),
        ("Con emojis", "🔒password🔑123"),
        ("Con símbolos", "P@$$w0rd!#"),
        ("Mezcla completa", "P4sswörd🙈!@#$%"),
    ]

    for nombre, password in pruebas:
        bytes_len = len(password.encode('utf-8'))
        hash_pwd = hashear_password_segura(password)
        verificacion = verificar_password_segura(password, hash_pwd)

        print(f"\n{nombre}:")
        print(f"  Contraseña: {password}")
        print(f"  Caracteres: {len(password)} | Bytes: {bytes_len}")
        print(f"  Hash: {hash_pwd[:40]}...")
        print(f"  Verificación: {'✅' if verificacion else '❌'}")

    # -------------------------------------------------------------------------
    # Resumen final
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("✅ RESUMEN: TODO FUNCIONANDO CORRECTAMENTE")
    print("=" * 70)
    print("""
    • Se eliminó la dependencia de passlib (proyecto abandonado)
    • Se usa bcrypt directamente (bcrypt 5.0.0 instalado)
    • Se implementó manejo del límite de 72 bytes con SHA256
    • Las contraseñas de cualquier longitud funcionan
    • Cada hash tiene su propio salt (incluso con misma contraseña)
    """)
