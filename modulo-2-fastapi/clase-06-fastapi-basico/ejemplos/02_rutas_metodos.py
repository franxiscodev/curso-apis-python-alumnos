"""
Ejemplo 02: Rutas y Métodos HTTP
================================
Diferentes métodos HTTP con FastAPI.

Ejecutar:
    uvicorn 02_rutas_metodos:app --reload
"""

from fastapi import FastAPI

app = FastAPI(title="Métodos HTTP")


# =============================================================================
# MÉTODOS HTTP
# =============================================================================


@app.get("/items")
def listar_items():
    """
    GET - Obtener recursos.

    Usado para leer/listar datos. No modifica nada.
    """
    return {"metodo": "GET", "accion": "Listar items"}


@app.post("/items")
def crear_item():
    """
    POST - Crear recurso.

    Usado para crear nuevos recursos.
    """
    return {"metodo": "POST", "accion": "Crear item"}


@app.put("/items/{item_id}")
def reemplazar_item(item_id: int):
    """
    PUT - Reemplazar recurso completo.

    Usado para actualizar TODO el recurso.
    """
    return {"metodo": "PUT", "accion": f"Reemplazar item {item_id}"}


@app.patch("/items/{item_id}")
def actualizar_item(item_id: int):
    """
    PATCH - Actualizar parcialmente.

    Usado para actualizar PARTE del recurso.
    """
    return {"metodo": "PATCH", "accion": f"Actualizar item {item_id}"}


@app.delete("/items/{item_id}")
def eliminar_item(item_id: int):
    """
    DELETE - Eliminar recurso.

    Usado para borrar recursos.
    """
    return {"metodo": "DELETE", "accion": f"Eliminar item {item_id}"}


# =============================================================================
# MÚLTIPLES RUTAS
# =============================================================================


# Una función puede manejar múltiples rutas
@app.get("/")
@app.get("/home")
@app.get("/inicio")
def pagina_principal():
    """Múltiples rutas apuntan a la misma función."""
    return {"mensaje": "Página principal"}


# =============================================================================
# RUTAS CON PREFIJOS
# =============================================================================


@app.get("/api/v1/usuarios")
def listar_usuarios_v1():
    """API versión 1."""
    return {"version": "v1", "usuarios": []}


@app.get("/api/v2/usuarios")
def listar_usuarios_v2():
    """API versión 2 con más datos."""
    return {"version": "v2", "usuarios": [], "total": 0}


# =============================================================================
# ORDEN DE RUTAS IMPORTA
# =============================================================================


# ⚠️ El orden importa cuando hay rutas similares
@app.get("/usuarios/me")  # Debe ir ANTES de /usuarios/{id}
def usuario_actual():
    """Retorna el usuario actual."""
    return {"usuario": "usuario_actual"}


@app.get("/usuarios/{usuario_id}")  # Esta ruta es más general
def obtener_usuario(usuario_id: int):
    """Retorna un usuario por ID."""
    return {"usuario_id": usuario_id}


# Si /usuarios/{usuario_id} estuviera primero,
# /usuarios/me intentaría convertir "me" a int → Error


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
