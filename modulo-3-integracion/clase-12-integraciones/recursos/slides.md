---
marp: true
theme: default
paginate: true
header: 'Clase 12: Integraciones Externas'
footer: 'Curso APIs Avanzadas con Python'
---

# Integraciones Externas
## Resiliencia y Background Tasks

Clase 12 - Módulo 3: Integración y Asincronía

---

# El Problema

Tu API depende de servicios externos que pueden:

- **Tardar** más de lo esperado (timeouts)
- **Fallar** con errores 500
- **Caerse** completamente

Tu API debe seguir funcionando

---

# httpx Avanzado

```python
import httpx

TIMEOUT = httpx.Timeout(
    connect=5.0,    # Conexión
    read=10.0,      # Respuesta
)

async with httpx.AsyncClient(timeout=TIMEOUT) as client:
    try:
        resp = await client.get(url)
        resp.raise_for_status()
    except httpx.TimeoutException:
        ...  # Timeout
    except httpx.HTTPStatusError:
        ...  # Error HTTP (4xx, 5xx)
```

---

# Retry con Backoff Exponencial

```python
async def get_con_retry(client, url, intentos=3):
    for i in range(intentos):
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp
        except (httpx.TimeoutException, httpx.ConnectError):
            if i < intentos - 1:
                await asyncio.sleep(1 * (2 ** i))
                # 1s, 2s, 4s...
    return None
```

---

# Circuit Breaker

```
     CERRADO ──(N fallos)──→ ABIERTO
        ↑                       │
        │                  (timeout)
        │                       ↓
        └───(éxito)──── SEMI-ABIERTO
```

| Estado | Comportamiento |
|--------|---------------|
| Cerrado | Llamadas pasan normalmente |
| Abierto | Falla inmediato (sin espera) |
| Semi-abierto | Prueba una llamada |

---

# Circuit Breaker: Código

```python
class CircuitBreaker:
    def __init__(self, umbral=3, recuperacion=30):
        self.estado = "cerrado"
        self.fallos = 0

    async def ejecutar(self, coroutine):
        if self.estado == "abierto":
            if time.time() - self.ultimo > self.recuperacion:
                self.estado = "semi_abierto"
            else:
                return None  # Fallback
        try:
            resultado = await coroutine
            self.fallos = 0
            return resultado
        except Exception:
            self.fallos += 1
```

---

# Background Tasks

```python
from fastapi import BackgroundTasks

def enviar_email(dest: str, asunto: str):
    time.sleep(2)  # Tarea lenta
    print(f"Email enviado a {dest}")

@app.post("/pedidos")
async def crear_pedido(
    pedido: Pedido,
    bg: BackgroundTasks
):
    bg.add_task(enviar_email, pedido.email, "Confirmación")
    return {"mensaje": "Pedido recibido"}
    # Email se envía DESPUÉS de responder
```

---

# BackgroundTasks vs Celery

| Característica | BackgroundTasks | Celery |
|---------------|----------------|--------|
| Complejidad | Baja | Alta |
| Persistencia | No | Sí (Redis/RabbitMQ) |
| Reintentos | No | Sí |
| Distribución | No | Sí (workers) |
| Ideal para | Emails, logs | ETL, ML, reportes |

---

# Patrones de Resiliencia

| Patrón | Qué hace |
|--------|----------|
| **Retry** | Reintentar N veces con backoff |
| **Timeout** | Límite de tiempo por petición |
| **Circuit Breaker** | Fallar rápido si servicio está caído |
| **Fallback** | Valor alternativo (caché) |
| **Bulkhead** | Aislar servicios entre sí |

---

# Resumen

| Concepto | Herramienta |
|----------|-------------|
| HTTP async | `httpx.AsyncClient` |
| Timeouts | `httpx.Timeout` |
| Retry | Backoff exponencial |
| Circuit Breaker | Clase custom / tenacity |
| Background | `BackgroundTasks` |
| Colas | `asyncio.Queue` / Celery |

---

# Próximo Módulo

**Módulo 4: Producción y Escalabilidad**

- Testing comprehensivo
- Containerización y CI/CD
- Observabilidad y proyecto final

---

# Recursos

- **httpx**: https://www.python-httpx.org
- **tenacity**: https://tenacity.readthedocs.io
- **Circuit Breaker**: https://martinfowler.com/bliki/CircuitBreaker.html

**Practica:**
```bash
uvicorn ejemplos.api_integradora:app --reload
```
