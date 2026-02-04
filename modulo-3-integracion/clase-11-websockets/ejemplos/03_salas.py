"""
Ejemplo 03: Salas (Rooms) de WebSocket
=======================================
Mensajes dirigidos a grupos específicos de clientes.

Ejecutar:
    uvicorn ejemplos.03_salas:app --reload
    Abrir http://127.0.0.1:8000 en el navegador
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI(title="WebSocket Salas", version="1.0.0")


# === ROOM MANAGER ===


class RoomManager:
    """Gestiona salas de WebSocket."""

    def __init__(self):
        self.salas: dict[str, list[WebSocket]] = {}

    async def unirse(self, sala: str, websocket: WebSocket):
        await websocket.accept()
        if sala not in self.salas:
            self.salas[sala] = []
        self.salas[sala].append(websocket)

    def salir(self, sala: str, websocket: WebSocket):
        if sala in self.salas:
            self.salas[sala].remove(websocket)
            if not self.salas[sala]:
                del self.salas[sala]

    async def broadcast_sala(self, sala: str, mensaje: str):
        """Envía mensaje solo a los clientes de una sala."""
        for conexion in self.salas.get(sala, []):
            await conexion.send_text(mensaje)


rooms = RoomManager()

HTML_CLIENTE = """
<!DOCTYPE html>
<html><head><title>Salas</title></head>
<body>
<h2>WebSocket Salas</h2>
<label>Sala: <input id="sala" value="general"></label>
<button onclick="conectar()">Conectar</button>
<br><br>
<input id="msg" type="text" placeholder="Mensaje..." disabled>
<button id="btnEnviar" onclick="enviar()" disabled>Enviar</button>
<ul id="log"></ul>
<script>
let ws;
function conectar() {
    const sala = document.getElementById("sala").value;
    ws = new WebSocket(`ws://localhost:8000/ws/${sala}`);
    ws.onmessage = (e) => {
        const li = document.createElement("li");
        li.textContent = e.data;
        document.getElementById("log").appendChild(li);
    };
    ws.onopen = () => {
        document.getElementById("msg").disabled = false;
        document.getElementById("btnEnviar").disabled = false;
    };
}
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


@app.get("/salas", tags=["Estado"])
async def listar_salas():
    """Lista salas activas y cantidad de usuarios."""
    return {sala: len(conns) for sala, conns in rooms.salas.items()}


# === WEBSOCKET CON SALAS ===


@app.websocket("/ws/{sala}")
async def websocket_sala(websocket: WebSocket, sala: str):
    """Conecta al cliente a una sala específica."""
    await rooms.unirse(sala, websocket)
    await rooms.broadcast_sala(sala, f"[{sala}] Nuevo usuario conectado")
    try:
        while True:
            mensaje = await websocket.receive_text()
            await rooms.broadcast_sala(sala, f"[{sala}] {mensaje}")
    except WebSocketDisconnect:
        rooms.salir(sala, websocket)
        await rooms.broadcast_sala(sala, f"[{sala}] Usuario desconectado")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
