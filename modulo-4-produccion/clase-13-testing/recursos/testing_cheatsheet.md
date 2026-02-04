# Testing Comprehensivo - Cheatsheet

Guía rápida de pytest, TestClient y mocking con FastAPI.

---

## pytest Básico

```python
def test_suma():
    assert 1 + 1 == 2

def test_excepcion():
    import pytest
    with pytest.raises(ValueError):
        int("no_es_numero")
```

```bash
pytest archivo.py -v           # Verbose
pytest -k "test_crear"         # Filtrar por nombre
pytest --tb=short              # Traceback corto
```

---

## TestClient

```python
from fastapi.testclient import TestClient

client = TestClient(app)

# GET
resp = client.get("/items")
assert resp.status_code == 200
assert len(resp.json()) > 0

# POST
resp = client.post("/items", json={"nombre": "X", "precio": 10})
assert resp.status_code == 201

# DELETE
resp = client.delete("/items/1")
assert resp.status_code == 204

# Con headers
resp = client.get("/protegido", headers={"Authorization": "Bearer token"})

# Con query params
resp = client.get("/items", params={"page": 1, "size": 10})
```

---

## Fixtures

```python
import pytest

@pytest.fixture
def datos():
    return {"nombre": "Test"}

@pytest.fixture
def client_limpio():
    store.clear()
    yield TestClient(app)
    store.clear()

@pytest.fixture(autouse=True)  # Se aplica a todos los tests
def reset():
    data.clear()
    yield
```

---

## Mocking Dependencias

```python
@pytest.fixture
def client_mock():
    def mock_dep():
        return {"fake": True}
    app.dependency_overrides[dependencia_real] = mock_dep
    yield TestClient(app)
    app.dependency_overrides.clear()
```

---

## Testing Auth

```python
def token_test(username="user", rol="user"):
    return jwt.encode(
        {"sub": username, "rol": rol, "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
        SECRET, algorithm="HS256"
    )

def test_protegido():
    resp = client.get("/ruta", headers={"Authorization": f"Bearer {token_test()}"})
    assert resp.status_code == 200

def test_sin_token():
    resp = client.get("/ruta")
    assert resp.status_code == 401
```

---

## Parametrize

```python
@pytest.mark.parametrize("entrada,esperado", [
    (1, "uno"),
    (2, "dos"),
    (3, "tres"),
])
def test_convertir(entrada, esperado):
    assert convertir(entrada) == esperado
```

---

## Cobertura

```bash
uv add pytest-cov

pytest --cov=mi_app -v
pytest --cov=mi_app --cov-report=html  # Reporte HTML
```

---

## Status Codes Comunes en Tests

| Code | Significado | Cuándo testearlo |
|------|-------------|-----------------|
| 200 | OK | Happy path |
| 201 | Created | POST exitoso |
| 204 | No Content | DELETE exitoso |
| 401 | Unauthorized | Sin token |
| 403 | Forbidden | Sin permisos |
| 404 | Not Found | ID inexistente |
| 422 | Validation | Body inválido |

---

## Tips

1. **Un assert por test** cuando sea posible
2. **Nombres descriptivos**: `test_crear_usuario_duplicado_retorna_409`
3. **Fixtures** para datos y setup reutilizables
4. **autouse=True** para reset automático entre tests
5. **dependency_overrides** para mockear cualquier Depends()
6. **parametrize** para probar múltiples inputs
