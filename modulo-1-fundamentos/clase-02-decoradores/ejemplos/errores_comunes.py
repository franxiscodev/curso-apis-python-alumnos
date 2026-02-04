"""
Errores Comunes con Decoradores
===============================
Ejemplos de errores frecuentes y cómo evitarlos.

Objetivo: Aprender a identificar y corregir errores típicos con decoradores.
"""

from functools import wraps

# =============================================================================
# ERROR 1: Olvidar @wraps - pérdida de metadatos
# =============================================================================


def decorador_malo(func):
    """❌ NO usa @wraps - pierde información de la función."""
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def decorador_bueno(func):
    """✅ USA @wraps - preserva información."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@decorador_malo
def funcion_a():
    """Documentación de funcion_a."""
    pass


@decorador_bueno
def funcion_b():
    """Documentación de funcion_b."""
    pass


print("ERROR 1: Olvidar @wraps")
print(f"  Sin @wraps: __name__ = '{funcion_a.__name__}', __doc__ = {funcion_a.__doc__}")
print(f"  Con @wraps: __name__ = '{funcion_b.__name__}', __doc__ = '{funcion_b.__doc__}'")


# =============================================================================
# ERROR 2: Olvidar retornar el resultado de la función
# =============================================================================


def decorador_sin_return(func):
    """❌ No retorna el resultado de func()."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Ejecutando...")
        func(*args, **kwargs)  # ¡Falta return!
    return wrapper


def decorador_con_return(func):
    """✅ Retorna el resultado correctamente."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Ejecutando...")
        return func(*args, **kwargs)  # ✅ Con return
    return wrapper


@decorador_sin_return
def sumar_mal(a: int, b: int) -> int:
    return a + b


@decorador_con_return
def sumar_bien(a: int, b: int) -> int:
    return a + b


print("\nERROR 2: Olvidar return")
print(f"  Sin return: sumar_mal(2, 3) = {sumar_mal(2, 3)}")  # None!
print(f"  Con return: sumar_bien(2, 3) = {sumar_bien(2, 3)}")  # 5


# =============================================================================
# ERROR 3: Decorador con parámetros - olvidar un nivel de anidación
# =============================================================================


# ❌ INCORRECTO - Solo 2 niveles cuando necesita 3
# def repetir_mal(veces: int, func):  # Esto NO funciona como decorador
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         for _ in range(veces):
#             func(*args, **kwargs)
#     return wrapper
#
# @repetir_mal(3)  # TypeError: repetir_mal() missing 1 required argument: 'func'
# def saludar():
#     print("Hola")


# ✅ CORRECTO - 3 niveles de anidación
def repetir_bien(veces: int):
    """Nivel 1: Recibe parámetros, retorna decorador."""
    def decorador(func):
        """Nivel 2: Recibe función, retorna wrapper."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Nivel 3: Ejecuta la función."""
            for _ in range(veces):
                func(*args, **kwargs)
        return wrapper
    return decorador


@repetir_bien(veces=2)
def saludar():
    print("  Hola")


print("\nERROR 3: Niveles de anidación")
print("Correcto con 3 niveles:")
saludar()


# =============================================================================
# ERROR 4: Modificar argumentos mutables en el decorador
# =============================================================================


def decorador_que_muta_mal(func):
    """❌ Modifica el argumento original - efecto secundario inesperado."""
    @wraps(func)
    def wrapper(lista: list, *args, **kwargs):
        lista.append("AGREGADO POR DECORADOR")  # ¡Muta la lista original!
        return func(lista, *args, **kwargs)
    return wrapper


def decorador_que_copia_bien(func):
    """✅ Trabaja con una copia - sin efectos secundarios."""
    @wraps(func)
    def wrapper(lista: list, *args, **kwargs):
        lista_copia = lista.copy()
        lista_copia.append("AGREGADO POR DECORADOR")
        return func(lista_copia, *args, **kwargs)
    return wrapper


@decorador_que_muta_mal
def procesar_lista_mal(lista: list) -> int:
    return len(lista)


@decorador_que_copia_bien
def procesar_lista_bien(lista: list) -> int:
    return len(lista)


mi_lista = ["a", "b"]
print("\nERROR 4: Mutar argumentos")
print(f"  Lista original: {mi_lista}")
procesar_lista_mal(mi_lista)
print(f"  Después de decorador malo: {mi_lista}")  # ['a', 'b', 'AGREGADO...']

mi_lista2 = ["a", "b"]
procesar_lista_bien(mi_lista2)
print(f"  Después de decorador bueno: {mi_lista2}")  # ['a', 'b'] - sin modificar


# =============================================================================
# ERROR 5: Orden incorrecto de stacking
# =============================================================================


def primero(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("  1. Primero - antes")
        resultado = func(*args, **kwargs)
        print("  1. Primero - después")
        return resultado
    return wrapper


def segundo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("  2. Segundo - antes")
        resultado = func(*args, **kwargs)
        print("  2. Segundo - después")
        return resultado
    return wrapper


# Los decoradores se APLICAN de abajo hacia arriba
# Pero se EJECUTAN de arriba hacia abajo
@primero   # Se aplica 2°, se ejecuta 1°
@segundo   # Se aplica 1°, se ejecuta 2°
def mi_funcion():
    print("  → Función ejecutándose")


print("\nERROR 5: Orden de stacking")
print("Orden de ejecución:")
mi_funcion()


# =============================================================================
# ERROR 6: Decorador que no acepta funciones async
# =============================================================================


def decorador_sync_only(func):
    """❌ No funciona con funciones async."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Ejecutando...")
        return func(*args, **kwargs)  # Retorna coroutine sin await
    return wrapper


import asyncio


def decorador_async_compatible(func):
    """✅ Funciona con funciones sync y async."""
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        print("Ejecutando async...")
        return await func(*args, **kwargs)

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        print("Ejecutando sync...")
        return func(*args, **kwargs)

    # Detectar si la función es async
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper


print("\nERROR 6: Decoradores y async")
print("Para funciones async, el decorador debe usar 'await'")
print("(Ver ejemplo en código - requiere asyncio.run() para ejecutar)")


# =============================================================================
# RESUMEN
# =============================================================================

print("\n" + "=" * 60)
print("RESUMEN DE ERRORES COMUNES")
print("=" * 60)
print("""
1. Olvidar @wraps         → Usa siempre @wraps(func)
2. Olvidar return         → return func(*args, **kwargs)
3. Niveles incorrectos    → Con params: 3 niveles de anidación
4. Mutar argumentos       → Trabajar con copias
5. Orden de stacking      → Aplican abajo→arriba, ejecutan arriba→abajo
6. Async incompatible     → Detectar y usar await para async
""")
