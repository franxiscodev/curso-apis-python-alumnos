"""
API Testeable: Diseñada para Testing
=======================================
API con dependencias inyectables para facilitar testing.

Ejecutar:
    uvicorn ejemplos.api_testeable:app --reload
Tests:
    pytest ejemplos/api_testeable.py -v
"""

import pytest
from fastapi import Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel

# === MODELOS ===


class TareaCrear(BaseModel):
    titulo: str
    descripcion: str = ""


class TareaResponse(BaseModel):
    id: int
    titulo: str
    descripcion: str
    completada: bool


# === ALMACÉN (DEPENDENCIA INYECTABLE) ===


class AlmacenTareas:
    """Almacén en memoria, reemplazable en tests."""

    def __init__(self):
        self.tareas: dict[int, dict] = {}
        self.next_id = 1

    def listar(self) -> list[dict]:
        return list(self.tareas.values())

    def obtener(self, id: int) -> dict | None:
        return self.tareas.get(id)

    def crear(self, datos: dict) -> dict:
        tarea = {"id": self.next_id, **datos, "completada": False}
        self.tareas[self.next_id] = tarea
        self.next_id += 1
        return tarea

    def completar(self, id: int) -> dict | None:
        if id in self.tareas:
            self.tareas[id]["completada"] = True
            return self.tareas[id]
        return None


almacen = AlmacenTareas()


def get_almacen() -> AlmacenTareas:
    return almacen


# === API ===

app = FastAPI(title="API Testeable", version="1.0.0")


@app.get("/tareas", response_model=list[TareaResponse], tags=["Tareas"])
def listar(store: AlmacenTareas = Depends(get_almacen)):
    return store.listar()


@app.post("/tareas", response_model=TareaResponse, status_code=201, tags=["Tareas"])
def crear(tarea: TareaCrear, store: AlmacenTareas = Depends(get_almacen)):
    return store.crear(tarea.model_dump())


@app.patch("/tareas/{id}/completar", response_model=TareaResponse, tags=["Tareas"])
def completar(id: int, store: AlmacenTareas = Depends(get_almacen)):
    tarea = store.completar(id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea


# === TESTS ===


@pytest.fixture
def client_test():
    """Client con almacén limpio."""
    store = AlmacenTareas()
    app.dependency_overrides[get_almacen] = lambda: store
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_listar_vacio(client_test):
    response = client_test.get("/tareas")
    assert response.status_code == 200
    assert response.json() == []


def test_crear_tarea(client_test):
    response = client_test.post("/tareas", json={"titulo": "Test"})
    assert response.status_code == 201
    assert response.json()["titulo"] == "Test"
    assert response.json()["completada"] is False


def test_completar_tarea(client_test):
    client_test.post("/tareas", json={"titulo": "Hacer algo"})
    response = client_test.patch("/tareas/1/completar")
    assert response.status_code == 200
    assert response.json()["completada"] is True


def test_completar_inexistente(client_test):
    response = client_test.patch("/tareas/999/completar")
    assert response.status_code == 404


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
