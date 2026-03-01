"""
CRUD con SQLAlchemy
====================
Operaciones Create, Read, Update, Delete con sesiones.

Ejecutar:
    python ejemplos/02_crud_sqlalchemy.py

Conceptos:
    - session.add() para crear
    - select() con filtros para leer
    - Asignación directa para actualizar
    - session.delete() para eliminar
    - commit() y rollback()
"""

from sqlalchemy import String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


# =============================================================================
# SETUP
# =============================================================================


engine = create_engine("sqlite:///ejemplo_02.db")


class Base(DeclarativeBase):
    pass


class Contacto(Base):
    """Modelo de contacto."""
    __tablename__ = "contactos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    telefono: Mapped[str | None] = mapped_column(String(20), default=None)

    def __repr__(self) -> str:
        return f"Contacto(id={self.id}, nombre='{self.nombre}')"


Base.metadata.create_all(bind=engine)


# =============================================================================
# OPERACIONES CRUD
# =============================================================================


def crear_contacto(session: Session, nombre: str, email: str,
                   telefono: str | None = None) -> Contacto:
    """CREATE: Insertar nuevo contacto."""
    contacto = Contacto(nombre=nombre, email=email, telefono=telefono)
    session.add(contacto)
    session.commit()
    session.refresh(contacto)  # Obtener el ID generado
    return contacto


def obtener_contacto(session: Session, contacto_id: int) -> Contacto | None:
    """READ: Obtener contacto por ID."""
    return session.get(Contacto, contacto_id)


def listar_contactos(session: Session, nombre: str | None = None) -> list[Contacto]:
    """READ: Listar contactos con filtro opcional."""
    stmt = select(Contacto)
    if nombre:
        stmt = stmt.where(Contacto.nombre.contains(nombre))
    return list(session.execute(stmt).scalars().all())


def actualizar_contacto(session: Session, contacto_id: int,
                        **campos) -> Contacto | None:
    """UPDATE: Actualizar campos de un contacto."""
    contacto = session.get(Contacto, contacto_id)
    if not contacto:
        return None
    for campo, valor in campos.items():
        if hasattr(contacto, campo):
            setattr(contacto, campo, valor)
    session.commit()
    session.refresh(contacto)
    return contacto


def eliminar_contacto(session: Session, contacto_id: int) -> bool:
    """DELETE: Eliminar contacto por ID."""
    contacto = session.get(Contacto, contacto_id)
    if not contacto:
        return False
    session.delete(contacto)
    session.commit()
    return True


# =============================================================================
# DEMOSTRACIÓN
# =============================================================================


if __name__ == "__main__":
    with Session(engine) as db:
        # CREATE
        print("=== CREAR ===")
        c1 = crear_contacto(db, "Ana García", "ana3@ejemplo.com", "600111222")
        c2 = crear_contacto(db, "Luis Pérez", "luis15@ejemplo.com")
        c3 = crear_contacto(db, "María López",
                            "maria@ejemplo.com", "600333444")
        print(f"Creados: {c1}, {c2}, {c3}")

        # READ
        print("\n=== LEER ===")
        contacto = obtener_contacto(db, 1)
        print(f"Por ID 1: {contacto}")

        todos = listar_contactos(db)
        print(f"Total: {len(todos)}")

        filtrados = listar_contactos(db, nombre="García")
        print(f"Con 'García': {filtrados}")

        # UPDATE
        print("\n=== ACTUALIZAR ===")
        actualizado = actualizar_contacto(db, 2, telefono="600999888")
        print(f"Actualizado: {actualizado} → tel: {actualizado.telefono}")

        # DELETE
        print("\n=== ELIMINAR ===")
        eliminado = eliminar_contacto(db, 3)
        print(f"Eliminado ID 3: {eliminado}")
        print(f"Total restante: {len(listar_contactos(db))}")

    # Cerrar el engine para liberar el archivo
    # engine.dispose()

    import os
    os.remove("ejemplo_02.db")
    print("\nBase de datos eliminada (era solo demo)")
