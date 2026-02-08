# *args y **kwargs - Cheatsheet

Guia rapida de argumentos variables en Python.

---

## *args: Argumentos Posicionales Variables

```python
def funcion(*args):
    # args es una TUPLA
    for arg in args:
        print(arg)

funcion(1, 2, 3)      # args = (1, 2, 3)
funcion("a", "b")     # args = ("a", "b")
funcion()              # args = ()
```

---

## **kwargs: Argumentos de Palabra Clave Variables

```python
def funcion(**kwargs):
    # kwargs es un DICCIONARIO
    for clave, valor in kwargs.items():
        print(f"{clave} = {valor}")

funcion(nombre="Ana", edad=30)  # kwargs = {"nombre": "Ana", "edad": 30}
funcion()                        # kwargs = {}
```

---

## Orden de Parametros (obligatorio)

```python
def funcion(normales, *args, keyword_only, **kwargs):
    pass
```

| Posicion | Tipo | Ejemplo |
|----------|------|---------|
| 1° | Parametros normales | `a, b, c=10` |
| 2° | `*args` | `*args` |
| 3° | Keyword-only | `obligatorio, opcional=True` |
| 4° | `**kwargs` | `**kwargs` |

```python
# Ejemplo completo
def ejemplo(a, b, *args, obligatorio, opcional=True, **kwargs):
    pass

ejemplo(1, 2, 3, 4, obligatorio="si", extra="dato")
# a=1, b=2, args=(3,4), obligatorio="si", opcional=True, kwargs={"extra": "dato"}
```

---

## Unpacking con * (listas/tuplas → argumentos)

```python
def sumar(a, b, c):
    return a + b + c

numeros = [1, 2, 3]
sumar(*numeros)        # → sumar(1, 2, 3) → 6

# Funciona con cualquier iterable
sumar(*range(1, 4))    # → sumar(1, 2, 3)
sumar(*(10, 20, 30))   # → sumar(10, 20, 30)
```

---

## Unpacking con ** (diccionarios → keyword arguments)

```python
def crear(nombre, email, activo=True):
    return {"nombre": nombre, "email": email, "activo": activo}

datos = {"nombre": "Ana", "email": "ana@test.com"}
crear(**datos)         # → crear(nombre="Ana", email="ana@test.com")

# Combinar con argumentos explicitos
crear(**datos, activo=False)
```

---

## Merge de Diccionarios

```python
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}

merged = {**d1, **d2}  # {"a": 1, "b": 3, "c": 4}
# El ultimo gana en duplicados
```

---

## Forwarding (pasar argumentos a otra funcion)

```python
def wrapper(*args, **kwargs):
    # Recibe cualquier cosa
    resultado = otra_funcion(*args, **kwargs)
    # Pasa todo intacto
    return resultado
```

---

## Keyword-Only Arguments con *

```python
# * solo (sin nombre) fuerza keyword-only
def funcion(a, b, *, timeout=30, ssl=True):
    pass

funcion(1, 2, timeout=60)   # OK
funcion(1, 2, 60)           # TypeError!

# Con *args, lo que sigue es automaticamente keyword-only
def funcion(*args, sep=" "):
    pass
```

---

## En Decoradores (clase-02)

```python
from functools import wraps

def mi_decorador(func):
    @wraps(func)
    def wrapper(*args, **kwargs):       # Acepta cualquier firma
        print(f"Llamando {func.__name__}")
        resultado = func(*args, **kwargs)  # Forwarding
        return resultado
    return wrapper

@mi_decorador
def cualquier_funcion(a, b, c=10):
    return a + b + c
```

---

## En Herencia (clase-03)

```python
class Padre:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

class Hijo(Padre):
    def __init__(self, escuela, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Forwarding al padre
        self.escuela = escuela

Hijo("MIT", "Ana", 20)  # escuela="MIT", nombre="Ana", edad=20
```

---

## Tips

1. `args` y `kwargs` son **nombres por convencion**. Lo importante es `*` y `**`
2. `*args` es una **tupla** (inmutable), `**kwargs` es un **diccionario**
3. El orden es **estricto**: normales → *args → keyword-only → **kwargs
4. En **definicion**: `*` empaqueta. En **llamada**: `*` desempaqueta
5. Forwarding (`*args, **kwargs` → `func(*args, **kwargs)`) es la base de decoradores
6. Keyword-only con `*` solo: `def f(a, *, b)` → `b` solo por nombre
7. `{**d1, **d2}` es la forma mas limpia de mergear diccionarios
