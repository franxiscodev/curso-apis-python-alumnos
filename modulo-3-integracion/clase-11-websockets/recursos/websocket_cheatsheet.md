# WebSockets y Real-time - Cheatsheet

Guía rápida de WebSockets y SSE con FastAPI.

---

## WebSocket Básico

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
        print("Desconectado")
```

---

## ConnectionManager

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

manager = ConnectionManager()
```

---

## Salas (Rooms)

```python
class RoomManager:
    def __init__(self):
        self.salas: dict[str, list[WebSocket]] = {}

    async def unirse(self, sala: str, ws: WebSocket):
        await ws.accept()
        self.salas.setdefault(sala, []).append(ws)

    def salir(self, sala: str, ws: WebSocket):
        if sala in self.salas:
            self.salas[sala].remove(ws)
            if not self.salas[sala]:
                del self.salas[sala]

    async def broadcast_sala(self, sala: str, msg: str):
        for ws in self.salas.get(sala, []):
            await ws.send_text(msg)
```

---

## WebSocket con Path Parameters

```python
@app.websocket("/ws/{sala}/{usuario}")
async def ws_chat(ws: WebSocket, sala: str, usuario: str):
    await ws.accept()
    try:
        while True:
            texto = await ws.receive_text()
            # Procesar mensaje...
    except WebSocketDisconnect:
        pass
```

---

## Server-Sent Events (SSE)

```python
import asyncio
import json
from typing import AsyncGenerator
from fastapi.responses import StreamingResponse

async def generar_eventos() -> AsyncGenerator[str, None]:
    while True:
        dato = {"valor": 42}
        yield f"data: {json.dumps(dato)}\n\n"
        await asyncio.sleep(1)

@app.get("/sse/stream")
async def stream():
    return StreamingResponse(
        generar_eventos(),
        media_type="text/event-stream"
    )
```

---

## Cliente JavaScript: WebSocket

```javascript
const ws = new WebSocket("ws://localhost:8000/ws");

ws.onopen = () => console.log("Conectado");
ws.onmessage = (e) => console.log("Mensaje:", e.data);
ws.onclose = () => console.log("Desconectado");

ws.send("Hola servidor");
```

---

## Cliente JavaScript: SSE

```javascript
const es = new EventSource("/sse/stream");

es.onmessage = (e) => {
    const datos = JSON.parse(e.data);
    console.log(datos);
};

// Cerrar conexión
es.close();
```

---

## Métodos WebSocket en FastAPI

| Método | Descripción |
|--------|-------------|
| `await ws.accept()` | Aceptar conexión |
| `await ws.receive_text()` | Recibir texto |
| `await ws.receive_json()` | Recibir JSON |
| `await ws.send_text(msg)` | Enviar texto |
| `await ws.send_json(data)` | Enviar JSON |
| `await ws.close()` | Cerrar conexión |

---

## Cuándo usar cada uno

| Necesidad | Protocolo |
|-----------|-----------|
| Chat, colaboración | WebSocket |
| Notificaciones push | WebSocket o SSE |
| Dashboard en vivo | SSE |
| Feed de datos | SSE |
| Juegos multijugador | WebSocket |
| Progreso de tareas | SSE |

---

## Tips

1. **Siempre** manejar `WebSocketDisconnect` con try/except
2. **ConnectionManager** como patrón estándar para broadcasting
3. **SSE** reconecta automáticamente en el navegador
4. **JSON** con `send_json()`/`receive_json()` para datos estructurados
5. **Salas** con diccionario para dirigir mensajes a grupos
6. **Limpiar** conexiones al desconectar para evitar memory leaks
