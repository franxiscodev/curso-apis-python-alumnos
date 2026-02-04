# POO para APIs - Cheatsheet

Guía rápida de programación orientada a objetos aplicada a APIs.

---

## Clase Básica

```python
class Usuario:
    def __init__(self, nombre: str, email: str):
        self.nombre = nombre
        self.email = email

    def __repr__(self) -> str:
        return f"Usuario({self.nombre!r})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Usuario):
            return NotImplemented
        return self.email == other.email
```

---

## @property

```python
class Producto:
    def __init__(self, nombre: str, precio: float):
        self.nombre = nombre
        self._precio = precio

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float):
        if valor < 0:
            raise ValueError("Precio no puede ser negativo")
        self._precio = valor

p = Producto("Widget", 9.99)
p.precio = 15.0   # Usa el setter (valida)
print(p.precio)   # Usa el getter
```

---

## @classmethod y @staticmethod

```python
class Pedido:
    def __init__(self, items: list[str], total: float):
        self.items = items
        self.total = total

    @classmethod
    def desde_dict(cls, datos: dict) -> "Pedido":
        """Constructor alternativo."""
        return cls(items=datos["items"], total=datos["total"])

    @staticmethod
    def calcular_impuesto(monto: float, tasa: float = 0.21) -> float:
        """No necesita self ni cls."""
        return round(monto * tasa, 2)
```

---

## Herencia

```python
class UsuarioBase:
    def __init__(self, nombre: str, email: str):
        self.nombre = nombre
        self.email = email

class Admin(UsuarioBase):
    def __init__(self, nombre: str, email: str, permisos: list[str]):
        super().__init__(nombre, email)
        self.permisos = permisos

class Cliente(UsuarioBase):
    def __init__(self, nombre: str, email: str, direccion: str):
        super().__init__(nombre, email)
        self.direccion = direccion
```

---

## Clase Abstracta (ABC)

```python
from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def obtener(self, id: int) -> dict | None:
        ...

    @abstractmethod
    def listar(self) -> list[dict]:
        ...

    @abstractmethod
    def crear(self, datos: dict) -> dict:
        ...

class MemoryRepository(Repository):
    def __init__(self):
        self.datos: dict[int, dict] = {}

    def obtener(self, id: int) -> dict | None:
        return self.datos.get(id)

    def listar(self) -> list[dict]:
        return list(self.datos.values())

    def crear(self, datos: dict) -> dict:
        ...
```

---

## Patrón Repository

```python
class ProductoRepository:
    def __init__(self):
        self._productos: dict[int, dict] = {}
        self._next_id = 1

    def listar(self) -> list[dict]:
        return list(self._productos.values())

    def obtener(self, id: int) -> dict | None:
        return self._productos.get(id)

    def crear(self, datos: dict) -> dict:
        producto = {"id": self._next_id, **datos}
        self._productos[self._next_id] = producto
        self._next_id += 1
        return producto

    def eliminar(self, id: int) -> bool:
        return self._productos.pop(id, None) is not None
```

---

## Dataclass vs Clase Manual

```python
from dataclasses import dataclass

# Clase manual (más control)
class Producto:
    def __init__(self, nombre: str, precio: float):
        self.nombre = nombre
        self.precio = precio

# Dataclass (genera __init__, __repr__, __eq__)
@dataclass
class Producto:
    nombre: str
    precio: float
    stock: int = 0
```

---

## Progresión en el Curso

| Clase | Estructura | Validación |
|-------|-----------|------------|
| 01 | `dict`, `TypedDict` | No |
| 03 | Clases, `dataclass` | Manual (`@property`) |
| 05 | Pydantic `BaseModel` | Automática |
| 08 | SQLAlchemy `Model` | BD + Pydantic |

---

## Patrones para APIs

| Patrón | Qué hace | Ejemplo |
|--------|----------|---------|
| Entity | Representa recurso | `Usuario`, `Producto` |
| DTO | Datos de transferencia | `UsuarioCrear`, `UsuarioResponse` |
| Repository | Abstrae acceso a datos | `ProductoRepository` |
| Factory | Crea objetos complejos | `Pedido.desde_dict()` |

---

## Tips

1. **Preferir composición** sobre herencia profunda
2. **`@property`** para validación en getters/setters
3. **Repository** separa lógica de negocio de acceso a datos
4. **`__repr__`** siempre implementar para debugging
5. **ABC** para definir interfaces (contratos)
6. **dataclass** cuando solo necesitas almacenar datos
