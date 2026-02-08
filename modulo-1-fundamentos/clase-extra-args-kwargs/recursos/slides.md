---
marp: true
theme: default
paginate: true
header: 'Clase Extra: *args y **kwargs en Python'
footer: 'Curso APIs Python - Modulo 1'
---

# Clase Extra
## *args y **kwargs en Python

---

# El Problema

Como hace `print()` para aceptar cualquier cantidad de argumentos?

```python
print("hola")                     # 1 argumento
print("hola", "mundo", "!")       # 3 argumentos
print(1, 2, 3, 4, 5, 6, 7, 8)   # 8 argumentos
```

Y `max()`, `min()`, `dict()`...?

**Respuesta**: `*args` y `**kwargs`

---

# *args: Argumentos Posicionales Variables

El `*` captura argumentos posicionales en una **tupla**:

```python
def sumar(*numeros):
    print(type(numeros))  # <class 'tuple'>
    return sum(numeros)

sumar(1, 2, 3)    # numeros = (1, 2, 3) → 6
sumar(10, 20)      # numeros = (10, 20) → 30
sumar()            # numeros = () → 0
```

---

# **kwargs: Argumentos de Palabra Clave Variables

El `**` captura keyword arguments en un **diccionario**:

```python
def crear_perfil(**datos):
    print(type(datos))  # <class 'dict'>
    return datos

crear_perfil(nombre="Ana", edad=30)
# datos = {"nombre": "Ana", "edad": 30}
```

---

# Orden Obligatorio de Parametros

```python
def funcion(normales, *args, keyword_only, **kwargs):
```

| Posicion | Tipo | Ejemplo |
|----------|------|---------|
| 1° | Parametros normales | `a, b` |
| 2° | `*args` | `*args` |
| 3° | Keyword-only | `obligatorio` |
| 4° | `**kwargs` | `**kwargs` |

**Este orden es estricto.** Alterarlo da SyntaxError.

---

# Unpacking con *

Desempaquetar una lista/tupla en argumentos:

```python
def sumar(a, b, c):
    return a + b + c

numeros = [1, 2, 3]
sumar(*numeros)     # → sumar(1, 2, 3) → 6
```

El `*` en la **llamada** hace lo opuesto al `*` en la **definicion**.

---

# Unpacking con **

Desempaquetar un diccionario en keyword arguments:

```python
def crear_usuario(nombre, email, activo=True):
    return {"nombre": nombre, "email": email, "activo": activo}

datos = {"nombre": "Ana", "email": "ana@test.com"}
crear_usuario(**datos)
# → crear_usuario(nombre="Ana", email="ana@test.com")
```

---

# Merge de Diccionarios

```python
defaults = {"color": "azul", "tamaño": "mediano"}
custom = {"color": "rojo", "fuente": "Arial"}

config = {**defaults, **custom}
# {"color": "rojo", "tamaño": "mediano", "fuente": "Arial"}
```

El ultimo diccionario gana en claves duplicadas.

---

# Forwarding de Argumentos

El patron **mas importante** de esta clase:

```python
def wrapper(*args, **kwargs):
    # Recibe CUALQUIER argumento
    resultado = funcion_original(*args, **kwargs)
    # Los pasa INTACTOS
    return resultado
```

La funcion original recibe exactamente lo mismo.

---

# Keyword-Only con *

El `*` solo fuerza que lo siguiente sea por nombre:

```python
def conectar(host, puerto, *, timeout=30, ssl=True):
    ...

conectar("localhost", 8080, timeout=60)    # OK
conectar("localhost", 8080, 60)            # TypeError!
```

Asi funciona `print()`: `sep` y `end` son keyword-only.

---

# Caso: Decoradores (preview clase-02)

```python
def medir_tiempo(func):
    def wrapper(*args, **kwargs):       # ← Hoy
        inicio = time.time()
        resultado = func(*args, **kwargs)  # ← Hoy
        print(f"Tardo {time.time() - inicio:.4f}s")
        return resultado
    return wrapper
```

Sin `*args/**kwargs`, el decorador no seria generico.

---

# Caso: Herencia (preview clase-03)

```python
class Perro(Animal):
    def __init__(self, raza, *args, **kwargs):
        super().__init__(*args, **kwargs)  # ← Forwarding
        self.raza = raza
```

Pasa los argumentos al constructor padre sin conocerlos.

---

# Errores Comunes

| Error | Solucion |
|-------|----------|
| Orden incorrecto `(**kwargs, *args)` | Respetar: normales, *args, kw-only, **kwargs |
| Olvidar desempaquetar `func(args)` | Usar `func(*args, **kwargs)` |
| Confundir definicion y llamada | `*` en def = empaquetar, `*` en llamada = desempaquetar |
| `*args` no es una lista | Es una tupla (inmutable) |

---

# Ejercicios

1. `ejercicio_01.py` → Funciones con *args y **kwargs
2. `ejercicio_02.py` → Unpacking y forwarding
3. `ejercicio_03.py` → Wrapper generico (puente a decoradores)

---

# Resumen

- `*args` = tupla de argumentos posicionales variables
- `**kwargs` = diccionario de keyword arguments variables
- Orden: `(normales, *args, keyword_only, **kwargs)`
- `*lista` y `**dict` desempaquetan en llamadas
- Forwarding: `wrapper(*args, **kwargs)` → `func(*args, **kwargs)`
- Base fundamental para decoradores (clase-02)

---

# Preguntas?

## Proxima clase:
**Decoradores en Python** (clase-02)

---

# Tarea para Casa

1. Completar los 3 ejercicios
2. Investigar: como usa `print()` los parametros `sep` y `end`?
3. (Opcional) Crear una funcion `crear_tabla(**columnas)` que genere texto tabular
