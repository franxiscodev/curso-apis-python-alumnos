"""
Ejercicio 01: Funciones con *args y **kwargs
=============================================
Crear funciones que usen argumentos variables.

Instrucciones:
1. Completa las 3 funciones siguiendo las indicaciones
2. Cada funcion usa *args, **kwargs o ambos
3. Ejecuta el archivo para verificar con los asserts

Ejecutar:
    python ejercicio_01.py
"""

# =============================================================================
# EJERCICIO 1: calcular_promedio(*numeros)
# Recibe un numero variable de argumentos numericos y retorna el promedio.
# Si no recibe argumentos, retorna 0.0
# =============================================================================


def calcular_promedio(*numeros):
    """
    Calcula el promedio de N numeros.

    Ejemplos:
        calcular_promedio(10, 20, 30) → 20.0
        calcular_promedio(5) → 5.0
        calcular_promedio() → 0.0
    """
    # TODO: Implementar
    # Hint: numeros es una tupla, puedes usar len() y sum()
    # Hint: cuidado con la division por cero cuando no hay argumentos
    pass


# =============================================================================
# EJERCICIO 2: crear_perfil(nombre, **datos)
# Recibe un nombre obligatorio y datos adicionales como kwargs.
# Retorna un diccionario con "nombre" y todos los datos extra.
# =============================================================================


def crear_perfil(nombre, **datos):
    """
    Crea un perfil con nombre obligatorio y datos opcionales.

    Ejemplos:
        crear_perfil("Ana") → {"nombre": "Ana"}
        crear_perfil("Ana", edad=30) → {"nombre": "Ana", "edad": 30}
        crear_perfil("Ana", edad=30, ciudad="Madrid")
            → {"nombre": "Ana", "edad": 30, "ciudad": "Madrid"}
    """
    # TODO: Implementar
    # Hint: crea un diccionario con "nombre" y agrega los datos extra
    pass


# =============================================================================
# EJERCICIO 3: formatear_mensaje(plantilla, *args, **kwargs)
# Recibe una plantilla string y la formatea con los argumentos.
# - *args se usan para {} posicionales
# - **kwargs se usan para {nombre} con nombre
# =============================================================================


def formatear_mensaje(plantilla, *args, **kwargs):
    """
    Formatea una plantilla con argumentos posicionales y con nombre.

    Ejemplos:
        formatear_mensaje("Hola {} y {}", "Ana", "Carlos")
            → "Hola Ana y Carlos"
        formatear_mensaje("{nombre} tiene {edad} años", nombre="Ana", edad=30)
            → "Ana tiene 30 años"
        formatear_mensaje("{} dice: {msg}", "Ana", msg="hola")
            → "Ana dice: hola"
    """
    # TODO: Implementar
    # Hint: str.format() acepta *args y **kwargs
    # plantilla.format(*args, **kwargs)
    pass


# =============================================================================
# VERIFICACION (no modificar)
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Verificando ejercicio 01")
    print("=" * 60)

    # --- Test calcular_promedio ---
    print("\n--- Test calcular_promedio ---")

    assert calcular_promedio(10, 20, 30) == 20.0, "promedio(10,20,30) debe ser 20.0"
    print("  calcular_promedio(10, 20, 30) = 20.0 OK")

    assert calcular_promedio(5) == 5.0, "promedio(5) debe ser 5.0"
    print("  calcular_promedio(5) = 5.0 OK")

    assert calcular_promedio() == 0.0, "promedio() debe ser 0.0"
    print("  calcular_promedio() = 0.0 OK")

    assert calcular_promedio(1, 2, 3, 4, 5) == 3.0, "promedio(1,2,3,4,5) debe ser 3.0"
    print("  calcular_promedio(1, 2, 3, 4, 5) = 3.0 OK")

    # --- Test crear_perfil ---
    print("\n--- Test crear_perfil ---")

    assert crear_perfil("Ana") == {"nombre": "Ana"}, "perfil solo con nombre"
    print('  crear_perfil("Ana") OK')

    assert crear_perfil("Ana", edad=30) == {"nombre": "Ana", "edad": 30}
    print('  crear_perfil("Ana", edad=30) OK')

    perfil = crear_perfil("Carlos", edad=25, ciudad="Madrid", rol="dev")
    assert perfil == {"nombre": "Carlos", "edad": 25, "ciudad": "Madrid", "rol": "dev"}
    print('  crear_perfil("Carlos", edad=25, ciudad="Madrid", rol="dev") OK')

    # --- Test formatear_mensaje ---
    print("\n--- Test formatear_mensaje ---")

    assert formatear_mensaje("Hola {} y {}", "Ana", "Carlos") == "Hola Ana y Carlos"
    print('  formatear_mensaje con args OK')

    assert formatear_mensaje("{nombre} tiene {edad} años", nombre="Ana", edad=30) == "Ana tiene 30 años"
    print('  formatear_mensaje con kwargs OK')

    assert formatear_mensaje("{} dice: {msg}", "Ana", msg="hola") == "Ana dice: hola"
    print('  formatear_mensaje con args y kwargs OK')

    print("\nTodos los tests pasaron")
