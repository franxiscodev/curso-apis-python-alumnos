"""
Solucion Ejercicio 01: Funciones con *args y **kwargs
=====================================================

Ejecutar:
    python ejercicio_01_solucion.py
"""


# =============================================================================
# SOLUCION 1: calcular_promedio
# =============================================================================


def calcular_promedio(*numeros):
    """Calcula el promedio de N numeros."""
    if not numeros:
        return 0.0
    return sum(numeros) / len(numeros)


# =============================================================================
# SOLUCION 2: crear_perfil
# =============================================================================


def crear_perfil(nombre, **datos):
    """Crea un perfil con nombre obligatorio y datos opcionales."""
    perfil = {"nombre": nombre}
    perfil.update(datos)
    return perfil


# =============================================================================
# SOLUCION 3: formatear_mensaje
# =============================================================================


def formatear_mensaje(plantilla, *args, **kwargs):
    """Formatea una plantilla con argumentos posicionales y con nombre."""
    return plantilla.format(*args, **kwargs)


# =============================================================================
# VERIFICACION
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Verificando solucion ejercicio 01")
    print("=" * 60)

    # --- calcular_promedio ---
    print("\n--- calcular_promedio ---")
    assert calcular_promedio(10, 20, 30) == 20.0
    assert calcular_promedio(5) == 5.0
    assert calcular_promedio() == 0.0
    assert calcular_promedio(1, 2, 3, 4, 5) == 3.0
    print("  Todos los tests pasaron OK")

    # --- crear_perfil ---
    print("\n--- crear_perfil ---")
    assert crear_perfil("Ana") == {"nombre": "Ana"}
    assert crear_perfil("Ana", edad=30) == {"nombre": "Ana", "edad": 30}
    assert crear_perfil("Carlos", edad=25, ciudad="Madrid", rol="dev") == {
        "nombre": "Carlos", "edad": 25, "ciudad": "Madrid", "rol": "dev"
    }
    print("  Todos los tests pasaron OK")

    # --- formatear_mensaje ---
    print("\n--- formatear_mensaje ---")
    assert formatear_mensaje("Hola {} y {}", "Ana", "Carlos") == "Hola Ana y Carlos"
    assert formatear_mensaje("{nombre} tiene {edad} años", nombre="Ana", edad=30) == "Ana tiene 30 años"
    assert formatear_mensaje("{} dice: {msg}", "Ana", msg="hola") == "Ana dice: hola"
    print("  Todos los tests pasaron OK")

    print("\nTodas las soluciones son correctas")
