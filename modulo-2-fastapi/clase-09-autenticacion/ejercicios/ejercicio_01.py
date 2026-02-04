"""
Ejercicio 01: Registro y Login Básico
=======================================
Implementar flujo de registro y login con JWT.

OBJETIVO:
Practicar hashing de contraseñas y generación de tokens JWT.

INSTRUCCIONES:
1. Implementar la función hashear_password usando CryptContext
2. Implementar la función verificar_password
3. Implementar la función crear_token (JWT con expiración 30 min)
4. Completar endpoint POST /registro:
   - Recibe UsuarioRegistro (username, password, nombre)
   - Hashea la contraseña antes de guardar
   - Retorna 409 si username ya existe
5. Completar endpoint POST /login:
   - Recibe OAuth2PasswordRequestForm
   - Verifica credenciales
   - Retorna token JWT

PRUEBAS:
    uvicorn ejercicio_01:app --reload

    # Registrar
    POST /registro {"username": "ana", "password": "segura123", "nombre": "Ana"}

    # Login (en Swagger: botón Authorize, o form-data)
    POST /login  username=ana  password=segura123

PISTAS:
- CryptContext(schemes=["bcrypt"], deprecated="auto")
- jwt.encode(payload, SECRET_KEY, algorithm="HS256")
- OAuth2PasswordRequestForm tiene .username y .password
"""

from datetime import datetime, timedelta, timezone

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field

app = FastAPI(title="Auth Básico", version="1.0.0")

SECRET_KEY = "clave-de-desarrollo"
ALGORITHM = "HS256"

# TODO: Configurar pwd_context con bcrypt
pwd_context = None

# "Base de datos" en memoria
usuarios_db: dict[str, dict] = {}


class UsuarioRegistro(BaseModel):
    """Schema para registro."""
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=100)
    nombre: str = Field(min_length=1, max_length=100)


# TODO: Implementar hashear_password(password: str) -> str


# TODO: Implementar verificar_password(plano: str, hash: str) -> bool


# TODO: Implementar crear_token(datos: dict) -> str
# Debe incluir campo "exp" con expiración de 30 minutos


# TODO: POST /registro
# - Verificar que username no exista (409 si existe)
# - Guardar con password hasheada
# - Retornar {"mensaje": "...", "username": "..."}


# TODO: POST /login
# - Usar OAuth2PasswordRequestForm
# - Verificar credenciales
# - Retornar {"access_token": token, "token_type": "bearer"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
