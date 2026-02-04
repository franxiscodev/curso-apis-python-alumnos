"""
Ejercicio 01: Modelo Usuario con Validación
============================================

Objetivo:
Crear un modelo Pydantic para Usuario con validaciones.

Requisitos:
1. Campos:
   - id: int | None (opcional, None por defecto)
   - nombre: str (1-50 caracteres)
   - email: EmailStr
   - edad: int (18-120 años)
   - activo: bool (True por defecto)

2. Validadores:
   - nombre: no puede estar vacío, convertir a title case
   - edad: debe estar entre 18 y 120

3. Configuración:
   - str_strip_whitespace: True
   - extra: "forbid"
"""

from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict


# =============================================================================
# TU CÓDIGO AQUÍ
# =============================================================================


class Usuario(BaseModel):
    """
    Modelo de usuario con validación.

    TODO: Implementar según los requisitos.
    """
    pass


# =============================================================================
# VERIFICACIÓN (No modificar)
# =============================================================================

if __name__ == "__main__":
    from pydantic import ValidationError

    print("=" * 60)
    print("Verificando Ejercicio 01: Modelo Usuario")
    print("=" * 60)

    # Test 1: Creación básica
    print("\n--- Test 1: Creación básica ---")
    try:
        usuario = Usuario(
            nombre="ana garcía",
            email="ana@ejemplo.com",
            edad=28
        )
        if usuario.nombre == "Ana García":
            print(f"  ✓ Nombre normalizado: '{usuario.nombre}'")
        else:
            print(f"  ✗ Nombre no normalizado: '{usuario.nombre}'")

        if usuario.activo is True:
            print("  ✓ activo=True por defecto")
        else:
            print("  ✗ activo debería ser True")

        if usuario.id is None:
            print("  ✓ id=None por defecto")
        else:
            print("  ✗ id debería ser None")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 2: Validación de email
    print("\n--- Test 2: Validación de email ---")
    try:
        Usuario(nombre="Test", email="no-es-email", edad=25)
        print("  ✗ Debería rechazar email inválido")
    except ValidationError:
        print("  ✓ Email inválido rechazado")

    # Test 3: Validación de edad
    print("\n--- Test 3: Validación de edad ---")
    try:
        Usuario(nombre="Test", email="test@test.com", edad=15)
        print("  ✗ Debería rechazar edad < 18")
    except ValidationError:
        print("  ✓ Edad < 18 rechazada")

    try:
        Usuario(nombre="Test", email="test@test.com", edad=150)
        print("  ✗ Debería rechazar edad > 120")
    except ValidationError:
        print("  ✓ Edad > 120 rechazada")

    # Test 4: Nombre vacío
    print("\n--- Test 4: Nombre vacío ---")
    try:
        Usuario(nombre="   ", email="test@test.com", edad=25)
        print("  ✗ Debería rechazar nombre vacío/espacios")
    except ValidationError:
        print("  ✓ Nombre vacío rechazado")

    # Test 5: extra="forbid"
    print("\n--- Test 5: Campos extra rechazados ---")
    try:
        Usuario(
            nombre="Test",
            email="test@test.com",
            edad=25,
            campo_extra="valor"
        )
        print("  ✗ Debería rechazar campos extra")
    except ValidationError:
        print("  ✓ Campo extra rechazado")

    # Test 6: Strip whitespace
    print("\n--- Test 6: Strip whitespace ---")
    try:
        usuario = Usuario(
            nombre="  Carlos  ",
            email="carlos@test.com",
            edad=30
        )
        if usuario.nombre == "Carlos":
            print(f"  ✓ Espacios eliminados: '{usuario.nombre}'")
        else:
            print(f"  ✗ Espacios no eliminados: '{usuario.nombre}'")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 7: Serialización
    print("\n--- Test 7: Serialización ---")
    try:
        usuario = Usuario(nombre="Ana", email="ana@test.com", edad=28)
        data = usuario.model_dump()
        campos_esperados = {"id", "nombre", "email", "edad", "activo"}
        if set(data.keys()) == campos_esperados:
            print(f"  ✓ model_dump(): {data}")
        else:
            print(f"  ✗ Campos incorrectos: {data.keys()}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    print("\n" + "=" * 60)
    print("Ejecuta la solución con:")
    print("  python ejercicios/soluciones/ejercicio_01_solucion.py")
