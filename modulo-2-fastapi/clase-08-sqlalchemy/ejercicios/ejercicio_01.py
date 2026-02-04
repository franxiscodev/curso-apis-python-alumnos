"""
Ejercicio 01: Modelos SQLAlchemy y Creación de Tablas
======================================================
Definir modelos SQLAlchemy 2.0 y realizar operaciones básicas.

OBJETIVO:
Practicar la definición de modelos con Mapped y mapped_column.

INSTRUCCIONES:
1. Definir un modelo SQLAlchemy `Estudiante` con:
   - id: int (primary key)
   - nombre: str (max 100 caracteres)
   - email: str (max 100, unique)
   - edad: int
   - carrera: str (max 50)
   - promedio: float (nullable, puede ser None)

2. Crear las tablas en SQLite

3. Insertar al menos 3 estudiantes

4. Consultar:
   - Todos los estudiantes
   - Estudiantes de una carrera específica
   - Estudiantes ordenados por promedio (descendente)

PRUEBAS:
    python ejercicio_01.py

    # Debe imprimir:
    # - Lista de todos los estudiantes
    # - Filtrados por carrera
    # - Ordenados por promedio

PISTAS:
- Usa DeclarativeBase como base
- Mapped[str | None] para campos opcionales
- select(Modelo).where(...) para filtrar
- .order_by(Modelo.campo.desc()) para ordenar descendente
"""

from sqlalchemy import String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

engine = create_engine("sqlite:///ejercicio_01.db")


class Base(DeclarativeBase):
    pass


# TODO: Definir modelo Estudiante
# class Estudiante(Base):
#     __tablename__ = "estudiantes"
#     ...


# Crear tablas
Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    with Session(engine) as db:
        # TODO: Insertar al menos 3 estudiantes
        pass

        # TODO: Consultar todos
        # todos = db.execute(select(Estudiante)).scalars().all()
        # print("Todos:", todos)

        # TODO: Filtrar por carrera
        # filtrados = db.execute(
        #     select(Estudiante).where(Estudiante.carrera == "...")
        # ).scalars().all()

        # TODO: Ordenar por promedio descendente
        # ordenados = db.execute(
        #     select(Estudiante).order_by(Estudiante.promedio.desc())
        # ).scalars().all()

    # Limpiar
    import os
    os.remove("ejercicio_01.db")
