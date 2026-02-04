---
marp: true
theme: default
paginate: true
header: 'Clase 04: Arquitectura REST'
footer: 'Curso APIs Python - Módulo 1'
---

# Clase 04
## Arquitectura REST y Diseño de APIs

---

# ¿Qué es REST?

**REST** = Representational State Transfer

- Estilo arquitectónico para sistemas distribuidos
- Definido por Roy Fielding (2000)
- NO es un protocolo ni una especificación
- ES una guía de diseño para APIs web

---

# Las 6 Restricciones REST

1. **Cliente-Servidor**: Separación de responsabilidades
2. **Sin Estado**: Cada request contiene toda la información
3. **Cacheable**: Responses pueden ser cacheadas
4. **Interfaz Uniforme**: URIs, métodos HTTP estándar
5. **Sistema en Capas**: Intermediarios transparentes
6. **Código Bajo Demanda**: (Opcional)

---

# Sin Estado (Stateless)

```python
# ❌ Con estado (servidor recuerda)
GET /siguiente-pagina

# ✅ Sin estado (toda info en request)
GET /productos?page=2&limit=10
```

Cada request es **independiente**.

---

# Recursos y URIs

Un **recurso** es cualquier cosa que pueda ser nombrada:
- Usuario, Producto, Pedido

```
/usuarios          → Colección
/usuarios/123      → Recurso individual
/usuarios/123/pedidos → Sub-recurso
```

---

# Convenciones de URIs

| Regla | Ejemplo | ¿Correcto? |
|-------|---------|------------|
| Sustantivos plurales | `/usuarios` | ✅ |
| Verbos | `/obtenerUsuarios` | ❌ |
| Minúsculas | `/usuarios` | ✅ |
| Kebab-case | `/tipos-producto` | ✅ |
| Snake_case | `/tipos_producto` | ⚠️ |

---

# URIs: Buenas Prácticas

```python
# ✅ BUENO
GET    /api/v1/usuarios
GET    /api/v1/usuarios/123
GET    /api/v1/usuarios/123/pedidos
DELETE /api/v1/usuarios/123

# ❌ MALO
GET    /api/v1/obtenerUsuario/123
POST   /api/v1/crearUsuario
DELETE /api/v1/borrarUsuario/123
```

---

# Métodos HTTP y CRUD

| CRUD | Método | URI | Descripción |
|------|--------|-----|-------------|
| Create | POST | /usuarios | Crear |
| Read | GET | /usuarios | Listar |
| Read | GET | /usuarios/123 | Obtener |
| Update | PUT | /usuarios/123 | Reemplazar |
| Update | PATCH | /usuarios/123 | Actualizar parcial |
| Delete | DELETE | /usuarios/123 | Eliminar |

---

# GET - Obtener

```http
GET /api/v1/productos HTTP/1.1
GET /api/v1/productos/123 HTTP/1.1
GET /api/v1/productos?categoria=laptops HTTP/1.1
```

- **Seguro**: No modifica datos
- **Idempotente**: Misma llamada = mismo resultado
- **Cacheable**

---

# POST - Crear

```http
POST /api/v1/productos HTTP/1.1
Content-Type: application/json

{
    "nombre": "Laptop",
    "precio": 999.99
}
```

- Retorna **201 Created**
- Header **Location**: `/productos/123`
- **NO idempotente**

---

# PUT vs PATCH

### PUT - Reemplaza TODO
```json
PUT /productos/123
{"nombre": "Laptop", "precio": 999, "descripcion": "..."}
```
Campos omitidos se pierden.

### PATCH - Actualiza PARCIAL
```json
PATCH /productos/123
{"precio": 899}
```
Solo modifica lo enviado.

---

# DELETE - Eliminar

```http
DELETE /api/v1/productos/123 HTTP/1.1
```

- Retorna **204 No Content**
- **Idempotente**: Eliminar algo ya eliminado = mismo estado

---

# Propiedades de Métodos

| Método | Seguro | Idempotente | Body Request |
|--------|--------|-------------|--------------|
| GET | ✅ | ✅ | No |
| POST | ❌ | ❌ | Sí |
| PUT | ❌ | ✅ | Sí |
| PATCH | ❌ | ✅ | Sí |
| DELETE | ❌ | ✅ | No |

---

# Códigos de Estado HTTP

| Rango | Categoría |
|-------|-----------|
| 2xx | Éxito |
| 3xx | Redirección |
| 4xx | Error del Cliente |
| 5xx | Error del Servidor |

---

# Códigos 2xx - Éxito

```python
200 OK           # GET exitoso
201 Created      # POST creó recurso
204 No Content   # DELETE exitoso
```

---

# Códigos 4xx - Error Cliente

```python
400 Bad Request          # JSON malformado
401 Unauthorized         # No autenticado
403 Forbidden            # Sin permisos
404 Not Found            # No existe
409 Conflict             # Email duplicado
422 Unprocessable Entity # Validación falló
```

---

# Guía de Selección

```
¿Éxito?
├── Sí → ¿Creó algo? → 201
│        ¿Hay contenido? → 200
│        ¿Sin contenido? → 204
│
└── No → ¿Cliente o Servidor?
         ├── No autenticado → 401
         ├── Sin permisos → 403
         ├── No encontrado → 404
         ├── Datos inválidos → 422
         └── Servidor → 500
```

---

# Response: Recurso Individual

```json
{
    "id": 123,
    "nombre": "Ana García",
    "email": "ana@ejemplo.com",
    "creado_en": "2024-01-15T10:30:00Z"
}
```

---

# Response: Colección Paginada

```json
{
    "data": [
        {"id": 1, "nombre": "Producto A"},
        {"id": 2, "nombre": "Producto B"}
    ],
    "meta": {
        "total": 150, "page": 1,
        "per_page": 10, "total_pages": 15
    },
    "links": {
        "self": "/productos?page=1",
        "next": "/productos?page=2"
    }
}
```

---

# Response: Error

```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Datos inválidos",
        "details": [
            {"field": "email", "message": "Formato inválido"}
        ]
    }
}
```

---

# Versionado de API

```python
# En la URI (recomendado)
GET /api/v1/usuarios
GET /api/v2/usuarios

# En header
Accept: application/vnd.api+json; version=2

# Query param
GET /api/usuarios?version=2
```

---

# Resumen

| Concepto | Clave |
|----------|-------|
| GET | Leer (seguro, idempotente) |
| POST | Crear (201 Created) |
| PUT | Reemplazar todo |
| PATCH | Actualizar parcial |
| DELETE | Eliminar (204) |
| 4xx | Error del cliente |
| 5xx | Error del servidor |

---

# Ejercicios

1. Diseñar URIs para sistema de biblioteca
2. Mapear operaciones a métodos HTTP
3. Diseñar respuestas y errores

---

# ¿Preguntas?

## Próxima clase:
**Pydantic y Validación de Datos**

---

# Tarea para Casa

1. Completar los 3 ejercicios
2. Analizar la API de GitHub: documentar 5 endpoints
3. (Opcional) Leer especificación OpenAPI 3.0
