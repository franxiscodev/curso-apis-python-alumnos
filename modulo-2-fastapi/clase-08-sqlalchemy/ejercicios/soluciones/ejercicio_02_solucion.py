"""
Ejercicio 02: CRUD con SQLAlchemy - SOLUCIÓN
==============================================
"""

from sqlalchemy import String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

engine = create_engine("sqlite:///ejercicio_02.db")


class Base(DeclarativeBase):
    pass


class Libro(Base):
    """Modelo de libro."""
    __tablename__ = "libros"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200))
    autor: Mapped[str] = mapped_column(String(100))
    año: Mapped[int]
    paginas: Mapped[int]

    def __repr__(self) -> str:
        return f"Libro(id={self.id}, titulo='{self.titulo}')"


Base.metadata.create_all(bind=engine)


# =============================================================================
# FUNCIONES CRUD
# =============================================================================


def crear_libro(session: Session, titulo: str, autor: str,
                año: int, paginas: int) -> Libro:
    """Crear nuevo libro."""
    libro = Libro(titulo=titulo, autor=autor, año=año, paginas=paginas)
    session.add(libro)
    session.commit()
    session.refresh(libro)
    return libro


def obtener_libro(session: Session, libro_id: int) -> Libro | None:
    """Obtener libro por ID."""
    return session.get(Libro, libro_id)


def listar_libros(session: Session, autor: str | None = None) -> list[Libro]:
    """Listar libros con filtro opcional por autor."""
    stmt = select(Libro)
    if autor:
        stmt = stmt.where(Libro.autor.contains(autor))
    return list(session.execute(stmt).scalars().all())


def actualizar_libro(session: Session, libro_id: int, **campos) -> Libro | None:
    """Actualizar campos de un libro."""
    libro = session.get(Libro, libro_id)
    if not libro:
        return None
    for campo, valor in campos.items():
        if hasattr(libro, campo):
            setattr(libro, campo, valor)
    session.commit()
    session.refresh(libro)
    return libro


def eliminar_libro(session: Session, libro_id: int) -> bool:
    """Eliminar libro por ID."""
    libro = session.get(Libro, libro_id)
    if not libro:
        return False
    session.delete(libro)
    session.commit()
    return True


# =============================================================================
# DEMOSTRACIÓN
# =============================================================================


if __name__ == "__main__":
    with Session(engine) as db:
        print("=== CREAR ===")
        l1 = crear_libro(db, "Cien Años de Soledad", "García Márquez", 1967, 471)
        l2 = crear_libro(db, "El Amor en los Tiempos del Cólera",
                         "García Márquez", 1985, 348)
        l3 = crear_libro(db, "Rayuela", "Julio Cortázar", 1963, 600)
        print(f"Creados: {l1}, {l2}, {l3}")

        print("\n=== LEER ===")
        obtenido = obtener_libro(db, 1)
        print(f"Por ID 1: {obtenido}")

        todos = listar_libros(db)
        print(f"Total: {len(todos)}")

        por_autor = listar_libros(db, autor="García")
        print(f"García Márquez: {por_autor}")

        print("\n=== ACTUALIZAR ===")
        actualizado = actualizar_libro(db, 3, paginas=635)
        print(f"Rayuela actualizado: páginas={actualizado.paginas}")

        print("\n=== ELIMINAR ===")
        eliminado = eliminar_libro(db, 2)
        print(f"Eliminado ID 2: {eliminado}")
        print(f"Total restante: {len(listar_libros(db))}")

    import os
    os.remove("ejercicio_02.db")
    print("\nBase de datos eliminada")
