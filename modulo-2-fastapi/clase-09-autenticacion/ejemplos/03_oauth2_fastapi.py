"""
OAuth2 con FastAPI
===================
Proteger endpoints con Bearer tokens.

Ejecutar:
    uvicorn ejemplos.03_oauth2_fastapi:app --reload

Conceptos:
    - OAuth2PasswordBearer para extraer tokens
    - OAuth2PasswordRequestForm para login
    - Depends() para proteger rutas
    - Swagger UI "Authorize" button
"""

from datetime import timedelta, timezone, datetime

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

app = FastAPI(title="OAuth2 Demo", version="1.0.0")

SECRET_KEY = "clave-secreta-de-desarrollo"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# =============================================================================
# MODELOS Y "BASE DE DATOS"
# =============================================================================


class UsuarioResponse(BaseModel):
    """Schema de respuesta de usuario."""
    username: str
    nombre: str
    rol: str


# Base de datos simulada con contraseñas hasheadas
usuarios_db: dict[str, dict] = {
    "admin": {
        "username": "admin",
        "nombre": "Administrador",
        "password_hash": pwd_context.hash("admin123"),
        "rol": "admin"
    },
    "usuario1": {
        "username": "usuario1",
        "nombre": "Ana García",
        "password_hash": pwd_context.hash("pass123"),
        "rol": "usuario"
    }
}


# =============================================================================
# FUNCIONES DE AUTENTICACIÓN
# =============================================================================


def autenticar_usuario(username: str, password: str) -> dict | None:
    """Verifica credenciales y retorna usuario o None."""
    usuario = usuarios_db.get(username)
    if not usuario or not pwd_context.verify(password, usuario["password_hash"]):
        return None
    return usuario


def crear_token(datos: dict) -> str:
    """Crea JWT con expiración de 30 minutos."""
    payload = datos.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=30)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def obtener_usuario_actual(token: str = Depends(oauth2_scheme)) -> dict:
    """Dependency: decodifica token y retorna usuario."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    usuario = usuarios_db.get(username)
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return usuario


# =============================================================================
# ENDPOINTS
# =============================================================================


@app.post("/auth/login", tags=["Auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login: retorna token JWT."""
    usuario = autenticar_usuario(form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"}
        )
    token = crear_token(datos={"sub": usuario["username"]})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/publico", tags=["Endpoints"])
def ruta_publica():
    """Endpoint público: no requiere autenticación."""
    return {"mensaje": "Esto es público, cualquiera puede verlo"}


@app.get("/protegido", response_model=UsuarioResponse, tags=["Endpoints"])
def ruta_protegida(usuario: dict = Depends(obtener_usuario_actual)):
    """Endpoint protegido: requiere token válido."""
    return usuario


@app.get("/mi-perfil", response_model=UsuarioResponse, tags=["Endpoints"])
def mi_perfil(usuario: dict = Depends(obtener_usuario_actual)):
    """Obtener perfil del usuario autenticado."""
    return usuario


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
