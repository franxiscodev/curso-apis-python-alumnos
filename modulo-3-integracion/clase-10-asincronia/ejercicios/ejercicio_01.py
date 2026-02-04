"""
Ejercicio 01: Funciones Async Básicas
=======================================
Practicar async/await y asyncio.gather.

OBJETIVO:
Entender la diferencia entre ejecución secuencial y concurrente.

INSTRUCCIONES:
1. Implementar descargar_datos(fuente, segundos):
   - Función async que simula una descarga con asyncio.sleep
   - Retorna {"fuente": fuente, "datos": f"datos de {fuente}"}

2. Implementar descargas_secuenciales(fuentes):
   - Llama a descargar_datos para cada fuente, una por una
   - Mide el tiempo total

3. Implementar descargas_concurrentes(fuentes):
   - Usa asyncio.gather para llamar a todas las fuentes a la vez
   - Mide el tiempo total

4. Comparar tiempos en el main

PRUEBAS:
    python ejercicio_01.py

    # Debe mostrar:
    # Secuencial: ~3.0s (suma de todos)
    # Concurrente: ~1.0s (el máximo de todos)

PISTAS:
- asyncio.sleep(segundos) para simular I/O
- asyncio.gather(*tareas) para ejecutar concurrentemente
- time.perf_counter() para medir tiempo
"""

import asyncio
import time


fuentes = [
    ("API_ventas", 1.0),
    ("API_clientes", 0.8),
    ("API_inventario", 0.5),
    ("BD_reportes", 0.7),
]


# TODO: Implementar descargar_datos(fuente: str, segundos: float) -> dict


# TODO: Implementar descargas_secuenciales(fuentes) -> tuple[list, float]
# Retorna (resultados, tiempo_total)


# TODO: Implementar descargas_concurrentes(fuentes) -> tuple[list, float]
# Retorna (resultados, tiempo_total)


async def main():
    print("=== Secuencial ===")
    # resultados, tiempo = await descargas_secuenciales(fuentes)
    # print(f"Tiempo: {tiempo:.2f}s, Resultados: {len(resultados)}")

    print("\n=== Concurrente ===")
    # resultados, tiempo = await descargas_concurrentes(fuentes)
    # print(f"Tiempo: {tiempo:.2f}s, Resultados: {len(resultados)}")


if __name__ == "__main__":
    asyncio.run(main())
