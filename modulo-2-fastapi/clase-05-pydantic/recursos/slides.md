---
marp: true
theme: default
paginate: true
header: 'Clase 05: Pydantic'
footer: 'Curso APIs Python - Módulo 1'
---

# Clase 05
## Pydantic y Validación de Datos

---

# ¿Qué es Pydantic?

- Librería de **validación de datos** usando type hints
- Motor de validación de **FastAPI**
- Versión actual: **Pydantic v2** (más rápido)

```python
from pydantic import BaseModel

class Usuario(BaseModel):
    nombre: str
    edad: int
    email: str
```

---

# ¿Por qué Pydantic?

| Sin Pydantic | Con Pydantic |
|--------------|--------------|
| `if not isinstance(...)` | Type hints |
| Validación manual | Validación automática |
| Errores genéricos | Errores descriptivos |
| `to_dict()` manual | `model_dump()` |

---

# BaseModel Básico

```python
from pydantic import BaseModel

class Producto(BaseModel):
    id: int
    nombre: str
    precio: float
    activo: bool = True  # Default

# Creación
p = Producto(id=1, nombre="Laptop", precio=999.99)
print(p.nombre)   # "Laptop"
print(p.activo)   # True
```

---

# Tipos de Datos

```python
from pydantic import BaseModel, EmailStr
from datetime import datetime

class Usuario(BaseModel):
    nombre: str
    email: EmailStr           # Valida formato
    edad: int | None = None   # Opcional
    activo: bool = True
    creado_en: datetime
```

---

# Field: Configuración de Campos

```python
from pydantic import BaseModel, Field

class Producto(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    precio: float = Field(gt=0, description="Mayor a 0")
    stock: int = Field(default=0, ge=0)
```

| Opción | Descripción |
|--------|-------------|
| `gt`, `ge` | Mayor que, mayor o igual |
| `lt`, `le` | Menor que, menor o igual |
| `min_length` | Longitud mínima string |

---

# @field_validator

Valida un campo específico:

```python
from pydantic import BaseModel, field_validator

class Usuario(BaseModel):
    nombre: str

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Nombre vacío")
        return v.strip().title()
```

---

# @field_validator mode="before"

Se ejecuta **antes** de la conversión de tipo:

```python
class Producto(BaseModel):
    precio: float

    @field_validator("precio", mode="before")
    @classmethod
    def limpiar_precio(cls, v):
        if isinstance(v, str):
            v = v.replace("$", "").replace(",", "")
        return v

# Acepta: "$1,299.99" → 1299.99
```

---

# @model_validator

Valida el modelo completo (múltiples campos):

```python
from pydantic import BaseModel, model_validator

class Rango(BaseModel):
    minimo: int
    maximo: int

    @model_validator(mode="after")
    def validar_rango(self) -> "Rango":
        if self.minimo > self.maximo:
            raise ValueError("min > max")
        return self
```

---

# Serialización: model_dump()

```python
usuario = Usuario(nombre="Ana", email="ana@test.com", edad=30)

# A diccionario
data = usuario.model_dump()

# Opciones
usuario.model_dump(exclude={"email"})
usuario.model_dump(include={"nombre"})
usuario.model_dump(exclude_none=True)
usuario.model_dump(by_alias=True)

# A JSON
json_str = usuario.model_dump_json(indent=2)
```

---

# Deserialización: model_validate()

```python
# Desde diccionario
data = {"nombre": "Ana", "email": "ana@test.com"}
usuario = Usuario.model_validate(data)

# Desde JSON string
json_str = '{"nombre": "Ana", "email": "ana@test.com"}'
usuario = Usuario.model_validate_json(json_str)
```

---

# Modelos Anidados

```python
class Direccion(BaseModel):
    calle: str
    ciudad: str

class Usuario(BaseModel):
    nombre: str
    direccion: Direccion  # Anidado

# Pydantic convierte dicts automáticamente
usuario = Usuario(
    nombre="Ana",
    direccion={"calle": "Gran Vía", "ciudad": "Madrid"}
)
print(usuario.direccion.ciudad)  # "Madrid"
```

---

# Listas de Modelos

```python
class Producto(BaseModel):
    nombre: str
    precio: float

class Pedido(BaseModel):
    productos: list[Producto]

pedido = Pedido(productos=[
    {"nombre": "Laptop", "precio": 999},
    {"nombre": "Mouse", "precio": 29}
])
```

---

# Herencia de Modelos

```python
class UsuarioBase(BaseModel):
    nombre: str
    email: str

class UsuarioCrear(BaseModel):
    nombre: str
    email: str 
    password: str

class UsuarioCrear(UsuarioBase):
    password: str

class UsuarioResponse(UsuarioBase):
    id: int
    # Sin password!
```

---

# model_config

```python
from pydantic import BaseModel, ConfigDict

class Usuario(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,   # Strip strings
        extra="forbid",               # Rechazar campos extra
        validate_assignment=True,     # Validar en asignación
    )

    nombre: str
    email: str
```

---

# Alias

```python
class UsuarioAPI(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    nombre_completo: str = Field(alias="fullName")
    correo: str = Field(alias="email")

# Entrada con alias
data = {"fullName": "Ana", "email": "ana@test.com"}
usuario = UsuarioAPI.model_validate(data)

# Salida con alias
usuario.model_dump(by_alias=True)
```

---

# Manejo de Errores

```python
from pydantic import ValidationError

try:
    Usuario(nombre="", edad="no es numero")
except ValidationError as e:
    print(e.errors())
    # [
    #   {'loc': ('edad',), 'msg': '...', 'type': '...'}
    # ]
```

---

# Pydantic + FastAPI (Preview)

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UsuarioCrear(BaseModel):
    nombre: str
    email: str

@app.post("/usuarios")
async def crear(usuario: UsuarioCrear):
    # FastAPI valida automáticamente
    return {"id": 1, **usuario.model_dump()}
```

---

# Pydantic v1 vs v2

| v1 | v2 |
|----|----|
| `@validator` | `@field_validator` |
| `.dict()` | `.model_dump()` |
| `.parse_obj()` | `.model_validate()` |
| `class Config` | `model_config` |

---

# Resumen

| Concepto | Uso |
|----------|-----|
| `BaseModel` | Clase base |
| `Field()` | Configurar campos |
| `@field_validator` | Validar un campo |
| `@model_validator` | Validar modelo |
| `model_dump()` | Modelo → dict |
| `model_validate()` | dict → Modelo |

---

# Ejercicios

1. Modelo Usuario con validación
2. Producto con validadores custom
3. Sistema de pedidos con modelos anidados

---

# ¿Preguntas?

## Próxima clase:
**FastAPI Básico**

---

# Tarea para Casa

1. Completar los 3 ejercicios
2. Crear un modelo para tu proyecto personal
3. (Opcional) Explorar `pydantic-settings`
