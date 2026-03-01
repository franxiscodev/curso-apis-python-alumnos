"""
Solucion Ejercicio 03: Wrapper Generico (Conexion con Decoradores)
==================================================================

Ejecutar:
    python ejercicio_03_solucion.py
"""


# =============================================================================
# SOLUCION 1: registrar_llamada
# =============================================================================


def registrar_llamada(func, *args, **kwargs):
    """Ejecuta func y registra la llamada."""
    print(f"Llamando a {func.__name__} con args={args} kwargs={kwargs}")
    return func(*args, **kwargs)


# =============================================================================
# SOLUCION 2: con_valores_por_defecto
# =============================================================================


def con_valores_por_defecto(func, **defaults):
    """Retorna una nueva funcion con valores por defecto inyectados."""
    def nueva_funcion(*args, **kwargs):
        # Combinar: kwargs del usuario sobreescriben los defaults
        combinados = {**defaults, **kwargs}
        return func(*args, **combinados)
    return nueva_funcion


# =============================================================================
# SOLUCION 3: crear_decorador_log
# =============================================================================


def crear_decorador_log():
    """Retorna un decorador que registra llamadas a funciones."""
    def decorador(func):
        def wrapper(*args, **kwargs):
            print(f"[LOG] Ejecutando {func.__name__}")
            resultado = func(*args, **kwargs)
            print(f"[LOG] {func.__name__} retorno: {resultado}")
            return resultado
        return wrapper
    return decorador


# =============================================================================
# VERIFICACION
# =============================================================================

if __name__ == "__main__":
    import io
    import sys

    print("=" * 60)
    print("Verificando solucion ejercicio 03")
    print("=" * 60)

    # --- registrar_llamada ---
    print("\n--- registrar_llamada ---")

    def sumar(a, b):
        return a + b

    captura = io.StringIO()
    sys.stdout = captura
    resultado = registrar_llamada(sumar, 1, 2)
    sys.stdout = sys.__stdout__

    assert resultado == 3
    assert "sumar" in captura.getvalue()
    print("  registrar_llamada funciona OK")

    # --- con_valores_por_defecto ---
    print("\n--- con_valores_por_defecto ---")

    def crear_usuario(nombre, rol="viewer", activo=True):
        return {"nombre": nombre, "rol": rol, "activo": activo}

    crear_admin = con_valores_por_defecto(crear_usuario, rol="admin")
    assert crear_admin("Ana") == {"nombre": "Ana", "rol": "admin", "activo": True}
    assert crear_admin("Carlos", rol="superadmin") == {"nombre": "Carlos", "rol": "superadmin", "activo": True}

    crear_inactivo = con_valores_por_defecto(crear_usuario, activo=False)
    assert crear_inactivo("Luis") == {"nombre": "Luis", "rol": "viewer", "activo": False}
    print("  con_valores_por_defecto funciona OK")

    # --- crear_decorador_log ---
    print("\n--- crear_decorador_log ---")

    mi_log = crear_decorador_log()

    @mi_log
    def multiplicar(a, b):
        return a * b

    captura = io.StringIO()
    sys.stdout = captura
    resultado = multiplicar(3, 4)
    sys.stdout = sys.__stdout__
    salida = captura.getvalue()

    assert resultado == 12
    assert "[LOG]" in salida
    assert "multiplicar" in salida
    print("  crear_decorador_log funciona OK")

    print("\nTodas las soluciones son correctas")
