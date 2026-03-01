"""
Solución Ejercicio 03: Conectar Type Hints con Estructuras HTTP
===============================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import TypedDict

# =============================================================================
# EJERCICIO 3.1: Modelo para POST /productos
# =============================================================================


class ProductoInput(TypedDict):
    """Datos que el cliente envía para crear un producto."""
    nombre: str
    precio: float
    stock: int
    categorias: list[str]


@dataclass
class Producto:
    """Producto con ID asignado (respuesta del servidor)."""
    nombre: str
    precio: float
    stock: int
    categorias: list[str]
    id: int | None = None
    creado_en: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict[str, str | int | float | list[str]]:
        """Convierte a diccionario para respuesta JSON."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
            "categorias": self.categorias,
            "creado_en": self.creado_en.isoformat()
        }


def crear_producto(datos: ProductoInput) -> Producto:
    """
    Simula POST /api/v1/productos

    Args:
        datos: Datos del producto a crear (del body JSON)

    Returns:
        Producto creado con ID y timestamp
    """
    return Producto(
        id=1,  # En producción vendría de la DB
        nombre=datos["nombre"],
        precio=datos["precio"],
        stock=datos["stock"],
        categorias=datos["categorias"]
    )


# =============================================================================
# EJERCICIO 3.2: Modelo para GET /productos con filtros
# =============================================================================


class ListadoProductos(TypedDict):
    """Respuesta de GET /productos (listado paginado)."""
    total: int
    productos: list[dict[str, str | int | float | list[str]]]


# Base de datos simulada
_productos_db: list[Producto] = [
    Producto(id=1, nombre="Laptop HP", precio=899.99, stock=50,
             categorias=["electrónica", "computación"]),
    Producto(id=2, nombre="Mouse Logitech", precio=29.99, stock=200,
             categorias=["electrónica", "accesorios"]),
    Producto(id=3, nombre="Teclado Mecánico", precio=149.99, stock=0,
             categorias=["electrónica", "accesorios"]),
]


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
    resultado = _productos_db.copy()

    # Aplicar filtros
    if categoria:
        resultado = [p for p in resultado if categoria in p.categorias]

    if precio_max is not None:
        resultado = [p for p in resultado if p.precio <= precio_max]

    if disponible is not None:
        if disponible:
            resultado = [p for p in resultado if p.stock > 0]
        else:
            resultado = [p for p in resultado if p.stock == 0]

    return {
        "total": len(resultado),
        "productos": [p.to_dict() for p in resultado]
    }


# =============================================================================
# EJERCICIO 3.3: Modelo para PATCH /productos/{id}
# =============================================================================


class ProductoUpdate(TypedDict, total=False):
    """Campos opcionales para actualización parcial (PATCH)."""
    nombre: str
    precio: float
    stock: int
    categorias: list[str]


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
    # Buscar producto
    producto = next((p for p in _productos_db if p.id == producto_id), None)

    if producto is None:
        return None

    # Aplicar cambios (solo los campos enviados)
    if "nombre" in cambios:
        producto.nombre = cambios["nombre"]
    if "precio" in cambios:
        producto.precio = cambios["precio"]
    if "stock" in cambios:
        producto.stock = cambios["stock"]
    if "categorias" in cambios:
        producto.categorias = cambios["categorias"]

    return producto


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
    print(f"Como JSON: {producto.to_dict()}")

    print("\n=== Ejercicio 3.2: GET /productos?categoria=electrónica ===")
    listado = listar_productos(categoria="electrónica")
    print(f"Total: {listado['total']}")
    for p in listado["productos"]:
        print(f"  - {p['nombre']}: ${p['precio']}")

    print("\n=== Ejercicio 3.2: GET /productos?precio_max=100&disponible=true ===")
    listado2 = listar_productos(precio_max=100, disponible=True)
    print(f"Total: {listado2['total']}")
    for p in listado2["productos"]:
        print(f"  - {p['nombre']}: ${p['precio']} (stock: {p['stock']})")

    print("\n=== Ejercicio 3.3: PATCH /productos/1 ===")
    cambios: ProductoUpdate = {"precio": 799.99, "stock": 45}
    actualizado = actualizar_producto(1, cambios)
    print(f"Actualizado: {actualizado}")

    print("\n=== Ejercicio 3.3: PATCH /productos/999 (no existe) ===")
    no_existe = actualizar_producto(999, {"precio": 100})
    print(f"Resultado: {no_existe}")

    print("\n✓ Solución verificada")
