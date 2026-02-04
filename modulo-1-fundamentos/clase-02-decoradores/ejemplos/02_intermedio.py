"""
Ejemplo 02: Decoradores con Parámetros y Stacking
=================================================
Decoradores que aceptan configuración y cómo combinar múltiples decoradores.

Objetivo: Crear decoradores configurables (fábricas de decoradores).
"""

from functools import wraps
import time

# =============================================================================
# DECORADOR CON PARÁMETROS: Estructura de 3 niveles
# =============================================================================


def repetir(veces: int):
    """
    Fábrica de decoradores: crea un decorador que repite la función N veces.

    Estructura:
    - repetir(veces=3)    → Retorna decorador
    - decorador(func)     → Retorna wrapper
    - wrapper(*args)      → Ejecuta la función
    """
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            resultado = None
            for i in range(veces):
                print(f"  Ejecución {i + 1}/{veces}")
                resultado = func(*args, **kwargs)
            return resultado
        return wrapper
    return decorador


@repetir(veces=3)
def saludar(nombre: str) -> str:
    """Saluda a una persona."""
    mensaje = f"¡Hola, {nombre}!"
    print(f"    {mensaje}")
    return mensaje


# =============================================================================
# DECORADOR CON VALOR POR DEFECTO OPCIONAL
# =============================================================================


def reintentar(max_intentos: int = 3, espera: float = 1.0):
    """
    Decorador que reintenta una función si falla.

    Args:
        max_intentos: Número máximo de intentos
        espera: Segundos entre intentos
    """
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ultimo_error = None
            for intento in range(1, max_intentos + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    ultimo_error = e
                    print(f"  Intento {intento}/{max_intentos} falló: {e}")
                    if intento < max_intentos:
                        print(f"  Esperando {espera}s antes de reintentar...")
                        time.sleep(espera)
            raise ultimo_error
        return wrapper
    return decorador


# Simulamos una función que falla aleatoriamente
import random

@reintentar(max_intentos=3, espera=0.5)
def operacion_inestable() -> str:
    """Simula una operación que puede fallar."""
    if random.random() < 0.7:  # 70% de probabilidad de fallo
        raise ConnectionError("Error de conexión simulado")
    return "¡Éxito!"


# =============================================================================
# STACKING: Múltiples decoradores
# =============================================================================


def medir_tiempo(func):
    """Decorador que mide el tiempo de ejecución."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        fin = time.perf_counter()
        print(f"  ⏱ {func.__name__} tardó {fin - inicio:.4f}s")
        return resultado
    return wrapper


def log_entrada_salida(func):
    """Decorador que registra entrada y salida."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"  → Entrando a {func.__name__}")
        resultado = func(*args, **kwargs)
        print(f"  ← Saliendo de {func.__name__}")
        return resultado
    return wrapper


# Stacking: se aplican de ABAJO hacia ARRIBA
# Pero se ejecutan de ARRIBA hacia ABAJO
@medir_tiempo         # 3° en aplicarse, 1° en ejecutarse
@log_entrada_salida   # 2° en aplicarse, 2° en ejecutarse
@repetir(veces=2)     # 1° en aplicarse, 3° en ejecutarse
def proceso_complejo(datos: str) -> str:
    """Procesa datos con múltiples decoradores."""
    time.sleep(0.1)  # Simula trabajo
    return f"Procesado: {datos}"


# =============================================================================
# DECORADOR QUE MODIFICA EL RETORNO
# =============================================================================


def como_json(func):
    """Decorador que envuelve el resultado en estructura JSON de API."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        resultado = func(*args, **kwargs)
        return {
            "success": True,
            "data": resultado,
            "error": None
        }
    return wrapper


def manejar_errores(func):
    """Decorador que captura excepciones y las convierte en respuesta JSON."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": str(e)
            }
    return wrapper


@manejar_errores
@como_json
def obtener_usuario(user_id: int) -> dict:
    """Obtiene un usuario por ID."""
    if user_id <= 0:
        raise ValueError("ID debe ser positivo")
    return {"id": user_id, "nombre": "Ana"}


# =============================================================================
# EJECUCIÓN DE EJEMPLOS
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DECORADOR CON PARÁMETROS: @repetir(veces=3)")
    print("=" * 60)
    resultado = saludar("Carlos")

    print("\n" + "=" * 60)
    print("STACKING DE DECORADORES")
    print("=" * 60)
    resultado = proceso_complejo("mis datos")
    print(f"Resultado: {resultado}")

    print("\n" + "=" * 60)
    print("DECORADORES QUE MODIFICAN RETORNO")
    print("=" * 60)

    print("\nCaso exitoso:")
    print(obtener_usuario(1))

    print("\nCaso con error:")
    print(obtener_usuario(-1))

    print("\n" + "=" * 60)
    print("DECORADOR DE REINTENTOS (puede variar)")
    print("=" * 60)
    try:
        resultado = operacion_inestable()
        print(f"Resultado: {resultado}")
    except ConnectionError as e:
        print(f"Falló después de todos los intentos: {e}")
