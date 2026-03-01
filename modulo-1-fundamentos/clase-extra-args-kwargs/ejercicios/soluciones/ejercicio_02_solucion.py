"""
Solucion Ejercicio 02: Unpacking y Forwarding
==============================================

Ejecutar:
    python ejercicio_02_solucion.py
"""


# =============================================================================
# SOLUCION 1: combinar_listas
# =============================================================================


def combinar_listas(*listas):
    """Combina multiples listas en una sola."""
    resultado = []
    for lista in listas:
        resultado.extend(lista)
    return resultado


# =============================================================================
# SOLUCION 2: merge_diccionarios
# =============================================================================


def merge_diccionarios(*diccionarios):
    """Combina multiples diccionarios en uno solo."""
    resultado = {}
    for diccionario in diccionarios:
        resultado.update(diccionario)
    return resultado


# =============================================================================
# SOLUCION 3: llamar_con_config
# =============================================================================


def llamar_con_config(func, config):
    """Llama a func con los pares clave-valor de config como kwargs."""
    return func(**config)


# =============================================================================
# VERIFICACION
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Verificando solucion ejercicio 02")
    print("=" * 60)

    # --- combinar_listas ---
    print("\n--- combinar_listas ---")
    assert combinar_listas([1, 2], [3, 4]) == [1, 2, 3, 4]
    assert combinar_listas([1], [2], [3]) == [1, 2, 3]
    assert combinar_listas() == []
    assert combinar_listas(["a", "b"], ["c"], ["d", "e", "f"]) == ["a", "b", "c", "d", "e", "f"]
    print("  Todos los tests pasaron OK")

    # --- merge_diccionarios ---
    print("\n--- merge_diccionarios ---")
    assert merge_diccionarios({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}
    assert merge_diccionarios({"a": 1}, {"a": 2}) == {"a": 2}
    assert merge_diccionarios() == {}
    assert merge_diccionarios({"x": 1}, {"y": 2}, {"z": 3}) == {"x": 1, "y": 2, "z": 3}
    print("  Todos los tests pasaron OK")

    # --- llamar_con_config ---
    print("\n--- llamar_con_config ---")

    def saludar(nombre, saludo="Hola"):
        return f"{saludo}, {nombre}!"

    assert llamar_con_config(saludar, {"nombre": "Ana"}) == "Hola, Ana!"
    assert llamar_con_config(saludar, {"nombre": "Ana", "saludo": "Hey"}) == "Hey, Ana!"

    def sumar(a, b, c=0):
        return a + b + c

    assert llamar_con_config(sumar, {"a": 1, "b": 2}) == 3
    assert llamar_con_config(sumar, {"a": 1, "b": 2, "c": 10}) == 13
    print("  Todos los tests pasaron OK")

    print("\nTodas las soluciones son correctas")
