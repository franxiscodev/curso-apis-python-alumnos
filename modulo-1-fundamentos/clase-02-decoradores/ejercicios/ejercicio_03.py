"""
Ejercicio 03: Decorador de Caché Simple
=======================================
Crea un decorador que cachee resultados de funciones.

Instrucciones:
1. Completa el decorador `cache_simple`
2. Debe almacenar resultados basándose en los argumentos
3. Si se llama con los mismos argumentos, retorna el valor cacheado
4. Incluye método para ver estadísticas del caché
"""

from functools import wraps
import time

# =============================================================================
# EJERCICIO: Completa el decorador de caché
# =============================================================================


def cache_simple(func):
    """
    Decorador que cachea resultados de una función.

    Comportamiento:
    - Primera llamada con args X: ejecuta función, guarda resultado
    - Segunda llamada con args X: retorna resultado guardado (no ejecuta)
    - Llamada con args Y: ejecuta función, guarda nuevo resultado

    El decorador debe exponer:
    - wrapper.cache: el diccionario de caché
    - wrapper.stats(): retorna {"hits": N, "misses": M}
    - wrapper.clear(): limpia el caché

    Ejemplo:
        @cache_simple
        def fibonacci(n):
            ...

        fibonacci(10)  # MISS - calcula
        fibonacci(10)  # HIT - retorna cacheado
        fibonacci(5)   # MISS - calcula
        fibonacci(10)  # HIT - retorna cacheado

        fibonacci.stats()  # {"hits": 2, "misses": 2}
    """
    # TODO: Crea el diccionario de caché
    # TODO: Crea contadores para hits y misses

    # TODO: Agrega @wraps
    def wrapper(*args, **kwargs):
        # TODO: Crea una clave única basada en los argumentos
        # Hint: cache_key = (args, tuple(sorted(kwargs.items())))
        # O más simple: cache_key = str(args) + str(kwargs)

        # TODO: Verifica si la clave está en el caché
        # Si está: incrementa hits, retorna valor cacheado, muestra [CACHE HIT]
        # Si no está: incrementa misses, ejecuta función, guarda en caché, muestra [CACHE MISS]

        pass

    # TODO: Exponer el caché y funciones de utilidad
    # wrapper.cache = ...
    # wrapper.stats = lambda: {"hits": ..., "misses": ...}
    # wrapper.clear = lambda: ...

    return wrapper


# =============================================================================
# FUNCIONES DE PRUEBA (no modificar)
# =============================================================================


@cache_simple
def fibonacci(n: int) -> int:
    """Calcula el n-ésimo número de Fibonacci (ineficiente sin caché)."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@cache_simple
def consulta_simulada(query: str, limit: int = 10) -> list[dict]:
    """Simula una consulta costosa a base de datos."""
    time.sleep(0.5)  # Simular latencia
    return [{"query": query, "limit": limit, "resultado": f"dato_{i}"} for i in range(limit)]


# =============================================================================
# VERIFICACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Verificando decorador cache_simple")
    print("=" * 60)

    print("\n--- Test 1: Fibonacci con caché ---")
    print("Calculando fibonacci(10)...")
    inicio = time.perf_counter()
    resultado = fibonacci(10)
    tiempo1 = time.perf_counter() - inicio
    print(f"  Resultado: {resultado} ({tiempo1:.4f}s)")

    print("\nCalculando fibonacci(10) de nuevo...")
    inicio = time.perf_counter()
    resultado = fibonacci(10)
    tiempo2 = time.perf_counter() - inicio
    print(f"  Resultado: {resultado} ({tiempo2:.4f}s)")

    print(f"\n  Segunda llamada debería ser más rápida:")
    print(f"  Primera: {tiempo1:.4f}s, Segunda: {tiempo2:.4f}s")

    print("\n--- Test 2: Consulta simulada ---")
    print("Primera consulta (debería tardar ~0.5s)...")
    inicio = time.perf_counter()
    datos1 = consulta_simulada("SELECT * FROM users", limit=5)
    tiempo1 = time.perf_counter() - inicio
    print(f"  Tiempo: {tiempo1:.2f}s, Resultados: {len(datos1)}")

    print("\nMisma consulta (debería ser instantánea)...")
    inicio = time.perf_counter()
    datos2 = consulta_simulada("SELECT * FROM users", limit=5)
    tiempo2 = time.perf_counter() - inicio
    print(f"  Tiempo: {tiempo2:.4f}s, Resultados: {len(datos2)}")

    print("\nConsulta diferente (debería tardar ~0.5s)...")
    inicio = time.perf_counter()
    datos3 = consulta_simulada("SELECT * FROM products", limit=3)
    tiempo3 = time.perf_counter() - inicio
    print(f"  Tiempo: {tiempo3:.2f}s, Resultados: {len(datos3)}")

    print("\n--- Test 3: Estadísticas del caché ---")
    if hasattr(consulta_simulada, 'stats'):
        stats = consulta_simulada.stats()
        print(f"  Stats de consulta_simulada: {stats}")
        print(f"  Hits: {stats.get('hits', 'N/A')}, Misses: {stats.get('misses', 'N/A')}")
    else:
        print("  (No implementaste .stats())")

    print("\n--- Test 4: Ver caché ---")
    if hasattr(consulta_simulada, 'cache'):
        print(f"  Entradas en caché: {len(consulta_simulada.cache)}")
    else:
        print("  (No expusiste .cache)")

    print("\n--- Test 5: Limpiar caché ---")
    if hasattr(consulta_simulada, 'clear'):
        consulta_simulada.clear()
        print("  Caché limpiado")
        if hasattr(consulta_simulada, 'cache'):
            print(f"  Entradas después de limpiar: {len(consulta_simulada.cache)}")
    else:
        print("  (No implementaste .clear())")

    print("\n--- Test 6: Verificar metadatos ---")
    print(f"  Nombre: {fibonacci.__name__}")
    print(f"  Docstring: {fibonacci.__doc__[:50]}...")
    assert fibonacci.__name__ == "fibonacci", "Falta @wraps"

    print("\n✓ Ejercicio completado")
