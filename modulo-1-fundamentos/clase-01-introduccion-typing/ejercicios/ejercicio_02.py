"""
Ejercicio 02: Crear Modelo de Recurso API
=========================================
Crea estructuras de datos tipadas para una API de biblioteca.

Instrucciones:
1. Completa las definiciones de TypedDict y dataclass
2. Implementa las funciones indicadas
3. Los tests al final deben pasar

Nota: Usa sintaxis moderna Python 3.10+ (str | None en lugar de Optional[str])
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import TypedDict

# =============================================================================
# EJERCICIO 2.1: Definir TypedDict para un Libro
# =============================================================================

# TODO: Completa el TypedDict con los campos:
# - isbn: str
# - titulo: str
# - autor: str
# - año_publicacion: int
# - disponible: bool


class LibroDict(TypedDict):
    """Estructura de un libro como diccionario tipado."""
    pass  # TODO: Reemplaza pass con los campos


# =============================================================================
# EJERCICIO 2.2: Crear dataclass Libro
# =============================================================================

# TODO: Completa el dataclass con:
# - isbn: str (requerido)
# - titulo: str (requerido)
# - autor: str (requerido)
# - año_publicacion: int (requerido)
# - disponible: bool (default: True)
# - fecha_registro: datetime (default: ahora)


@dataclass
class Libro:
    """Modelo de Libro para API de biblioteca."""
    pass  # TODO: Reemplaza con los atributos

    def to_dict(self) -> dict[str, str | int | bool]:
        """Convierte el libro a diccionario."""
        # TODO: Implementa la conversión
        pass


# =============================================================================
# EJERCICIO 2.3: Implementar funciones CRUD tipadas
# =============================================================================

# Simulamos una "base de datos" en memoria
_libros_db: dict[str, Libro] = {}


def agregar_libro(libro: Libro) -> Libro:
    """
    Agrega un libro a la biblioteca.

    Args:
        libro: Libro a agregar

    Returns:
        El libro agregado
    """
    # TODO: Implementa - guarda en _libros_db usando isbn como clave
    pass


def obtener_libro(isbn: str) -> Libro | None:
    """
    Busca un libro por ISBN.

    Args:
        isbn: ISBN del libro

    Returns:
        El libro si existe, None si no
    """
    # TODO: Implementa
    pass


def listar_disponibles() -> list[Libro]:
    """
    Lista todos los libros disponibles.

    Returns:
        Lista de libros con disponible=True
    """
    # TODO: Implementa - filtra solo los disponibles
    pass


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

    print(f"\nBuscar ISBN existente: {obtener_libro('978-0-13-468599-1')}")
    print(f"Buscar ISBN inexistente: {obtener_libro('000-0-00-000000-0')}")
    print(f"Libros disponibles: {[l.titulo for l in listar_disponibles()]}")

    print("\n✓ Ejercicio completado")
