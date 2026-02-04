"""
API Chat: Aplicación de Chat con Salas
========================================
Integra WebSocket + salas + historial + endpoints REST.

Ejecutar:
    uvicorn ejemplos.api_chat:app --reload
"""

from datetime import datetime, timezone

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI(title="Chat API", version="1.0.0")


# === CHAT MANAGER ===


class ChatManager:
    """Gestiona salas, conexiones y historial."""

    def __init__(self):
        self.salas: dict[str, list[WebSocket]] = {}
        self.historial: dict[str, list[dict]] = {}
        self.usuarios: dict[WebSocket, str] = {}

    async def conectar(self, sala: str, usuario: str, ws: WebSocket):
        await ws.accept()
        self.salas.setdefault(sala, []).append(ws)
        self.historial.setdefault(sala, [])
        self.usuarios[ws] = usuario
        await self._broadcast(sala, f"[Sistema] {usuario} se unió a #{sala}")

    async def desconectar(self, sala: str, ws: WebSocket):
        usuario = self.usuarios.pop(ws, "Anónimo")
        if sala in self.salas:
            self.salas[sala].remove(ws)
            if not self.salas[sala]:
                del self.salas[sala]
        await self._broadcast(sala, f"[Sistema] {usuario} salió de #{sala}")

    async def enviar_mensaje(self, sala: str, ws: WebSocket, texto: str):
        usuario = self.usuarios.get(ws, "Anónimo")
        mensaje = {
            "usuario": usuario,
            "texto": texto,
            "sala": sala,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.historial[sala].append(mensaje)
        # Limitar historial a últimos 50 mensajes
        self.historial[sala] = self.historial[sala][-50:]
        await self._broadcast(sala, f"{usuario}: {texto}")

    async def _broadcast(self, sala: str, mensaje: str):
        for ws in self.salas.get(sala, []):
            await ws.send_text(mensaje)


chat = ChatManager()


# === ENDPOINTS REST ===


@app.get("/salas", tags=["Chat"])
async def listar_salas():
    """Lista salas activas con cantidad de usuarios."""
    return {
        sala: {"usuarios": len(conns)}
        for sala, conns in chat.salas.items()
    }


@app.get("/historial/{sala}", tags=["Chat"])
async def ver_historial(sala: str):
    """Últimos mensajes de una sala."""
    return {"sala": sala, "mensajes": chat.historial.get(sala, [])}


# === WEBSOCKET ===


@app.websocket("/ws/{sala}/{usuario}")
async def websocket_chat(ws: WebSocket, sala: str, usuario: str):
    """Conecta un usuario a una sala de chat."""
    await chat.conectar(sala, usuario, ws)
    try:
        while True:
            texto = await ws.receive_text()
            await chat.enviar_mensaje(sala, ws, texto)
    except WebSocketDisconnect:
        await chat.desconectar(sala, ws)


# === HTML DE PRUEBA ===

HTML = """
<!DOCTYPE html>
<html><head><title>Chat</title></head>
<body>
<h2>Chat con Salas</h2>
<label>Usuario: <input id="user" value="usuario1"></label>
<label>Sala: <input id="sala" value="general"></label>
<button onclick="conectar()">Conectar</button>
<br><br>
<input id="msg" type="text" placeholder="Mensaje..." disabled>
<button id="btn" onclick="enviar()" disabled>Enviar</button>
<ul id="log"></ul>
<script>
let ws;
function conectar() {
    const user = document.getElementById("user").value;
    const sala = document.getElementById("sala").value;
    ws = new WebSocket(`ws://localhost:8000/ws/${sala}/${user}`);
    ws.onmessage = (e) => {
        const li = document.createElement("li");
        li.textContent = e.data;
        document.getElementById("log").appendChild(li);
    };
    ws.onopen = () => {
        document.getElementById("msg").disabled = false;
        document.getElementById("btn").disabled = false;
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
    return HTML


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
