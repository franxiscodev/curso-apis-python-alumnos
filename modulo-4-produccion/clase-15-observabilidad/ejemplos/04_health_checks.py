"""
Ejemplo 04: Health Checks
===========================
Liveness, readiness y startup probes.

Ejecutar:
    uvicorn ejemplos.04_health_checks:app --reload
"""

import time
from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(title="Health Checks", version="1.0.0")

# === ESTADO DEL SERVICIO ===

INICIO = time.time()
servicios_estado: dict[str, bool] = {
    "database": True,
    "cache": True,
    "external_api": True,
}


# === HEALTH CHECKS ===


@app.get("/health", tags=["Salud"])
def health():
    """Liveness probe: ¿el servicio está vivo?

    Kubernetes usa esto para saber si debe reiniciar el pod.
    Debe ser simple y rápido: NO verificar dependencias.
    """
    return {"status": "alive"}


@app.get("/ready", tags=["Salud"])
def ready():
    """Readiness probe: ¿puede recibir tráfico?

    Kubernetes usa esto para saber si debe enviar requests.
    Verifica que las dependencias estén disponibles.
    """
    all_ok = all(servicios_estado.values())
    checks = {
        nombre: "ok" if ok else "fail"
        for nombre, ok in servicios_estado.items()
    }
    status = "ready" if all_ok else "not_ready"
    return {"status": status, "checks": checks}


@app.get("/startup", tags=["Salud"])
def startup():
    """Startup probe: ¿terminó de arrancar?

    Kubernetes espera a que este endpoint responda OK
    antes de empezar a enviar liveness y readiness probes.
    """
    uptime = time.time() - INICIO
    return {
        "status": "started",
        "uptime_seconds": round(uptime, 1),
        "started_at": datetime.fromtimestamp(
            INICIO, tz=timezone.utc
        ).isoformat(),
    }


@app.get("/info", tags=["Salud"])
def info():
    """Información completa del servicio."""
    return {
        "servicio": "health-checks-demo",
        "version": "1.0.0",
        "uptime": round(time.time() - INICIO, 1),
        "servicios": servicios_estado,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# === SIMULAR FALLOS ===


@app.post("/simular/fallo/{servicio}", tags=["Simulación"])
def simular_fallo(servicio: str):
    """Simula caída de un servicio para probar readiness."""
    if servicio in servicios_estado:
        servicios_estado[servicio] = False
        return {"mensaje": f"{servicio} marcado como caído"}
    return {"error": f"Servicio '{servicio}' no existe"}


@app.post("/simular/recuperar/{servicio}", tags=["Simulación"])
def simular_recuperar(servicio: str):
    """Simula recuperación de un servicio."""
    if servicio in servicios_estado:
        servicios_estado[servicio] = True
        return {"mensaje": f"{servicio} recuperado"}
    return {"error": f"Servicio '{servicio}' no existe"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
