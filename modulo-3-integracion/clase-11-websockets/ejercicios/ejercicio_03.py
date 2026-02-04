"""
Ejercicio 03: Chat con Salas y Usuarios
=========================================
Aplicación de chat completa con salas.

OBJETIVO:
Integrar WebSocket con salas, usuarios e historial.

INSTRUCCIONES:
1. Implementar ChatManager:
   - Diccionario de salas → lista de (WebSocket, usuario)
   - Historial de mensajes por sala (últimos 20)
   - conectar(sala, usuario, ws)
   - desconectar(sala, ws)
   - enviar(sala, ws, texto) → broadcast a la sala

2. Implementar WebSocket /ws/{sala}/{usuario}:
   - Conectar al usuario a la sala
   - Recibir y retransmitir mensajes
   - Notificar al entrar/salir

3. Implementar endpoints REST:
   - GET /salas → listar salas activas
   - GET /historial/{sala} → últimos mensajes

PRUEBAS:
    uvicorn ejercicio_03:app --reload

    Abrir http://127.0.0.1:8000 en varias pestañas
    Conectarse a diferentes salas con diferentes usuarios

PISTAS:
- dict[str, list[tuple[WebSocket, str]]] para salas
- self.historial[sala].append({...}) para guardar mensajes
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI(title="Chat con Salas", version="1.0.0")

HTML_CLIENTE = """
<!DOCTYPE html>
<html><head><title>Chat</title></head>
<body>
<h2>Chat con Salas</h2>
<label>Usuario: <input id="user" value="user1"></label>
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
    return HTML_CLIENTE


# TODO: Implementar clase ChatManager

# TODO: Crear instancia global del ChatManager

# TODO: WebSocket /ws/{sala}/{usuario}

# TODO: GET /salas (listar salas activas con usuarios)

# TODO: GET /historial/{sala} (mensajes recientes)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
