"""
Ejemplo 01: *args, **kwargs y Combinaciones
============================================
Conceptos basicos de argumentos variables en Python.

Ejecutar:
    python 01_basico.py
"""

# =============================================================================
# SECCION 1: *args - Argumentos posicionales variables
# =============================================================================

print("=" * 60)
print("SECCION 1: *args")
print("=" * 60)


def sumar_todo(*numeros):
    """Suma un numero variable de argumentos."""
    print(f"  Tipo de numeros: {type(numeros)}")
    print(f"  Valor de numeros: {numeros}")
    return sum(numeros)


# Llamar con diferente cantidad de argumentos
print("\nsumar_todo(1, 2, 3):")
resultado = sumar_todo()
print(f"  Resultado: {resultado}")  # 6

print("\nsumar_todo(10, 20):")
resultado = sumar_todo(10, 20)
print(f"  Resultado: {resultado}")  # 30

print("\nsumar_todo():")
resultado = sumar_todo()
print(f"  Resultado: {resultado}")  # 0


# Combinando parametros normales con *args
def saludar(saludo, *nombres):
    """El primer argumento es el saludo, el resto son nombres."""
    print(f"\n  saludo = {saludo!r}")
    print(f"  nombres = {nombres}")
    for nombre in nombres:
        print(f"  {saludo}, {nombre}!")


print("\nsaludar('Hola', 'Ana', 'Carlos', 'Luis'):")
saludar("Hola", "Ana", "Carlos", "Luis")


# Iterar y operar sobre *args
def estadisticas(*valores):
    """Calcula estadisticas basicas de N numeros."""
    if not valores:
        return {"error": "No se proporcionaron valores"}
    return {
        "cantidad": len(valores),
        "suma": sum(valores),
        "promedio": sum(valores) / len(valores),
        "minimo": min(valores),
        "maximo": max(valores),
    }


print("\nestadisticas(10, 20, 30, 40, 50):")
stats = estadisticas(10, 20, 30, 40, 50)
for clave, valor in stats.items():
    print(f"  {clave}: {valor}")


# =============================================================================
# SECCION 2: **kwargs - Argumentos de palabra clave variables
# =============================================================================

print("\n" + "=" * 60)
print("SECCION 2: **kwargs")
print("=" * 60)


def crear_perfil(**datos):
    """Crea un perfil con los datos proporcionados."""
    print(f"  Tipo de datos: {type(datos)}")
    print(f"  Valor de datos: {datos}")
    return datos


print("\ncrear_perfil(nombre='Ana', edad=30, ciudad='Madrid'):")
perfil = crear_perfil(nombre="Ana", edad=30, ciudad="Madrid")
print(f"  Perfil: {perfil}")


# Combinando parametros normales con **kwargs
def crear_usuario(nombre, email, **extras):
    """El nombre y email son obligatorios, el resto es opcional."""
    usuario = {"nombre": nombre, "email": email}
    usuario.update(extras)
    return usuario


print("\ncrear_usuario('Carlos', 'carlos@test.com', rol='admin', activo=True):")
usuario = crear_usuario("Carlos", "carlos@test.com", rol="admin", activo=True)
print(f"  Usuario: {usuario}")

print("\ncrear_usuario('Ana', 'ana@test.com'):")
usuario = crear_usuario("Ana", "ana@test.com")
print(f"  Usuario: {usuario}")


# Recorrer kwargs
def mostrar_config(**opciones):
    """Muestra todas las opciones recibidas."""
    print("  Configuracion:")
    for clave, valor in opciones.items():
        print(f"    {clave} = {valor!r}")


print("\nmostrar_config(tema='oscuro', idioma='es', notificaciones=True):")
mostrar_config(tema="oscuro", idioma="es", notificaciones=True)


# =============================================================================
# SECCION 3: Combinando parametros normales, *args y **kwargs
# =============================================================================

print("\n" + "=" * 60)
print("SECCION 3: Combinando todo")
print("=" * 60)


def funcion_completa(a, b, *args, **kwargs):
    """Combina parametros normales, *args y **kwargs."""
    print(f"  a = {a}")
    print(f"  b = {b}")
    print(f"  args = {args}")
    print(f"  kwargs = {kwargs}")


print("\nfuncion_completa(1, 2, 3, 4, 5, x=10, y=20):")
funcion_completa(1, 2, 3, 4, 5, x=10, y=20)
# a=1, b=2, args=(3, 4, 5), kwargs={"x": 10, "y": 20}

print("\nfuncion_completa(1, 2):")
funcion_completa(1, 2)
# a=1, b=2, args=(), kwargs={}


# Orden obligatorio: (normales, *args, keyword-only, **kwargs)
def orden_completo(a, b, *args, obligatorio, **kwargs):
    """Demuestra el orden completo de parametros."""
    print(f"  a = {a}")
    print(f"  b = {b}")
    print(f"  args = {args}")
    print(f"  obligatorio = {obligatorio}")
    print(f"  kwargs = {kwargs}")


print("\norden_completo(1, 2, 3, 4, obligatorio='si', extra='dato'):")
orden_completo(1, 2, 3, 4, obligatorio="si", extra="dato")


# =============================================================================
# SECCION 4: El nombre es convencion, el operador es lo importante
# =============================================================================

print("\n" + "=" * 60)
print("SECCION 4: El nombre es convencion")
print("=" * 60)


# Funciona igual con cualquier nombre
def con_otros_nombres(*elementos, **opciones):
    """Misma funcionalidad, nombres diferentes."""
    print(f"  elementos: {elementos}")
    print(f"  opciones: {opciones}")


print("\ncon_otros_nombres(1, 2, 3, color='rojo', tamaño='grande'):")
con_otros_nombres(1, 2, 3, color="rojo", tamaño="grande")


# Incluso nombres mas descriptivos
def registrar_venta(vendedor, *productos, **detalles):
    """Nombres descriptivos mejoran la legibilidad."""
    print(f"  Vendedor: {vendedor}")
    print(f"  Productos: {productos}")
    print(f"  Detalles: {detalles}")


print("\nregistrar_venta('Ana', 'laptop', 'mouse', descuento=10, envio='express'):")
registrar_venta("Ana", "laptop", "mouse", descuento=10, envio="express")

print("\n" + "=" * 60)
print("Fin del ejemplo 01")
print("=" * 60)
