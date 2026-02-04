# Integraciones Externas - Cheatsheet

Guía rápida de httpx avanzado, circuit breaker y background tasks.

---

## httpx con Timeouts

```python
import httpx

TIMEOUT = httpx.Timeout(connect=5.0, read=10.0, write=5.0, pool=5.0)

async with httpx.AsyncClient(timeout=TIMEOUT) as client:
    response = await client.get("https://api.com/datos")
```

---

## Retry con Backoff

```python
async def get_con_retry(client, url, intentos=3, backoff=1.0):
    for i in range(intentos):
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp
        except (httpx.TimeoutException, httpx.ConnectError):
            if i < intentos - 1:
                await asyncio.sleep(backoff * (2 ** i))
    return None
```

---

## Manejo de Errores httpx

```python
try:
    response = await client.get(url)
    response.raise_for_status()
except httpx.TimeoutException:
    ...  # Timeout (connect o read)
except httpx.ConnectError:
    ...  # No se puede conectar
except httpx.HTTPStatusError as e:
    status = e.response.status_code
    if status >= 500:
        ...  # Error del servidor
    else:
        ...  # Error del cliente (4xx)
```

---

## Circuit Breaker

```python
class CircuitBreaker:
    def __init__(self, nombre, umbral=3, recuperacion=30):
        self.nombre = nombre
        self.umbral = umbral
        self.recuperacion = recuperacion
        self.estado = "cerrado"
        self.fallos = 0
        self.ultimo_fallo = 0

    async def ejecutar(self, coroutine):
        if self.estado == "abierto":
            if time.time() - self.ultimo_fallo > self.recuperacion:
                self.estado = "semi_abierto"
            else:
                return None  # Falla rápido
        try:
            resultado = await coroutine
            self.fallos = 0
            self.estado = "cerrado"
            return resultado
        except Exception:
            self.fallos += 1
            self.ultimo_fallo = time.time()
            if self.fallos >= self.umbral:
                self.estado = "abierto"
            return None
```

---

## Background Tasks

```python
from fastapi import BackgroundTasks

def tarea_lenta(param1: str, param2: int):
    time.sleep(5)
    print(f"Completado: {param1}, {param2}")

@app.post("/accion")
async def endpoint(bg: BackgroundTasks):
    bg.add_task(tarea_lenta, "valor1", 42)
    return {"mensaje": "Tarea en proceso"}
```

---

## Cola con asyncio.Queue

```python
cola = asyncio.Queue(maxsize=100)

# Productor
await cola.put({"tipo": "email", "datos": {...}})

# Consumidor (worker)
async def worker():
    while True:
        tarea = await cola.get()
        await procesar(tarea)
        cola.task_done()

# Iniciar worker
asyncio.create_task(worker())
```

---

## Fallback con Caché

```python
cache: dict[str, list] = {}

async def consultar_con_fallback(client, fuente, url):
    try:
        resp = await client.get(url)
        datos = resp.json()
        cache[fuente] = datos  # Actualizar caché
        return {"datos": datos, "origen": "api"}
    except Exception:
        if fuente in cache:
            return {"datos": cache[fuente], "origen": "cache"}
        return {"datos": None, "origen": "sin_datos"}
```

---

## Patrones de Resiliencia

| Patrón | Problema | Solución |
|--------|----------|----------|
| Retry | Fallo transitorio | Reintentar con backoff |
| Timeout | Servicio lento | Límite de tiempo |
| Circuit Breaker | Servicio caído | Fallar rápido |
| Fallback | Sin respuesta | Caché o valor default |
| Bulkhead | Fallo en cascada | Aislar servicios |

---

## Dependencias

```bash
uv add httpx
```

---

## Tips

1. **Siempre** configurar timeouts en clientes HTTP
2. **Backoff exponencial** para no saturar un servicio caído
3. **Circuit breaker** por servicio, no global
4. **BackgroundTasks** para tareas que no necesitan respuesta
5. **Caché** como fallback cuando el servicio externo falla
6. **Logs** en background para no ralentizar la respuesta
