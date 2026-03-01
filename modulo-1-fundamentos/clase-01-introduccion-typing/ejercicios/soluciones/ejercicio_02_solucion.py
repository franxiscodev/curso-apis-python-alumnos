"""
Solución Ejercicio 02: Crear Modelo de Recurso API
==================================================
Sintaxis moderna Python 3.10+
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import TypedDict

# =============================================================================
# EJERCICIO 2.1: TypedDict para un Libro
# =============================================================================


class LibroDict(TypedDict):
    """Estructura de un libro como diccionario tipado."""
    isbn: str
    titulo: str
    autor: str
    año_publicacion: int
    disponible: bool


# =============================================================================
# EJERCICIO 2.2: Dataclass Libro
# =============================================================================


@dataclass
class Libro:
    """Modelo de Libro para API de biblioteca."""
    isbn: str
    titulo: str
    autor: str
    año_publicacion: int
    disponible: bool = True
    fecha_registro: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict[str, str | int | bool]:
        """Convierte el libro a diccionario."""
        return {
            "isbn": self.isbn,
            "titulo": self.titulo,
            "autor": self.autor,
            "año_publicacion": self.año_publicacion,
            "disponible": self.disponible,
            "fecha_registro": self.fecha_registro.isoformat()
        }


# =============================================================================
# EJERCICIO 2.3: Funciones CRUD tipadas
# =============================================================================

_libros_db: dict[str, Libro] = {}


def agregar_libro(libro: Libro) -> Libro:
    """
    Agrega un libro a la biblioteca.

    Args:
        libro: Libro a agregar

    Returns:
        El libro agregado
    """
    _libros_db[libro.isbn] = libro
    return libro


def obtener_libro(isbn: str) -> Libro | None:
    """
    Busca un libro por ISBN.

    Args:
        isbn: ISBN del libro

    Returns:
        El libro si existe, None si no
    """
    return _libros_db.get(isbn)


def listar_disponibles() -> list[Libro]:
    """
    Lista todos los libros disponibles.

    Returns:
        Lista de libros con disponible=True
    """
    return [libro for libro in _libros_db.values() if libro.disponible]


# =============================================================================
# VERIFICACIÓN
# =============================================================================

if __name__ == "__main__":
    # Test TypedDict
    libro_dict: LibroDict = {
        "isbn": "978-0-13-468599-1",
        "titulo": "Clean Code",
        "autor": "Robert C. Martin",
        "año_publicacion": 2008,
        "disponible": True
    }
    print(f"LibroDict: {libro_dict}")

    # Test dataclass
    libro1 = Libro(
        isbn="978-0-13-468599-1",
        titulo="Clean Code",
        autor="Robert C. Martin",
        año_publicacion=2008
    )
    print(f"\nLibro: {libro1}")
    print(f"Como dict: {libro1.to_dict()}")

    # Test CRUD
    agregar_libro(libro1)
    libro2 = Libro(
        isbn="978-0-596-51774-8",
        titulo="JavaScript: The Good Parts",
        autor="Douglas Crockford",
        año_publicacion=2008,
        disponible=False
    )
    agregar_libro(libro2)

    print(f"\nBuscar existente: {obtener_libro('978-0-13-468599-1')}")
    print(f"Buscar inexistente: {obtener_libro('000-0-00-000000-0')}")
    print(f"Disponibles: {[l.titulo for l in listar_disponibles()]}")

    print("\n✓ Solución verificada")
