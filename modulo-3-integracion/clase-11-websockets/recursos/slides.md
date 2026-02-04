---
marp: true
theme: default
paginate: true
header: 'Clase 11: WebSockets y Real-time'
footer: 'Curso APIs Avanzadas con Python'
---

# WebSockets y Real-time
## Comunicación bidireccional

Clase 11 - Módulo 3: Integración y Asincronía

---

# HTTP vs WebSocket

| HTTP | WebSocket |
|------|-----------|
| Solicitud → Respuesta | Bidireccional |
| Conexión se cierra | Conexión persistente |
| Cliente inicia | Ambos inician |
| Stateless | Stateful |

**HTTP** = enviar cartas | **WebSocket** = llamada telefónica

---

# WebSocket en FastAPI

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            mensaje = await websocket.receive_text()
            await websocket.send_text(f"Echo: {mensaje}")
    except WebSocketDisconnect:
        print("Cliente desconectado")
```

---

# Flujo WebSocket

```
Cliente                    Servidor
  |--- Upgrade HTTP -------->|
  |<-- 101 Switching --------|
  |                          |
  |--- send("hola") -------->|
  |<-- send("Echo: hola") ---|
  |--- send("mundo") ------->|
  |<-- send("Echo: mundo") --|
  |                          |
  |--- close() ------------->|
```

---

# ConnectionManager

```python
class ConnectionManager:
    def __init__(self):
        self.conexiones: list[WebSocket] = []

    async def conectar(self, ws: WebSocket):
        await ws.accept()
        self.conexiones.append(ws)

    def desconectar(self, ws: WebSocket):
        self.conexiones.remove(ws)

    async def broadcast(self, mensaje: str):
        for conn in self.conexiones:
            await conn.send_text(mensaje)
```

---

# Salas (Rooms)

```python
class RoomManager:
    def __init__(self):
        self.salas: dict[str, list[WebSocket]] = {}

    async def unirse(self, sala: str, ws: WebSocket):
        await ws.accept()
        self.salas.setdefault(sala, []).append(ws)

    async def broadcast_sala(self, sala: str, msg: str):
        for ws in self.salas.get(sala, []):
            await ws.send_text(msg)
```

Cada sala es un grupo independiente de conexiones

---

# Server-Sent Events (SSE)

```python
from fastapi.responses import StreamingResponse

async def generar_eventos():
    while True:
        yield f"data: {json.dumps(dato)}\n\n"
        await asyncio.sleep(1)

@app.get("/sse/stream")
async def stream():
    return StreamingResponse(
        generar_eventos(),
        media_type="text/event-stream"
    )
```

Unidireccional: servidor → cliente

---

# WebSocket vs SSE

| Característica | WebSocket | SSE |
|---------------|-----------|-----|
| Dirección | Bidireccional | Servidor → Cliente |
| Protocolo | ws:// | HTTP |
| Reconexión | Manual | Automática |
| Complejidad | Mayor | Menor |
| Uso | Chat, juegos | Feeds, métricas |

---

# Resumen

| Concepto | Herramienta |
|----------|-------------|
| WebSocket básico | `@app.websocket("/ws")` |
| Aceptar conexión | `await ws.accept()` |
| Recibir | `await ws.receive_text()` |
| Enviar | `await ws.send_text()` |
| Desconexión | `except WebSocketDisconnect` |
| Broadcasting | `ConnectionManager` |
| Salas | `dict[str, list[WebSocket]]` |
| SSE | `StreamingResponse` |

---

# Próxima Clase

**Clase 12: Integraciones Externas**

- httpx avanzado y circuit breakers
- Celery + Redis para tareas en background
- Resiliencia en servicios distribuidos

---

# Recursos

- **FastAPI WebSockets**: https://fastapi.tiangolo.com/advanced/websockets/
- **MDN WebSocket API**: https://developer.mozilla.org/en-US/docs/Web/API/WebSocket

**Practica:**
```bash
uvicorn ejemplos.api_chat:app --reload
```
