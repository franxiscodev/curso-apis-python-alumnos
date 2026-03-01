"""
Solución Ejercicio 03: Decorador de Caché Simple
================================================
"""

from functools import wraps
import time


def cache_simple(func):
    """
    Decorador que cachea resultados de una función.

    Comportamiento:
    - Primera llamada con args X: ejecuta función, guarda resultado
    - Segunda llamada con args X: retorna resultado guardado (no ejecuta)
    - Llamada con args Y: ejecuta función, guarda nuevo resultado
    """
    # Diccionario de caché
    cache: dict = {}

    # Contadores para estadísticas
    stats_data = {"hits": 0, "misses": 0}

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Crear clave única basada en argumentos
        # Convertimos kwargs a tuple ordenada para que sea hasheable
        cache_key = (args, tuple(sorted(kwargs.items())))

        # Verificar si está en caché
        if cache_key in cache:
            stats_data["hits"] += 1
            print(f"[CACHE HIT] {func.__name__}{args}")
            return cache[cache_key]

        # No está en caché - ejecutar función
        stats_data["misses"] += 1
        print(f"[CACHE MISS] {func.__name__}{args} - ejecutando...")

        resultado = func(*args, **kwargs)

        # Guardar en caché
        cache[cache_key] = resultado

        return resultado

    # Exponer el caché y funciones de utilidad
    wrapper.cache = cache
    wrapper.stats = lambda: stats_data.copy()
    wrapper.clear = lambda: (cache.clear(), stats_data.update({"hits": 0, "misses": 0}))

    return wrapper


# =============================================================================
# FUNCIONES DE PRUEBA
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
    stats = consulta_simulada.stats()
    print(f"  Stats de consulta_simulada: {stats}")
    print(f"  Hits: {stats['hits']}, Misses: {stats['misses']}")

    print("\n--- Test 4: Ver caché ---")
    print(f"  Entradas en caché: {len(consulta_simulada.cache)}")

    print("\n--- Test 5: Limpiar caché ---")
    consulta_simulada.clear()
    print("  Caché limpiado")
    print(f"  Entradas después de limpiar: {len(consulta_simulada.cache)}")

    print("\n--- Test 6: Verificar metadatos ---")
    print(f"  Nombre: {fibonacci.__name__}")
    print(f"  Docstring: {fibonacci.__doc__[:50]}...")
    assert fibonacci.__name__ == "fibonacci", "Falta @wraps"

    print("\n✓ Ejercicio completado")
