---
marp: true
theme: default
paginate: true
header: 'Clase 03: POO para APIs'
footer: 'Curso APIs Python - Módulo 1'
---

# Clase 03
## Programación Orientada a Objetos para APIs

---

# ¿Por qué POO en APIs?

Las APIs REST trabajan con **recursos** (usuarios, productos, pedidos).

En Python, representamos estos recursos como **clases**.

```
Recurso API          Clase Python
───────────          ────────────
GET /usuarios/1  →   Usuario(id=1, nombre="Ana")
POST /productos  →   Producto(nombre="Laptop", precio=999)
```

---

# Anatomía de una Clase para API

```python
class Usuario:
    def __init__(self, nombre: str, email: str, id: int | None = None):
        self.id = id
        self.nombre = nombre
        self.email = email

    def to_dict(self) -> dict:
        """Serializa a diccionario (para JSON response)."""
        return {"id": self.id, "nombre": self.nombre, "email": self.email}

    @classmethod
    def from_dict(cls, data: dict) -> "Usuario":
        """Deserializa desde diccionario (desde JSON request)."""
        return cls(id=data.get("id"), nombre=data["nombre"], email=data["email"])
```

---

# @property: Getters y Setters

`@property` convierte un método en un atributo:

```python
class Producto:
    def __init__(self, precio: float):
        self._precio = precio  # Atributo "privado"

    @property
    def precio(self) -> float:
        """Getter."""
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        """Setter con validación."""
        if valor < 0:
            raise ValueError("Precio no puede ser negativo")
        self._precio = valor
```

---

# @property: Propiedades Calculadas

```python
class Producto:
    def __init__(self, precio: float, descuento: float = 0):
        self._precio = precio
        self._descuento = descuento

    @property
    def precio_final(self) -> float:
        """Propiedad calculada - sin almacenamiento."""
        return self._precio * (1 - self._descuento / 100)

# Uso:
p = Producto(precio=100, descuento=20)
print(p.precio_final)  # 80.0 (calculado automáticamente)
```

---

# @classmethod

Recibe la **clase** (`cls`) como primer argumento.
Útil para constructores alternativos:

```python
class Usuario:
    def __init__(self, nombre: str, email: str):
        self.nombre = nombre
        self.email = email

    @classmethod
    def from_dict(cls, data: dict) -> "Usuario":
        """Constructor alternativo desde diccionario."""
        return cls(nombre=data["nombre"], email=data["email"])

    @classmethod
    def crear_anonimo(cls) -> "Usuario":
        """Crea usuario anónimo."""
        return cls(nombre="Anónimo", email="anonimo@sistema.com")
```

---

# @staticmethod

No recibe `self` ni `cls`. Función normal dentro de la clase:

```python
class Validador:
    @staticmethod
    def es_email_valido(email: str) -> bool:
        """Valida formato de email."""
        return "@" in email and "." in email.split("@")[1]

    @staticmethod
    def es_precio_valido(precio: float) -> bool:
        return precio > 0

# Uso:
Validador.es_email_valido("ana@test.com")  # True
```

---

# Comparación: @classmethod vs @staticmethod

| Aspecto | @classmethod | @staticmethod |
|---------|-------------|---------------|
| Primer arg | `cls` (la clase) | Ninguno |
| Acceso a clase | Sí | No |
| Uso típico | Constructores alternativos | Utilidades |
| Herencia | Respeta subclases | No afecta |

---

# Métodos Especiales (Dunder)

```python
class Usuario:
    def __init__(self, id: int, nombre: str):
        self.id = id
        self.nombre = nombre

    def __repr__(self) -> str:
        """Para debugging."""
        return f"Usuario(id={self.id}, nombre='{self.nombre}')"

    def __eq__(self, other: object) -> bool:
        """Comparación por igualdad."""
        if not isinstance(other, Usuario):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Para usar en sets/dicts."""
        return hash(self.id)
```

---

# Herencia: Modelo Base

```python
class ModeloBase:
    def __init__(self):
        self.id: int | None = None
        self.creado_en: datetime = datetime.now()

    def to_dict(self) -> dict:
        return {"id": self.id, "creado_en": self.creado_en.isoformat()}


class Usuario(ModeloBase):
    def __init__(self, nombre: str):
        super().__init__()  # ← Importante!
        self.nombre = nombre

    def to_dict(self) -> dict:
        base = super().to_dict()
        base["nombre"] = self.nombre
        return base
```

---

# Composición sobre Herencia

Preferir **composición** cuando no hay relación "es un":

