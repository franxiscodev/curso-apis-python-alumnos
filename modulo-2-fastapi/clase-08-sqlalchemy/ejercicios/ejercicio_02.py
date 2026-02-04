"""
Ejercicio 02: CRUD con SQLAlchemy
===================================
Implementar funciones CRUD completas con sesiones.

OBJETIVO:
Practicar operaciones CRUD usando SQLAlchemy y sesiones.

INSTRUCCIONES:
1. Usar el modelo Libro definido abajo

2. Implementar las siguientes funciones:
   - crear_libro(session, titulo, autor, año, paginas) → Libro
   - obtener_libro(session, libro_id) → Libro | None
   - listar_libros(session, autor=None) → list[Libro]
   - actualizar_libro(session, libro_id, **campos) → Libro | None
   - eliminar_libro(session, libro_id) → bool

3. Demostrar cada operación en el bloque main

PRUEBAS:
    python ejercicio_02.py

    # Debe mostrar:
    # - Libro creado con ID
    # - Libro obtenido por ID
    # - Lista filtrada por autor
    # - Libro actualizado
    # - Libro eliminado

PISTAS:
- session.add(obj) + session.commit() para crear
- session.get(Modelo, id) para obtener por ID
- setattr(obj, campo, valor) para actualizar campos dinámicamente
- session.delete(obj) + session.commit() para eliminar
- session.refresh(obj) para obtener datos actualizados después de commit
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


# TODO: Implementar crear_libro


# TODO: Implementar obtener_libro


# TODO: Implementar listar_libros (con filtro opcional por autor)


# TODO: Implementar actualizar_libro


# TODO: Implementar eliminar_libro


if __name__ == "__main__":
    with Session(engine) as db:
        # TODO: Demostrar cada operación CRUD
        print("=== CREAR ===")
        # libro = crear_libro(db, "Cien Años de Soledad",
        #                     "García Márquez", 1967, 471)
        # print(f"Creado: {libro}")

        print("\n=== LEER ===")
        # obtenido = obtener_libro(db, 1)
        # print(f"Obtenido: {obtenido}")

        print("\n=== ACTUALIZAR ===")
        # actualizado = actualizar_libro(db, 1, paginas=500)
        # print(f"Actualizado: {actualizado}")

        print("\n=== ELIMINAR ===")
        # eliminado = eliminar_libro(db, 1)
        # print(f"Eliminado: {eliminado}")

    import os
    os.remove("ejercicio_02.db")
