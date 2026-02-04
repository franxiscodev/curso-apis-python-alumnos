# Curso de APIs con Python y FastAPI

Material del curso de desarrollo de APIs con Python y FastAPI.

## Requisitos

- Python 3.11 o superior
- [uv](https://docs.astral.sh/uv/) (gestor de paquetes)

## Instalacion

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd curso-apis-python-alumnos

# Instalar dependencias con uv
uv sync
```

## Estructura del Curso

### Modulo 1 Fundamentos

- **clase-01-introduccion-typing**: Introduccion Typing
- **clase-02-decoradores**: Decoradores
- **clase-03-poo-apis**: Poo Apis
- **clase-04-arquitectura-rest**: Arquitectura Rest

### Modulo 2 Fastapi

- **clase-05-pydantic**: Pydantic
- **clase-06-fastapi-basico**: Fastapi Basico
- **clase-07-crud-completo**: Crud Completo
- **clase-08-sqlalchemy**: Sqlalchemy
- **clase-09-autenticacion**: Autenticacion
- **clase-extra-apirouter**: Apirouter

### Modulo 3 Integracion

- **clase-10-asincronia**: Asincronia
- **clase-11-websockets**: Websockets
- **clase-12-integraciones**: Integraciones

### Modulo 4 Produccion

- **clase-13-testing**: Testing
- **clase-14-contenedores**: Contenedores
- **clase-15-observabilidad**: Observabilidad

## Estructura de Cada Clase

Cada clase contiene:

- `ejemplos/` - Codigo de ejemplo explicado
- `ejercicios/` - Ejercicios para practicar
- `recursos/` - Slides y material de referencia

## Como Usar

1. Navega a la clase que quieras estudiar
2. Revisa los ejemplos en orden numerico
3. Intenta resolver los ejercicios
4. Consulta los recursos para referencia rapida

## Ejecucion de Ejemplos

```bash
# Activar entorno virtual
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Ejecutar un ejemplo
python modulo-1-fundamentos/clase-01-introduccion-typing/ejemplos/01_basico.py

# Para APIs FastAPI
uvicorn modulo-2-fastapi.clase-06-fastapi-basico.ejemplos.01_hola_mundo:app --reload
```
