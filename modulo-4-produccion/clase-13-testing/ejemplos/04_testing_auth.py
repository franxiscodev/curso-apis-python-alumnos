"""
Ejemplo 04: Testing de Endpoints Protegidos
=============================================
Tests de autenticación JWT con FastAPI.

Ejecutar:
    pytest ejemplos/04_testing_auth.py -v
"""

from datetime import datetime, timedelta, timezone

import pytest
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.testclient import TestClient
from jose import jwt

# === API CON AUTH ===

SECRET_KEY = "test-secret-key"
ALGORITHM = "HS256"

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def obtener_usuario(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"username": payload["sub"], "rol": payload.get("rol", "user")}
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")


@app.get("/publico")
def ruta_publica():
    return {"mensaje": "Acceso libre"}


@app.get("/protegido")
def ruta_protegida(usuario: dict = Depends(obtener_usuario)):
    return {"mensaje": f"Hola {usuario['username']}"}


@app.get("/admin")
def ruta_admin(usuario: dict = Depends(obtener_usuario)):
    if usuario["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Solo admin")
    return {"mensaje": "Panel admin"}


# === HELPERS DE TEST ===


def crear_token_test(username: str, rol: str = "user") -> str:
    payload = {
        "sub": username,
        "rol": rol,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# === FIXTURES ===

client = TestClient(app)


@pytest.fixture
def token_usuario():
    return crear_token_test("testuser", "user")


@pytest.fixture
def token_admin():
    return crear_token_test("admin", "admin")


# === TESTS ===


def test_ruta_publica():
    response = client.get("/publico")
    assert response.status_code == 200


def test_protegido_sin_token():
    response = client.get("/protegido")
    assert response.status_code == 401


def test_protegido_con_token(token_usuario):
    response = client.get(
        "/protegido", headers={"Authorization": f"Bearer {token_usuario}"}
    )
    assert response.status_code == 200
    assert response.json()["mensaje"] == "Hola testuser"


def test_admin_con_usuario_normal(token_usuario):
    response = client.get(
        "/admin", headers={"Authorization": f"Bearer {token_usuario}"}
    )
    assert response.status_code == 403


def test_admin_con_admin(token_admin):
    response = client.get(
        "/admin", headers={"Authorization": f"Bearer {token_admin}"}
    )
    assert response.status_code == 200
    assert "admin" in response.json()["mensaje"].lower()


def test_token_invalido():
    response = client.get(
        "/protegido", headers={"Authorization": "Bearer token-falso"}
    )
    assert response.status_code == 401
