"""
Ejercicio 03: API Completa con Auth y Roles
=============================================
API de tareas con autenticación, BD y roles.

OBJETIVO:
Integrar todos los conceptos: SQLAlchemy + Auth + Roles.

INSTRUCCIONES:
1. Modelos SQLAlchemy:
   - Usuario: id, username (unique), nombre, password_hash, rol (default "usuario")
   - Tarea: id, titulo, descripcion (nullable), completada (default False),
            usuario_id (ForeignKey)

2. Auth:
   - POST /auth/registro → Registrar usuario (hashear password)
   - POST /auth/login → Login, retornar JWT
   - GET /auth/me → Perfil del usuario actual

3. Tareas (protegidas):
   - GET /tareas → Listar solo las tareas del usuario actual
   - POST /tareas → Crear tarea asociada al usuario actual
   - PUT /tareas/{id} → Actualizar (solo si es del usuario)
   - DELETE /tareas/{id} → Eliminar (solo si es del usuario o admin)

4. Admin:
   - GET /admin/usuarios → Listar todos los usuarios (solo admin)
   - GET /admin/tareas → Listar todas las tareas (solo admin)

PRUEBAS:
    uvicorn ejercicio_03:app --reload

    # 1. Registrar usuario
    # 2. Login → obtener token
    # 3. Crear tareas
    # 4. Verificar que solo ve sus propias tareas

PISTAS:
- Tarea.usuario_id = usuario_actual.id
- Filtrar: select(Tarea).where(Tarea.usuario_id == usuario.id)
- Admin puede ver/eliminar todo, usuarios solo lo suyo
"""

from fastapi import FastAPI

app = FastAPI(title="Tareas Auth API", version="1.0.0")

# TODO: Imports (sqlalchemy, jose, passlib, pydantic, fastapi.security)

# TODO: Configuración (SECRET_KEY, engine, SessionLocal, pwd_context, oauth2_scheme)

# TODO: Modelos SQLAlchemy (Usuario, Tarea con ForeignKey)

# TODO: Crear tablas + usuario admin inicial

# TODO: Schemas Pydantic (UsuarioRegistro, UsuarioResponse, TareaCrear, TareaResponse, TokenResponse)

# TODO: get_db, crear_token, obtener_usuario_actual, requiere_admin

# TODO: POST /auth/registro

# TODO: POST /auth/login

# TODO: GET /auth/me

# TODO: GET /tareas (solo del usuario actual)

# TODO: POST /tareas (asociar al usuario actual)

# TODO: PUT /tareas/{id} (solo si es del usuario)

# TODO: DELETE /tareas/{id} (usuario dueño o admin)

# TODO: GET /admin/usuarios (solo admin)

# TODO: GET /admin/tareas (solo admin)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
