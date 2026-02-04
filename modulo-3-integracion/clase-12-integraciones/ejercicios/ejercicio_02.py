"""
Ejercicio 02: Circuit Breaker Básico
======================================
Implementar un circuit breaker para servicios externos.

OBJETIVO:
Practicar el patrón circuit breaker.

INSTRUCCIONES:
1. Implementar clase CircuitBreaker:
   - Estados: cerrado, abierto, semi_abierto
   - Umbral de fallos configurable
   - Tiempo de recuperación configurable
   - Método ejecutar(coroutine) protegido

2. Implementar GET /servicio/{nombre}:
   - Simula llamadas a servicios (algunos fallan)
   - Protegido por circuit breaker
   - Retorna resultado o estado del circuito

3. Implementar GET /estado:
   - Muestra estado de todos los circuit breakers

PRUEBAS:
    uvicorn ejercicio_02:app --reload

    GET /servicio/api-estable (siempre funciona)
    GET /servicio/api-inestable (falla 50% del tiempo)
    GET /estado

PISTAS:
- time.time() para medir cuándo fue el último fallo
- Enum para los estados del circuito
- fallos_consecutivos >= umbral → abrir circuito
"""

import asyncio
import time
from enum import Enum

from fastapi import FastAPI

app = FastAPI(title="Circuit Breaker", version="1.0.0")


# TODO: Implementar Enum de estados

# TODO: Implementar clase CircuitBreaker

# TODO: Crear circuit breakers para servicios simulados

# TODO: Funciones async que simulan servicios (estable e inestable)

# TODO: GET /servicio/{nombre}

# TODO: GET /estado (estado de todos los circuit breakers)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
