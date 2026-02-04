---
marp: true
theme: default
paginate: true
header: 'Clase 02: Decoradores en Python'
footer: 'Curso APIs Python - Módulo 1'
---

# Clase 02
## Decoradores en Python

---

# ¿Qué es un Decorador?

Una función que **recibe otra función**, le añade funcionalidad y la **retorna modificada**.

```python
@mi_decorador
def mi_funcion():
    pass

# Equivale a:
mi_funcion = mi_decorador(mi_funcion)
```

---

# ¿Por qué importan para APIs?

FastAPI usa decoradores para definir rutas:

```python
@app.get("/usuarios")      # ← Decorador
async def listar_usuarios():
    return [{"id": 1}]

@app.post("/usuarios")     # ← Decorador
async def crear_usuario(data: dict):
    return {"id": 2}
```

---

# Prerequisito: Funciones son Objetos

```python
def saludar(nombre):
    return f"Hola, {nombre}"

# Asignar a variable
mi_func = saludar
mi_func("Ana")  # "Hola, Ana"

# Pasar como argumento
def ejecutar(func, valor):
    return func(valor)

ejecutar(saludar, "Carlos")  # "Hola, Carlos"
```

---

# Anatomía de un Decorador

```python
from functools import wraps

def mi_decorador(func):
    @wraps(func)  # ← Preserva metadatos
    def wrapper(*args, **kwargs):
        print("Antes")           # Código antes
        resultado = func(*args, **kwargs)
        print("Después")         # Código después
        return resultado
    return wrapper
```

---

# Flujo de Ejecución

```
1. @mi_decorador se aplica
2. Python ejecuta: funcion = mi_decorador(funcion)
3. mi_decorador retorna wrapper
4. Ahora funcion → wrapper
5. Al llamar funcion(), se ejecuta wrapper()
```

---

# ¡Siempre usa @wraps!

### Sin @wraps ❌
```python
print(funcion.__name__)  # "wrapper"
print(funcion.__doc__)   # None
```

### Con @wraps ✅
```python
print(funcion.__name__)  # "funcion"
print(funcion.__doc__)   # "Documentación..."
```

---

# Ejemplo: Decorador de Logging

```python
from functools import wraps

def log_llamada(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"→ Llamando {func.__name__}")
        resultado = func(*args, **kwargs)
        print(f"← Retornó: {resultado}")
        return resultado
    return wrapper

@log_llamada
def sumar(a, b):
    return a + b
```

---

# Decoradores con Parámetros

Necesitas **3 niveles de anidación**:

```python
def repetir(veces):           # Nivel 1: parámetros
    def decorador(func):      # Nivel 2: recibe función
        @wraps(func)
        def wrapper(*args):   # Nivel 3: ejecuta
            for _ in range(veces):
                func(*args)
        return wrapper
    return decorador

@repetir(veces=3)
def saludar():
    print("Hola")
```

---

# Stacking (Apilar Decoradores)

```python
@decorador_a    # 2° aplicarse, 1° ejecutarse
@decorador_b    # 1° aplicarse, 2° ejecutarse
def funcion():
    pass

# Equivale a:
funcion = decorador_a(decorador_b(funcion))
```

**Aplican**: abajo → arriba
**Ejecutan**: arriba → abajo

---

# Decoradores Built-in

| Decorador | Uso |
|-----------|-----|
| `@property` | Método como atributo |
| `@staticmethod` | Sin acceso a self |
| `@classmethod` | Recibe cls |
| `@functools.wraps` | Preserva metadatos |
| `@functools.lru_cache` | Caché automático |

---

# Casos de Uso en APIs

```python
@log_request          # Logging
@medir_tiempo         # Performance
@requiere_auth        # Autenticación
@validar_entrada      # Validación
@cache_resultado      # Caché
@reintentar(veces=3)  # Retry
```

---

# Conexión con FastAPI

```python
# En FastAPI, @app.get() es un decorador con parámetros:
@app.get("/usuarios/{id}")
async def obtener_usuario(id: int):
    return {"id": id}

# Internamente hace algo como:
# 1. app.get("/usuarios/{id}") retorna un decorador
# 2. El decorador registra la función en el router
# 3. Asocia ruta + método HTTP + función
```

---

# Ejemplo: Decorador de Auth (Preview)

```python
def requiere_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = kwargs.get("token")
        if not token or token not in TOKENS_VALIDOS:
            return {"error": "No autorizado", "status": 401}
        return func(*args, **kwargs)
    return wrapper

@requiere_auth
def endpoint_protegido(token: str):
    return {"data": "secreto"}
```

---

# Errores Comunes

| Error | Solución |
|-------|----------|
| Perder metadatos | Usar `@wraps(func)` |
| Olvidar `return` | `return func(*args)` |
| Parámetros: 2 niveles | Necesitas 3 niveles |
| Mutar argumentos | Trabajar con copias |
| Orden stacking | Recordar: abajo→arriba |

---

# Ejercicios

1. `ejercicio_01.py` → Decorador de logging
2. `ejercicio_02.py` → Decorador con parámetros (limitar llamadas)
3. `ejercicio_03.py` → Decorador de caché

---

# Resumen

✅ Decorador = función que modifica otra función
✅ Siempre usar `@functools.wraps`
✅ Con parámetros = 3 niveles de anidación
✅ Stacking: aplican abajo→arriba, ejecutan arriba→abajo
✅ FastAPI usa decoradores para rutas

---

# ¿Preguntas?

## Próxima clase:
**Programación Orientada a Objetos para APIs**

---

# Tarea para casa

1. Completar los 3 ejercicios
2. Investigar: ¿Qué hace `@lru_cache`?
3. (Opcional) Crear decorador que cuente llamadas
