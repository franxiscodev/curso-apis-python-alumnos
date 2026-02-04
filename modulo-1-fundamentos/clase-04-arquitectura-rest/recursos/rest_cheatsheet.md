---
marp: true
theme: default
paginate: true
header: 'REST API Cheatsheet'
footer: 'Curso APIs Python - Módulo 1'
---

# REST API Cheatsheet
---
## Métodos HTTP

| Método | CRUD | Idempotente | Seguro | Body Request | Status Éxito |
|--------|------|-------------|--------|--------------|--------------|
| GET | Read | ✅ | ✅ | ❌ | 200 |
| POST | Create | ❌ | ❌ | ✅ | 201 |
| PUT | Update (full) | ✅ | ❌ | ✅ | 200 |
| PATCH | Update (partial) | ✅ | ❌ | ✅ | 200 |
| DELETE | Delete | ✅ | ❌ | ❌ | 204 |
---
## Códigos de Estado Comunes

### 2xx - Éxito
| Código | Nombre | Uso |
|--------|--------|-----|
| 200 | OK | GET exitoso |
| 201 | Created | POST creó recurso |
| 204 | No Content | DELETE exitoso |
---
### 4xx - Error Cliente
| Código | Nombre | Uso |
|--------|--------|-----|
| 400 | Bad Request | JSON malformado |
| 401 | Unauthorized | Sin autenticación |
| 403 | Forbidden | Sin permisos |
| 404 | Not Found | Recurso no existe |
| 409 | Conflict | Duplicado (ej: email) |
| 422 | Unprocessable Entity | Validación falló |
| 429 | Too Many Requests | Rate limit |
---
### 5xx - Error Servidor
| Código | Nombre | Uso |
|--------|--------|-----|
| 500 | Internal Server Error | Error genérico |
| 502 | Bad Gateway | Servicio upstream caído |
| 503 | Service Unavailable | Mantenimiento |
---
## Diseño de URIs

### ✅ Correcto
```
GET    /api/v1/usuarios
GET    /api/v1/usuarios/123
POST   /api/v1/usuarios
PUT    /api/v1/usuarios/123
PATCH  /api/v1/usuarios/123
DELETE /api/v1/usuarios/123

# Relaciones
GET    /api/v1/usuarios/123/pedidos
POST   /api/v1/usuarios/123/pedidos

# Filtros
GET    /api/v1/productos?categoria=laptops
GET    /api/v1/productos?precio_min=100&precio_max=500
GET    /api/v1/productos?page=2&per_page=20
```
---
### ❌ Incorrecto
```
GET    /api/v1/obtenerUsuarios      # Verbo en URI
POST   /api/v1/crearUsuario         # Verbo en URI
DELETE /api/v1/borrarUsuario/123    # Verbo en URI
GET    /api/v1/usuario              # Singular
```
---
## Estructura de Respuestas

### Recurso Individual
```json
{
    "id": 1,
    "nombre": "Ana García",
    "email": "ana@ejemplo.com"
}
```
---
### Colección con Paginación
```json
{
    "data": [...],
    "meta": {
        "total": 100,
        "page": 1,
        "per_page": 10,
        "total_pages": 10
    },
    "links": {
        "self": "/productos?page=1",
        "next": "/productos?page=2",
        "last": "/productos?page=10"
    }
}
```
---
### Error
```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Descripción del error",
        "details": [
            {"field": "email", "message": "Formato inválido"}
        ]
    }
}
```
---
## Headers Comunes

### Request
```
Content-Type: application/json
Accept: application/json
Authorization: Bearer <token>
```

### Response
```
Content-Type: application/json
Location: /productos/123  (después de POST)
Cache-Control: max-age=3600
```
---
## Reglas de Oro

1. **URIs = Sustantivos**: `/usuarios`, no `/obtenerUsuarios`
2. **Plurales**: `/productos`, no `/producto`
3. **Minúsculas + kebab-case**: `/tipos-producto`
4. **Jerarquía para relaciones**: `/usuarios/123/pedidos`
5. **Filtros como query params**: `?categoria=x&precio=100`
6. **Versionado en URI**: `/api/v1/...`
7. **Sin estado**: Cada request es independiente

