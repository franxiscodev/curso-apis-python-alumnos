"""
Ejercicio 03: API Completa de Inventario
==========================================
Crear una API completa de inventario desde cero.

OBJETIVO:
Integrar todos los conceptos: CRUD + paginación + filtrado + errores.

INSTRUCCIONES:
1. Modelos para Producto:
   - ProductoCrear: nombre (1-100), descripcion (opcional, max 500),
     precio (>0), categoria (1-50), stock (>=0, default 0)
   - ProductoActualizar: todo opcional
   - ProductoResponse: id + campos + disponible (bool calculado)

2. Endpoints:
   GET    /productos         → Listar con paginación + filtros
   POST   /productos         → Crear (409 si nombre duplicado)
   GET    /productos/{id}    → Obtener (404 si no existe)
   PUT    /productos/{id}    → Actualizar parcial
   DELETE /productos/{id}    → Eliminar (400 si stock > 0)
   GET    /estadisticas      → Total, disponibles, por categoría,
                                precio promedio

3. Filtros en GET /productos:
   - categoria (exacto)
   - precio_min, precio_max (rango)
   - disponible (bool)
   - buscar (parcial en nombre, case-insensitive)
   - sort_by (nombre/precio/categoria), order (asc/desc)
   - page, size (paginación)

4. Reglas de negocio:
   - No crear productos con nombre duplicado (409)
   - No eliminar productos con stock > 0 (400)
   - Disponible se calcula: stock > 0

PRUEBAS:
    uvicorn ejercicio_03:app --reload

    POST /productos {"nombre": "Laptop", "precio": 999.99,
                     "categoria": "Electrónica", "stock": 10}
    GET  /productos?categoria=Electrónica&sort_by=precio&order=desc
    GET  /estadisticas

PISTAS:
- Crea datos iniciales para probar
- El campo "disponible" no se recibe, se calcula
- Recalcular "disponible" al actualizar stock
"""

from fastapi import FastAPI

app = FastAPI(
    title="Inventario API",
    description="API completa de gestión de inventario",
    version="1.0.0"
)


# TODO: Importar lo necesario (HTTPException, Query, Path, status, BaseModel, Field, etc.)

# TODO: Definir modelos (ProductoCrear, ProductoActualizar, ProductoResponse, Paginado)

# TODO: Crear "base de datos" en memoria y función siguiente_id()

# TODO: Crear datos iniciales (al menos 5 productos variados)

# TODO: Implementar GET /productos (paginación + filtros + ordenamiento)

# TODO: Implementar POST /productos (validar nombre único)

# TODO: Implementar GET /productos/{producto_id} (404)

# TODO: Implementar PUT /productos/{producto_id} (update parcial)

# TODO: Implementar DELETE /productos/{producto_id} (400 si stock > 0)

# TODO: Implementar GET /estadisticas


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
