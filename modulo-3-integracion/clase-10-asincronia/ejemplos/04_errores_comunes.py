"""
Errores Comunes en Async
==========================
Antipatterns y cómo evitarlos.

Ejecutar:
    python ejemplos/04_errores_comunes.py

Conceptos:
    - time.sleep vs asyncio.sleep
    - Olvidar await
    - Mezclar sync y async incorrectamente
    - Soluciones correctas
"""

import asyncio
import time


# =============================================================================
# ERROR 1: Usar time.sleep en código async
# =============================================================================


async def error_time_sleep():
    """MAL: time.sleep bloquea el event loop."""
    print("  time.sleep: bloquea TODO (no solo esta tarea)")
    time.sleep(1)  # Bloquea el hilo completo
    return "bloqueante"


async def correcto_asyncio_sleep():
    """BIEN: asyncio.sleep no bloquea."""
    print("  asyncio.sleep: libera el event loop mientras espera")
    await asyncio.sleep(1)  # No bloquea
    return "no bloqueante"


# =============================================================================
# ERROR 2: Olvidar await
# =============================================================================


async def obtener_dato():
    """Función async que retorna datos."""
    await asyncio.sleep(0.1)
    return 42


async def error_sin_await():
    """MAL: sin await retorna un objeto coroutine, no el resultado."""
    resultado = obtener_dato()  # Falta await
    print(f"  Sin await: {resultado}")  # <coroutine object ...>
    print(f"  Tipo: {type(resultado)}")
    # Limpiar coroutine no awaited
    resultado.close()


async def correcto_con_await():
    """BIEN: con await retorna el valor real."""
    resultado = await obtener_dato()
    print(f"  Con await: {resultado}")  # 42
    print(f"  Tipo: {type(resultado)}")


# =============================================================================
# ERROR 3: Ejecutar secuencialmente en vez de concurrentemente
# =============================================================================


async def tarea(nombre: str, seg: float) -> str:
    """Tarea async genérica."""
    await asyncio.sleep(seg)
    return f"{nombre} listo"


async def error_secuencial():
    """MAL: await uno por uno = secuencial, pierde ventaja de async."""
    inicio = time.perf_counter()
    r1 = await tarea("A", 0.5)
    r2 = await tarea("B", 0.5)
    r3 = await tarea("C", 0.5)
    total = time.perf_counter() - inicio
    print(f"  Secuencial: {total:.2f}s (esperado ~1.5s)")
    return [r1, r2, r3]


async def correcto_concurrente():
    """BIEN: gather ejecuta todo concurrentemente."""
    inicio = time.perf_counter()
    r1, r2, r3 = await asyncio.gather(
        tarea("A", 0.5), tarea("B", 0.5), tarea("C", 0.5)
    )
    total = time.perf_counter() - inicio
    print(f"  Concurrente: {total:.2f}s (esperado ~0.5s)")
    return [r1, r2, r3]


# =============================================================================
# DEMOSTRACIÓN
# =============================================================================


async def main():
    print("=== Error 1: time.sleep vs asyncio.sleep ===")
    await correcto_asyncio_sleep()
    print()

    print("=== Error 2: Olvidar await ===")
    await error_sin_await()
    await correcto_con_await()
    print()

    print("=== Error 3: Secuencial vs Concurrente ===")
    await error_secuencial()
    await correcto_concurrente()
    print()

    print("=== Reglas ===")
    print("1. Nunca time.sleep() en async → usar asyncio.sleep()")
    print("2. Siempre await en funciones async")
    print("3. Usar gather() para múltiples tareas async")
    print("4. No usar requests → usar httpx.AsyncClient")


if __name__ == "__main__":
    asyncio.run(main())
