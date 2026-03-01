"""
Ejercicio 01: Modelos SQLAlchemy y Creación de Tablas - SOLUCIÓN
=================================================================
"""

from sqlalchemy import String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

engine = create_engine("sqlite:///ejercicio_01.db")


class Base(DeclarativeBase):
    pass


class Estudiante(Base):
    """Modelo de estudiante."""
    __tablename__ = "estudiantes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    edad: Mapped[int]
    carrera: Mapped[str] = mapped_column(String(50))
    promedio: Mapped[float | None] = mapped_column(default=None)

    def __repr__(self) -> str:
        return f"Estudiante(id={self.id}, nombre='{self.nombre}', promedio={self.promedio})"


Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    with Session(engine) as db:
        # Insertar estudiantes
        estudiantes = [
            Estudiante(nombre="Ana García", email="ana@uni.edu",
                       edad=22, carrera="Data Science", promedio=9.2),
            Estudiante(nombre="Luis Pérez", email="luis@uni.edu",
                       edad=24, carrera="Ingeniería", promedio=8.5),
            Estudiante(nombre="María López", email="maria@uni.edu",
                       edad=21, carrera="Data Science", promedio=9.7),
            Estudiante(nombre="Carlos Ruiz", email="carlos@uni.edu",
                       edad=23, carrera="Ingeniería", promedio=7.8),
            Estudiante(nombre="Laura Martín", email="laura@uni.edu",
                       edad=22, carrera="Data Science", promedio=8.9),
        ]
        db.add_all(estudiantes)
        db.commit()

        # Consultar todos
        print("=== Todos los estudiantes ===")
        todos = db.execute(select(Estudiante)).scalars().all()
        for e in todos:
            print(f"  {e}")

        # Filtrar por carrera
        print("\n=== Data Science ===")
        ds = db.execute(
            select(Estudiante).where(Estudiante.carrera == "Data Science")
        ).scalars().all()
        for e in ds:
            print(f"  {e}")

        # Ordenar por promedio descendente
        print("\n=== Por promedio (desc) ===")
        ordenados = db.execute(
            select(Estudiante).order_by(Estudiante.promedio.desc())
        ).scalars().all()
        for e in ordenados:
            print(f"  {e.nombre}: {e.promedio}")

    import os
    os.remove("ejercicio_01.db")
    print("\nBase de datos eliminada")
