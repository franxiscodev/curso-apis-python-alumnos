"""
Ejemplo 02: Broadcasting con ConnectionManager
================================================
Enviar mensajes a todos los clientes conectados.

Ejecutar:
    uvicorn ejemplos.02_broadcasting:app --reload
    Abrir http://127.0.0.1:8000 en varias pestañas
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI(title="Broadcasting", version="1.0.0")


# === CONNECTION MANAGER ===


class ConnectionManager:
    """Gestiona conexiones WebSocket activas."""

    def __init__(self):
        self.conexiones: list[WebSocket] = []

    async def conectar(self, websocket: WebSocket):
        await websocket.accept()
        self.conexiones.append(websocket)

    def desconectar(self, websocket: WebSocket):
        self.conexiones.remove(websocket)

    async def broadcast(self, mensaje: str):
        """Envía mensaje a todos los clientes conectados."""
        for conexion in self.conexiones:
            await conexion.send_text(mensaje)


manager = ConnectionManager()

# === HTML DE PRUEBA ===

HTML_CLIENTE = """
<!DOCTYPE html>
<html><head><title>Broadcast Chat</title></head>
<body>
<h2>Broadcast Chat</h2>
<p>Conectados: abre varias pestañas para probar</p>
<input id="msg" type="text" placeholder="Mensaje...">
<button onclick="enviar()">Enviar</button>
<ul id="log"></ul>
<script>
const ws = new WebSocket("ws://localhost:8000/ws");
ws.onmessage = (e) => {
    const li = document.createElement("li");
    li.textContent = e.data;
    document.getElementById("log").appendChild(li);
};
function enviar() {
    const input = document.getElementById("msg");
    ws.send(input.value);
    input.value = "";
}
</script></body></html>
"""


@app.get("/", response_class=HTMLResponse)
async def pagina():
    return HTML_CLIENTE


@app.get("/conectados", tags=["Estado"])
async def conectados():
    """Número de clientes conectados."""
    return {"conectados": len(manager.conexiones)}


# === WEBSOCKET CON BROADCAST ===


@app.websocket("/ws")
async def websocket_broadcast(websocket: WebSocket):
    """Cada mensaje se reenvía a todos los clientes."""
    await manager.conectar(websocket)
    try:
        while True:
            mensaje = await websocket.receive_text()
            await manager.broadcast(f"Anónimo: {mensaje}")
    except WebSocketDisconnect:
        manager.desconectar(websocket)
        await manager.broadcast("Un usuario se ha desconectado")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
