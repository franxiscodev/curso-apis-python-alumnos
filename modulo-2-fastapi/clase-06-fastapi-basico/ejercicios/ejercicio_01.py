"""
Ejercicio 01: Endpoints Básicos
===============================
Crear una API simple con diferentes rutas y métodos HTTP.

OBJETIVO:
Practicar la creación de endpoints con diferentes métodos HTTP.

INSTRUCCIONES:
1. Crear una aplicación FastAPI con título "Biblioteca API"
2. Implementar los siguientes endpoints:
   - GET  /           → Retornar info de la API
   - GET  /libros     → Listar libros
   - POST /libros     → "Crear" libro
   - GET  /libros/{id} → Obtener libro por ID
   - PUT  /libros/{id} → Actualizar libro
   - DELETE /libros/{id} → Eliminar libro

3. Cada endpoint debe retornar un dict con:
   - "metodo": el método HTTP usado
   - "endpoint": la ruta
   - "mensaje": descripción de la acción

PRUEBAS:
    uvicorn ejercicio_01:app --reload

    # Probar con curl o navegador:
    GET  http://localhost:8000/
    GET  http://localhost:8000/libros
    POST http://localhost:8000/libros
    GET  http://localhost:8000/libros/1

PISTAS:
- Usa @app.get(), @app.post(), @app.put(), @app.delete()
- Para path parameters: /ruta/{parametro}
- El parámetro se declara como argumento de la función
"""

from fastapi import FastAPI

# TODO: Crear la aplicación FastAPI con título "Biblioteca API"
app = None  # Reemplazar con FastAPI(...)


# TODO: Implementar endpoint raíz
# GET / → {"metodo": "GET", "endpoint": "/", "mensaje": "Bienvenido a la Biblioteca API"}


# TODO: Implementar GET /libros
# → {"metodo": "GET", "endpoint": "/libros", "mensaje": "Listando todos los libros"}


# TODO: Implementar POST /libros
# → {"metodo": "POST", "endpoint": "/libros", "mensaje": "Creando nuevo libro"}


# TODO: Implementar GET /libros/{libro_id}
# → {"metodo": "GET", "endpoint": "/libros/{id}", "mensaje": "Obteniendo libro con ID: {libro_id}"}


# TODO: Implementar PUT /libros/{libro_id}
# → {"metodo": "PUT", "endpoint": "/libros/{id}", "mensaje": "Actualizando libro con ID: {libro_id}"}


# TODO: Implementar DELETE /libros/{libro_id}
# → {"metodo": "DELETE", "endpoint": "/libros/{id}", "mensaje": "Eliminando libro con ID: {libro_id}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
