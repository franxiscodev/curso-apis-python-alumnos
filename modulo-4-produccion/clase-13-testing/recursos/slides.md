---
marp: true
theme: default
paginate: true
header: 'Clase 13: Testing Comprehensivo'
footer: 'Curso APIs Avanzadas con Python'
---

# Testing Comprehensivo
## pytest, TestClient, Fixtures y Mocking

Clase 13 - Módulo 4: Producción y Escalabilidad

---

# Pirámide de Tests

```
        /  E2E  \          Pocos, lentos
       /  Integ. \         Algunos
      /  Unitarios \       Muchos, rápidos
```

| Tipo | Herramienta | Velocidad |
|------|-------------|-----------|
| Unitario | pytest | Rápido |
| Integración | TestClient | Medio |
| Load | Locust | Lento |

---

# pytest Básico

```python
def calcular_total(precio, cantidad):
    return precio * cantidad

def test_calcular_total():
    assert calcular_total(10, 3) == 30

def test_calcular_total_cero():
    assert calcular_total(10, 0) == 0
```

```bash
pytest test_file.py -v
```

---

# TestClient de FastAPI

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_listar():
    response = client.get("/items")
    assert response.status_code == 200

def test_crear():
    response = client.post(
        "/items",
        json={"nombre": "Test", "precio": 10}
    )
    assert response.status_code == 201
```

---

# Fixtures

```python
import pytest

@pytest.fixture
def datos_prueba():
    return {"nombre": "Test", "precio": 10.0}

@pytest.fixture
def client_limpio():
    # Setup
    store.clear()
    client = TestClient(app)
    yield client
    # Cleanup
    store.clear()

def test_con_fixture(client_limpio, datos_prueba):
    resp = client_limpio.post("/items", json=datos_prueba)
    assert resp.status_code == 201
```

---

# Mocking de Dependencias

```python
@pytest.fixture
def client_mock():
    def mock_db():
        return FakeDB()

    app.dependency_overrides[get_db] = mock_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
```

Reemplaza dependencias reales por simulaciones

---

# Testing Auth

```python
def crear_token_test(username, rol="user"):
    return jwt.encode(
        {"sub": username, "rol": rol, "exp": ...},
        SECRET_KEY
    )

def test_endpoint_protegido():
    token = crear_token_test("user1")
    resp = client.get(
        "/protegido",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200
```

---

# parametrize

```python
@pytest.mark.parametrize("edad,esperado", [
    (10, "menor"),
    (30, "adulto"),
    (70, "senior"),
])
def test_categorizar(edad, esperado):
    assert categorizar(edad) == esperado
```

Un test, múltiples casos

---

# Cobertura

```bash
pytest --cov=mi_app --cov-report=term-missing

Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
mi_app/main.py      45      3    93%   34-36
mi_app/models.py    20      0   100%
```

Objetivo: >80% en código crítico

---

# Resumen

| Concepto | Herramienta |
|----------|-------------|
| Tests unitarios | `pytest` + `assert` |
| Tests endpoints | `TestClient` |
| Fixtures | `@pytest.fixture` |
| Mocking deps | `dependency_overrides` |
| Parametrizar | `@pytest.mark.parametrize` |
| Cobertura | `pytest-cov` |
| Auth testing | Token de test + headers |

---

# Próxima Clase

**Clase 14: Containerización y CI/CD**

- Docker multi-stage builds
- GitHub Actions pipeline
- Tests automatizados en CI

---

# Recursos

- **pytest**: https://docs.pytest.org
- **FastAPI Testing**: https://fastapi.tiangolo.com/tutorial/testing/
- **pytest-cov**: https://pytest-cov.readthedocs.io

**Practica:**
```bash
pytest ejemplos/ -v --cov
```
