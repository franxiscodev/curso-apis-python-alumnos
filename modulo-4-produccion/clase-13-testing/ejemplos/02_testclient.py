"""
Ejemplo 02: TestClient de FastAPI
====================================
Tests de integración para endpoints.

Ejecutar:
    pytest ejemplos/02_testclient.py -v
"""

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel

# === API A TESTEAR ===

app = FastAPI()

items: dict[int, dict] = {
    1: {"id": 1, "nombre": "Item A", "precio": 10.0},
    2: {"id": 2, "nombre": "Item B", "precio": 20.0},
}
next_id = 3


class ItemCrear(BaseModel):
    nombre: str
    precio: float


@app.get("/items")
def listar_items():
    return list(items.values())


@app.get("/items/{item_id}")
def obtener_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return items[item_id]


@app.post("/items", status_code=201)
def crear_item(item: ItemCrear):
    global next_id
    nuevo = {"id": next_id, "nombre": item.nombre, "precio": item.precio}
    items[next_id] = nuevo
    next_id += 1
    return nuevo


@app.delete("/items/{item_id}", status_code=204)
def eliminar_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    del items[item_id]


# === TESTS ===

client = TestClient(app)


def test_listar_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_obtener_item_existente():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["nombre"] == "Item A"


def test_obtener_item_no_existente():
    response = client.get("/items/999")
    assert response.status_code == 404
    assert "no encontrado" in response.json()["detail"]


def test_crear_item():
    response = client.post(
        "/items", json={"nombre": "Item Nuevo", "precio": 30.0}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Item Nuevo"
    assert data["precio"] == 30.0
    assert "id" in data


def test_crear_item_invalido():
    response = client.post("/items", json={"nombre": "Sin precio"})
    assert response.status_code == 422  # Validation error


def test_eliminar_item_no_existente():
    response = client.delete("/items/999")
    assert response.status_code == 404
