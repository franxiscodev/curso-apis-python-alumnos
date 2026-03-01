"""
Ejemplo 01: Hola Mundo con FastAPI
==================================
Primera aplicación FastAPI.

Ejecutar:
    uvicorn modulo-2-fastapi.clase-06-fastapi-basico.ejemplos.01_hola_mundo:app --reload

O desde la carpeta ejemplos:
    cd modulo-2-fastapi/clase-06-fastapi-basico/ejemplos
    uvicorn 01_hola_mundo:app --reload

Documentación automática:
    - Swagger UI: http://localhost:8000/docs
    - ReDoc: http://localhost:8000/redoc
"""

from fastapi import FastAPI

# =============================================================================
# CREAR LA APLICACIÓN
# =============================================================================

# Instancia principal de FastAPI
app = FastAPI(
    title="Mi Primera API mi titulo",
    description="API de ejemplo para aprender FastAPI",
    version="1.0.0"
)


# =============================================================================
# RUTAS BÁSICAS
# =============================================================================


@app.get("/")
def raiz():
    """
    Endpoint raíz.

    Retorna un mensaje de bienvenida.
    """
    return {"mensaje": "CHAU, FastAPI!"}


@app.get("/saludo")
def saludo():
    """Retorna un saludo simple."""
    return {"saludo": "¡Bienvenido a la API!"}


@app.get("/info")
def info():
    """Retorna información de la API."""
    return {
        "nombre": "Mi Primera API",
        "version": "1.0.0",
        "framework": "FastAPI",
        "documentacion": "/docs"
    }


# =============================================================================
# EJECUCIÓN DIRECTA (alternativa a uvicorn CLI)
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    # Esto permite ejecutar con: python 01_hola_mundo.py
    uvicorn.run(app, host="127.0.0.1", port=8000)
