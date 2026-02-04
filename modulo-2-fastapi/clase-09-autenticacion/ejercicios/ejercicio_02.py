"""
Ejercicio 02: Proteger Endpoints Existentes
=============================================
Agregar autenticación a una API de notas existente.

OBJETIVO:
Practicar OAuth2PasswordBearer y Depends para proteger rutas.

INSTRUCCIONES:
1. Completar la función obtener_usuario_actual:
   - Decodificar el token JWT
   - Buscar el usuario en usuarios_db
   - Retornar 401 si token inválido o usuario no existe

2. Proteger los endpoints:
   - GET /notas          → Solo usuarios autenticados
   - POST /notas         → Solo usuarios autenticados
   - DELETE /notas/{id}  → Solo el creador de la nota

3. Agregar campo "creado_por" a las notas

PRUEBAS:
    uvicorn ejercicio_02:app --reload

    # 1. Login con: admin/admin123
    # 2. Copiar token del response
    # 3. Click "Authorize" en Swagger, pegar token
    # 4. Ahora los endpoints protegidos funcionan

PISTAS:
- OAuth2PasswordBearer(tokenUrl="/auth/login")
- jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
- Depends(obtener_usuario_actual) en los endpoints protegidos
"""

from datetime import datetime, timedelta, timezone

from fastapi import Depends, FastAPI, HTTPException, Path, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field

app = FastAPI(title="Notas Protegidas", version="1.0.0")

SECRET_KEY = "clave-de-desarrollo"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Usuarios con password hasheada
usuarios_db: dict[str, dict] = {
    "admin": {
        "username": "admin", "nombre": "Admin",
        "password_hash": pwd_context.hash("admin123"),
    },
    "ana": {
        "username": "ana", "nombre": "Ana García",
        "password_hash": pwd_context.hash("ana123"),
    },
}

# Base de datos de notas
notas_db: dict[int, dict] = {}
contador_id = 0


class NotaCrear(BaseModel):
    """Schema para crear nota."""
    titulo: str = Field(min_length=1, max_length=100)
    contenido: str | None = None


class NotaResponse(BaseModel):
    """Schema de respuesta."""
    id: int
    titulo: str
    contenido: str | None
    creado_por: str


def crear_token(datos: dict) -> str:
    """Crea JWT."""
    payload = {**datos, "exp": datetime.now(timezone.utc) + timedelta(minutes=30)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# TODO: Implementar obtener_usuario_actual(token: str = Depends(oauth2_scheme))
# - Decodificar token con jwt.decode
# - Obtener "sub" del payload
# - Buscar usuario en usuarios_db
# - Retornar el dict del usuario
# - HTTPException(401) si algo falla


@app.post("/auth/login", tags=["Auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login."""
    usuario = usuarios_db.get(form_data.username)
    if not usuario or not pwd_context.verify(form_data.password, usuario["password_hash"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    token = crear_token({"sub": usuario["username"]})
    return {"access_token": token, "token_type": "bearer"}


# TODO: GET /notas → Proteger con Depends(obtener_usuario_actual)
@app.get("/notas", response_model=list[NotaResponse], tags=["Notas"])
def listar_notas():
    """Listar notas (TODO: proteger)."""
    return list(notas_db.values())


# TODO: POST /notas → Proteger y agregar "creado_por" con username del usuario
@app.post("/notas", response_model=NotaResponse, status_code=201, tags=["Notas"])
def crear_nota(nota: NotaCrear):
    """Crear nota (TODO: proteger y agregar creado_por)."""
    global contador_id
    contador_id += 1
    nueva = {"id": contador_id, **nota.model_dump(), "creado_por": "???"}
    notas_db[contador_id] = nueva
    return nueva


# TODO: DELETE /notas/{id} → Solo el creador puede eliminar su nota
@app.delete("/notas/{nota_id}", status_code=204, tags=["Notas"])
def eliminar_nota(nota_id: int = Path(ge=1)):
    """Eliminar nota (TODO: solo el creador)."""
    if nota_id not in notas_db:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    del notas_db[nota_id]
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
