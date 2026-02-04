"""
Ejercicio 01: Tipar Funciones Existentes
========================================
Agrega type hints a las funciones sin tipos.

Instrucciones:
1. Analiza cada función y determina los tipos correctos
2. Agrega type hints a parámetros y retorno
3. Ejecuta el archivo para verificar que funciona
"""

# =============================================================================
# EJERCICIO 1.1: Funciones simples
# Agrega type hints a estas funciones
# =============================================================================

# TODO: Agrega tipos a los parámetros y al retorno
def sumar(a, b):
    """Suma dos números."""
    return a + b


# TODO: Agrega tipos
def concatenar(texto1, texto2):
    """Une dos textos con un espacio."""
    return f"{texto1} {texto2}"


# TODO: Agrega tipos
def es_par(numero):
    """Verifica si un número es par."""
    return numero % 2 == 0


# =============================================================================
# EJERCICIO 1.2: Funciones con valores por defecto
# =============================================================================

# TODO: Agrega tipos (nota: tiene valor por defecto)
def formatear_precio(precio, moneda="USD"):
    """Formatea un precio con su moneda."""
    return f"{moneda} {precio:.2f}"


# TODO: Agrega tipos
def crear_mensaje(titulo, cuerpo, urgente=False):
    """Crea un mensaje formateado."""
    prefijo = "[URGENTE] " if urgente else ""
    return f"{prefijo}{titulo}: {cuerpo}"


# =============================================================================
# EJERCICIO 1.3: Funciones que retornan estructuras
# =============================================================================

# TODO: Agrega tipos (retorna un diccionario)
def crear_punto(x, y):
    """Crea un punto con coordenadas x, y."""
    return {"x": x, "y": y}


# TODO: Agrega tipos (retorna una lista)
def rango_numeros(inicio, fin):
    """Genera lista de números desde inicio hasta fin (exclusive)."""
    return list(range(inicio, fin))


# =============================================================================
# VERIFICACIÓN
# =============================================================================

if __name__ == "__main__":
    # Si los tipos están bien, esto debe funcionar sin errores
    print(sumar(5, 3))              # 8
    print(concatenar("Hola", "Mundo"))  # Hola Mundo
    print(es_par(4))                # True
    print(formatear_precio(99.99))  # USD 99.99
    print(crear_mensaje("Alerta", "Sistema OK"))
    print(crear_punto(10, 20))      # {'x': 10, 'y': 20}
    print(rango_numeros(1, 5))      # [1, 2, 3, 4]

    print("\n✓ Todas las funciones ejecutadas correctamente")
    print("Ahora verifica tus tipos con: python -m mypy ejercicio_01.py")
