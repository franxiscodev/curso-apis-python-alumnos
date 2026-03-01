"""
Solución Ejercicio 01: Tipar Funciones Existentes
=================================================
"""

# =============================================================================
# EJERCICIO 1.1: Funciones simples
# =============================================================================


def sumar(a: int, b: int) -> int:
    """Suma dos números."""
    return a + b


def concatenar(texto1: str, texto2: str) -> str:
    """Une dos textos con un espacio."""
    return f"{texto1} {texto2}"


def es_par(numero: int) -> bool:
    """Verifica si un número es par."""
    return numero % 2 == 0


# =============================================================================
# EJERCICIO 1.2: Funciones con valores por defecto
# =============================================================================


def formatear_precio(precio: float, moneda: str = "USD") -> str:
    """Formatea un precio con su moneda."""
    return f"{moneda} {precio:.2f}"


def crear_mensaje(titulo: str, cuerpo: str, urgente: bool = False) -> str:
    """Crea un mensaje formateado."""
    prefijo = "[URGENTE] " if urgente else ""
    return f"{prefijo}{titulo}: {cuerpo}"


# =============================================================================
# EJERCICIO 1.3: Funciones que retornan estructuras
# =============================================================================


def crear_punto(x: float, y: float) -> dict[str, float]:
    """Crea un punto con coordenadas x, y."""
    return {"x": x, "y": y}


def rango_numeros(inicio: int, fin: int) -> list[int]:
    """Genera lista de números desde inicio hasta fin (exclusive)."""
    return list(range(inicio, fin))


# =============================================================================
# VERIFICACIÓN
# =============================================================================

if __name__ == "__main__":
    print(sumar(5, 3))
    print(concatenar("Hola", "Mundo"))
    print(es_par(4))
    print(formatear_precio(99.99))
    print(crear_mensaje("Alerta", "Sistema OK"))
    print(crear_punto(10, 20))
    print(rango_numeros(1, 5))

    print("\n✓ Solución verificada")
