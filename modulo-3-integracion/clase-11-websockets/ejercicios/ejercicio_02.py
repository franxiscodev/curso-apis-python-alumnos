"""
Ejercicio 02: Broadcasting de Notificaciones
==============================================
Sistema de notificaciones en tiempo real.

OBJETIVO:
Practicar ConnectionManager y broadcasting.

INSTRUCCIONES:
1. Implementar ConnectionManager:
   - conectar(websocket) → acepta y agrega a lista
   - desconectar(websocket) → remueve de lista
   - broadcast(mensaje) → envía a todos

2. Implementar WebSocket /ws:
   - Usa el ConnectionManager
   - Broadcasting de cada mensaje a todos los clientes

3. Implementar POST /notificar:
   - Endpoint REST que envía notificación a todos los conectados
   - Recibe {"mensaje": "texto"} en el body

PRUEBAS:
    uvicorn ejercicio_02:app --reload

    Abrir http://127.0.0.1:8000 en varias pestañas
    Enviar POST /notificar desde Swagger UI (/docs)

PISTAS:
- Lista de conexiones: list[WebSocket]
- for conexion in self.conexiones: await conexion.send_text(msg)
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Notificaciones", version="1.0.0")

HTML_CLIENTE = """
<!DOCTYPE html>
<html><head><title>Notificaciones</title></head>
<body>
<h2>Notificaciones en Tiempo Real</h2>
<p>Abre /docs en otra pestaña y usa POST /notificar</p>
<ul id="log"></ul>
<script>
const ws = new WebSocket("ws://localhost:8000/ws");
ws.onmessage = (e) => {
    const li = document.createElement("li");
    li.textContent = e.data;
    document.getElementById("log").appendChild(li);
};
</script></body></html>
"""


class Notificacion(BaseModel):
    mensaje: str


@app.get("/", response_class=HTMLResponse)
async def pagina():
    return HTML_CLIENTE


# TODO: Implementar clase ConnectionManager

# TODO: Crear instancia global del manager

# TODO: WebSocket /ws (conectar, loop receive, broadcast, desconectar)

# TODO: POST /notificar (enviar broadcast desde endpoint REST)

# TODO: GET /conectados (número de clientes conectados)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
