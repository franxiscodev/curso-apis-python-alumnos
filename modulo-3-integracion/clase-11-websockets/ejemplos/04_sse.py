"""
Ejemplo 04: Server-Sent Events (SSE)
======================================
Alternativa unidireccional a WebSocket.

Ejecutar:
    uvicorn ejemplos.04_sse:app --reload
    Abrir http://127.0.0.1:8000 en el navegador
"""

import asyncio
import json
import random
from datetime import datetime, timezone
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse

app = FastAPI(title="Server-Sent Events", version="1.0.0")


# === GENERADOR DE EVENTOS ===


async def generar_metricas() -> AsyncGenerator[str, None]:
    """Genera métricas simuladas cada segundo."""
    while True:
        metrica = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cpu": round(random.uniform(10, 90), 1),
            "memoria": round(random.uniform(30, 80), 1),
            "requests_por_segundo": random.randint(50, 500),
        }
        yield f"data: {json.dumps(metrica)}\n\n"
        await asyncio.sleep(1)


async def generar_notificaciones() -> AsyncGenerator[str, None]:
    """Genera notificaciones simuladas cada 3 segundos."""
    tipos = ["info", "warning", "error", "success"]
    mensajes = [
        "Nuevo usuario registrado",
        "CPU alta en servidor-02",
        "Deploy completado",
        "Backup finalizado",
    ]
    while True:
        evento = {
            "tipo": random.choice(tipos),
            "mensaje": random.choice(mensajes),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        yield f"data: {json.dumps(evento)}\n\n"
        await asyncio.sleep(3)


# === ENDPOINTS SSE ===


@app.get("/sse/metricas", tags=["SSE"])
async def stream_metricas():
    """Stream de métricas del sistema en tiempo real."""
    return StreamingResponse(
        generar_metricas(), media_type="text/event-stream"
    )


@app.get("/sse/notificaciones", tags=["SSE"])
async def stream_notificaciones():
    """Stream de notificaciones del sistema."""
    return StreamingResponse(
        generar_notificaciones(), media_type="text/event-stream"
    )


# === HTML DE PRUEBA ===

HTML_CLIENTE = """
<!DOCTYPE html>
<html><head><title>SSE Demo</title></head>
<body>
<h2>Server-Sent Events</h2>
<h3>Métricas (cada 1s)</h3>
<ul id="metricas"></ul>
<h3>Notificaciones (cada 3s)</h3>
<ul id="notifs"></ul>
<script>
const esMetricas = new EventSource("/sse/metricas");
esMetricas.onmessage = (e) => {
    const d = JSON.parse(e.data);
    const li = document.createElement("li");
    li.textContent = `CPU: ${d.cpu}% | RAM: ${d.memoria}% | RPS: ${d.requests_por_segundo}`;
    const ul = document.getElementById("metricas");
    ul.insertBefore(li, ul.firstChild);
    if (ul.children.length > 5) ul.removeChild(ul.lastChild);
};
const esNotifs = new EventSource("/sse/notificaciones");
esNotifs.onmessage = (e) => {
    const d = JSON.parse(e.data);
    const li = document.createElement("li");
    li.textContent = `[${d.tipo}] ${d.mensaje}`;
    document.getElementById("notifs").insertBefore(li, document.getElementById("notifs").firstChild);
};
</script></body></html>
"""


@app.get("/", response_class=HTMLResponse)
async def pagina():
    return HTML_CLIENTE


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
