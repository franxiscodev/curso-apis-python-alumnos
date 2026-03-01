"""
Setup y Modelos SQLAlchemy 2.0
===============================+
Configuración del engine, Base y definición de modelos.

Ejecutar:
    python ejemplos/01_setup_modelos.py

Conceptos:
    - DeclarativeBase (SQLAlchemy 2.0)
    - Mapped y mapped_column
    - Engine y creación de tablas
    - Inserción y consulta básica
"""

from sqlalchemy import String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


# =============================================================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# =============================================================================


# Engine: conexión a SQLite (archivo local)
# echo=True muestra las queries SQL generadas
engine = create_engine("sqlite:///ejemplo_01.db", echo=True)


# Base declarativa: todas las tablas heredan de esta clase
class Base(DeclarativeBase):
    pass


# =============================================================================
# MODELOS (equivalente a definir tablas SQL)
# =============================================================================


class Producto(Base):
    """Modelo SQLAlchemy para la tabla 'productos'."""
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    precio: Mapped[float]
    categoria: Mapped[str] = mapped_column(String(50))
    stock: Mapped[int] = mapped_column(default=0)
    descripcion: Mapped[str | None] = mapped_column(String(500), default=None)

    def __repr__(self) -> str:
        return f"Producto(id={self.id}, nombre='{self.nombre}', precio={self.precio})"


# =============================================================================
# CREAR TABLAS Y DEMOSTRACIÓN
# =============================================================================


if __name__ == "__main__":
    # Crear todas las tablas definidas
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente\n")

    # Insertar datos
    with Session(engine) as session:
        productos = [
            Producto(nombre="Laptop Pro", precio=1299.99,
                     categoria="Electrónica", stock=10),
            Producto(nombre="Mouse Inalámbrico", precio=29.99,
                     categoria="Accesorios", stock=50),
            Producto(nombre="Teclado Mecánico", precio=89.99,
                     categoria="Accesorios", stock=25,
                     descripcion="Switches azules"),
        ]
        session.add_all(productos)
        session.commit()
        print(f"Insertados {len(productos)} productos\n")

    # Consultar datos
    with Session(engine) as session:
        # Todos los productos
        todos = session.execute(select(Producto)).scalars().all()
        print("Todos los productos:")
        for p in todos:
            print(f"  {p}")

        # Filtrar por categoría
        accesorios = session.execute(
            select(Producto).where(Producto.categoria == "Accesorios")
        ).scalars().all()
        print(f"\nAccesorios: {len(accesorios)} encontrados")

        # Ordenar por precio
        por_precio = session.execute(
            select(Producto).order_by(Producto.precio.desc())
        ).scalars().all()
        print("\nOrdenados por precio (desc):")
        for p in por_precio:
            print(f"  {p.nombre}: ${p.precio}")

    # Cerrar el engine para liberar el archivo
    engine.dispose()

    # Limpiar archivo de ejemplo
    import os
    os.remove("ejemplo_01.db")
    print("\nBase de datos eliminada (era solo demo)")
