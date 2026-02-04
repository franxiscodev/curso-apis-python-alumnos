"""
Ejemplo 03: Fixtures y Mocking
================================
Fixtures reutilizables y mock de dependencias.

Ejecutar:
    pytest ejemplos/03_fixtures_mocking.py -v
"""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

# === API CON DEPENDENCIA ===

app = FastAPI()


def obtener_servicio_externo() -> dict:
    """Dependencia que llama a un servicio externo."""
    raise RuntimeError("No debería llamarse en tests")


@app.get("/datos")
def obtener_datos(servicio: dict = Depends(obtener_servicio_externo)):
    return {"datos": servicio, "origen": "externo"}


# === FIXTURES ===


@pytest.fixture
def datos_prueba():
    """Fixture que provee datos de prueba."""
    return [
        {"id": 1, "nombre": "Test A", "valor": 100},
        {"id": 2, "nombre": "Test B", "valor": 200},
    ]


@pytest.fixture
def client_con_mock():
    """TestClient con dependencia mockeada."""
    def mock_servicio():
        return {"status": "ok", "datos": [1, 2, 3]}

    app.dependency_overrides[obtener_servicio_externo] = mock_servicio
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# === TESTS CON FIXTURES ===


def test_datos_prueba(datos_prueba):
    assert len(datos_prueba) == 2
    assert datos_prueba[0]["nombre"] == "Test A"


def test_endpoint_con_mock(client_con_mock):
    response = client_con_mock.get("/datos")
    assert response.status_code == 200
    data = response.json()
    assert data["datos"]["status"] == "ok"


# === TESTS CON PATCH ===


def test_con_patch():
    """Mockear una función con patch."""
    with patch("ejemplos.03_fixtures_mocking.obtener_servicio_externo") as mock:
        mock.return_value = {"mock": True}
        resultado = mock()
        assert resultado["mock"] is True


# === PARAMETRIZE ===


@pytest.mark.parametrize("precio,cantidad,esperado", [
    (10.0, 1, 10.0),
    (10.0, 3, 30.0),
    (5.5, 2, 11.0),
    (0.0, 10, 0.0),
])
def test_calcular_total_parametrizado(precio, cantidad, esperado):
    assert precio * cantidad == esperado
