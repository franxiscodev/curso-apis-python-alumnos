"""
httpx Async: Llamadas HTTP Concurrentes
=========================================
Cliente HTTP asíncrono para llamar APIs externas.

Ejecutar:
    python ejemplos/03_httpx_async.py

Conceptos:
    - httpx.AsyncClient vs requests
    - Llamadas concurrentes con gather
    - Context manager async (async with)
    - Medición de rendimiento
"""

import asyncio
import time

import httpx


# =============================================================================
# LLAMADA INDIVIDUAL
# =============================================================================


async def obtener_url(client: httpx.AsyncClient, url: str) -> dict:
    """Obtiene datos de una URL de forma asíncrona."""
    response = await client.get(url)
    return {
        "url": url,
        "status": response.status_code,
        "tamaño": len(response.content)
    }


# =============================================================================
# LLAMADAS CONCURRENTES
# =============================================================================


async def llamadas_concurrentes(urls: list[str]) -> list[dict]:
    """Llama a múltiples URLs concurrentemente."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        tareas = [obtener_url(client, url) for url in urls]
        return await asyncio.gather(*tareas)


# =============================================================================
# LLAMADAS SECUENCIALES (para comparar)
# =============================================================================


async def llamadas_secuenciales(urls: list[str]) -> list[dict]:
    """Llama a URLs una por una (para comparar)."""
    resultados = []
    async with httpx.AsyncClient(timeout=10.0) as client:
        for url in urls:
            resultado = await obtener_url(client, url)
            resultados.append(resultado)
    return resultados


# =============================================================================
# DEMOSTRACIÓN
# =============================================================================


async def main():
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
    ]

    print(f"Llamando a {len(urls)} URLs...\n")

    # Secuencial
    print("=== Secuencial ===")
    inicio = time.perf_counter()
    resultados_seq = await llamadas_secuenciales(urls)
    tiempo_seq = time.perf_counter() - inicio
    print(f"Tiempo: {tiempo_seq:.2f}s")
    for r in resultados_seq:
        print(f"  {r['url']}: {r['status']}")

    # Concurrente
    print("\n=== Concurrente ===")
    inicio = time.perf_counter()
    resultados_con = await llamadas_concurrentes(urls)
    tiempo_con = time.perf_counter() - inicio
    print(f"Tiempo: {tiempo_con:.2f}s")
    for r in resultados_con:
        print(f"  {r['url']}: {r['status']}")

    print(f"\nAhorro: {tiempo_seq - tiempo_con:.2f}s "
          f"({tiempo_seq / tiempo_con:.1f}x más rápido)")


if __name__ == "__main__":
    asyncio.run(main())
