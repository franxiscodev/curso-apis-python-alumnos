"""
Ejercicio 02: Path y Query Parameters
=====================================
Implementar endpoints con validación de parámetros.

OBJETIVO:
Practicar el uso de Path() y Query() para validar parámetros.

INSTRUCCIONES:
1. Crear una API de películas con los siguientes endpoints:

   GET /peliculas
   - Query params:
     - genero: str opcional, filtrar por género
     - año_min: int opcional, año mínimo (>= 1900)
     - año_max: int opcional, año máximo (<= 2030)
     - ordenar: str, valores permitidos ["titulo", "año", "rating"], default "titulo"
     - page: int, >= 1, default 1
     - limit: int, entre 1 y 50, default 10
   - Retornar dict con todos los filtros aplicados

   GET /peliculas/{pelicula_id}
   - Path param pelicula_id: int >= 1
   - Retornar dict con el ID recibido

   GET /peliculas/{pelicula_id}/actores
   - Path param pelicula_id: int >= 1
   - Query param principal: bool opcional, si True solo actores principales
   - Retornar dict con pelicula_id y filtro de principal

   GET /buscar
   - Query param q: str requerido, mínimo 2 caracteres, máximo 100
   - Query param en_titulo: bool, default True
   - Query param en_sinopsis: bool, default False
   - Retornar dict con los parámetros de búsqueda

PRUEBAS:
    uvicorn ejercicio_02:app --reload

    GET /peliculas?genero=accion&año_min=2000&limit=20
    GET /peliculas/42
    GET /peliculas/42/actores?principal=true
    GET /buscar?q=matrix&en_titulo=true&en_sinopsis=true

PISTAS:
- Usa Path() y Query() de fastapi para validaciones
- ge=valor para "mayor o igual", le=valor para "menor o igual"
- min_length y max_length para strings
- Literal["opcion1", "opcion2"] para valores permitidos (importar de typing)
"""

from fastapi import FastAPI, Path, Query
from typing import Literal

app = FastAPI(title="Películas API")


# TODO: GET /peliculas con todos los query params validados
@app.get("/peliculas")
def listar_peliculas():
    # Implementar con parámetros validados
    pass


# TODO: GET /peliculas/{pelicula_id} con path param validado
@app.get("/peliculas/{pelicula_id}")
def obtener_pelicula(pelicula_id: int):
    # Implementar con Path() validado
    pass


# TODO: GET /peliculas/{pelicula_id}/actores
@app.get("/peliculas/{pelicula_id}/actores")
def obtener_actores(pelicula_id: int):
    # Implementar con path y query params
    pass


# TODO: GET /buscar con query param requerido y validado
@app.get("/buscar")
def buscar():
    # Implementar búsqueda
    pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
