# Programación Asíncrona - Cheatsheet

Guía rápida de async/await con FastAPI y httpx.

---

## async/await Básico

```python
import asyncio

async def obtener_datos(fuente: str) -> dict:
    """Coroutine que simula I/O."""
    await asyncio.sleep(1)
    return {"fuente": fuente, "datos": [1, 2, 3]}

# Ejecutar una coroutine
resultado = asyncio.run(obtener_datos("api"))
```

---

## asyncio.gather: Concurrencia

```python
async def main():
    # Ejecuta todas las tareas concurrentemente
    resultados = await asyncio.gather(
        obtener_datos("ventas"),
        obtener_datos("clientes"),
        obtener_datos("stock"),
    )
    # resultados = [resultado1, resultado2, resultado3]
```

---

## FastAPI: Endpoints Async

```python
from fastapi import FastAPI

app = FastAPI()

# Async endpoint (I/O no bloqueante)
@app.get("/async")
async def leer_datos():
    datos = await obtener_datos("fuente")
    return datos

# Sync endpoint (FastAPI usa threadpool)
@app.get("/sync")
def calcular():
    return {"resultado": sum(range(1000))}
```

---

## gather en Endpoints

```python
@app.get("/dashboard")
async def dashboard():
    ventas, clientes = await asyncio.gather(
        obtener_ventas(),
        obtener_clientes(),
    )
    return {"ventas": ventas, "clientes": clientes}
```

---

## httpx: Cliente HTTP Async

```python
import httpx

# Llamada única
async with httpx.AsyncClient(timeout=10.0) as client:
    response = await client.get("https://api.com/datos")
    data = response.json()

# Múltiples llamadas concurrentes
async with httpx.AsyncClient(timeout=10.0) as client:
    tareas = [client.get(url) for url in urls]
    respuestas = await asyncio.gather(*tareas)
```

---

## Manejo de Errores

```python
import httpx

async def llamar_api(client: httpx.AsyncClient, url: str) -> dict:
    try:
        response = await client.get(url)
        response.raise_for_status()
        return {"ok": True, "datos": response.json()}
    except httpx.TimeoutException:
        return {"ok": False, "error": "Timeout"}
    except httpx.RequestError as e:
        return {"ok": False, "error": str(e)}
```

---

## Medir Tiempo

```python
import time

inicio = time.perf_counter()
resultados = await asyncio.gather(*tareas)
total = time.perf_counter() - inicio
print(f"Tiempo: {total:.2f}s")
```

---

## Equivalencias Sync → Async

| Síncrono | Asíncrono |
|----------|-----------|
| `def func()` | `async def func()` |
| `time.sleep(n)` | `await asyncio.sleep(n)` |
| `requests.get(url)` | `await client.get(url)` |
| `for item in items` | `async for item in items` |
| `with open(f)` | `async with aiofiles.open(f)` |

---

## Errores Comunes

```python
# MAL: bloquea el event loop
async def malo():
    time.sleep(5)           # Bloquea todo
    requests.get("https:…") # Bloquea todo

# BIEN: no bloquea
async def bueno():
    await asyncio.sleep(5)
    async with httpx.AsyncClient() as client:
        await client.get("https:…")
```

---

## Dependencias Necesarias

```bash
uv add httpx
```

- **httpx**: Cliente HTTP con soporte async/sync
- **asyncio**: Incluido en Python stdlib
- **FastAPI**: Ya soporta async nativamente

---

## Tips

1. **async no es paralelo**: es concurrente en un solo hilo
2. **gather** para ejecutar múltiples coroutines a la vez
3. **httpx.AsyncClient** siempre con `async with` (context manager)
4. **timeout** siempre configurar en clientes HTTP
5. **No mezclar** código bloqueante (requests, time.sleep) con async
6. **perf_counter** para medir tiempos (más preciso que time.time)
