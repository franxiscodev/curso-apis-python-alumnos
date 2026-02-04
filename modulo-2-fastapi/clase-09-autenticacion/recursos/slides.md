---
marp: true
theme: default
paginate: true
header: 'Clase 09: Autenticación y Seguridad'
footer: 'Curso APIs Avanzadas con Python'
---

# Autenticación y Seguridad
## JWT, OAuth2 y Roles

Clase 09 - Módulo 2: FastAPI

---

# Autenticación vs Autorización

| Concepto | Pregunta | Ejemplo |
|----------|----------|---------|
| **Autenticación** | ¿Quién eres? | Login |
| **Autorización** | ¿Qué puedes hacer? | Roles |

---

# El Flujo Completo

```
1. POST /login (username + password)
       ↓
2. Servidor verifica → genera JWT
       ↓
3. Cliente envía: Authorization: Bearer <token>
       ↓
4. Servidor decodifica → identifica usuario
```

---

# Hashing de Contraseñas

**Regla #1**: Nunca guardar en texto plano

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

# Hashear
hash = pwd_context.hash("mi_password")
# → "$2b$12$LJ3m4ys..."

# Verificar
pwd_context.verify("mi_password", hash)  # True
pwd_context.verify("otra", hash)         # False
```

---

# ¿Por qué bcrypt?

- **Lento a propósito** → dificulta fuerza bruta
- **Salt automático** → mismo password ≠ mismo hash
- **Irreversible** → no se puede obtener el password

---

# JWT: JSON Web Tokens

```
eyJhbGciOiJI...  .  eyJzdWIiOiJ1...  .  SflKxwRJSM...
|-- Header --|     |-- Payload --|     |--- Firma ---|
```

| Parte | Contenido |
|-------|-----------|
| Header | Algoritmo (HS256) |
| Payload | sub, exp, datos |
| Firma | Verificación con SECRET_KEY |

---

# Crear y Verificar JWT

```python
from jose import jwt

SECRET_KEY = "mi-clave-secreta"

# Crear
token = jwt.encode(
    {"sub": "usuario1", "exp": datetime.utcnow() + timedelta(hours=1)},
    SECRET_KEY, algorithm="HS256"
)

# Verificar
payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
# → {"sub": "usuario1", "exp": ...}
```

---

# OAuth2 en FastAPI

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@app.get("/protegido")
def ruta(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, ...)
    return {"usuario": payload["sub"]}
```

Swagger UI agrega botón **Authorize**

---

# Dependency: obtener_usuario_actual

```python
def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme)
) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, ...)
        username = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401)

    usuario = buscar_usuario(username)
    if not usuario:
        raise HTTPException(status_code=401)
    return usuario
```

---

# Login Endpoint

```python
from fastapi.security import OAuth2PasswordRequestForm

@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    usuario = autenticar(form.username, form.password)
    if not usuario:
        raise HTTPException(status_code=401)

    token = jwt.encode(
        {"sub": usuario.username, "exp": ...},
        SECRET_KEY
    )
    return {"access_token": token, "token_type": "bearer"}
```

---

# Proteger Endpoints

```python
# Cualquier usuario autenticado
@app.get("/datos")
def ver(usuario = Depends(obtener_usuario_actual)):
    return {"usuario": usuario.username}

# Solo admin
@app.delete("/usuarios/{id}")
def borrar(id: int, admin = Depends(requiere_admin)):
    ...
```

---

# Roles: Factory de Dependencies

```python
def requiere_rol(*roles):
    def verificar(
        usuario = Depends(obtener_usuario_actual)
    ):
        if usuario.rol not in roles:
            raise HTTPException(
                status_code=403,
                detail="Sin permisos"
            )
        return usuario
    return verificar

# Uso
@app.post("/articulos")
def crear(user = Depends(requiere_rol("admin", "editor"))):
    ...
```

---

# 401 vs 403

| Código | Significado | Cuándo |
|--------|-------------|--------|
| **401** | No autenticado | Token falta o inválido |
| **403** | No autorizado | Token válido pero sin permisos |

---

# Resumen

| Concepto | Herramienta |
|----------|-------------|
| Hashing | `passlib` + bcrypt |
| Tokens | `python-jose` (JWT) |
| Extraer token | `OAuth2PasswordBearer` |
| Login form | `OAuth2PasswordRequestForm` |
| Proteger | `Depends(obtener_usuario)` |
| Roles | `Depends(requiere_rol(...))` |

---

# Próximo Módulo

**Módulo 3: Integración y Asincronía**

- Programación asíncrona
- WebSockets y real-time
- Integraciones externas

---

# Recursos

- **FastAPI Security**: https://fastapi.tiangolo.com/tutorial/security/
- **JWT.io**: https://jwt.io
- **OWASP**: https://cheatsheetseries.owasp.org

**Practica:**
```bash
uvicorn ejemplos.api_auth_completa:app --reload
```
