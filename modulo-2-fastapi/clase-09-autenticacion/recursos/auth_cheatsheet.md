# Autenticación y Seguridad - Cheatsheet

Guía rápida de autenticación JWT con FastAPI.

---

## Hashing de Contraseñas

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hashear
hash = pwd_context.hash("contraseña")

# Verificar
pwd_context.verify("contraseña", hash)  # True/False
```

---

## Tokens JWT

```python
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

SECRET_KEY = "mi-clave-secreta"
ALGORITHM = "HS256"

# Crear token
def crear_token(datos: dict, expira: timedelta = timedelta(minutes=30)) -> str:
    payload = {**datos, "exp": datetime.now(timezone.utc) + expira}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Decodificar token
def decodificar_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
```

---

## OAuth2 en FastAPI

```python
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Esquema OAuth2 (extrae token del header)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Dependency: usuario actual
def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    usuario = buscar_usuario(username)
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return usuario
```

---

## Endpoint de Login

```python
@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = autenticar(form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"}
        )
    token = crear_token({"sub": usuario.username})
    return {"access_token": token, "token_type": "bearer"}
```

---

## Proteger Endpoints

```python
# Requiere autenticación
@app.get("/protegido")
def ruta(usuario = Depends(obtener_usuario_actual)):
    return {"usuario": usuario.username}

# Requiere rol específico
def requiere_rol(*roles):
    def verificar(usuario = Depends(obtener_usuario_actual)):
        if usuario.rol not in roles:
            raise HTTPException(status_code=403, detail="Sin permisos")
        return usuario
    return verificar

@app.delete("/item/{id}")
def borrar(id: int, admin = Depends(requiere_rol("admin"))):
    ...
```

---

## Registro con BD

```python
@app.post("/auth/registro", status_code=201)
def registrar(datos: UsuarioRegistro, db: Session = Depends(get_db)):
    # Verificar único
    if db.execute(select(Usuario).where(Usuario.username == datos.username)).scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Ya existe")
    # Crear con password hasheada
    nuevo = Usuario(
        username=datos.username,
        password_hash=pwd_context.hash(datos.password)
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
```

---

## Pydantic con from_attributes

```python
class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    nombre: str
    rol: str
    # Sin password_hash (nunca exponer)
```

---

## Status Codes de Auth

| Código | Significado | Cuándo |
|--------|-------------|--------|
| 200 | Login exitoso | Token retornado |
| 201 | Registro exitoso | Usuario creado |
| 401 | No autenticado | Token falta/inválido/expirado |
| 403 | No autorizado | Token válido, sin permisos |
| 409 | Conflicto | Username/email duplicado |

---

## Dependencias Necesarias

```bash
uv add python-jose[cryptography] passlib[bcrypt] python-multipart
```

- **python-jose**: Crear/verificar JWT
- **passlib[bcrypt]**: Hashing de contraseñas
- **python-multipart**: Requerido por OAuth2PasswordRequestForm

---

## Tips

1. **SECRET_KEY** en variable de entorno, nunca en código
2. **Expiración** siempre en los tokens (30 min es un buen default)
3. **Nunca** retornar password_hash en responses
4. **401** = "no sé quién eres", **403** = "sé quién eres pero no puedes"
5. **bcrypt** es lento a propósito: seguridad > velocidad
6. **OAuth2PasswordBearer** habilita el botón Authorize en Swagger
