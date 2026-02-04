"""
Ejercicio 02: Decorador con Parámetros
======================================
Crea un decorador configurable que limite el número de llamadas.

Instrucciones:
1. Completa la función `limitar_llamadas(max_llamadas)`
2. El decorador debe contar las llamadas a la función
3. Si se excede el límite, debe lanzar un error
4. Recuerda: decoradores con parámetros = 3 niveles de anidación
"""

from functools import wraps

# =============================================================================
# EJERCICIO: Completa el decorador con parámetros
# =============================================================================


def limitar_llamadas(max_llamadas: int):
    """
    Fábrica de decoradores que limita el número de llamadas a una función.

    Args:
        max_llamadas: Número máximo de veces que se puede llamar la función

    Raises:
        RuntimeError: Cuando se excede el límite de llamadas

    Ejemplo de uso:
        @limitar_llamadas(max_llamadas=3)
        def mi_funcion():
            pass

        mi_funcion()  # OK - llamada 1
        mi_funcion()  # OK - llamada 2
        mi_funcion()  # OK - llamada 3
        mi_funcion()  # RuntimeError!
    """
    # TODO: Necesitas una variable para contar las llamadas
    # Hint: Puedes usar una lista [0] para que sea mutable en el closure
    # O usar nonlocal en Python 3

    def decorador(func):
        # TODO: Agrega @wraps
        # TODO: Inicializa el contador aquí (dentro del decorador, fuera del wrapper)

        def wrapper(*args, **kwargs):
            # TODO: Incrementa el contador

            # TODO: Verifica si se excedió el límite
            # Si se excede: raise RuntimeError(f"...")

            # TODO: Muestra mensaje de cuántas llamadas van
            # Formato: [LLAMADA X/Y] nombre_funcion

            # TODO: Ejecuta y retorna el resultado
            pass

        # TODO: Agrega un método para resetear el contador
        # wrapper.reset = lambda: ...

        return wrapper

    return decorador


# =============================================================================
# FUNCIONES DE PRUEBA (no modificar)
# =============================================================================


@limitar_llamadas(max_llamadas=3)
def api_costosa() -> dict:
    """Simula una API con límite de llamadas."""
    return {"status": "ok", "data": "resultado"}


@limitar_llamadas(max_llamadas=2)
def recurso_limitado(valor: int) -> int:
    """Recurso con solo 2 llamadas permitidas."""
    return valor * 2


# =============================================================================
# VERIFICACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Verificando decorador limitar_llamadas")
    print("=" * 60)

    print("\n--- Test 1: Llamadas dentro del límite ---")
    print("Llamando api_costosa() 3 veces (límite: 3)")

    for i in range(3):
        resultado = api_costosa()
        print(f"  Resultado {i+1}: {resultado}")

    print("\n--- Test 2: Exceder el límite ---")
    print("Llamando api_costosa() una vez más...")
    try:
        api_costosa()
        print("  ❌ Debería haber lanzado RuntimeError")
    except RuntimeError as e:
        print(f"  ✓ RuntimeError capturado: {e}")

    print("\n--- Test 3: Reset del contador ---")
    if hasattr(api_costosa, 'reset'):
        api_costosa.reset()
        print("  Contador reseteado")
        resultado = api_costosa()
        print(f"  Llamada después de reset: {resultado}")
    else:
        print("  (Opcional) No implementaste wrapper.reset")

    print("\n--- Test 4: Verificar metadatos ---")
    print(f"  Nombre: {api_costosa.__name__}")
    assert api_costosa.__name__ == "api_costosa", "Falta @wraps"

    print("\n--- Test 5: Otra función con límite diferente ---")
    print("Llamando recurso_limitado() 2 veces (límite: 2)")
    print(f"  {recurso_limitado(5)}")
    print(f"  {recurso_limitado(10)}")

    try:
        recurso_limitado(15)
        print("  ❌ Debería haber lanzado RuntimeError")
    except RuntimeError:
        print("  ✓ RuntimeError en tercera llamada")

    print("\n✓ Ejercicio completado")
