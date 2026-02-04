"""
Ejemplo 01: Diseño de Recursos y URIs
=====================================
Modelado de recursos y convenciones de URIs RESTful.
"""

from dataclasses import dataclass, field
from datetime import datetime


# =============================================================================
# RECURSOS: Representación de entidades como clases
# =============================================================================


@dataclass
class Usuario:
    """Recurso: Usuario del sistema."""
    id: int | None = None
    nombre: str = ""
    email: str = ""
    creado_en: datetime = field(default_factory=datetime.now)


@dataclass
class Producto:
    """Recurso: Producto del catálogo."""
    id: int | None = None
    nombre: str = ""
    precio: float = 0.0
    categoria: str = ""
    stock: int = 0


@dataclass
class Pedido:
    """Recurso: Pedido de un cliente."""
    id: int | None = None
    usuario_id: int = 0
    productos: list[dict] = field(default_factory=list)
    total: float = 0.0
    estado: str = "pendiente"


# =============================================================================
# DISEÑO DE URIs
# =============================================================================


# Diccionario que mapea URIs a descripciones
ENDPOINTS_API = {
    # --- Usuarios ---
    "GET /api/v1/usuarios": "Listar todos los usuarios",
    "POST /api/v1/usuarios": "Crear nuevo usuario",
    "GET /api/v1/usuarios/{id}": "Obtener usuario por ID",
    "PUT /api/v1/usuarios/{id}": "Reemplazar usuario completo",
    "PATCH /api/v1/usuarios/{id}": "Actualizar campos del usuario",
    "DELETE /api/v1/usuarios/{id}": "Eliminar usuario",

    # --- Productos ---
    "GET /api/v1/productos": "Listar productos (con filtros)",
    "POST /api/v1/productos": "Crear producto",
    "GET /api/v1/productos/{id}": "Obtener producto por ID",
    "PUT /api/v1/productos/{id}": "Reemplazar producto",
    "PATCH /api/v1/productos/{id}": "Actualizar producto parcialmente",
    "DELETE /api/v1/productos/{id}": "Eliminar producto",

    # --- Pedidos (relación con usuarios) ---
    "GET /api/v1/usuarios/{id}/pedidos": "Listar pedidos del usuario",
    "POST /api/v1/usuarios/{id}/pedidos": "Crear pedido para usuario",
    "GET /api/v1/pedidos/{id}": "Obtener pedido por ID",
    "PATCH /api/v1/pedidos/{id}": "Actualizar estado del pedido",

    # --- Búsqueda y filtros ---
    "GET /api/v1/productos?categoria=laptops": "Filtrar por categoría",
    "GET /api/v1/productos?precio_min=100&precio_max=500": "Filtrar por precio",
    "GET /api/v1/productos?ordenar=precio&dir=asc": "Ordenar resultados",
    "GET /api/v1/productos?page=2&per_page=20": "Paginación",
}


# =============================================================================
# EJEMPLOS DE URIs: BUENAS VS MALAS PRÁCTICAS
# =============================================================================


URIS_CORRECTAS = [
    # Sustantivos, plurales
    "/api/v1/usuarios",
    "/api/v1/productos",
    "/api/v1/pedidos",

    # Jerárquico para relaciones
    "/api/v1/usuarios/123/pedidos",
    "/api/v1/pedidos/456/productos",

    # Query params para filtros
    "/api/v1/productos?categoria=electronica",
    "/api/v1/usuarios?activo=true&rol=admin",

    # Kebab-case para palabras compuestas
    "/api/v1/tipos-producto",
    "/api/v1/metodos-pago",
]

URIS_INCORRECTAS = [
    # ❌ Verbos en la URI
    ("/api/v1/obtenerUsuarios", "Usar GET /usuarios"),
    ("/api/v1/crearProducto", "Usar POST /productos"),
    ("/api/v1/eliminarPedido/123", "Usar DELETE /pedidos/123"),

    # ❌ Singulares
    ("/api/v1/usuario", "Usar /usuarios (plural)"),

    # ❌ Acciones como recursos
    ("/api/v1/usuarios/123/activar", "Usar PATCH /usuarios/123 con {activo: true}"),

    # ❌ CamelCase o snake_case
    ("/api/v1/tiposProducto", "Usar /tipos-producto (kebab-case)"),
    ("/api/v1/tipos_producto", "Usar /tipos-producto (kebab-case)"),

    # ❌ Extensiones de archivo
    ("/api/v1/usuarios.json", "Content-Type en headers, no en URI"),
]


# =============================================================================
# FUNCIÓN PARA CONSTRUIR URIs
# =============================================================================


def construir_uri(
    recurso: str,
    id: int | None = None,
    sub_recurso: str | None = None,
    version: str = "v1"
) -> str:
    """
    Construye una URI RESTful.

    Args:
        recurso: Nombre del recurso (ej: "usuarios")
        id: ID del recurso (opcional)
        sub_recurso: Sub-recurso relacionado (opcional)
        version: Versión de la API

    Returns:
        URI construida
    """
    base = f"/api/{version}/{recurso}"

    if id is not None:
        base += f"/{id}"

    if sub_recurso:
        base += f"/{sub_recurso}"

    return base


# =============================================================================
# DEMOSTRACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Diseño de Recursos y URIs REST")
    print("=" * 60)

    # --- Recursos ---
    print("\n--- Recursos como Clases ---")
    usuario = Usuario(id=1, nombre="Ana García", email="ana@ejemplo.com")
    producto = Producto(id=100, nombre="Laptop", precio=999.99, categoria="laptops")
    print(f"Usuario: {usuario}")
    print(f"Producto: {producto}")

    # --- URIs del API ---
    print("\n--- Endpoints del API ---")
    for endpoint, descripcion in list(ENDPOINTS_API.items())[:8]:
        print(f"  {endpoint}")
        print(f"    → {descripcion}\n")

    # --- URIs correctas ---
    print("\n--- URIs Correctas ✅ ---")
    for uri in URIS_CORRECTAS[:5]:
        print(f"  {uri}")

    # --- URIs incorrectas ---
    print("\n--- URIs Incorrectas ❌ ---")
    for uri, correccion in URIS_INCORRECTAS[:4]:
        print(f"  {uri}")
        print(f"    → Corrección: {correccion}\n")

    # --- Construir URIs ---
    print("\n--- Construir URIs ---")
    print(f"  {construir_uri('usuarios')}")
    print(f"  {construir_uri('usuarios', id=123)}")
    print(f"  {construir_uri('usuarios', id=123, sub_recurso='pedidos')}")

    print("\n✓ Ejemplo completado")
