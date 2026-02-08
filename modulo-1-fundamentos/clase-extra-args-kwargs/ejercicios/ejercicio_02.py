"""
Ejercicio 02: Unpacking y Forwarding
=====================================
Practicar unpacking de colecciones y forwarding de argumentos.

Instrucciones:
1. Completa las 3 funciones siguiendo las indicaciones
2. Usa unpacking (*) y (**) en las implementaciones
3. Ejecuta el archivo para verificar con los asserts

Ejecutar:
    python ejercicio_02.py
"""

# =============================================================================
# EJERCICIO 1: combinar_listas(*listas)
# Recibe un numero variable de listas y retorna una sola lista combinada.
# =============================================================================


def combinar_listas(*listas):
    """
    Combina multiples listas en una sola.

    Ejemplos:
        combinar_listas([1, 2], [3, 4]) → [1, 2, 3, 4]
        combinar_listas([1], [2], [3]) → [1, 2, 3]
        combinar_listas() → []
    """
    # TODO: Implementar
    # Hint: itera sobre cada lista en 'listas' y agrega sus elementos
    # Puedes usar un bucle, list comprehension, o sum(listas, [])
    pass


# =============================================================================
# EJERCICIO 2: merge_diccionarios(*diccionarios)
# Recibe un numero variable de diccionarios y retorna uno solo combinado.
# Si hay claves repetidas, el ultimo diccionario gana.
# =============================================================================


def merge_diccionarios(*diccionarios):
    """
    Combina multiples diccionarios en uno solo.

    Ejemplos:
        merge_diccionarios({"a": 1}, {"b": 2}) → {"a": 1, "b": 2}
        merge_diccionarios({"a": 1}, {"a": 2}) → {"a": 2}
        merge_diccionarios() → {}
    """
    # TODO: Implementar
    # Hint: itera sobre los diccionarios y actualiza un resultado
    # O usa el patron {**d1, **d2, **d3}
    pass


# =============================================================================
# EJERCICIO 3: llamar_con_config(func, config)
# Recibe una funcion y un diccionario de configuracion.
# Llama a la funcion desempaquetando el diccionario como kwargs.
# =============================================================================


def llamar_con_config(func, config):
    """
    Llama a func con los pares clave-valor de config como keyword arguments.

    Ejemplos:
        def saludar(nombre, saludo="Hola"):
            return f"{saludo}, {nombre}!"

        llamar_con_config(saludar, {"nombre": "Ana"})
            → "Hola, Ana!"
        llamar_con_config(saludar, {"nombre": "Ana", "saludo": "Hey"})
            → "Hey, Ana!"
    """
    # TODO: Implementar
    # Hint: usa ** para desempaquetar config al llamar a func
    pass


# =============================================================================
# VERIFICACION (no modificar)
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Verificando ejercicio 02")
    print("=" * 60)

    # --- Test combinar_listas ---
    print("\n--- Test combinar_listas ---")

    assert combinar_listas([1, 2], [3, 4]) == [1, 2, 3, 4]
    print("  combinar_listas([1,2], [3,4]) OK")

    assert combinar_listas([1], [2], [3]) == [1, 2, 3]
    print("  combinar_listas([1], [2], [3]) OK")

    assert combinar_listas() == []
    print("  combinar_listas() OK")

    assert combinar_listas(["a", "b"], ["c"], ["d", "e", "f"]) == ["a", "b", "c", "d", "e", "f"]
    print("  combinar_listas con strings OK")

    # --- Test merge_diccionarios ---
    print("\n--- Test merge_diccionarios ---")

    assert merge_diccionarios({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}
    print('  merge_diccionarios({"a":1}, {"b":2}) OK')

    assert merge_diccionarios({"a": 1}, {"a": 2}) == {"a": 2}
    print('  merge con sobreescritura OK')

    assert merge_diccionarios() == {}
    print("  merge_diccionarios() OK")

    assert merge_diccionarios({"x": 1}, {"y": 2}, {"z": 3}) == {"x": 1, "y": 2, "z": 3}
    print("  merge de 3 diccionarios OK")

    # --- Test llamar_con_config ---
    print("\n--- Test llamar_con_config ---")

    def saludar(nombre, saludo="Hola"):
        return f"{saludo}, {nombre}!"

    assert llamar_con_config(saludar, {"nombre": "Ana"}) == "Hola, Ana!"
    print('  llamar_con_config con defaults OK')

    assert llamar_con_config(saludar, {"nombre": "Ana", "saludo": "Hey"}) == "Hey, Ana!"
    print('  llamar_con_config con override OK')

    def sumar(a, b, c=0):
        return a + b + c

    assert llamar_con_config(sumar, {"a": 1, "b": 2}) == 3
    print('  llamar_con_config con sumar OK')

    assert llamar_con_config(sumar, {"a": 1, "b": 2, "c": 10}) == 13
    print('  llamar_con_config con c=10 OK')

    print("\nTodos los tests pasaron")
