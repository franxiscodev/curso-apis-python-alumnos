"""
Ejemplo 03: Decoradores, Herencia y APIs Flexibles
====================================================
Casos reales donde *args y **kwargs son esenciales.

NOTA: Este archivo es un PREVIEW de conceptos de clase-02 (decoradores)
y clase-03 (herencia). No se preocupen si algo parece nuevo; el objetivo
es ver DONDE aparecen *args y **kwargs en el mundo real.

Ejecutar:
    python 03_avanzado.py
"""

import time
from functools import wraps

# =============================================================================
# SECCION 1: Patron wrapper en decoradores (preview de clase-02)
# =============================================================================

print("=" * 60)
print("SECCION 1: Patron wrapper en decoradores")
print("=" * 60)

# Un decorador es una funcion que envuelve a otra funcion.
# No necesitan entender TODO ahora. Fijense en *args y **kwargs.


def medir_tiempo(func):
    """Decorador que mide cuanto tarda una funcion."""
    @wraps(func)  # Preserva el nombre/doc de la funcion original
    def wrapper(*args, **kwargs):          # ← Acepta CUALQUIER argumento
        inicio = time.time()
        resultado = func(*args, **kwargs)  # ← Los pasa INTACTOS
        total = time.time() - inicio
        print(f"  {func.__name__} tardo {total:.4f}s")
        return resultado
    return wrapper


@medir_tiempo  # Aplica el decorador
def calcular_suma(n):
    """Suma los numeros del 1 al n."""
    return sum(range(1, n + 1))


@medir_tiempo
def buscar_maximo(*numeros, verbose=False):
    """Encuentra el maximo de N numeros."""
    resultado = max(numeros)
    if verbose:
        print(f"  Buscando en {len(numeros)} numeros...")
    return resultado


print("\ncalcular_suma(1_000_000):")
print(f"  Resultado: {calcular_suma(1_000_000)}")

print("\nbuscar_maximo(3, 1, 4, 1, 5, 9, 2, 6, verbose=True):")
print(f"  Resultado: {buscar_maximo(3, 1, 4, 1, 5, 9, 2, 6, verbose=True)}")

# Lo importante: el wrapper funciona con CUALQUIER funcion gracias a *args/**kwargs
# calcular_suma tiene 1 parametro, buscar_maximo tiene *args y un keyword
# El mismo wrapper sirve para ambas!


# =============================================================================
# SECCION 2: super().__init__() con forwarding (preview de clase-03)
# =============================================================================

print("\n" + "=" * 60)
print("SECCION 2: Herencia con forwarding")
print("=" * 60)


class Animal:
    """Clase base."""
    def __init__(self, nombre, especie, edad=0):
        self.nombre = nombre
        self.especie = especie
        self.edad = edad

    def __repr__(self):
        return f"{self.__class__.__name__}(nombre={self.nombre!r}, especie={self.especie!r}, edad={self.edad})"


class Perro(Animal):
    """Clase hija que agrega atributos y forwardea el resto al padre."""
    def __init__(self, raza, *args, **kwargs):
        super().__init__(*args, **kwargs)  # ← Forwarding al padre
        self.raza = raza

    def __repr__(self):
        return f"Perro(raza={self.raza!r}, nombre={self.nombre!r}, especie={self.especie!r})"


# Perro recibe su propio parametro (raza) y pasa el resto a Animal
rex = Perro("Labrador", "Rex", "Canino", edad=5)
print(f"\nrex = {rex}")
print(f"  raza: {rex.raza}")
print(f"  nombre: {rex.nombre}")
print(f"  especie: {rex.especie}")
print(f"  edad: {rex.edad}")


class Cachorro(Perro):
    """Doble herencia: Cachorro → Perro → Animal."""
    def __init__(self, vacunado=False, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Forwardea a Perro → Animal
        self.vacunado = vacunado

    def __repr__(self):
        return f"Cachorro(raza={self.raza!r}, nombre={self.nombre!r}, vacunado={self.vacunado})"


luna = Cachorro(True, "Golden", "Luna", "Canino", edad=1)
print(f"\nluna = {luna}")
print(f"  vacunado: {luna.vacunado}, raza: {luna.raza}, nombre: {luna.nombre}")


# =============================================================================
# SECCION 3: Funciones de configuracion flexible
# =============================================================================

print("\n" + "=" * 60)
print("SECCION 3: Configuracion flexible")
print("=" * 60)


def crear_conexion(host, puerto, **opciones):
    """Crea una configuracion de conexion con valores por defecto."""
    config = {
        "host": host,
        "puerto": puerto,
        "timeout": 30,
        "retries": 3,
        "ssl": True,
        "pool_size": 5,
    }
    config.update(opciones)  # Sobreescribir con las opciones del usuario
    return config


print("\nConexion con defaults:")
conn1 = crear_conexion("localhost", 5432)
for k, v in conn1.items():
    print(f"  {k}: {v}")

print("\nConexion personalizada:")
conn2 = crear_conexion("db.prod.com", 5432, timeout=60, ssl=False, pool_size=20)
for k, v in conn2.items():
    print(f"  {k}: {v}")


# Patron: combinar multiples fuentes de configuracion
def configurar_app(**overrides):
    """Combina config por defecto, de entorno y del usuario."""
    defaults = {"debug": False, "log_level": "INFO", "workers": 4}
    entorno = {"log_level": "WARNING"}  # Simulando variables de entorno

    # Merge con prioridad: defaults < entorno < overrides del usuario
    config = {**defaults, **entorno, **overrides}
    return config


print("\nconfigurar_app(debug=True, workers=8):")
config = configurar_app(debug=True, workers=8)
for k, v in config.items():
    print(f"  {k}: {v}")


# =============================================================================
# SECCION 4: Factory functions y APIs flexibles
# =============================================================================

print("\n" + "=" * 60)
print("SECCION 4: Factory functions")
print("=" * 60)


# Factory function: crea funciones configuradas
def crear_formateador(prefijo="", sufijo="", **estilos):
    """Crea una funcion de formato personalizada."""
    def formatear(texto):
        resultado = f"{prefijo}{texto}{sufijo}"
        if estilos.get("mayusculas"):
            resultado = resultado.upper()
        if estilos.get("centrar"):
            resultado = resultado.center(estilos.get("ancho", 40))
        return resultado
    return formatear


# Crear diferentes formateadores
titulo = crear_formateador(prefijo="=== ", sufijo=" ===", mayusculas=True)
subtitulo = crear_formateador(prefijo="--- ", sufijo=" ---")
centrado = crear_formateador(centrar=True, ancho=50)

print(f"\ntitulo('hola mundo'): {titulo('hola mundo')}")
print(f"subtitulo('seccion'): {subtitulo('seccion')}")
print(f"centrado('texto'): '{centrado('texto')}'")


# Funcion que acepta y forwardea a otra API
def ejecutar_consulta(consulta, *parametros, **opciones):
    """Simula ejecutar una consulta con parametros variables."""
    print(f"\n  Consulta: {consulta}")
    if parametros:
        print(f"  Parametros posicionales: {parametros}")
    if opciones:
        print(f"  Opciones: {opciones}")
    return {"consulta": consulta, "filas": 42}


print("\nejecutar_consulta('SELECT * FROM usuarios', 'activo', limit=10, offset=0):")
resultado = ejecutar_consulta("SELECT * FROM usuarios", "activo", limit=10, offset=0)
print(f"  Resultado: {resultado}")

print("\n" + "=" * 60)
print("Fin del ejemplo 03")
print("=" * 60)
