# Pydantic v2 Cheatsheet

## Modelo Básico

```python
from pydantic import BaseModel, Field, EmailStr

class Usuario(BaseModel):
    id: int | None = None
    nombre: str = Field(min_length=1, max_length=100)
    email: EmailStr
    activo: bool = True
```

## Field - Opciones Comunes

| Opción | Descripción | Ejemplo |
|--------|-------------|---------|
| `default` | Valor por defecto | `Field(default=0)` |
| `default_factory` | Factory para mutables | `Field(default_factory=list)` |
| `alias` | Nombre alternativo | `Field(alias="userName")` |
| `gt`, `ge` | Mayor que, mayor/igual | `Field(gt=0)` |
| `lt`, `le` | Menor que, menor/igual | `Field(lt=100)` |
| `min_length` | Longitud mínima | `Field(min_length=1)` |
| `max_length` | Longitud máxima | `Field(max_length=100)` |
| `pattern` | Regex | `Field(pattern=r"^\d{5}$")` |

## Validadores

### @field_validator
```python
from pydantic import field_validator

@field_validator("nombre")
@classmethod
def validar_nombre(cls, v: str) -> str:
    if not v.strip():
        raise ValueError("Vacío")
    return v.title()
```

### @field_validator mode="before"
```python
@field_validator("precio", mode="before")
@classmethod
def limpiar_precio(cls, v):
    if isinstance(v, str):
        v = v.replace("$", "")
    return v
```

### @model_validator
```python
from pydantic import model_validator

@model_validator(mode="after")
def validar_modelo(self) -> "MiModelo":
    if self.min > self.max:
        raise ValueError("min > max")
    return self
```

## Serialización

```python
# Modelo → dict
data = modelo.model_dump()
data = modelo.model_dump(exclude={"password"})
data = modelo.model_dump(include={"nombre", "email"})
data = modelo.model_dump(exclude_none=True)
data = modelo.model_dump(by_alias=True)

# Modelo → JSON string
json_str = modelo.model_dump_json(indent=2)
```

## Deserialización

```python
# dict → Modelo
modelo = MiModelo.model_validate(data)

# JSON string → Modelo
modelo = MiModelo.model_validate_json(json_str)
```

## Configuración (model_config)

```python
from pydantic import ConfigDict

class MiModelo(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,    # Strip strings
        extra="forbid",                # Rechazar campos extra
        # extra="ignore",              # Ignorar campos extra
        validate_assignment=True,      # Validar en asignación
        frozen=True,                   # Inmutable
        populate_by_name=True,         # Acepta alias o nombre
    )
```

## Alias

```python
class Usuario(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    # validation_alias: para INPUT (deserialización)
    # serialization_alias: para OUTPUT (serialización)
    nombre: str = Field(
        validation_alias="fullName",
        serialization_alias="name"
    )
```

## Tipos Especiales

| Tipo | Uso |
|------|-----|
| `EmailStr` | Valida formato email |
| `HttpUrl` | Valida URL |
| `SecretStr` | Oculta en logs/repr |
| `constr(...)` | String con restricciones |
| `conint(...)` | Int con restricciones |
| `confloat(...)` | Float con restricciones |

## Modelos Anidados

```python
class Direccion(BaseModel):
    ciudad: str

class Usuario(BaseModel):
    direccion: Direccion  # Anidado
    # Pydantic convierte dicts automáticamente

class Pedido(BaseModel):
    productos: list[Producto]  # Lista de modelos
```

## Herencia (Patrón DTO)

```python
class UsuarioBase(BaseModel):
    nombre: str
    email: str

class UsuarioCrear(UsuarioBase):
    password: str

class UsuarioResponse(UsuarioBase):
    id: int
    # Sin password
```

## Manejo de Errores

```python
from pydantic import ValidationError

try:
    usuario = Usuario(...)
except ValidationError as e:
    print(e.errors())       # Lista de errores
    print(e.json())         # JSON de errores

    for error in e.errors():
        print(error['loc'])  # Ubicación
        print(error['msg'])  # Mensaje
        print(error['type']) # Tipo de error
```

## Pydantic v1 → v2 Migración

| v1 | v2 |
|----|----|
| `@validator` | `@field_validator` |
| `.dict()` | `.model_dump()` |
| `.json()` | `.model_dump_json()` |
| `.parse_obj()` | `.model_validate()` |
| `.parse_raw()` | `.model_validate_json()` |
| `class Config` | `model_config = ConfigDict(...)` |
| `schema()` | `model_json_schema()` |
| `__fields__` | `model_fields` |
