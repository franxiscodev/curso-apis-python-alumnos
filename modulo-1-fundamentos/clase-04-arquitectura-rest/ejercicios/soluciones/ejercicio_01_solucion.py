"""
Solución Ejercicio 01: Diseño de URIs para Sistema de Biblioteca
================================================================
"""


ENDPOINTS: dict[str, str] = {
    # --- LIBROS ---
    # Listar todos los libros
    "listar_libros": "/api/v1/libros",

    # Obtener un libro por ID
    "obtener_libro": "/api/v1/libros/{id}",

    # Crear un nuevo libro
    "crear_libro": "/api/v1/libros",

    # Actualizar libro completo
    "actualizar_libro_completo": "/api/v1/libros/{id}",

    # Actualizar libro parcialmente
    "actualizar_libro_parcial": "/api/v1/libros/{id}",

    # Eliminar libro
    "eliminar_libro": "/api/v1/libros/{id}",

    # Filtrar libros por categoría
    "libros_por_categoria": "/api/v1/libros?categoria={categoria}",

    # Buscar libros por título o autor
    "buscar_libros": "/api/v1/libros?q={termino}",

    # --- AUTORES ---
    # Listar autores
    "listar_autores": "/api/v1/autores",

    # Obtener autor
    "obtener_autor": "/api/v1/autores/{id}",

    # Listar libros de un autor específico (relación jerárquica)
    "libros_de_autor": "/api/v1/autores/{id}/libros",

    # --- PRÉSTAMOS ---
    # Listar todos los préstamos
    "listar_prestamos": "/api/v1/prestamos",

    # Obtener préstamo específico
    "obtener_prestamo": "/api/v1/prestamos/{id}",

    # Crear préstamo (usuario toma un libro)
    "crear_prestamo": "/api/v1/prestamos",

    # Devolver libro (actualizar préstamo)
    "devolver_libro": "/api/v1/prestamos/{id}",

    # Listar préstamos de un usuario (relación jerárquica)
    "prestamos_de_usuario": "/api/v1/usuarios/{id}/prestamos",

    # Listar préstamos activos (filtro)
    "prestamos_activos": "/api/v1/prestamos?estado=activo",

    # --- USUARIOS ---
    # Listar usuarios
    "listar_usuarios": "/api/v1/usuarios",

    # Historial de préstamos de un usuario
    "historial_usuario": "/api/v1/usuarios/{id}/prestamos?incluir_devueltos=true",

    # --- CATEGORÍAS ---
    # Listar categorías
    "listar_categorias": "/api/v1/categorias",

    # Libros en una categoría (dos opciones válidas)
    "libros_en_categoria": "/api/v1/categorias/{id}/libros",
}


METODOS: dict[str, str] = {
    "listar_libros": "GET",
    "obtener_libro": "GET",
    "crear_libro": "POST",
    "actualizar_libro_completo": "PUT",
    "actualizar_libro_parcial": "PATCH",
    "eliminar_libro": "DELETE",
    "crear_prestamo": "POST",
    "devolver_libro": "PATCH",  # Solo actualiza estado a "devuelto"
}


# =============================================================================
# EXPLICACIÓN DE DECISIONES DE DISEÑO
# =============================================================================

EXPLICACIONES = """
DECISIONES DE DISEÑO:

1. VERSIONADO:
   - Usamos /api/v1/ para permitir evolución sin romper clientes

2. SUSTANTIVOS PLURALES:
   - /libros (no /libro)
   - /autores (no /autor)
   - /prestamos (no /prestamo)

3. JERARQUÍA PARA RELACIONES:
   - /autores/{id}/libros → Libros de un autor específico
   - /usuarios/{id}/prestamos → Préstamos de un usuario
   - /categorias/{id}/libros → Libros en una categoría

4. FILTROS COMO QUERY PARAMS:
   - /libros?categoria=ficcion
   - /prestamos?estado=activo
   - /libros?q=cervantes (búsqueda)

5. DEVOLVER LIBRO:
   - Usamos PATCH /prestamos/{id} porque solo actualizamos el estado
   - NO creamos un endpoint /prestamos/{id}/devolver (verbo en URI)
   - El body sería: {"estado": "devuelto", "fecha_devolucion": "..."}

6. ALTERNATIVAS VÁLIDAS:
   - /libros?autor_id=5 (en vez de /autores/5/libros)
   - Ambas son válidas, depende de qué es más natural para tu API
"""


if __name__ == "__main__":
    print("=" * 60)
    print("Solución Ejercicio 01: URIs de Biblioteca")
    print("=" * 60)

    print("\n--- Endpoints Diseñados ---")
    for nombre, uri in ENDPOINTS.items():
        metodo = METODOS.get(nombre, "GET")
        print(f"  {metodo:6} {uri}")
        print(f"         → {nombre}")

    print("\n--- Métodos HTTP ---")
    for operacion, metodo in METODOS.items():
        print(f"  {metodo:6} → {operacion}")

    print(EXPLICACIONES)

    print("\n✓ Solución completada")
