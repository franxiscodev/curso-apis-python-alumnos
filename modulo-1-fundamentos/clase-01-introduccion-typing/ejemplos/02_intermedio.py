"""
Ejemplo 02: Tipos Complejos - Sintaxis Moderna Python 3.10+
===========================================================
Uso de tipos complejos con la sintaxis moderna (PEP 604).

Objetivo: Tipar estructuras de datos complejas como las que usan las APIs.

Nota: Desde Python 3.10 usamos `str | int` en lugar de `Union[str, int]`
      y `str | None` en lugar de `Optional[str]`. Esta es la sintaxis
      que FastAPI y Pydantic v2 recomiendan.
"""

# =============================================================================
# LISTAS Y DICCIONARIOS (Sintaxis moderna Python 3.9+)
# =============================================================================

# Lista de strings
nombres: list[str] = ["Ana", "Carlos", "María"]

# Diccionario string -> int
edades: dict[str, int] = {"Ana": 28, "Carlos": 35, "María": 22}

# Lista de diccionarios (muy común en APIs)
usuarios: list[dict[str, str | int]] = [
    {"nombre": "Ana", "edad": 28},
    {"nombre": "Carlos", "edad": 35},
]


# =============================================================================
# VALORES OPCIONALES - Pueden ser None (sintaxis: T | None)
# =============================================================================

def buscar_usuario(user_id: int) -> dict[str, str | int] | None:
    """
    Busca un usuario por ID. Retorna None si no existe.

    Args:
        user_id: ID del usuario a buscar

    Returns:
        Diccionario con datos del usuario o None si no existe
    """
    # Simulamos una "base de datos"
    usuarios_db = {
        1: {"id": 1, "nombre": "Ana", "email": "ana@ejemplo.com"},
        2: {"id": 2, "nombre": "Carlos", "email": "carlos@ejemplo.com"},
    }
    return usuarios_db.get(user_id)  # Retorna None si no existe


# =============================================================================
# UNION DE TIPOS - Múltiples tipos posibles (sintaxis: A | B)
# =============================================================================

def procesar_id(identificador: int | str) -> str:
    """
    Procesa un ID que puede ser numérico o string.

    Args:
        identificador: ID como entero o string

    Returns:
        ID normalizado como string
    """
    return str(identificador)


def formatear_valor(valor: int | float | str) -> str:
    """
    Formatea un valor que puede ser de varios tipos.

    Args:
        valor: Valor a formatear (entero, decimal o texto)

    Returns:
        Valor formateado como string
    """
    if isinstance(valor, float):
        return f"{valor:.2f}"
    return str(valor)


# =============================================================================
# FUNCIONES CON PARÁMETROS OPCIONALES
# =============================================================================

def crear_respuesta(
    data: dict[str, str | int | list],
    mensaje: str = "Operación exitosa",
    codigo: int = 200
) -> dict[str, str | int | dict]:
    """
    Crea una respuesta de API estandarizada.

    Args:
        data: Datos a incluir en la respuesta
        mensaje: Mensaje descriptivo (default: "Operación exitosa")
        codigo: Código HTTP (default: 200)

    Returns:
        Respuesta formateada como diccionario
    """
    return {
        "codigo": codigo,
        "mensaje": mensaje,
        "data": data
    }


# =============================================================================
# EJECUCIÓN DE EJEMPLOS
# =============================================================================

if __name__ == "__main__":
    # Buscar usuario existente
    usuario = buscar_usuario(1)
    print(f"Usuario encontrado: {usuario}")
    # Salida: Usuario encontrado: {'id': 1, 'nombre': 'Ana', ...}

    # Buscar usuario que no existe
    usuario_inexistente = buscar_usuario(999)
    print(f"Usuario no encontrado: {usuario_inexistente}")
    # Salida: Usuario no encontrado: None

    # Procesar diferentes tipos de ID
    print(f"ID entero: {procesar_id(123.23)}")
    print(f"ID string: {procesar_id('ABC-456')}")

    # Formatear diferentes tipos
    print(f"Formatear int: {formatear_valor(100)}")
    print(f"Formatear float: {formatear_valor(99.999)}")
    print(f"Formatear str: {formatear_valor('texto')}")

    # Crear respuesta de API
    respuesta = crear_respuesta(
        data={"id": 1, "nombre": "Ana"},
        mensaje="Usuario creado"
    )
    print(f"Respuesta API: {respuesta}")
