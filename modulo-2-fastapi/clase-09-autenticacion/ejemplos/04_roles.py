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
from passlib.context import CryptContext
from pydantic import BaseModel

app = FastAPI(title="Roles Demo", version="1.0.0")

SECRET_KEY = "clave-secreta-de-desarrollo"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


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
        "password_hash": pwd_context.hash("admin123"), "rol": "admin"
    },
    "editor": {
        "username": "editor", "nombre": "Editor",
        "password_hash": pwd_context.hash("editor123"), "rol": "editor"
    },
    "lector": {
        "username": "lector", "nombre": "Lector",
        "password_hash": pwd_context.hash("lector123"), "rol": "lector"
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
    if not usuario or not pwd_context.verify(form_data.password, usuario["password_hash"]):
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
