"""
Ejemplo 01: httpx Avanzado
===========================
Timeouts, retries y manejo de errores robusto.

Ejecutar:
    python ejemplos/01_httpx_avanzado.py
"""

import asyncio
import time

import httpx


# === CONFIGURACIÓN DE TIMEOUTS ===

TIMEOUT = httpx.Timeout(
    connect=5.0,   # Tiempo para establecer conexión
    read=10.0,     # Tiempo para recibir respuesta
    write=5.0,     # Tiempo para enviar request
    pool=5.0,      # Tiempo esperando conexión del pool
)


# === CLIENTE CON RETRY ===


async def get_con_retry(
    client: httpx.AsyncClient,
    url: str,
    max_intentos: int = 3,
    backoff: float = 1.0,
) -> httpx.Response | None:
    """GET con reintentos y backoff exponencial."""
    for intento in range(1, max_intentos + 1):
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response
        except httpx.TimeoutException:
            print(f"  Intento {intento}: Timeout")
        except httpx.ConnectError:
            print(f"  Intento {intento}: Error de conexión")
        except httpx.HTTPStatusError as e:
            print(f"  Intento {intento}: HTTP {e.response.status_code}")
            if e.response.status_code < 500:
                return None  # No reintentar errores 4xx

        if intento < max_intentos:
            espera = backoff * (2 ** (intento - 1))
            print(f"  Esperando {espera}s antes de reintentar...")
            await asyncio.sleep(espera)

    print(f"  Falló después de {max_intentos} intentos")
    return None


# === MÚLTIPLES SERVICIOS ===


async def consultar_servicios():
    """Consulta múltiples servicios con manejo de errores."""
    urls = {
        "httpbin": "https://httpbin.org/get",
        "jsonplaceholder": "https://jsonplaceholder.typicode.com/posts/1",
        "inexistente": "https://servicio-que-no-existe.xyz/api",
    }

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        for nombre, url in urls.items():
            print(f"\nConsultando {nombre}...")
            inicio = time.perf_counter()
            response = await get_con_retry(client, url)
            elapsed = time.perf_counter() - inicio

            if response:
                print(f"  OK: {response.status_code} ({elapsed:.2f}s)")
            else:
                print(f"  FALLÓ ({elapsed:.2f}s)")


async def main():
    print("=== httpx con Retry y Timeouts ===")
    await consultar_servicios()


if __name__ == "__main__":
    asyncio.run(main())