```python
# ❌ Herencia incorrecta (Pedido NO ES Usuario)
class Pedido(Usuario):
    pass

# ✅ Composición (Pedido TIENE un Usuario)
class Pedido:
    def __init__(self, usuario: Usuario, productos: list[Producto]):
        self.usuario = usuario      # Composición
        self.productos = productos  # Composición
        self.total = sum(p.precio for p in productos)
```

---

# Cuándo Herencia vs Composición

| Relación | Usar |
|----------|------|
| "Es un" (Usuario → Admin) | Herencia |
| "Tiene un" (Pedido → Usuario) | Composición |
| "Usa un" (Service → Repository) | Composición |

**Regla**: Si dudas, usa composición.

---

# Clases Abstractas (ABC)

```python
from abc import ABC, abstractmethod

class Notificador(ABC):
    """Interfaz abstracta."""

    @abstractmethod
    def enviar(self, destinatario: str, mensaje: str) -> bool:
        pass


class NotificadorEmail(Notificador):
    def enviar(self, destinatario: str, mensaje: str) -> bool:
        print(f"[EMAIL] {destinatario}: {mensaje}")
        return True

# Notificador()  # TypeError! No se puede instanciar
```

---

# Patrón Repository

Separa la lógica de negocio del acceso a datos:

```python
class UsuarioRepository(ABC):
    @abstractmethod
    def obtener(self, id: int) -> Usuario | None:
        pass

    @abstractmethod
    def guardar(self, usuario: Usuario) -> Usuario:
        pass


class UsuarioMemoryRepository(UsuarioRepository):
    def __init__(self):
        self._usuarios: dict[int, Usuario] = {}

    def obtener(self, id: int) -> Usuario | None:
        return self._usuarios.get(id)
```

---

# Beneficios del Repository

1. **Testing**: Fácil de mockear
2. **Flexibilidad**: Cambiar BD sin tocar lógica
3. **Separación**: Lógica de negocio separada de persistencia

```python
# En desarrollo/testing:
repo = UsuarioMemoryRepository()

# En producción:
repo = UsuarioPostgresRepository(db_connection)

# El servicio no cambia:
service = UsuarioService(repo)
```

---

# Patrón DTO (Data Transfer Object)

Objetos específicos para request/response:

```python
from dataclasses import dataclass

@dataclass
class UsuarioCrearDTO:
    """Para crear (sin ID)."""
    nombre: str
    email: str

@dataclass
class UsuarioResponseDTO:
    """Para respuesta (con ID y timestamps)."""
    id: int
    nombre: str
    email: str
    creado_en: str
```

---

# Conexión con Pydantic

Lo que aprendemos hoy se simplifica con Pydantic (Clase 05):

```python
# POO Manual:
class Usuario:
    def __init__(self, nombre: str, email: str):
        if not nombre:
            raise ValueError("Nombre requerido")
        self.nombre = nombre
        self.email = email

# Con Pydantic:
from pydantic import BaseModel, EmailStr

class Usuario(BaseModel):
    nombre: str
    email: EmailStr  # Validación automática
```

---

# Resumen: Conceptos Clave

| Concepto | Uso en APIs |
|----------|-------------|
| **Clase** | Representa recurso |
| **@property** | Validación, campos calculados |
| **@classmethod** | `from_dict`, constructores alternativos |
| **@staticmethod** | Utilidades sin estado |
| **Herencia** | Modelo base con campos comunes |
| **Composición** | Relaciones entre recursos |
| **Repository** | Abstrae acceso a datos |
| **DTO** | Objetos para request/response |

---

# Errores Comunes

| Error | Solución |
|-------|----------|
| Olvidar `super().__init__()` | Siempre llamar en herencia |
| Lista como default `[]` | Usar `None` y crear nueva |
| `__eq__` sin `__hash__` | Implementar ambos juntos |
| Herencia incorrecta | Usar composición |
| `type()` en vez de `isinstance()` | Usar `isinstance()` |

---

# Ejercicios

1. `ejercicio_01.py` → Clase Producto con validación
2. `ejercicio_02.py` → Herencia: Usuario → Admin, Cliente
3. `ejercicio_03.py` → Repository de Pedidos

---

# ¿Preguntas?

## Próxima clase:
**Arquitectura REST y Diseño de APIs**

---

# Tarea para Casa

1. Completar los 3 ejercicios
2. Investigar: ¿Qué es `__slots__` y cuándo usarlo?
3. (Opcional) Implementar un patrón Singleton para conexión a DB
