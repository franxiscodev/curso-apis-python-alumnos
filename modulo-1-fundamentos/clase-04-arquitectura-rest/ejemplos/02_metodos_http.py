"""
Ejemplo 02: Métodos HTTP y Operaciones CRUD
===========================================
Mapeo de métodos HTTP a operaciones CRUD y sus características.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


# =============================================================================
# ENUMS PARA MÉTODOS HTTP
# =============================================================================


class MetodoHTTP(Enum):
    """Métodos HTTP estándar."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class OperacionCRUD(Enum):
    """Operaciones CRUD."""
    CREATE = "Create"
    READ = "Read"
    UPDATE = "Update"
    DELETE = "Delete"


# =============================================================================
# CARACTERÍSTICAS DE MÉTODOS HTTP
# =============================================================================


@dataclass
class CaracteristicasMetodo:
    """Características de un método HTTP."""
    metodo: MetodoHTTP
    crud: OperacionCRUD | None
    seguro: bool
    idempotente: bool
    tiene_body_request: bool
    tiene_body_response: bool
    descripcion: str


METODOS_HTTP = {
    MetodoHTTP.GET: CaracteristicasMetodo(
        metodo=MetodoHTTP.GET,
        crud=OperacionCRUD.READ,
        seguro=True,
        idempotente=True,
        tiene_body_request=False,
        tiene_body_response=True,
        descripcion="Obtener recurso(s). No modifica datos."
    ),
    MetodoHTTP.POST: CaracteristicasMetodo(
        metodo=MetodoHTTP.POST,
        crud=OperacionCRUD.CREATE,
        seguro=False,
        idempotente=False,
        tiene_body_request=True,
        tiene_body_response=True,
        descripcion="Crear nuevo recurso. Cada llamada crea uno nuevo."
    ),
    MetodoHTTP.PUT: CaracteristicasMetodo(
        metodo=MetodoHTTP.PUT,
        crud=OperacionCRUD.UPDATE,
        seguro=False,
        idempotente=True,
        tiene_body_request=True,
        tiene_body_response=True,
        descripcion="Reemplazar recurso completo."
    ),
    MetodoHTTP.PATCH: CaracteristicasMetodo(
        metodo=MetodoHTTP.PATCH,
        crud=OperacionCRUD.UPDATE,
        seguro=False,
        idempotente=True,
        tiene_body_request=True,
        tiene_body_response=True,
        descripcion="Actualizar campos específicos del recurso."
    ),
    MetodoHTTP.DELETE: CaracteristicasMetodo(
        metodo=MetodoHTTP.DELETE,
        crud=OperacionCRUD.DELETE,
        seguro=False,
        idempotente=True,
        tiene_body_request=False,
        tiene_body_response=False,
        descripcion="Eliminar recurso."
    ),
}


# =============================================================================
# SIMULACIÓN DE OPERACIONES CRUD
# =============================================================================


@dataclass
class Producto:
    """Modelo de producto para demostración."""
    id: int | None = None
    nombre: str = ""
    precio: float = 0.0
    descripcion: str = ""
    actualizado_en: datetime = field(default_factory=datetime.now)


class ProductoService:
    """Servicio que simula operaciones CRUD."""

    def __init__(self):
        self._productos: dict[int, Producto] = {}
        self._next_id = 1

    # GET /productos
    def listar(self) -> list[Producto]:
        """READ - Obtener todos (GET /productos)."""
        print("[GET] Listando todos los productos")
        return list(self._productos.values())

    # GET /productos/{id}
    def obtener(self, id: int) -> Producto | None:
        """READ - Obtener uno (GET /productos/{id})."""
        print(f"[GET] Obteniendo producto {id}")
        return self._productos.get(id)

    # POST /productos
    def crear(self, datos: dict) -> Producto:
        """CREATE - Crear nuevo (POST /productos)."""
        print(f"[POST] Creando producto: {datos}")
        producto = Producto(
            id=self._next_id,
            nombre=datos["nombre"],
            precio=datos["precio"],
            descripcion=datos.get("descripcion", "")
        )
        self._productos[producto.id] = producto
        self._next_id += 1
        return producto

    # PUT /productos/{id}
    def reemplazar(self, id: int, datos: dict) -> Producto | None:
        """UPDATE - Reemplazar completo (PUT /productos/{id})."""
        print(f"[PUT] Reemplazando producto {id}: {datos}")
        if id not in self._productos:
            return None
        producto = Producto(
            id=id,
            nombre=datos["nombre"],
            precio=datos["precio"],
            # Si no viene, queda vacío
            descripcion=datos.get("descripcion", ""),
            actualizado_en=datetime.now()
        )
        self._productos[id] = producto
        return producto

    # PATCH /productos/{id}
    def actualizar_parcial(self, id: int, datos: dict) -> Producto | None:
        """UPDATE - Actualización parcial (PATCH /productos/{id})."""
        print(f"[PATCH] Actualizando producto {id}: {datos}")
        producto = self._productos.get(id)
        if not producto:
            return None
        # Solo actualiza campos enviados
        if "nombre" in datos:
            producto.nombre = datos["nombre"]
        if "precio" in datos:
            producto.precio = datos["precio"]
        if "descripcion" in datos:
            producto.descripcion = datos["descripcion"]
        producto.actualizado_en = datetime.now()
        return producto

    # DELETE /productos/{id}
    def eliminar(self, id: int) -> bool:
        """DELETE - Eliminar (DELETE /productos/{id})."""
        print(f"[DELETE] Eliminando producto {id}")
        if id in self._productos:
            del self._productos[id]
            return True
        return False


