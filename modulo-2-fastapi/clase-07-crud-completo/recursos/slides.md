---
marp: true
theme: default
paginate: true
header: 'Clase 07: CRUD Completo y Paginación'
footer: 'Curso APIs Avanzadas con Python'
---

# CRUD Completo y Paginación
## APIs Profesionales con FastAPI

Clase 07 - Módulo 2: FastAPI

---

# Repaso: ¿Qué sabemos?

De la **Clase 05** (Pydantic):
- Modelos, validación, Field

De la **Clase 06** (FastAPI Básico):
- Rutas, parámetros, request body, responses

**Hoy**: Patrones profesionales de CRUD

---

# Patrón de Modelos Separados

```python
class ProductoBase(BaseModel):
    nombre: str
    precio: float

class ProductoCrear(ProductoBase):
    pass  # Hereda campos de Base

class ProductoActualizar(BaseModel):
    nombre: str | None = None  # Todo opcional
    precio: float | None = None

class ProductoResponse(ProductoBase):
    id: int  # Campos adicionales
    disponible: bool
```

---

# ¿Por qué separar modelos?

| Modelo | Propósito |
|--------|-----------|
| **Base** | Campos comunes |
| **Create** | Lo requerido para crear |
| **Update** | Todo opcional (parcial) |
| **Response** | Incluye ID, calculados |

Cada operación tiene necesidades distintas

---

# Update Parcial

```python
@app.put("/productos/{id}")
def actualizar(id: int, producto: ProductoActualizar):
    actual = productos_db[id]

    # Solo actualiza campos enviados
    datos = producto.model_dump(exclude_none=True)
    for campo, valor in datos.items():
        actual[campo] = valor

    return actual
```

**Clave:** `model_dump(exclude_none=True)`

---

# Paginación: El Problema

```
GET /items → 10,000 resultados
```

Ineficiente y lento

**Solución: Paginación**

```
GET /items?page=1&size=10 → 10 resultados + metadata
```

---

# Paginación: La Respuesta

```json
{
  "items": [...],
  "total": 150,
  "page": 2,
  "size": 10,
  "pages": 15
}
```

El frontend sabe: "Página 2 de 15"

---

# Modelo de Paginación

```python
class PaginatedResponse(BaseModel):
    items: list[ItemResponse]
    total: int
    page: int
    size: int
    pages: int

@app.get("/items", response_model=PaginatedResponse)
def listar(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100)
):
    ...
```

---

# Helper de Paginación

```python
import math

def paginar(items: list, page: int, size: int):
    total = len(items)
    pages = math.ceil(total / size)
    start = (page - 1) * size
    return {
        "items": items[start:start + size],
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }
```

---

# Filtrado con Query Params

```python
@app.get("/items")
def listar(
    categoria: str | None = None,
    precio_min: float | None = None,
    precio_max: float | None = None,
):
    resultados = list(items_db.values())

    if categoria:
        resultados = [i for i in resultados
                      if i["categoria"] == categoria]
    if precio_min is not None:
        resultados = [i for i in resultados
                      if i["precio"] >= precio_min]
    ...
```

---

# Ordenamiento

```python
@app.get("/items")
def listar(
    sort_by: Literal["nombre", "precio"] = "nombre",
    order: Literal["asc", "desc"] = "asc"
):
    resultados = list(items_db.values())

    # Ordenar
    reverse = order == "desc"
    resultados.sort(
        key=lambda i: i[sort_by],
        reverse=reverse
    )
    return resultados
```

---

# Filtrar + Ordenar + Paginar

El orden importa:

1. **Filtrar** → Reducir dataset
2. **Ordenar** → Aplicar orden
3. **Paginar** → Cortar en páginas

Igual que en pandas:
```python
df[filtro].sort_values(col)[start:end]
```

---

# Errores HTTP: Más allá del 404

```python
# 404 - No encontrado
raise HTTPException(status_code=404,
    detail="Producto no encontrado")

# 409 - Conflicto (duplicado)
raise HTTPException(status_code=409,
    detail="Email ya registrado")

# 400 - Error de negocio
raise HTTPException(status_code=400,
    detail="No se puede eliminar con stock > 0")
```

---

# Errores por Operación

| Operación | Éxito | Errores |
|-----------|-------|---------|
| GET lista | 200 | - |
| GET uno | 200 | 404 |
| POST | 201 | 409, 400 |
| PUT | 200 | 404, 400 |
| DELETE | 204 | 404, 400 |

---

# Ejercicio Práctico

Crear una **API de Inventario**:

1. Modelos separados (Create/Update/Response)
2. CRUD completo con validaciones
3. Paginación con metadata
4. Filtros y ordenamiento
5. Errores HTTP consistentes

---

# Próxima Clase

**Clase 08: SQLAlchemy y Persistencia**

- Base de datos real (SQLite → PostgreSQL)
- Modelos SQLAlchemy vs Pydantic
- Migraciones con Alembic
- CRUD con persistencia real

---

# Recursos

- **Documentación**: https://fastapi.tiangolo.com/tutorial/
- **Pydantic**: https://docs.pydantic.dev
- **HTTP Status**: https://developer.mozilla.org/es/docs/Web/HTTP/Status

**Practica:**
```bash
uvicorn ejemplos.api_contactos:app --reload
```
