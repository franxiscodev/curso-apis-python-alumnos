"""
Ejercicio 01: WebSocket Echo Server
=====================================
Crear un servidor WebSocket básico.

OBJETIVO:
Practicar la conexión WebSocket y el ciclo receive/send.

INSTRUCCIONES:
1. Implementar WebSocket /ws:
   - Aceptar la conexión
   - Recibir mensajes en un loop
   - Responder con el mensaje en mayúsculas
   - Manejar desconexión con WebSocketDisconnect

2. Implementar GET /ws-info:
   - Retornar si hay alguien conectado (bool)

PRUEBAS:
    uvicorn ejercicio_01:app --reload

    Abrir http://127.0.0.1:8000 en el navegador
    Escribir mensajes y verificar que llegan en mayúsculas

PISTAS:
- await websocket.accept()
- mensaje = await websocket.receive_text()
- await websocket.send_text(respuesta)
- except WebSocketDisconnect para manejar cierre
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI(title="WebSocket Echo", version="1.0.0")

HTML_CLIENTE = """
<!DOCTYPE html>
<html><head><title>Echo Test</title></head>
<body>
<h2>WebSocket Echo</h2>
<input id="msg" type="text" placeholder="Escribe algo...">
<button onclick="enviar()">Enviar</button>
<ul id="log"></ul>
<script>
const ws = new WebSocket("ws://localhost:8000/ws");
ws.onmessage = (e) => {
    const li = document.createElement("li");
    li.textContent = "Respuesta: " + e.data;
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


# TODO: Variable para rastrear si hay alguien conectado

# TODO: WebSocket /ws (echo en mayúsculas)

# TODO: GET /ws-info (retornar estado de conexión)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
