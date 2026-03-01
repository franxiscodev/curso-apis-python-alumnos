"""
Solución Ejercicio 01: Crear Decorador de Logging
=================================================
"""

from functools import wraps
import time


def log_llamada(func):
    """
    Decorador que registra cada llamada a la función.

    Muestra:
    - Nombre de la función
    - Argumentos recibidos (args y kwargs)
    - Resultado retornado
    - Tiempo de ejecución en milisegundos
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Capturar tiempo de inicio
        inicio = time.perf_counter()

        # Formatear argumentos para mostrar
        args_str = ", ".join(repr(a) for a in args)
        kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
        todos_args = ", ".join(filter(None, [args_str, kwargs_str]))

        # Mensaje de inicio
        print(f"[LOG] Llamando a {func.__name__}({todos_args})")

        # Ejecutar función
        resultado = func(*args, **kwargs)

        # Calcular tiempo en milisegundos
        tiempo_ms = (time.perf_counter() - inicio) * 1000

        # Mensaje de fin
        print(f"[LOG] {func.__name__} retornó: {resultado!r} ({tiempo_ms:.2f}ms)")

        return resultado

    return wrapper


# =============================================================================
# FUNCIONES DE PRUEBA
# =============================================================================


@log_llamada
def sumar(a: int, b: int) -> int:
    """Suma dos números."""
    return a + b


@log_llamada
def crear_usuario(nombre: str, email: str, activo: bool = True) -> dict:
    """Crea un diccionario de usuario."""
    time.sleep(0.1)  # Simular latencia
    return {"nombre": nombre, "email": email, "activo": activo}


@log_llamada
def operacion_lenta(segundos: float) -> str:
    """Simula una operación lenta."""
    time.sleep(segundos)
    return f"Esperé {segundos} segundos"


# =============================================================================
# VERIFICACIÓN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Verificando decorador log_llamada")
    print("=" * 60)

    print("\n--- Test 1: Función simple ---")
    resultado = sumar(5, 3)
    print(f"Resultado capturado: {resultado}")
    assert resultado == 8, "sumar(5, 3) debería retornar 8"

    print("\n--- Test 2: Con kwargs ---")
    usuario = crear_usuario("Ana", "ana@ejemplo.com", activo=False)
    print(f"Usuario capturado: {usuario}")
    assert usuario["nombre"] == "Ana", "El nombre debería ser Ana"

    print("\n--- Test 3: Operación lenta ---")
    mensaje = operacion_lenta(0.2)
    print(f"Mensaje capturado: {mensaje}")

    print("\n--- Test 4: Verificar metadatos preservados ---")
    print(f"Nombre de sumar: {sumar.__name__}")
    print(f"Docstring de sumar: {sumar.__doc__}")
    assert sumar.__name__ == "sumar", "Falta @wraps - el nombre debería ser 'sumar'"

    print("\n✓ Todos los tests pasaron")
