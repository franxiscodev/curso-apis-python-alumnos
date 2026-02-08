"""
Ejemplo 02: Unpacking y Forwarding
====================================
Desempaquetar colecciones en llamadas y el patron de forwarding.

Ejecutar:
    python 02_intermedio.py
"""

# =============================================================================
# SECCION 1: Unpacking con * en llamadas a funciones
# =============================================================================

print("=" * 60)
print("SECCION 1: Unpacking con *")
print("=" * 60)


def sumar(a, b, c):
    """Suma tres numeros."""
    return a + b + c


# Sin unpacking: pasar cada elemento manualmente
numeros = [10, 20, 30]
print(f"\nnumeros = {numeros}")
print(f"sumar(numeros[0], numeros[1], numeros[2]) = {sumar(numeros[0], numeros[1], numeros[2])}")

# Con unpacking: el * desempaqueta la lista
print(f"sumar(*numeros) = {sumar(*numeros)}")  # Equivale a sumar(10, 20, 30)

# Funciona con tuplas tambien
coordenadas = (1, 2, 3)
print(f"\ncoordenadas = {coordenadas}")
print(f"sumar(*coordenadas) = {sumar(*coordenadas)}")

# Funciona con cualquier iterable
print(f"sumar(*range(1, 4)) = {sumar(*range(1, 4))}")  # sumar(1, 2, 3)


# Uso practico: pasar datos de una lista a print
datos = ["Python", "es", "genial"]
print(f"\ndatos = {datos}")
print(*datos)           # Python es genial
print(*datos, sep="-")  # Python-es-genial


# =============================================================================
# SECCION 2: Unpacking con ** en llamadas + merge de diccionarios
# =============================================================================

print("\n" + "=" * 60)
print("SECCION 2: Unpacking con **")
print("=" * 60)


def crear_usuario(nombre, email, activo=True):
    """Crea un dict de usuario."""
    return {"nombre": nombre, "email": email, "activo": activo}


# Sin unpacking
datos = {"nombre": "Ana", "email": "ana@test.com", "activo": False}
print(f"\ndatos = {datos}")
print(f"Manual: {crear_usuario(nombre=datos['nombre'], email=datos['email'], activo=datos['activo'])}")

# Con unpacking: el ** desempaqueta el diccionario
print(f"Con **: {crear_usuario(**datos)}")  # Equivale a crear_usuario(nombre="Ana", email="ana@test.com", activo=False)

# Parcial: combinar unpacking con argumentos explicitos
base = {"nombre": "Carlos", "email": "carlos@test.com"}
print(f"\ncrear_usuario(**base) = {crear_usuario(**base)}")
print(f"crear_usuario(**base, activo=False) = {crear_usuario(**base, activo=False)}")


# Merge de diccionarios con **
print("\n--- Merge de diccionarios ---")
defaults = {"color": "azul", "tamaño": "mediano", "fuente": "sans-serif"}
personalizados = {"color": "rojo", "fuente": "Arial"}

config = {**defaults, **personalizados}
print(f"defaults = {defaults}")
print(f"personalizados = {personalizados}")
print(f"{{**defaults, **personalizados}} = {config}")
# El segundo diccionario sobreescribe claves duplicadas

# Merge de 3 diccionarios
sistema = {"version": "2.0"}
todo = {**defaults, **personalizados, **sistema}
print(f"\nMerge de 3: {todo}")


# =============================================================================
# SECCION 3: Forwarding de argumentos
# =============================================================================

print("\n" + "=" * 60)
print("SECCION 3: Forwarding de argumentos")
print("=" * 60)


def funcion_original(a, b, c=10, mensaje="hola"):
    """Funcion que queremos llamar a traves de un wrapper."""
    return f"a={a}, b={b}, c={c}, mensaje={mensaje}"


# Wrapper que pasa TODOS los argumentos a la funcion original
def wrapper(*args, **kwargs):
    """Recibe cualquier cosa y la pasa a funcion_original."""
    print(f"  wrapper recibio: args={args}, kwargs={kwargs}")
    resultado = funcion_original(*args, **kwargs)
    print(f"  funcion_original retorno: {resultado}")
    return resultado


print("\n--- Forwarding transparente ---")

print("\nwrapper(1, 2):")
wrapper(1, 2)

print("\nwrapper(1, 2, c=20):")
wrapper(1, 2, c=20)

print("\nwrapper(1, b=2, mensaje='chau'):")
wrapper(1, b=2, mensaje="chau")


# Wrapper que agrega logica antes y despues
def wrapper_con_logica(*args, **kwargs):
    """Agrega comportamiento sin modificar los argumentos."""
    print("  [ANTES] A punto de ejecutar funcion_original")
    resultado = funcion_original(*args, **kwargs)
    print(f"  [DESPUES] Resultado obtenido: {resultado}")
    return resultado


print("\n--- Wrapper con logica adicional ---")
print("\nwrapper_con_logica(5, 10, mensaje='test'):")
wrapper_con_logica(5, 10, mensaje="test")


# =============================================================================
# SECCION 4: Keyword-only arguments con *
# =============================================================================

print("\n" + "=" * 60)
print("SECCION 4: Keyword-only arguments")
print("=" * 60)


# El * solo (sin nombre) fuerza keyword-only
def conectar(host, puerto, *, timeout=30, ssl=True):
    """timeout y ssl SOLO se pueden pasar por nombre."""
    print(f"  Conectando a {host}:{puerto} (timeout={timeout}, ssl={ssl})")


print("\nconectar('localhost', 8080, timeout=60, ssl=False):")
conectar("localhost", 8080, timeout=60, ssl=False)

print("\nconectar('db.server.com', 5432):")
conectar("db.server.com", 5432)

# Esto daria error:
# conectar("localhost", 8080, 60, False)  # TypeError: takes 2 positional arguments


# Keyword-only sin valor por defecto (obligatorio por nombre)
def dividir(a, b, *, redondear):
    """redondear es obligatorio pero solo por nombre."""
    resultado = a / b
    if redondear:
        resultado = round(resultado, 2)
    return resultado


print(f"\ndividir(10, 3, redondear=True) = {dividir(10, 3, redondear=True)}")
print(f"dividir(10, 3, redondear=False) = {dividir(10, 3, redondear=False)}")


# Combinando *args con keyword-only (como hace print)
def mi_print(*valores, sep=" ", end="\n"):
    """Replica simplificada de print()."""
    texto = sep.join(str(v) for v in valores)
    print(f"  mi_print output: '{texto}'", end=end)


print("\nmi_print('hola', 'mundo'):")
mi_print("hola", "mundo")
print()

print("mi_print('a', 'b', 'c', sep='-'):")
mi_print("a", "b", "c", sep="-")
print()

print("\n" + "=" * 60)
print("Fin del ejemplo 02")
print("=" * 60)
