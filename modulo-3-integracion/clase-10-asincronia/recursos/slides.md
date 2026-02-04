---
marp: true
theme: default
paginate: true
header: 'Clase 10: Programación Asíncrona'
footer: 'Curso APIs Avanzadas con Python'
---

# Programación Asíncrona
## async/await, gather y httpx

Clase 10 - Módulo 3: Integración y Asincronía

---

# ¿Síncrono vs Asíncrono?

| Síncrono | Asíncrono |
|----------|-----------|
| Una tarea a la vez | Múltiples tareas concurrentes |
| Espera bloqueante | Espera no bloqueante |
| `time.sleep()` | `asyncio.sleep()` |
| `requests.get()` | `httpx.AsyncClient.get()` |

**Analogía**: Cocinar un plato a la vez vs cocinar varios mientras esperas

---

# async/await Básico

```python
import asyncio

async def descargar(url: str) -> str:
    print(f"Descargando {url}...")
    await asyncio.sleep(1)  # Simula I/O
    return f"Datos de {url}"

# Ejecutar
resultado = asyncio.run(descargar("https://api.com"))
```

- `async def` → define una coroutine
- `await` → espera sin bloquear el hilo

---

# asyncio.gather: Concurrencia

```python
async def main():
    # Secuencial: 3 segundos
    r1 = await descargar("api1")
    r2 = await descargar("api2")
    r3 = await descargar("api3")

    # Concurrente: ~1 segundo
    r1, r2, r3 = await asyncio.gather(
        descargar("api1"),
        descargar("api2"),
        descargar("api3"),
    )
```

**gather** ejecuta todas las tareas concurrentemente

---

# FastAPI: async vs def

```python
# Async - FastAPI lo ejecuta directamente
@app.get("/async")
async def endpoint_async():
    await asyncio.sleep(1)
    return {"tipo": "async"}

# Sync - FastAPI lo ejecuta en threadpool
@app.get("/sync")
def endpoint_sync():
    time.sleep(1)
    return {"tipo": "sync"}
```

Ambos funcionan, pero **async** es más eficiente para I/O

---

# gather en Endpoints

```python
@app.get("/dashboard")
async def dashboard():
    ventas, clientes, stock = await asyncio.gather(
        obtener_ventas(),
        obtener_clientes(),
        obtener_stock(),
    )
    return {
        "ventas": ventas,
        "clientes": clientes,
        "stock": stock
    }
```

3 consultas que tardan 0.5s cada una → **0.5s total** en vez de 1.5s

---

# httpx: Cliente HTTP Async

```python
import httpx

async with httpx.AsyncClient(timeout=10.0) as client:
    # Una llamada
    resp = await client.get("https://api.com/datos")

    # Múltiples concurrentes
    tareas = [
        client.get("https://api1.com"),
        client.get("https://api2.com"),
    ]
    respuestas = await asyncio.gather(*tareas)
```

**httpx** = requests + async support

---

# Errores Comunes

| Error | Problema | Solución |
|-------|----------|----------|
| `time.sleep()` en async | Bloquea el event loop | `asyncio.sleep()` |
| `requests.get()` en async | Bloquea el event loop | `httpx.AsyncClient` |
| Olvidar `await` | Retorna coroutine, no resultado | Siempre `await` |
| `await` secuencial | No aprovecha concurrencia | `asyncio.gather()` |

---

# ¿Cuándo usar async?

**Sí usar async:**
- Llamadas HTTP externas
- Lectura de archivos
- Queries a base de datos
- Cualquier operación I/O

**No necesitas async:**
- Cálculos en memoria (CPU-bound)
- Endpoints simples sin I/O
- Lógica de negocio pura

---

# Resumen

| Concepto | Herramienta |
|----------|-------------|
| Coroutines | `async def` + `await` |
| Concurrencia | `asyncio.gather()` |
| HTTP async | `httpx.AsyncClient` |
| Endpoints | `async def endpoint()` |
| Medir tiempo | `time.perf_counter()` |

---

# Próxima Clase

**Clase 11: WebSockets y Real-time**

- Comunicación bidireccional
- Broadcasting y salas
- Server-Sent Events (SSE)

---

# Recursos

- **asyncio docs**: https://docs.python.org/3/library/asyncio.html
- **httpx docs**: https://www.python-httpx.org
- **FastAPI async**: https://fastapi.tiangolo.com/async/

**Practica:**
```bash
uvicorn ejemplos.api_agregador:app --reload
```
