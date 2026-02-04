"""
Ejercicio 03: API Completa con Base de Datos
==============================================
Crear una API FastAPI con persistencia SQLAlchemy.

OBJETIVO:
Integrar FastAPI + SQLAlchemy + Pydantic en una API completa.

INSTRUCCIONES:
1. Definir modelo SQLAlchemy `Nota` con:
   - id (primary key), titulo (str 100), contenido (str 1000, opcional),
     categoria (str 50), importante (bool, default False)

2. Definir schemas Pydantic:
   - NotaCrear: titulo, contenido, categoria, importante
   - NotaActualizar: todo opcional
   - NotaResponse: con from_attributes=True

3. Implementar endpoints:
   - GET    /notas         → Listar (filtro por categoría opcional)
   - POST   /notas         → Crear (status 201)
   - GET    /notas/{id}    → Obtener (404 si no existe)
   - PUT    /notas/{id}    → Actualizar parcial
   - DELETE /notas/{id}    → Eliminar (status 204)

4. Usar dependency injection con get_db

PRUEBAS:
    uvicorn ejercicio_03:app --reload

    POST /notas {"titulo": "Mi nota", "categoria": "Personal"}
    GET  /notas?categoria=Personal
    PUT  /notas/1 {"importante": true}

PISTAS:
- ConfigDict(from_attributes=True) en schemas de respuesta
- db.get(Modelo, id) para obtener por primary key
- setattr(obj, campo, valor) para update parcial
- Depends(get_db) en cada endpoint que necesite BD
"""

from fastapi import FastAPI

app = FastAPI(title="Notas API", version="1.0.0")

# TODO: Imports necesarios (SQLAlchemy, Pydantic, Depends, etc.)

# TODO: Configurar engine, SessionLocal, Base

# TODO: Definir modelo SQLAlchemy Nota

# TODO: Crear tablas

# TODO: Definir schemas Pydantic (NotaCrear, NotaActualizar, NotaResponse)

# TODO: Definir función get_db

# TODO: Implementar GET /notas (con filtro por categoría)

# TODO: Implementar POST /notas

# TODO: Implementar GET /notas/{nota_id}

# TODO: Implementar PUT /notas/{nota_id}

# TODO: Implementar DELETE /notas/{nota_id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
