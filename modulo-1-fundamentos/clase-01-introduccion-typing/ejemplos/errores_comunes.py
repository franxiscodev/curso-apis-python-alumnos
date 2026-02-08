"""
Errores Comunes con Type Hints
==============================
Ejemplos de errores frecuentes y cómo evitarlos.

Objetivo: Aprender a identificar y corregir errores típicos de tipado.

Nota: Ejecuta `python -m mypy errores_comunes.py` para ver los errores detectados.
"""

# =============================================================================
# ERROR 1: Confundir None con Optional
# =============================================================================

# ❌ INCORRECTO - None no es un tipo válido para retorno


def buscar_usuario_mal(user_id: int) -> None:
    """Esto dice que SIEMPRE retorna None, no que PUEDE retornar None."""
    if user_id == 1:
        return {"nombre": "Ana"}  # MyPy: error - retorna dict, no None
    return None


# ✅ CORRECTO - Usar | None para indicar que puede ser None
def buscar_usuario_bien(user_id: int) -> dict[str, str] | None:
    """Puede retornar un dict O None."""
    if user_id == 1:
        return {"nombre": "Ana"}
    return None


# =============================================================================
# ERROR 2: Mutar argumentos con valores por defecto mutables
# =============================================================================

# ❌ INCORRECTO - Lista mutable como valor por defecto
def agregar_item_mal(item: str, lista: list[str] = []) -> list[str]:
    """
    ¡PELIGRO! La lista se comparte entre todas las llamadas.
    Cada llamada modifica la MISMA lista.
    """
    lista.append(item)
    return lista


# ✅ CORRECTO - Usar None y crear lista nueva
def agregar_item_bien(item: str, lista: list[str] | None = None) -> list[str]:
    """Crea una lista nueva si no se proporciona una."""
    if lista is None:
        lista = []
    lista.append(item)
    return lista


# =============================================================================
# ERROR 3: Tipos incorrectos en diccionarios
# =============================================================================

# ❌ INCORRECTO - Tipo muy restrictivo
def crear_usuario_mal(nombre: str) -> dict[str, str]:
    """El tipo dice que TODOS los valores son str, pero id es int."""
    return {
        "id": 1,          # MyPy: error - int no es str
        "nombre": nombre
    }


# ✅ CORRECTO - Usar unión de tipos para valores mixtos
def crear_usuario_bien(nombre: str) -> dict[str, str | int]:
    """Los valores pueden ser str O int."""
    return {
        "id": 1,
        "nombre": nombre
    }


# =============================================================================
# ERROR 4: Olvidar tipar el retorno
# =============================================================================

# ❌ INCORRECTO - Sin tipo de retorno, MyPy asume Any
def calcular_total(precios: list[float]):
    """Sin -> tipo, el retorno es implícitamente Any."""
    return sum(precios)


# ✅ CORRECTO - Siempre especificar tipo de retorno
def calcular_total_bien(precios: list[float]) -> float:
    """Tipo de retorno explícito."""
    return sum(precios)


# =============================================================================
# ERROR 5: Confundir list con tipo específico
# =============================================================================

# ❌ INCORRECTO - list sin tipo es como list[Any]
def procesar_datos_mal(datos: list) -> list:
    """Sin especificar el tipo interno, perdemos validación."""
    return [d * 2 for d in datos]


# ✅ CORRECTO - Especificar tipo de elementos
def procesar_datos_bien(datos: list[int]) -> list[int]:
    """Sabemos exactamente qué contiene la lista."""
    return [d * 2 for d in datos]


# =============================================================================
# ERROR 6: Usar tipos en runtime sin validación
# =============================================================================

# ❌ INCORRECTO - Asumir que el tipo garantiza el valor
def dividir_mal(a: int, b: int) -> float:
    """
    Type hints NO validan en runtime.
    Si alguien pasa b=0, esto explota.
    """
    return a / b  # ZeroDivisionError si b=0


# ✅ CORRECTO - Validar en runtime además de tipar
def dividir_bien(a: int, b: int) -> float:
    """Validación explícita para casos edge."""
    if b == 0:
        raise ValueError("El divisor no puede ser cero")
    return a / b


# =============================================================================
# DEMOSTRACIÓN DE ERRORES
# =============================================================================

if __name__ == "__main__":
    print("=== Error 1: None vs Optional ===")
    resultado = buscar_usuario_bien(99)
    print(f"Usuario no encontrado: {resultado}")

    print("\n=== Error 2: Lista mutable por defecto ===")
    # Demostración del problema
    lista1 = agregar_item_mal("A")
    lista2 = agregar_item_mal("B")
    print(f"❌ Ambas listas son la misma: {lista1 is lista2}")  # True!
    print(f"   lista1 = {lista1}")  # ['A', 'B'] - ¡contamidado!

    # Versión correcta
    lista3 = agregar_item_bien("A")
    lista4 = agregar_item_bien("B")
    print(f"✅ Listas independientes: {lista3 is lista4}")  # False
    print(f"   lista3 = {lista3}, lista4 = {lista4}")

    print("\n=== Error 6: Validación en runtime ===")
    try:
        dividir_mal(10, 0)
    except ZeroDivisionError:
        print("❌ dividir_mal(10, 0) -> ZeroDivisionError")

    try:
        dividir_bien(10, 0)
    except ValueError as e:
        print(f"✅ dividir_bien(10, 0) -> ValueError: {e}")

    print("\n✓ Para ver TODOS los errores de tipo:")
    print("  python -m mypy errores_comunes.py")
