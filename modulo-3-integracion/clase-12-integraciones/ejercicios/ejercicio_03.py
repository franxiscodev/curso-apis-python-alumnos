"""
Ejercicio 03: API Integradora Completa
========================================
API que integra servicios externos con resiliencia.

OBJETIVO:
Combinar httpx, circuit breaker y background tasks.

INSTRUCCIONES:
1. Implementar CircuitBreaker (reutilizar del ejercicio 02)

2. Implementar GET /datos/{fuente}:
   - Consulta una API externa con circuit breaker
   - Fallback: retorna datos cacheados si el circuito está abierto

3. Implementar GET /dashboard:
   - Consulta múltiples fuentes concurrentemente
   - Cada fuente tiene su propio circuit breaker
   - Background task para registrar la consulta

4. Implementar GET /salud:
   - Estado de todos los circuit breakers
   - Número de consultas realizadas

PRUEBAS:
    uvicorn ejercicio_03:app --reload

    GET /datos/posts
    GET /dashboard
    GET /salud

PISTAS:
- asyncio.gather para consultas concurrentes
- BackgroundTasks para logging
- Diccionario como caché simple: cache[fuente] = datos
"""

import httpx
from fastapi import BackgroundTasks, FastAPI

app = FastAPI(title="API Integradora", version="1.0.0")

FUENTES = {
    "posts": "https://jsonplaceholder.typicode.com/posts?_limit=3",
    "users": "https://jsonplaceholder.typicode.com/users?_limit=3",
    "todos": "https://jsonplaceholder.typicode.com/todos?_limit=3",
}

# TODO: Implementar CircuitBreaker

# TODO: Crear circuit breakers y caché por fuente

# TODO: Función consultar(client, fuente) con circuit breaker y fallback

# TODO: GET /datos/{fuente}

# TODO: GET /dashboard (todas las fuentes concurrentemente)

# TODO: GET /salud (estado de circuit breakers)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
