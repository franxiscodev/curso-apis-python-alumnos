"""
Ejercicio 01: Diseño de URIs para Sistema de Biblioteca
=======================================================

Objetivo:
Diseñar las URIs RESTful para un sistema de gestión de biblioteca.

Recursos del sistema:
- Libros (con autor, ISBN, categoría)
- Autores
- Préstamos (un usuario toma prestado un libro)
- Usuarios (miembros de la biblioteca)
- Categorías

Requisitos:
1. Completa el diccionario ENDPOINTS con las URIs correctas
2. Sigue las convenciones REST:
   - Sustantivos plurales
   - Minúsculas
   - Kebab-case para palabras compuestas
   - Jerarquía para relaciones
   - Query params para filtros

NOTA: No hay código que ejecutar - este es un ejercicio de diseño.
"""


# =============================================================================
# TU CÓDIGO AQUÍ
# =============================================================================


# Completa las URIs para cada operación
ENDPOINTS: dict[str, str] = {
    # --- LIBROS ---
    # Listar todos los libros
    "listar_libros": "TODO",

    # Obtener un libro por ID
    "obtener_libro": "TODO",

    # Crear un nuevo libro
    "crear_libro": "TODO",

    # Actualizar libro completo
    "actualizar_libro_completo": "TODO",

    # Actualizar libro parcialmente
    "actualizar_libro_parcial": "TODO",

    # Eliminar libro
    "eliminar_libro": "TODO",

    # Filtrar libros por categoría
    "libros_por_categoria": "TODO",

    # Buscar libros por título o autor
    "buscar_libros": "TODO",

    # --- AUTORES ---
    # Listar autores
    "listar_autores": "TODO",

    # Obtener autor
    "obtener_autor": "TODO",

    # Listar libros de un autor específico
    "libros_de_autor": "TODO",

    # --- PRÉSTAMOS ---
    # Listar todos los préstamos
    "listar_prestamos": "TODO",

    # Obtener préstamo específico
    "obtener_prestamo": "TODO",

    # Crear préstamo (usuario toma un libro)
    "crear_prestamo": "TODO",

    # Devolver libro (actualizar préstamo)
    "devolver_libro": "TODO",

    # Listar préstamos de un usuario
    "prestamos_de_usuario": "TODO",

    # Listar préstamos activos (no devueltos)
    "prestamos_activos": "TODO",

    # --- USUARIOS ---
    # Listar usuarios
    "listar_usuarios": "TODO",

    # Historial de préstamos de un usuario
    "historial_usuario": "TODO",

    # --- CATEGORÍAS ---
    # Listar categorías
    "listar_categorias": "TODO",

    # Libros en una categoría
    "libros_en_categoria": "TODO",
}


# Indica el método HTTP para cada operación
METODOS: dict[str, str] = {
    "listar_libros": "TODO",
    "obtener_libro": "TODO",
    "crear_libro": "TODO",
    "actualizar_libro_completo": "TODO",
    "actualizar_libro_parcial": "TODO",
    "eliminar_libro": "TODO",
    "crear_prestamo": "TODO",
    "devolver_libro": "TODO",
}


# =============================================================================
# VERIFICACIÓN
# =============================================================================

def verificar_uri(uri: str) -> list[str]:
    """Verifica una URI y retorna problemas encontrados."""
    problemas = []

    if uri == "TODO":
        return ["No completada"]

    if not uri.startswith("/"):
        problemas.append("Debe empezar con /")

    if uri != uri.lower():
        problemas.append("Debe ser minúsculas")

    if "_" in uri.split("?")[0]:
        problemas.append("Usar kebab-case, no snake_case")

    verbos = ["obtener", "crear", "listar", "eliminar", "actualizar", "get", "post"]
    for verbo in verbos:
        if verbo in uri.lower():
            problemas.append(f"Evitar verbos en URI ('{verbo}')")

    return problemas


if __name__ == "__main__":
    print("=" * 60)
    print("Verificando Ejercicio 01: Diseño de URIs")
    print("=" * 60)

    total = 0
    correctas = 0

    print("\n--- Verificación de URIs ---")
    for nombre, uri in ENDPOINTS.items():
        total += 1
        problemas = verificar_uri(uri)

        if not problemas:
            print(f"  ✓ {nombre}: {uri}")
            correctas += 1
        else:
            print(f"  ✗ {nombre}: {uri}")
            for p in problemas:
                print(f"      → {p}")

    print(f"\n--- Resultado: {correctas}/{total} URIs correctas ---")

    print("\n--- Verificación de Métodos HTTP ---")
    metodos_validos = {"GET", "POST", "PUT", "PATCH", "DELETE"}
    for nombre, metodo in METODOS.items():
        if metodo in metodos_validos:
            print(f"  ✓ {nombre}: {metodo}")
        else:
            print(f"  ✗ {nombre}: {metodo} (debe ser GET/POST/PUT/PATCH/DELETE)")

    print("\n" + "=" * 60)
    print("Ejecuta la solución con:")
    print("  python ejercicios/soluciones/ejercicio_01_solucion.py")
