"""
Ejercicio 03: API Agregadora con httpx
========================================
API que consulta APIs externas concurrentemente.

OBJETIVO:
Integrar httpx async con FastAPI para llamadas externas.

INSTRUCCIONES:
1. Implementar GET /consultar/{servicio}:
   - Usa httpx.AsyncClient para llamar a una URL externa
   - Retorna status code y tamaño de la respuesta

2. Implementar GET /consultar-todos:
   - Llama a múltiples URLs concurrentemente con gather
   - Retorna resultados de todas y tiempo total

3. Implementar GET /mas-rapido:
   - Llama a múltiples URLs pero retorna solo la primera
   - Usa asyncio.wait con FIRST_COMPLETED (o gather y tomar la primera)

PRUEBAS:
    uvicorn ejercicio_03:app --reload

    GET /consultar/httpbin
    GET /consultar-todos
    GET /mas-rapido

PISTAS:
- async with httpx.AsyncClient() as client: ...
- await client.get(url)
- asyncio.gather(*tareas) para concurrencia
"""

from fastapi import FastAPI

app = FastAPI(title="API Agregadora", version="1.0.0")


SERVICIOS = {
    "httpbin": "https://httpbin.org/get",
    "jsonplaceholder": "https://jsonplaceholder.typicode.com/posts/1",
}

# TODO: Importar httpx, asyncio, time

# TODO: GET /consultar/{servicio} (async, usa httpx)

# TODO: GET /consultar-todos (async, gather con httpx)

# TODO: GET /mas-rapido (async, retorna el primero en responder)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
