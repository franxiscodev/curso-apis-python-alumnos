# Decoradores en Python - Cheatsheet

Guía rápida de decoradores y su relación con FastAPI.

---

## Decorador Simple

```python
import functools

def mi_decorador(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("Antes")
        resultado = func(*args, **kwargs)
        print("Después")
        return resultado
    return wrapper

@mi_decorador
def saludar(nombre: str) -> str:
    return f"Hola {nombre}"
```

---

## Decorador con Parámetros

```python
import functools

def repetir(veces: int):
    def decorador(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(veces):
                resultado = func(*args, **kwargs)
            return resultado
        return wrapper
    return decorador

@repetir(veces=3)
def saludar(nombre: str):
    print(f"Hola {nombre}")
```

---

## functools.wraps (SIEMPRE usarlo)

```python
# SIN wraps
def decorador(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorador
def mi_funcion():
    """Mi docstring."""
    pass

mi_funcion.__name__  # → "wrapper" ❌

# CON wraps
def decorador(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorador
def mi_funcion():
    """Mi docstring."""
    pass

mi_funcion.__name__  # → "mi_funcion" ✅
```

---

## Decorador de Timing

```python
import functools
import time

def medir_tiempo(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        total = time.perf_counter() - inicio
        print(f"{func.__name__}: {total:.4f}s")
        return resultado
    return wrapper
```

---

## Decorador de Logging

```python
import functools

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Llamando {func.__name__}({args}, {kwargs})")
        resultado = func(*args, **kwargs)
        print(f"{func.__name__} → {resultado}")
        return resultado
    return wrapper
```

---

## Stacking (Apilar Decoradores)

```python
@log
@medir_tiempo
def procesar(datos):
    ...

# Equivale a:
procesar = log(medir_tiempo(procesar))
# Se ejecutan de abajo hacia arriba
```

---

## Decoradores Built-in

| Decorador | Uso |
|-----------|-----|
| `@property` | Getter como atributo |
| `@staticmethod` | Método sin self |
| `@classmethod` | Método con cls |
| `@functools.wraps` | Preservar metadatos |
| `@functools.lru_cache` | Caché de resultados |
| `@dataclass` | Generar __init__, __repr__, etc. |

---

## Conexión con FastAPI

```python
from fastapi import FastAPI
app = FastAPI()

# @app.get() es un decorador con parámetros
@app.get("/usuarios")
def listar_usuarios():
    return [{"id": 1, "nombre": "Ana"}]

# Equivale a:
def listar_usuarios():
    return [{"id": 1, "nombre": "Ana"}]
listar_usuarios = app.get("/usuarios")(listar_usuarios)
```

---

## Tips

1. **Siempre** usar `@functools.wraps(func)` en el wrapper
2. **`*args, **kwargs`** para aceptar cualquier firma
3. Decorador con parámetros = **3 niveles de funciones**
4. El stacking se ejecuta de **abajo hacia arriba**
5. FastAPI `@app.get()`, `@app.post()` son decoradores con parámetros
6. Los decoradores son funciones que reciben y retornan funciones
