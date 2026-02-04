"""
API con Autenticación Completa
================================
Registro, login, JWT, roles y usuarios en SQLAlchemy.

Ejecutar:
    uvicorn ejemplos.api_auth_completa:app --reload

Credenciales iniciales:
    admin / admin123

Endpoints:
    POST /auth/registro     - Registrar nuevo usuario
    POST /auth/login        - Login (retorna JWT)
    GET  /auth/me           - Perfil del usuario actual
    GET  /usuarios          - Listar usuarios (solo admin)
"""

from datetime import datetime, timedelta, timezone

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import String, create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    sessionmaker,
)


# =============================================================================
# CONFIGURACIÓN
# =============================================================================


SECRET_KEY = "clave-secreta-solo-para-desarrollo-cambiar-en-produccion"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

engine = create_engine("sqlite:///auth_app.db")
SessionLocal = sessionmaker(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class Base(DeclarativeBase):
    pass


# =============================================================================
# MODELO SQLALCHEMY
# =============================================================================


class Usuario(Base):
    """Tabla de usuarios."""
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    nombre: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(String(200))
    rol: Mapped[str] = mapped_column(String(20), default="usuario")
    activo: Mapped[bool] = mapped_column(default=True)


Base.metadata.create_all(bind=engine)


# =============================================================================
# SCHEMAS PYDANTIC
# =============================================================================


class UsuarioRegistro(BaseModel):
    """Schema para registro."""
    username: str = Field(min_length=3, max_length=50)
    nombre: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=5, max_length=100)
    password: str = Field(min_length=6, max_length=100)


class UsuarioResponse(BaseModel):
    """Schema de respuesta (sin password)."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    nombre: str
    email: str
    rol: str
    activo: bool


class TokenResponse(BaseModel):
    """Schema de respuesta de token."""
    access_token: str
    token_type: str = "bearer"


# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================


def get_db():
    """Dependency de sesión."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def crear_token(datos: dict) -> str:
    """Crea JWT."""
    payload = {**datos, "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    """Dependency: obtener usuario desde token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    usuario = db.execute(
        select(Usuario).where(Usuario.username == username)
    ).scalar_one_or_none()

    if not usuario or not usuario.activo:
        raise HTTPException(status_code=401, detail="Usuario no encontrado o inactivo")
    return usuario


def requiere_admin(usuario: Usuario = Depends(obtener_usuario_actual)) -> Usuario:
    """Dependency: solo admins."""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Se requiere rol admin")
    return usuario


# =============================================================================
# DATOS INICIALES
# =============================================================================


def inicializar_admin():
    """Crea usuario admin si no existe."""
    with SessionLocal() as db:
        admin = db.execute(
            select(Usuario).where(Usuario.username == "admin")
        ).scalar_one_or_none()
        if not admin:
            admin = Usuario(
                username="admin", nombre="Administrador",
                email="admin@ejemplo.com",
                password_hash=pwd_context.hash("admin123"), rol="admin"
            )
            db.add(admin)
            db.commit()


inicializar_admin()


# =============================================================================
# APLICACIÓN
# =============================================================================


app = FastAPI(
    title="API con Autenticación",
    description="Registro, login, JWT y roles",
    version="1.0.0"
)


@app.post("/auth/registro", response_model=UsuarioResponse,
          status_code=201, tags=["Auth"])
def registrar(datos: UsuarioRegistro, db: Session = Depends(get_db)):
    """Registrar nuevo usuario."""
    # Verificar username único
    existente = db.execute(
        select(Usuario).where(Usuario.username == datos.username)
    ).scalar_one_or_none()
    if existente:
        raise HTTPException(status_code=409, detail="Username ya existe")

    # Verificar email único
    existente = db.execute(
        select(Usuario).where(Usuario.email == datos.email)
    ).scalar_one_or_none()
    if existente:
        raise HTTPException(status_code=409, detail="Email ya registrado")

    nuevo = Usuario(
        username=datos.username, nombre=datos.nombre,
        email=datos.email,
        password_hash=pwd_context.hash(datos.password)
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@app.post("/auth/login", response_model=TokenResponse, tags=["Auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    """Login: retorna token JWT."""
    usuario = db.execute(
        select(Usuario).where(Usuario.username == form_data.username)
    ).scalar_one_or_none()

    if not usuario or not pwd_context.verify(form_data.password, usuario.password_hash):
        raise HTTPException(
            status_code=401, detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"}
        )
    token = crear_token({"sub": usuario.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/auth/me", response_model=UsuarioResponse, tags=["Auth"])
def mi_perfil(usuario: Usuario = Depends(obtener_usuario_actual)):
    """Obtener perfil del usuario autenticado."""
    return usuario


@app.get("/usuarios", response_model=list[UsuarioResponse], tags=["Admin"])
def listar_usuarios(
    admin: Usuario = Depends(requiere_admin),
    db: Session = Depends(get_db)
):
    """Listar todos los usuarios (solo admin)."""
    return db.execute(select(Usuario)).scalars().all()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
