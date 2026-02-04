---
marp: true
theme: default
paginate: true
header: 'Clase 01: Introducción a APIs y Type Hints'
footer: 'Curso APIs Python - Módulo 1'
---

# Clase 01
## Introducción a APIs y Type Hints en Python

---

# ¿Qué es una API?

**API** = Application Programming Interface

Un **contrato** que define cómo dos sistemas se comunican.

```
Tu App  ───solicitud───>  Servidor
        <───respuesta───
```

---

# ¿Qué es REST?

**REST** = Representational State Transfer

- **Recursos** → URLs (`/usuarios`, `/productos/123`)
- **Métodos HTTP** → Acciones (GET, POST, PUT, DELETE)
- **JSON** → Formato de datos

---

# Métodos HTTP = Operaciones CRUD

| Método | Operación | Ejemplo |
|--------|-----------|---------|
| **GET** | Leer | `GET /usuarios/1` |
| **POST** | Crear | `POST /usuarios` + body |
| **PUT** | Reemplazar | `PUT /usuarios/1` + body completo |
| **PATCH** | Modificar | `PATCH /usuarios/1` + campos parciales |
| **DELETE** | Eliminar | `DELETE /usuarios/1` |

---

# Ejemplo: API REST

```http
GET /usuarios/1

HTTP/1.1 200 OK
{
  "id": 1,
  "nombre": "Ana García",
  "email": "ana@ejemplo.com"
}
```

---

# Códigos de Estado HTTP

```
2xx ÉXITO          4xx ERROR CLIENTE       5xx ERROR SERVIDOR
─────────          ─────────────────       ──────────────────
200 OK             400 Bad Request         500 Internal Error
201 Created        401 Unauthorized        503 Unavailable
204 No Content     404 Not Found
                   422 Unprocessable
```

---

# Herramientas para Probar APIs

En este curso usaremos **3 herramientas** complementarias:

| Herramienta | Tipo | Uso Principal |
|-------------|------|---------------|
| **Archivos .http** | Texto | Documentación ejecutable |
| **Thunder Client** | VS Code | Exploración visual |
| **Postman** | App externa | Testing profesional |

---

# Archivos .http (REST Client)

```http
### Variables
@baseUrl = http://localhost:8000

### Crear usuario
POST {{baseUrl}}/api/v1/usuarios
Content-Type: application/json

{
    "nombre": "Ana",
    "email": "ana@ejemplo.com"
}
```

✅ Versionable en Git | ✅ Junto al código | ✅ Sin salir de VS Code

---

# ¿Cuándo usar cada herramienta?

| Módulo | Herramienta | Razón |
|--------|-------------|-------|
| 1-2 | `.http` files | Aprender estructura HTTP |
| 3 | Thunder Client | WebSockets, visual |
| 4 | Postman | Testing profesional |

> Hoy: Revisa `recursos/api_conceptos.http`

---

# ¿Por qué Type Hints?

### Sin tipos ❌
```python
def crear_usuario(datos):
    # ¿Qué campos tiene "datos"?
    return {"id": 1}
```

### Con tipos ✅
```python
def crear_usuario(nombre: str, email: str) -> dict:
    return {"id": 1, "nombre": nombre}
```

---

# Conexión: JSON ↔ Python Types

```http
POST /usuarios
{ "nombre": "Ana", "email": "ana@ejemplo.com", "edad": 28 }
```

↓ Se representa en Python como ↓

```python
class UsuarioInput(TypedDict):
    nombre: str
    email: str
    edad: int
```

---

# Sintaxis Básica

## Variables

```python
nombre: str = "Ana"
edad: int = 25
precio: float = 19.99
activo: bool = True
```

---

# Sintaxis Básica

## Funciones

```python
def saludar(nombre: str) -> str:
    return f"Hola, {nombre}"

def es_mayor(edad: int) -> bool:
    return edad >= 18
```

---

# Tipos Complejos - Sintaxis Moderna (Python 3.10+)

| Moderno | Antiguo | Uso |
|---------|---------|-----|
| `list[str]` | `List[str]` | Lista |
| `dict[str,int]` | `Dict[str,int]` | Diccionario |
| `str \| None` | `Optional[str]` | Opcional |
| `str \| int` | `Union[str,int]` | Unión |

> FastAPI y Pydantic v2 usan la sintaxis moderna

---

# Valores Opcionales (pueden ser None)

```python
# Sintaxis moderna Python 3.10+
def buscar_usuario(id: int) -> dict | None:
    """Retorna usuario o None si no existe."""
    usuarios = {1: {"nombre": "Ana"}}
    return usuarios.get(id)

resultado = buscar_usuario(99)  # None
```

---

# Importante

## Type hints NO validan en runtime

```python
edad: int = "veinte"  # Python NO da error
```

Son **documentación** para:
- ✅ Autocompletado en VS Code
- ✅ Detección de errores con MyPy
- ✅ FastAPI genera documentación automática

---

# TypedDict - Diccionarios estructurados

```python
from typing import TypedDict

class Usuario(TypedDict):
    id: int
    nombre: str
    email: str

usuario: Usuario = {
    "id": 1,
    "nombre": "Ana",
    "email": "ana@ejemplo.com"
}
```

---

# dataclass - Clases de datos

```python
from dataclasses import dataclass

@dataclass
class Usuario:
    nombre: str
    email: str
    activo: bool = True

usuario = Usuario("Ana", "ana@ejemplo.com")
print(usuario.nombre)  # Ana
```

---

# Conexión con el Curso

| Hoy | Próximamente |
|-----|--------------|
| `TypedDict` | Pydantic `BaseModel` |
| `dataclass` | Pydantic con validación |
| Type hints | FastAPI automático |
| `.http` files | Testing real de API |

---

# Ejercicios Prácticos

1. `ejercicio_01.py` → Tipar funciones existentes
2. `ejercicio_02.py` → Crear modelo de Libro
3. `ejercicio_03.py` → **Conectar Types con HTTP**

Verifica con: `python -m mypy ejercicio_01.py`

---

# Resumen

✅ APIs REST = Recursos + Métodos HTTP + JSON
✅ Herramientas: `.http` → Thunder Client → Postman
✅ Type hints = Contrato de datos en Python
✅ Sintaxis moderna: `str | None`
✅ Los tipos son el **contrato** de la API

---

# ¿Preguntas?

## Próxima clase:
**Decoradores en Python**

---

# Tarea para casa

1. Instala extensión **REST Client** en VS Code
2. Abre `recursos/api_conceptos.http` y revísalo
3. Completa los 3 ejercicios
4. (Opcional) Instala **Thunder Client** y explóralo
