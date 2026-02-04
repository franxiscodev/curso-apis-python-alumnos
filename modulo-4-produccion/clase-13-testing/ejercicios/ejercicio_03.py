"""
Ejercicio 03: Tests Completos con Auth y Mock
===============================================
Testing avanzado con autenticación y mocking.

INSTRUCCIONES:
1. Escribir tests para endpoints protegidos
2. Crear fixture que genera tokens JWT de test
3. Mockear dependencia de servicio externo
4. Testear roles (user vs admin)

Ejecutar: pytest ejercicios/ejercicio_03.py -v
"""

from datetime import datetime, timedelta, timezone

import pytest
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.testclient import TestClient
from jose import jwt

SECRET = "test-secret"
ALGO = "HS256"

app = FastAPI()
oauth2 = OAuth2PasswordBearer(tokenUrl="/login")


def get_usuario(token: str = Depends(oauth2)) -> dict:
    try:
        p = jwt.decode(token, SECRET, algorithms=[ALGO])
        return {"username": p["sub"], "rol": p.get("rol", "user")}
    except Exception:
        raise HTTPException(status_code=401)


def get_datos_externos() -> dict:
    """Simula servicio externo."""
    raise RuntimeError("No llamar en tests")


@app.get("/perfil")
def perfil(user: dict = Depends(get_usuario)):
    return {"usuario": user["username"]}


@app.get("/admin")
def admin(user: dict = Depends(get_usuario)):
    if user["rol"] != "admin":
        raise HTTPException(status_code=403)
    return {"admin": True}


@app.get("/datos")
def datos(
    user: dict = Depends(get_usuario),
    externos: dict = Depends(get_datos_externos),
):
    return {"usuario": user["username"], "datos": externos}


# TODO: Helper crear_token(username, rol) → str

# TODO: Fixture token_user (rol="user")

# TODO: Fixture token_admin (rol="admin")

# TODO: Fixture client_con_mock (mockear get_datos_externos)

# TODO: test_perfil_sin_token (401)

# TODO: test_perfil_con_token (200)

# TODO: test_admin_sin_permisos (403)

# TODO: test_admin_con_permisos (200)

# TODO: test_datos_con_mock (200, servicio mockeado)
