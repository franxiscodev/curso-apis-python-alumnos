"""
Ejercicio 03: Conectar Type Hints con Estructuras HTTP
======================================================
Crea modelos de datos que correspondan a peticiones/respuestas HTTP.

CONTEXTO:
Este ejercicio conecta lo que aprendiste de Type Hints con las estructuras
JSON que verás en APIs REST. Revisa el archivo `recursos/api_conceptos.http`
para ver ejemplos de peticiones HTTP.

Instrucciones:
1. Analiza cada petición HTTP comentada
2. Crea el TypedDict o dataclass correspondiente
3. Implementa las funciones que simulan las respuestas
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import TypedDict

# =============================================================================
# EJERCICIO 3.1: Modelo para POST /productos
# =============================================================================
#
# Esta es la petición HTTP:
#
# POST /api/v1/productos
# Content-Type: application/json
#
# {
#     "nombre": "Laptop HP",
#     "precio": 899.99,
#     "stock": 50,
#     "categorias": ["electrónica", "computación"]
# }
#
# Respuesta esperada (201 Created):
# {
#     "id": 1,
#     "nombre": "Laptop HP",
#     "precio": 899.99,
#     "stock": 50,
#     "categorias": ["electrónica", "computación"],
#     "creado_en": "2025-01-18T10:30:00"
# }

# TODO: Crea un TypedDict para el INPUT (datos que envía el cliente)
class ProductoInput(TypedDict):
    """Datos que el cliente envía para crear un producto."""
    pass  # TODO: Completa los campos


# TODO: Crea un dataclass para el OUTPUT (respuesta del servidor)
@dataclass
class Producto:
    """Producto con ID asignado (respuesta del servidor)."""
    pass  # TODO: Completa los atributos


# TODO: Implementa la función que simula POST /productos
def crear_producto(datos: ProductoInput) -> Producto:
    """
    Simula POST /api/v1/productos

    Args:
        datos: Datos del producto a crear (del body JSON)

    Returns:
        Producto creado con ID y timestamp
    """
    # TODO: Implementa - crea un Producto con id=1 y fecha actual
    pass


# =============================================================================
# EJERCICIO 3.2: Modelo para GET /productos con filtros
# =============================================================================
#
# Esta es la petición HTTP:
#
# GET /api/v1/productos?categoria=electrónica&precio_max=1000&disponible=true
#
# Los query parameters se convierten en argumentos de función.
# Respuesta esperada (200 OK):
# {
#     "total": 2,
#     "productos": [
#         {"id": 1, "nombre": "Laptop HP", ...},
#         {"id": 2, "nombre": "Mouse", ...}
#     ]
# }

# TODO: Crea un TypedDict para la respuesta de listado
class ListadoProductos(TypedDict):
    """Respuesta de GET /productos (listado paginado)."""
    pass  # TODO: Completa los campos


# TODO: Implementa la función que simula GET /productos con filtros
def listar_productos(
    categoria: str | None = None,
    precio_max: float | None = None,
    disponible: bool | None = None
) -> ListadoProductos:
    """
    Simula GET /api/v1/productos?categoria=X&precio_max=Y&disponible=Z

    Args:
        categoria: Filtrar por categoría (query param opcional)
        precio_max: Precio máximo (query param opcional)
        disponible: Solo disponibles (query param opcional)

    Returns:
        Listado de productos que cumplen los filtros
    """
    # TODO: Implementa - retorna un ListadoProductos con datos de prueba
    pass


# =============================================================================
# EJERCICIO 3.3: Modelo para PATCH /productos/{id}
# =============================================================================
#
# Esta es la petición HTTP:
#
# PATCH /api/v1/productos/1
# Content-Type: application/json
#
# {
#     "precio": 799.99
# }
#
# Solo se envían los campos a modificar.
# Respuesta esperada (200 OK): Producto actualizado completo

# TODO: Crea un TypedDict para actualizaciones parciales
# Hint: Usa total=False para hacer todos los campos opcionales
class ProductoUpdate(TypedDict, total=False):
    """Campos opcionales para actualización parcial (PATCH)."""
    pass  # TODO: Completa los campos (sin id, sin creado_en)


# TODO: Implementa la función que simula PATCH /productos/{id}
def actualizar_producto(
    producto_id: int,
    cambios: ProductoUpdate
) -> Producto | None:
    """
    Simula PATCH /api/v1/productos/{id}

    Args:
        producto_id: ID del producto a actualizar (path param)
        cambios: Campos a modificar (body JSON parcial)

    Returns:
        Producto actualizado o None si no existe
    """
    # TODO: Implementa - simula actualización y retorna producto
    pass


# =============================================================================
# VERIFICACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=== Ejercicio 3.1: POST /productos ===")
    input_data: ProductoInput = {
        "nombre": "Laptop HP",
        "precio": 899.99,
        "stock": 50,
        "categorias": ["electrónica", "computación"]
    }
    producto = crear_producto(input_data)
    print(f"Creado: {producto}")

    print("\n=== Ejercicio 3.2: GET /productos?categoria=X ===")
    listado = listar_productos(categoria="electrónica", precio_max=1000)
    print(f"Listado: {listado}")

    print("\n=== Ejercicio 3.3: PATCH /productos/1 ===")
    cambios: ProductoUpdate = {"precio": 799.99}
    actualizado = actualizar_producto(1, cambios)
    print(f"Actualizado: {actualizado}")

    print("\n✓ Ejercicio completado")
    print("\nRevisa recursos/api_conceptos.http para ver las peticiones HTTP")
