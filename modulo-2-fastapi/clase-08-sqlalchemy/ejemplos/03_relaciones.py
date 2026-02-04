"""
Relaciones entre Tablas
========================
Relaciones one-to-many con SQLAlchemy 2.0.

Ejecutar:
    python ejemplos/03_relaciones.py

Conceptos:
    - ForeignKey para claves foráneas
    - relationship() con back_populates
    - Acceso a datos relacionados
    - Consultas con joins implícitos
"""

from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
)


# =============================================================================
# SETUP
# =============================================================================


engine = create_engine("sqlite:///ejemplo_03.db")


class Base(DeclarativeBase):
    pass


# =============================================================================
# MODELOS CON RELACIONES
# =============================================================================


class Autor(Base):
    """Un autor tiene muchos libros (one-to-many)."""
    __tablename__ = "autores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    pais: Mapped[str] = mapped_column(String(50))

    # Relación: un autor → muchos libros
    libros: Mapped[list["Libro"]] = relationship(back_populates="autor")

    def __repr__(self) -> str:
        return f"Autor(id={self.id}, nombre='{self.nombre}')"


class Libro(Base):
    """Un libro pertenece a un autor."""
    __tablename__ = "libros"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200))
    año: Mapped[int]

    # Clave foránea: apunta a autores.id
    autor_id: Mapped[int] = mapped_column(ForeignKey("autores.id"))

    # Relación inversa: un libro → un autor
    autor: Mapped["Autor"] = relationship(back_populates="libros")

    def __repr__(self) -> str:
        return f"Libro(id={self.id}, titulo='{self.titulo}')"


Base.metadata.create_all(bind=engine)


# =============================================================================
# DEMOSTRACIÓN
# =============================================================================


if __name__ == "__main__":
    with Session(engine) as db:
        # Crear autores
        garcia_marquez = Autor(nombre="Gabriel García Márquez", pais="Colombia")
        cortazar = Autor(nombre="Julio Cortázar", pais="Argentina")
        db.add_all([garcia_marquez, cortazar])
        db.commit()

        # Crear libros asociados a autores
        libros = [
            Libro(titulo="Cien Años de Soledad", año=1967, autor=garcia_marquez),
            Libro(titulo="El Amor en los Tiempos del Cólera", año=1985,
                  autor=garcia_marquez),
            Libro(titulo="Rayuela", año=1963, autor=cortazar),
            Libro(titulo="Bestiario", año=1951, autor=cortazar),
        ]
        db.add_all(libros)
        db.commit()

        # Acceder a libros desde el autor
        print("=== Libros por autor ===")
        autores = db.execute(select(Autor)).scalars().all()
        for autor in autores:
            print(f"\n{autor.nombre} ({autor.pais}):")
            for libro in autor.libros:
                print(f"  - {libro.titulo} ({libro.año})")

        # Acceder al autor desde el libro
        print("\n=== Autor de cada libro ===")
        todos_libros = db.execute(
            select(Libro).order_by(Libro.año)
        ).scalars().all()
        for libro in todos_libros:
            print(f"  {libro.titulo} ({libro.año}) → {libro.autor.nombre}")

        # Filtrar libros por país del autor
        print("\n=== Libros de autores colombianos ===")
        stmt = select(Libro).join(Autor).where(Autor.pais == "Colombia")
        colombianos = db.execute(stmt).scalars().all()
        for libro in colombianos:
            print(f"  {libro.titulo}")

    import os
    os.remove("ejemplo_03.db")
    print("\nBase de datos eliminada (era solo demo)")
