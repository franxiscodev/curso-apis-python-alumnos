"""
Autorización por Roles
========================
Dependencies para controlar acceso según rol del usuario.

Ejecutar:
    uvicorn ejemplos.04_roles:app --reload

Conceptos:
    - Dependency que verifica rol
    - Encadenamiento de dependencies
    - 403 Forbidden vs 401 Unauthorized
    - Credenciales: admin/admin123, usuario1/pass123
"""

from datetime import timedelta, timezone, datetime

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
import bcrypt  # Cambiado: de passlib a bcrypt

app = FastAPI(title="Roles Demo", version="1.0.0")

SECRET_KEY = "clave-secreta-de-desarrollo"
ALGORITHM = "HS256"

# Eliminado pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# =============================================================================
# FUNCIONES DE HASHING
# =============================================================================

def hash_password(password: str) -> str:
    """Hashea una contraseña usando bcrypt."""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(password_bytes, salt)
    return hash_bytes.decode('utf-8')


def verify_password(password_plain: str, password_hash: str) -> bool:
    """Verifica una contraseña contra su hash."""
    password_bytes = password_plain.encode('utf-8')
    hash_bytes = password_hash.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hash_bytes)


# =============================================================================
# DATOS
# =============================================================================


class UsuarioResponse(BaseModel):
    """Schema de respuesta."""
    username: str
    nombre: str
    rol: str


usuarios_db: dict[str, dict] = {
    "admin": {
        "username": "admin", "nombre": "Admin",
        "password_hash": hash_password("admin123"), "rol": "admin"  # Cambiado
    },
    "editor": {
        "username": "editor", "nombre": "Editor",
        "password_hash": hash_password("editor123"), "rol": "editor"  # Cambiado
    },
    "lector": {
        "username": "lector", "nombre": "Lector",
        "password_hash": hash_password("lector123"), "rol": "lector"  # Cambiado
    },
}


# =============================================================================
# AUTH + ROLES
# =============================================================================


def crear_token(datos: dict) -> str:
    """Crea JWT."""
    payload = {**datos, "exp": datetime.now(timezone.utc) + timedelta(minutes=30)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def obtener_usuario_actual(token: str = Depends(oauth2_scheme)) -> dict:
    """Dependency: usuario autenticado."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username or username not in usuarios_db:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    return usuarios_db[username]


def requiere_rol(*roles_permitidos: str):
    """Crea dependency que verifica si el usuario tiene uno de los roles."""
    def verificar(usuario: dict = Depends(obtener_usuario_actual)) -> dict:
        if usuario["rol"] not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere rol: {', '.join(roles_permitidos)}"
            )
        return usuario
    return verificar


# =============================================================================
# ENDPOINTS
# =============================================================================


@app.post("/auth/login", tags=["Auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login."""
    usuario = usuarios_db.get(form_data.username)
    if not usuario or not verify_password(form_data.password, usuario["password_hash"]):  # Cambiado
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    token = crear_token({"sub": usuario["username"]})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/articulos", tags=["Contenido"])
def listar_articulos(usuario: dict = Depends(obtener_usuario_actual)):
    """Cualquier usuario autenticado puede leer."""
    return {"articulos": ["Artículo 1", "Artículo 2"], "usuario": usuario["nombre"]}


@app.post("/articulos", tags=["Contenido"])
def crear_articulo(
    titulo: str,
    usuario: dict = Depends(requiere_rol("admin", "editor"))
):
    """Solo admin y editor pueden crear."""
    return {"mensaje": f"Artículo '{titulo}' creado por {usuario['nombre']}"}


@app.delete("/articulos/{id}", tags=["Contenido"])
def eliminar_articulo(
    id: int,
    usuario: dict = Depends(requiere_rol("admin"))
):
    """Solo admin puede eliminar."""
    return {"mensaje": f"Artículo {id} eliminado por {usuario['nombre']}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
