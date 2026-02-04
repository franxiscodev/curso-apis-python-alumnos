"""
Ejemplo 01: WebSocket Básico con FastAPI
==========================================
Servidor echo que responde lo que el cliente envía.

Ejecutar:
    uvicorn ejemplos.01_websocket_basico:app --reload
    Abrir http://127.0.0.1:8000 en el navegador
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI(title="WebSocket Básico", version="1.0.0")

# === HTML DE PRUEBA ===

HTML_CLIENTE = """
<!DOCTYPE html>
<html><head><title>WebSocket Echo</title></head>
<body>
<h2>WebSocket Echo</h2>
<input id="msg" type="text" placeholder="Escribe un mensaje...">
<button onclick="enviar()">Enviar</button>
<ul id="log"></ul>
<script>
const ws = new WebSocket("ws://localhost:8000/ws");
ws.onmessage = (e) => {
    const li = document.createElement("li");
    li.textContent = "Servidor: " + e.data;
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
    """Página HTML para probar el WebSocket."""
    return HTML_CLIENTE


# === WEBSOCKET ECHO ===


@app.websocket("/ws")
async def websocket_echo(websocket: WebSocket):
    """Acepta conexión y devuelve cada mensaje recibido."""
    await websocket.accept()
    try:
        while True:
            mensaje = await websocket.receive_text()
            await websocket.send_text(f"Echo: {mensaje}")
    except WebSocketDisconnect:
        print("Cliente desconectado")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
