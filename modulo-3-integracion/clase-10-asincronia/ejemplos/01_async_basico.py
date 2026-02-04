"""
Async/Await Básico
===================
Fundamentos de programación asíncrona con asyncio.

Ejecutar:
    python ejemplos/01_async_basico.py

Conceptos:
    - async def para definir coroutines
    - await para esperar resultados
    - asyncio.gather para concurrencia
    - Comparación sync vs async en tiempo
"""

import asyncio
import time


# =============================================================================
# FUNCIONES SÍNCRONAS (bloqueantes)
# =============================================================================


def tarea_sync(nombre: str, segundos: float) -> str:
    """Simula una tarea bloqueante."""
    print(f"  [sync] {nombre}: iniciando ({segundos}s)")
    time.sleep(segundos)
    print(f"  [sync] {nombre}: completada")
    return f"Resultado de {nombre}"


def ejecutar_sync():
    """Ejecuta tareas secuencialmente."""
    inicio = time.perf_counter()
    r1 = tarea_sync("API_1", 1.0)
    r2 = tarea_sync("API_2", 1.5)
    r3 = tarea_sync("API_3", 0.5)
    total = time.perf_counter() - inicio
    print(f"  Sync total: {total:.2f}s\n")
    return [r1, r2, r3]


# =============================================================================
# FUNCIONES ASÍNCRONAS (no bloqueantes)
# =============================================================================


async def tarea_async(nombre: str, segundos: float) -> str:
    """Simula una tarea asíncrona (no bloquea)."""
    print(f"  [async] {nombre}: iniciando ({segundos}s)")
    await asyncio.sleep(segundos)  # No bloquea el event loop
    print(f"  [async] {nombre}: completada")
    return f"Resultado de {nombre}"


async def ejecutar_async():
    """Ejecuta tareas concurrentemente con gather."""
    inicio = time.perf_counter()
    r1, r2, r3 = await asyncio.gather(
        tarea_async("API_1", 1.0),
        tarea_async("API_2", 1.5),
        tarea_async("API_3", 0.5),
    )
    total = time.perf_counter() - inicio
    print(f"  Async total: {total:.2f}s\n")
    return [r1, r2, r3]


# =============================================================================
# DEMOSTRACIÓN
# =============================================================================


if __name__ == "__main__":
    print("=== Ejecución Síncrona (secuencial) ===")
    resultados_sync = ejecutar_sync()

    print("=== Ejecución Asíncrona (concurrente) ===")
    resultados_async = asyncio.run(ejecutar_async())

    print("=== Resultados ===")
    print(f"Sync: {resultados_sync}")
    print(f"Async: {resultados_async}")
    print("\nLos resultados son iguales, pero async es ~3x más rápido")
