# Type Hints en Python - Cheatsheet

Guía rápida de type hints con sintaxis moderna Python 3.10+.

---

## Tipos Básicos

```python
nombre: str = "Ana"
edad: int = 30
precio: float = 19.99
activo: bool = True
```

---

## Tipos Opcionales (sintaxis moderna)

```python
# Python 3.10+ (usar esta)
email: str | None = None
codigo: int | str = "ABC"

# Antigua (NO usar)
from typing import Optional, Union
email: Optional[str] = None        # ❌ Evitar
codigo: Union[int, str] = "ABC"    # ❌ Evitar
```

---

## Colecciones (sintaxis moderna)

```python
# Python 3.9+ (usar esta)
nombres: list[str] = ["Ana", "Luis"]
edades: dict[str, int] = {"Ana": 30}
ids: set[int] = {1, 2, 3}
coordenada: tuple[float, float] = (1.0, 2.0)

# Antigua (NO usar)
from typing import List, Dict, Set, Tuple  # ❌ Evitar
```

---

## Funciones

```python
def saludar(nombre: str) -> str:
    return f"Hola {nombre}"

def buscar(id: int) -> dict | None:
    ...

def procesar(items: list[str]) -> list[str]:
    ...

# Sin retorno
def log(mensaje: str) -> None:
    print(mensaje)
```

---

## TypedDict

```python
from typing import TypedDict

class Usuario(TypedDict):
    id: int
    nombre: str
    email: str
    activo: bool

# Uso
user: Usuario = {"id": 1, "nombre": "Ana", "email": "a@b.com", "activo": True}
```

---

## Dataclass

```python
from dataclasses import dataclass

@dataclass
class Producto:
    id: int
    nombre: str
    precio: float
    stock: int = 0

# Uso
p = Producto(id=1, nombre="Widget", precio=9.99)
```

---

## Progresión en el Curso

```
dict          →  TypedDict    →  dataclass     →  Pydantic BaseModel
(sin tipos)     (tipos en dict)  (clase tipada)   (validación auto)
Clase 01        Clase 01         Clase 01          Clase 05
```

---

## Métodos HTTP (Preview)

| Método | Acción | Ejemplo |
|--------|--------|---------|
| GET | Leer | `GET /usuarios` |
| POST | Crear | `POST /usuarios` |
| PUT | Actualizar (completo) | `PUT /usuarios/1` |
| PATCH | Actualizar (parcial) | `PATCH /usuarios/1` |
| DELETE | Eliminar | `DELETE /usuarios/1` |

---

## Tips

1. **Siempre** usar sintaxis moderna: `str | None` no `Optional[str]`
2. **Siempre** `list[str]` no `List[str]` (Python 3.9+)
3. **Type hints no validan** en runtime, solo son anotaciones
4. **VS Code** usa los tipos para autocompletado e IntelliSense
5. **Pydantic** (Clase 05) sí valida los tipos en runtime
6. Los tipos son el **contrato** entre tu API y los clientes
