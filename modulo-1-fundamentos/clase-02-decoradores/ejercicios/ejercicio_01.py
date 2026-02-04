"""
Ejercicio 01: Crear Decorador de Logging
========================================
Crea un decorador que registre las llamadas a funciones.

Instrucciones:
1. Completa el decorador `log_llamada`
2. Debe mostrar: nombre de función, argumentos, resultado y tiempo
3. Usa @wraps para preservar metadatos
4. Ejecuta el archivo para verificar
"""

from functools import wraps
import time

# =============================================================================
# EJERCICIO: Completa el decorador
# =============================================================================


def log_llamada(func):
    """
    Decorador que registra cada llamada a la función.

    Debe mostrar:
    - Nombre de la función
    - Argumentos recibidos (args y kwargs)
    - Resultado retornado
    - Tiempo de ejecución en milisegundos

    Formato esperado:
    [LOG] Llamando a nombre_funcion(arg1, arg2, kwarg=valor)
    [LOG] nombre_funcion retornó: resultado (XXms)
    """
    # TODO: Agrega @wraps para preservar metadatos
    def wrapper(*args, **kwargs):
        # TODO: Captura el tiempo de inicio

        # TODO: Formatea los argumentos para mostrar
        # Hint: args_str = ", ".join(repr(a) for a in args)
        # Hint: kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())

        # TODO: Muestra el mensaje de inicio con print()
        # Formato: [LOG] Llamando a func_name(args)

        # TODO: Ejecuta la función y guarda el resultado

        # TODO: Calcula el tiempo transcurrido en milisegundos

        # TODO: Muestra el mensaje de fin con print()
        # Formato: [LOG] func_name retornó: resultado (XXms)

        # TODO: Retorna el resultado
        pass

    return wrapper


# =============================================================================
# FUNCIONES DE PRUEBA (no modificar)
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
