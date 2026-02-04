"""
Ejemplo 01: Type Hints Básicos
==============================
Introducción a la sintaxis de type hints en Python.

Objetivo: Aprender a tipar variables y funciones simples.
"""

# =============================================================================
# VARIABLES CON TIPOS
# =============================================================================

# Tipos primitivos básicos
nombre: str = "Ana García"
edad: int = 28
salario: float = 45000.50
activo: bool = True

# Python NO valida tipos en runtime - esto NO da error:
# edad: int = "veinte"  # Descomenta para ver que Python lo acepta


# =============================================================================
# FUNCIONES CON TIPOS
# =============================================================================

def saludar(nombre: str) -> str:
    """
    Genera un saludo personalizado.

    Args:
        nombre: Nombre de la persona a saludar

    Returns:
        Mensaje de saludo formateado
    """
    return f"¡Hola, {nombre}!"


def calcular_precio_final(precio: float, descuento: float) -> float:
    """
    Calcula el precio aplicando un descuento.

    Args:
        precio: Precio original del producto
        descuento: Porcentaje de descuento (0-100)

    Returns:
        Precio final después del descuento
    """
    return precio * (1 - descuento / 100)


def es_mayor_de_edad(edad: int) -> bool:
    """
    Verifica si una persona es mayor de edad.

    Args:
        edad: Edad en años

    Returns:
        True si es mayor de 18 años
    """
    return edad >= 18


# =============================================================================
# EJECUCIÓN DE EJEMPLOS
# =============================================================================

if __name__ == "__main__":
    # Probamos las funciones
    print(saludar("Carlos"))
    # Salida: ¡Hola, Carlos!

    precio_final = calcular_precio_final(100.0, 15.0)
    print(f"Precio con 15% descuento: {precio_final}")
    # Salida: Precio con 15% descuento: 85.0

    print(f"¿Es mayor de edad (20)? {es_mayor_de_edad(20)}")
    # Salida: ¿Es mayor de edad (20)? True
