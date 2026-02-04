"""
Ejercicio 01: Cliente HTTP Resiliente
=======================================
Crear un cliente httpx con retry y manejo de errores.

OBJETIVO:
Practicar httpx avanzado con reintentos y timeouts.

INSTRUCCIONES:
1. Implementar función get_con_retry(client, url, max_intentos, backoff):
   - Intenta GET hasta max_intentos veces
   - Backoff exponencial entre intentos
   - Retorna response o None si todos fallan

2. Implementar GET /consultar:
   - Recibe query param "url"
   - Usa get_con_retry para llamar a la URL
   - Retorna status, tamaño y tiempo

3. Implementar GET /consultar-multiple:
   - Consulta varias URLs predefinidas concurrentemente
   - Retorna resultados de todas

PRUEBAS:
    uvicorn ejercicio_01:app --reload

    GET /consultar?url=https://httpbin.org/get
    GET /consultar-multiple

PISTAS:
- httpx.Timeout(connect=5, read=10) para timeouts
- backoff exponencial: espera = base * (2 ** intento)
- httpx.TimeoutException, httpx.ConnectError para errores
"""

import httpx
from fastapi import FastAPI

app = FastAPI(title="Cliente Resiliente", version="1.0.0")

URLS = {
    "httpbin": "https://httpbin.org/get",
    "jsonplaceholder": "https://jsonplaceholder.typicode.com/posts/1",
}

# TODO: Implementar get_con_retry(client, url, max_intentos, backoff)

# TODO: GET /consultar (query param url, usa get_con_retry)

# TODO: GET /consultar-multiple (consulta URLS concurrentemente)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