# =============================================================================
# DIFERENCIA PUT VS PATCH
# =============================================================================


def demo_put_vs_patch():
    """Demuestra la diferencia entre PUT y PATCH."""
    print("\n" + "=" * 60)
    print("PUT vs PATCH")
    print("=" * 60)

    service = ProductoService()

    # Crear producto inicial
    producto = service.crear({
        "nombre": "Laptop",
        "precio": 999.99,
        "descripcion": "Laptop de alta gama"
    })
    print(f"\nProducto creado: {producto}")

    # PUT: Reemplaza TODO (si omites descripcion, queda vacía)
    print("\n--- PUT (reemplaza todo) ---")
    producto_put = service.reemplazar(1, {
        "nombre": "Laptop Pro",
        "precio": 1299.99
        # descripcion NO enviada - quedará vacía
    })
    print(f"Después de PUT: {producto_put}")
    print(
        f"  Descripción: '{producto_put.descripcion}' (vacía porque no se envió)")

    # Recrear para demo PATCH
    service.crear({
        "nombre": "Mouse",
        "precio": 29.99,
        "descripcion": "Mouse ergonómico"
    })

    # PATCH: Solo actualiza lo enviado
    print("\n--- PATCH (actualiza parcial) ---")
    producto_patch = service.actualizar_parcial(2, {
        "precio": 24.99
        # nombre y descripcion NO enviados - mantienen valor actual
    })
    print(f"Después de PATCH: {producto_patch}")
    print(
        f"  Descripción: '{producto_patch.descripcion}' (mantiene valor original)")


# =============================================================================
# DEMOSTRACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Métodos HTTP y Operaciones CRUD")
    print("=" * 60)

    # --- Características de métodos ---
    print("\n--- Características de Métodos HTTP ---")
    print(f"{'Método':<8} {'CRUD':<8} {'Seguro':<8} {'Idempotente':<12}")
    print("-" * 40)
    for metodo, caract in METODOS_HTTP.items():
        crud = caract.crud.value if caract.crud else "-"
        seguro = "✅" if caract.seguro else "❌"
        idemp = "✅" if caract.idempotente else "❌"
        print(f"{metodo.value:<8} {crud:<8} {seguro:<8} {idemp:<12}")

    # --- Flujo CRUD completo ---
    print("\n" + "=" * 60)
    print("Flujo CRUD Completo")
    print("=" * 60)

    service = ProductoService()

    # CREATE
    print("\n1. CREATE (POST)")
    p1 = service.crear({"nombre": "Teclado", "precio": 79.99})
    p2 = service.crear({"nombre": "Monitor", "precio": 299.99})

    # READ
    print("\n2. READ (GET)")
    todos = service.listar()
    print(f"  Productos: {len(todos)}")
    uno = service.obtener(1)
    print(f"  Producto 1: {uno}")

    # UPDATE
    print("\n3. UPDATE (PATCH)")
    service.actualizar_parcial(1, {"precio": 69.99})
    print(f"  Precio actualizado: {service.obtener(1).precio}")

    # DELETE
    print("\n4. DELETE")
    service.eliminar(2)
    print(f"  Productos restantes: {len(service.listar())}")

    # --- PUT vs PATCH ---
    demo_put_vs_patch()

    print("\n✓ Ejemplo completado")
