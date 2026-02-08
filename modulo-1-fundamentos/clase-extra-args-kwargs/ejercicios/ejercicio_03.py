"""
Ejercicio 03: Wrapper Generico (Conexion con Decoradores)
==========================================================
Practicar el patron de forwarding que es la base de los decoradores.

Este ejercicio es el PUENTE directo a clase-02 (decoradores).
Si puedes completar esto, estas listo para decoradores.

Instrucciones:
1. Completa las 3 funciones siguiendo las indicaciones
2. Todas usan *args y **kwargs para forwarding
3. Ejecuta el archivo para verificar con los asserts

Ejecutar:
    python ejercicio_03.py
"""

# =============================================================================
# EJERCICIO 1: registrar_llamada(func, *args, **kwargs)
# Llama a func con los argumentos dados, pero antes imprime la llamada.
# Retorna el resultado de func.
# =============================================================================


def registrar_llamada(func, *args, **kwargs):
    """
    Ejecuta func(*args, **kwargs) y registra la llamada.

    Antes de ejecutar, debe imprimir:
        Llamando a {nombre_funcion} con args={args} kwargs={kwargs}

    Retorna el resultado de la funcion.

    Ejemplo:
        def sumar(a, b): return a + b
        registrar_llamada(sumar, 1, 2)
        # Imprime: Llamando a sumar con args=(1, 2) kwargs={}
        # Retorna: 3
    """
    # TODO: Implementar
    # Hint: func.__name__ te da el nombre de la funcion
    # Hint: llama a func(*args, **kwargs) y retorna su resultado
    pass


# =============================================================================
# EJERCICIO 2: con_valores_por_defecto(func, **defaults)
# Retorna una nueva funcion que llama a func con valores por defecto.
# Los valores pasados al llamar la nueva funcion sobreescriben los defaults.
# =============================================================================


def con_valores_por_defecto(func, **defaults):
    """
    Retorna una nueva funcion con valores por defecto inyectados.

    Ejemplo:
        def crear_usuario(nombre, rol="viewer", activo=True):
            return {"nombre": nombre, "rol": rol, "activo": activo}

        crear_admin = con_valores_por_defecto(crear_usuario, rol="admin")
        crear_admin("Ana")
            → {"nombre": "Ana", "rol": "admin", "activo": True}
        crear_admin("Ana", rol="superadmin")
            → {"nombre": "Ana", "rol": "superadmin", "activo": True}
    """
    # TODO: Implementar
    # Hint: define una funcion interna que reciba *args y **kwargs
    # Hint: combina defaults con kwargs (kwargs tiene prioridad)
    # Hint: {**defaults, **kwargs} - el segundo sobreescribe al primero
    # Hint: retorna esa funcion interna
    pass


# =============================================================================
# EJERCICIO 3: crear_decorador_log()
# Retorna un decorador que imprime antes y despues de ejecutar la funcion.
# =============================================================================


def crear_decorador_log():
    """
    Retorna un decorador que registra llamadas a funciones.

    El decorador debe:
    1. Imprimir "[LOG] Ejecutando {nombre}" antes de llamar
    2. Ejecutar la funcion con *args y **kwargs
    3. Imprimir "[LOG] {nombre} retorno: {resultado}" despues
    4. Retornar el resultado

    Ejemplo:
        mi_log = crear_decorador_log()

        @mi_log
        def sumar(a, b):
            return a + b

        sumar(1, 2)
        # Imprime: [LOG] Ejecutando sumar
        # Imprime: [LOG] sumar retorno: 3
        # Retorna: 3
    """
    # TODO: Implementar
    # Hint: el decorador es una funcion que recibe func
    # Hint: dentro define wrapper(*args, **kwargs)
    # Hint: wrapper imprime, ejecuta func, imprime, retorna resultado
    # Hint: el decorador retorna wrapper
    # Hint: crear_decorador_log retorna el decorador
    pass


# =============================================================================
# VERIFICACION (no modificar)
# =============================================================================

if __name__ == "__main__":
    import io
    import sys

    print("=" * 60)
    print("Verificando ejercicio 03")
    print("=" * 60)

    # --- Test registrar_llamada ---
    print("\n--- Test registrar_llamada ---")

    def sumar(a, b):
        return a + b

    # Capturar print
    captura = io.StringIO()
    sys.stdout = captura
    resultado = registrar_llamada(sumar, 1, 2)
    sys.stdout = sys.__stdout__
    salida = captura.getvalue()

    assert resultado == 3, f"registrar_llamada(sumar, 1, 2) debe retornar 3, retorno {resultado}"
    assert "sumar" in salida, "Debe imprimir el nombre de la funcion"
    print(f"  registrar_llamada(sumar, 1, 2) = {resultado} OK")

    def saludar(nombre, exclamar=False):
        msg = f"Hola {nombre}"
        return f"{msg}!" if exclamar else msg

    captura = io.StringIO()
    sys.stdout = captura
    resultado = registrar_llamada(saludar, "Ana", exclamar=True)
    sys.stdout = sys.__stdout__

    assert resultado == "Hola Ana!", f"Debe retornar 'Hola Ana!', retorno {resultado}"
    print(f'  registrar_llamada(saludar, "Ana", exclamar=True) OK')

    # --- Test con_valores_por_defecto ---
    print("\n--- Test con_valores_por_defecto ---")

    def crear_usuario(nombre, rol="viewer", activo=True):
        return {"nombre": nombre, "rol": rol, "activo": activo}

    crear_admin = con_valores_por_defecto(crear_usuario, rol="admin")

    resultado = crear_admin("Ana")
    assert resultado == {"nombre": "Ana", "rol": "admin", "activo": True}, f"Resultado: {resultado}"
    print('  crear_admin("Ana") OK')

    resultado = crear_admin("Carlos", rol="superadmin")
    assert resultado == {"nombre": "Carlos", "rol": "superadmin", "activo": True}, f"Resultado: {resultado}"
    print('  crear_admin("Carlos", rol="superadmin") sobreescribe OK')

    crear_inactivo = con_valores_por_defecto(crear_usuario, activo=False)
    resultado = crear_inactivo("Luis")
    assert resultado == {"nombre": "Luis", "rol": "viewer", "activo": False}, f"Resultado: {resultado}"
    print('  crear_inactivo("Luis") OK')

    # --- Test crear_decorador_log ---
    print("\n--- Test crear_decorador_log ---")

    mi_log = crear_decorador_log()
    assert mi_log is not None, "crear_decorador_log debe retornar un decorador"

    @mi_log
    def multiplicar(a, b):
        return a * b

    captura = io.StringIO()
    sys.stdout = captura
    resultado = multiplicar(3, 4)
    sys.stdout = sys.__stdout__
    salida = captura.getvalue()

    assert resultado == 12, f"multiplicar(3, 4) debe retornar 12, retorno {resultado}"
    assert "[LOG]" in salida, "Debe imprimir [LOG]"
    assert "multiplicar" in salida, "Debe imprimir el nombre de la funcion"
    print(f"  @mi_log multiplicar(3, 4) = {resultado} OK")

    @mi_log
    def hola(nombre="mundo"):
        return f"Hola {nombre}"

    captura = io.StringIO()
    sys.stdout = captura
    resultado = hola(nombre="Python")
    sys.stdout = sys.__stdout__

    assert resultado == "Hola Python", f"Debe retornar 'Hola Python', retorno {resultado}"
    print(f'  @mi_log hola(nombre="Python") OK')

    print("\nTodos los tests pasaron")
