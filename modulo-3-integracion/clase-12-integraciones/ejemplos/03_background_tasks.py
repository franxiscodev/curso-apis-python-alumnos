"""
Ejemplo 03: Background Tasks en FastAPI
=========================================
Ejecutar tareas después de enviar la respuesta.

Ejecutar:
    uvicorn ejemplos.03_background_tasks:app --reload
"""

import time

from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel

app = FastAPI(title="Background Tasks", version="1.0.0")


# === MODELOS ===


class Pedido(BaseModel):
    cliente: str
    producto: str
    cantidad: int = 1


class Reporte(BaseModel):
    tipo: str
    parametros: dict = {}


# === TAREAS EN BACKGROUND ===


def enviar_email(destinatario: str, asunto: str, cuerpo: str):
    """Simula envío de email (tarea lenta)."""
    time.sleep(2)  # Simula latencia de SMTP
    print(f"Email enviado a {destinatario}: {asunto}")


def generar_reporte(tipo: str, parametros: dict):
    """Simula generación de reporte."""
    time.sleep(3)
    print(f"Reporte '{tipo}' generado con params: {parametros}")


def registrar_actividad(accion: str, detalle: str):
    """Registra actividad en log."""
    time.sleep(0.5)
    print(f"[LOG] {accion}: {detalle}")


# === ENDPOINTS ===


@app.post("/pedidos", tags=["Pedidos"])
async def crear_pedido(pedido: Pedido, background_tasks: BackgroundTasks):
    """Crea pedido y envía confirmación por email en background."""
    # Respuesta inmediata al cliente
    resultado = {
        "mensaje": "Pedido recibido",
        "cliente": pedido.cliente,
        "producto": pedido.producto,
    }

    # Tareas que se ejecutan DESPUÉS de responder
    background_tasks.add_task(
        enviar_email,
        pedido.cliente,
        "Confirmación de pedido",
        f"Tu pedido de {pedido.cantidad}x {pedido.producto} fue recibido",
    )
    background_tasks.add_task(
        registrar_actividad, "pedido_creado", f"{pedido.producto}"
    )

    return resultado


@app.post("/reportes", tags=["Reportes"])
async def solicitar_reporte(
    reporte: Reporte, background_tasks: BackgroundTasks
):
    """Solicita un reporte que se genera en background."""
    background_tasks.add_task(
        generar_reporte, reporte.tipo, reporte.parametros
    )
    return {"mensaje": f"Reporte '{reporte.tipo}' en proceso"}


@app.post("/notificar/{usuario}", tags=["Notificaciones"])
async def notificar_usuario(
    usuario: str, mensaje: str, background_tasks: BackgroundTasks
):
    """Envía notificación en background."""
    background_tasks.add_task(
        enviar_email, usuario, "Notificación", mensaje
    )
    return {"mensaje": f"Notificación enviada a {usuario}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
