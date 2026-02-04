"""
Ejemplo 01: Decoradores Básicos
===============================
Introducción a decoradores simples y uso de functools.wraps.

Objetivo: Entender cómo funcionan los decoradores internamente.
"""

from functools import wraps

# =============================================================================
# PREREQUISITO: Funciones son objetos
# =============================================================================


def saludar(nombre: str) -> str:
    """Retorna un saludo."""
    return f"Hola, {nombre}"


# Las funciones se pueden asignar a variables
mi_funcion = saludar
print(mi_funcion("Ana"))  # Hola, Ana

# Las funciones se pueden pasar como argumentos
def ejecutar_funcion(func, argumento):
    """Ejecuta una función con un argumento."""
    return func(argumento)


resultado = ejecutar_funcion(saludar, "Carlos")
print(resultado)  # Hola, Carlos


# =============================================================================
# DECORADOR SIMPLE: Sin @wraps (problema)
# =============================================================================


def decorador_sin_wraps(func):
    """Decorador que NO preserva metadatos - ¡NO HACER ESTO!"""
    def wrapper(*args, **kwargs):
        print(f"[LOG] Llamando función...")
        return func(*args, **kwargs)
    return wrapper


@decorador_sin_wraps
def funcion_mal_decorada():
    """Esta documentación se perderá."""
    return "resultado"


print(f"\nSin @wraps:")
print(f"  Nombre: {funcion_mal_decorada.__name__}")  # wrapper ❌
print(f"  Doc: {funcion_mal_decorada.__doc__}")      # None ❌


# =============================================================================
# DECORADOR CORRECTO: Con @wraps
# =============================================================================


def decorador_con_wraps(func):
    """Decorador que SÍ preserva metadatos - ¡SIEMPRE USAR @wraps!"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Llamando a {func.__name__}...")
        resultado = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} terminó")
        return resultado
    return wrapper


@decorador_con_wraps
def funcion_bien_decorada():
    """Esta documentación se preserva."""
    return "resultado"


print(f"\nCon @wraps:")
print(f"  Nombre: {funcion_bien_decorada.__name__}")  # funcion_bien_decorada ✅
print(f"  Doc: {funcion_bien_decorada.__doc__}")      # Esta documentación... ✅


# =============================================================================
# EJEMPLO PRÁCTICO: Decorador de logging
# =============================================================================


def log_llamadas(func):
    """
    Decorador que registra cada llamada a la función.

    Muestra los argumentos de entrada y el valor de retorno.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Formatear argumentos para mostrar
        args_str = ", ".join(repr(a) for a in args)
        kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
        todos_args = ", ".join(filter(None, [args_str, kwargs_str]))

        print(f"→ {func.__name__}({todos_args})")

        resultado = func(*args, **kwargs)

        print(f"← {func.__name__} retornó: {resultado!r}")

        return resultado

    return wrapper


@log_llamadas
def sumar(a: int, b: int) -> int:
    """Suma dos números."""
    return a + b


@log_llamadas
def crear_usuario(nombre: str, email: str, activo: bool = True) -> dict:
    """Crea un diccionario de usuario."""
    return {"nombre": nombre, "email": email, "activo": activo}


# =============================================================================
# EJECUCIÓN DE EJEMPLOS
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("DECORADOR DE LOGGING EN ACCIÓN")
    print("=" * 60)

    print("\n--- Llamada a sumar ---")
    resultado = sumar(5, 3)
    print(f"Resultado final: {resultado}")

    print("\n--- Llamada a crear_usuario ---")
    usuario = crear_usuario("Ana", "ana@ejemplo.com")
    print(f"Usuario creado: {usuario}")

    print("\n--- Llamada con kwargs ---")
    usuario2 = crear_usuario(nombre="Carlos", email="carlos@ejemplo.com", activo=False)
    print(f"Usuario creado: {usuario2}")
