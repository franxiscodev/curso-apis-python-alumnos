"""
API Integradora: Servicios Externos Resilientes
=================================================
Integra múltiples servicios con circuit breaker y fallbacks.

Ejecutar:
    uvicorn ejemplos.api_integradora:app --reload
"""

import asyncio
import time
from enum import Enum

import httpx
from fastapi import BackgroundTasks, FastAPI

app = FastAPI(title="API Integradora", version="1.0.0")


# === CIRCUIT BREAKER ===


class EstadoCB(Enum):
    CERRADO = "cerrado"
    ABIERTO = "abierto"
    SEMI_ABIERTO = "semi_abierto"


class CircuitBreaker:
    def __init__(self, nombre: str, umbral: int = 3, recuperacion: float = 30):
        self.nombre = nombre
        self.umbral = umbral
        self.recuperacion = recuperacion
        self.estado = EstadoCB.CERRADO
        self.fallos = 0
        self.ultimo_fallo: float = 0

    async def ejecutar(self, coro):
        if self.estado == EstadoCB.ABIERTO:
            if time.time() - self.ultimo_fallo > self.recuperacion:
                self.estado = EstadoCB.SEMI_ABIERTO
            else:
                return None  # Fallback: retorna None
        try:
            resultado = await coro
            self.fallos = 0
            if self.estado == EstadoCB.SEMI_ABIERTO:
                self.estado = EstadoCB.CERRADO
            return resultado
        except Exception:
            self.fallos += 1
            self.ultimo_fallo = time.time()
            if self.fallos >= self.umbral:
                self.estado = EstadoCB.ABIERTO
            return None


# === SERVICIOS ===

SERVICIOS = {
    "posts": {
        "url": "https://jsonplaceholder.typicode.com/posts?_limit=5",
        "cb": CircuitBreaker("posts"),
    },
    "users": {
        "url": "https://jsonplaceholder.typicode.com/users?_limit=5",
        "cb": CircuitBreaker("users"),
    },
}


async def consultar(client: httpx.AsyncClient, nombre: str) -> dict | None:
    """Consulta un servicio con circuit breaker."""
    servicio = SERVICIOS[nombre]

    async def _llamar():
        resp = await client.get(servicio["url"])
        resp.raise_for_status()
        return resp.json()

    return await servicio["cb"].ejecutar(_llamar())


# === ENDPOINTS ===


@app.get("/servicio/{nombre}", tags=["Servicios"])
async def consultar_servicio(nombre: str):
    """Consulta un servicio externo con protección."""
    if nombre not in SERVICIOS:
        return {"error": f"Servicio '{nombre}' no existe"}
    async with httpx.AsyncClient(timeout=10.0) as client:
        inicio = time.perf_counter()
        datos = await consultar(client, nombre)
        elapsed = time.perf_counter() - inicio
    return {
        "servicio": nombre,
        "datos": datos,
        "tiempo": f"{elapsed:.3f}s",
        "circuito": SERVICIOS[nombre]["cb"].estado.value,
    }


@app.get("/dashboard", tags=["Agregación"])
async def dashboard():
    """Consulta todos los servicios concurrentemente."""
    inicio = time.perf_counter()
    async with httpx.AsyncClient(timeout=10.0) as client:
        resultados = await asyncio.gather(
            consultar(client, "posts"),
            consultar(client, "users"),
        )
    return {
        "posts": resultados[0],
        "users": resultados[1],
        "tiempo": f"{time.perf_counter() - inicio:.3f}s",
    }


@app.get("/estado", tags=["Salud"])
async def estado_circuitos():
    """Estado de los circuit breakers."""
    return {
        nombre: {
            "estado": s["cb"].estado.value,
            "fallos": s["cb"].fallos,
        }
        for nombre, s in SERVICIOS.items()
    }


def log_consulta(servicio: str, exito: bool):
    """Registra consulta en background."""
    print(f"[LOG] {servicio}: {'OK' if exito else 'FALLO'}")


@app.get("/servicio-con-log/{nombre}", tags=["Servicios"])
async def consultar_con_log(nombre: str, bg: BackgroundTasks):
    """Consulta servicio y registra en background."""
    if nombre not in SERVICIOS:
        return {"error": f"Servicio '{nombre}' no existe"}
    async with httpx.AsyncClient(timeout=10.0) as client:
        datos = await consultar(client, nombre)
    bg.add_task(log_consulta, nombre, datos is not None)
    return {"servicio": nombre, "datos": datos}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
