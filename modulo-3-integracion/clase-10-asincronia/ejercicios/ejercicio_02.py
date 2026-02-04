"""
Ejercicio 02: Endpoints Async con FastAPI
==========================================
Crear endpoints asíncronos en FastAPI.

OBJETIVO:
Practicar async def en endpoints y gather para concurrencia.

INSTRUCCIONES:
1. Implementar GET /datos/{fuente_id}:
   - Async endpoint que simula obtener datos con asyncio.sleep
   - Retorna datos de la fuente solicitada
   - 404 si la fuente no existe

2. Implementar GET /agregar:
   - Usa asyncio.gather para obtener datos de todas las fuentes
   - Retorna los datos combinados y el tiempo total

3. Implementar GET /estadisticas:
   - Agrega datos de todas las fuentes concurrentemente
   - Calcula promedio, min, max de los valores

PRUEBAS:
    uvicorn ejercicio_02:app --reload

    GET /datos/ventas
    GET /agregar
    GET /estadisticas

PISTAS:
- async def para endpoints con I/O
- asyncio.gather(*[tarea1, tarea2, ...])
- time.perf_counter() para medir tiempo
"""

import asyncio
import time

from fastapi import FastAPI, HTTPException

app = FastAPI(title="Async Endpoints", version="1.0.0")


# Configuración de fuentes simuladas
FUENTES = {
    "ventas": {"latencia": 0.5, "valores": [100, 200, 150, 300]},
    "clientes": {"latencia": 0.3, "valores": [50, 75, 60, 90]},
    "inventario": {"latencia": 0.4, "valores": [500, 450, 600, 550]},
}


# TODO: Implementar función async obtener_datos_fuente(fuente_id)
# Simula latencia con asyncio.sleep, retorna los valores


# TODO: GET /datos/{fuente_id} (async)


# TODO: GET /agregar (async, usa gather)


# TODO: GET /estadisticas (async, agrega y calcula)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
