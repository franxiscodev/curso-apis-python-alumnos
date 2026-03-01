"""
Solución Ejercicio 02: Decorador con Parámetros
===============================================
"""

from functools import wraps


def limitar_llamadas(max_llamadas: int):
    """
    Fábrica de decoradores que limita el número de llamadas a una función.

    Args:
        max_llamadas: Número máximo de veces que se puede llamar la función

    Raises:
        RuntimeError: Cuando se excede el límite de llamadas
    """
    def decorador(func):
        # Contador de llamadas (usamos lista para que sea mutable en closure)
        contador = [0]

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Incrementar contador
            contador[0] += 1

            # Verificar límite
            if contador[0] > max_llamadas:
                raise RuntimeError(
                    f"Límite de {max_llamadas} llamadas excedido para {func.__name__}"
                )

            # Mostrar progreso
            print(f"[LLAMADA {contador[0]}/{max_llamadas}] {func.__name__}")

            # Ejecutar y retornar
            return func(*args, **kwargs)

        # Método para resetear el contador
        wrapper.reset = lambda: contador.__setitem__(0, 0)

        # Exponer contador para debugging
        wrapper.get_contador = lambda: contador[0]

        return wrapper

    return decorador


# =============================================================================
# FUNCIONES DE PRUEBA
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
