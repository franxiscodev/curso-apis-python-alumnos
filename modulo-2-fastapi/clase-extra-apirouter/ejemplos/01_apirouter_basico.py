"""
APIRouter Basico
================
Introduccion a APIRouter: crear routers, registrar rutas y montarlos
en la aplicacion principal.

Ejecutar:
    uvicorn ejemplos.01_apirouter_basico:app --reload

Endpoints:
    GET  /                        - Raiz de la app
    GET  /productos               - Listar productos
    POST /productos               - Crear producto
    GET  /productos/{producto_id} - Obtener producto
    GET  /usuarios                - Listar usuarios
    POST /usuarios                - Crear usuario
    GET  /usuarios/{usuario_id}   - Obtener usuario
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.routing import APIRouter
from pydantic import BaseModel, Field


# =============================================================================
# MODELOS
# =============================================================================


class Producto(BaseModel):
    """Modelo basico de producto."""
    nombre: str = Field(min_length=1, max_length=100, examples=["Laptop Pro"])
    precio: float = Field(gt=0, examples=[999.99])
    categoria: str = Field(min_length=1, examples=["Electronica"])


class ProductoResponse(Producto):
    """Respuesta con ID."""
    id: int


class Usuario(BaseModel):
    """Modelo basico de usuario."""
    nombre: str = Field(min_length=1, max_length=100, examples=["Ana Garcia"])
    email: str = Field(min_length=5, examples=["ana@ejemplo.com"])


class UsuarioResponse(Usuario):
    """Respuesta con ID."""
    id: int


# =============================================================================
# ROUTER DE PRODUCTOS
# =============================================================================


router_productos = APIRouter()

productos_db: dict[int, dict] = {}
contador_productos = 0


@router_productos.get("/", response_model=list[ProductoResponse])
def listar_productos():
    """Lista todos los productos."""
    return list(productos_db.values())


@router_productos.post(
    "/",
    response_model=ProductoResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_producto(producto: Producto):
    """Crea un nuevo producto."""
    global contador_productos
    contador_productos += 1
    nuevo = {"id": contador_productos, **producto.model_dump()}
    productos_db[contador_productos] = nuevo
    return nuevo


@router_productos.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: int):
    """Obtiene un producto por ID."""
    if producto_id not in productos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto {producto_id} no encontrado"
        )
    return productos_db[producto_id]


# =============================================================================
# ROUTER DE USUARIOS
# =============================================================================


router_usuarios = APIRouter()

usuarios_db: dict[int, dict] = {}
contador_usuarios = 0


@router_usuarios.get("/", response_model=list[UsuarioResponse])
def listar_usuarios():
    """Lista todos los usuarios."""
    return list(usuarios_db.values())


@router_usuarios.post(
    "/",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_usuario(usuario: Usuario):
    """Crea un nuevo usuario."""
    global contador_usuarios
    contador_usuarios += 1
    nuevo = {"id": contador_usuarios, **usuario.model_dump()}
    usuarios_db[contador_usuarios] = nuevo
    return nuevo


@router_usuarios.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int):
    """Obtiene un usuario por ID."""
    if usuario_id not in usuarios_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario {usuario_id} no encontrado"
        )
    return usuarios_db[usuario_id]


# =============================================================================
# APLICACION PRINCIPAL
# =============================================================================


app = FastAPI(
    title="APIRouter Basico",
    description="Ejemplo introductorio de APIRouter con multiples routers",
    version="1.0.0"
)


# Montar routers con prefijo y tags
app.include_router(
    router_productos,
    prefix="/productos",
    tags=["Productos"]
)

app.include_router(
    router_usuarios,
    prefix="/usuarios",
    tags=["Usuarios"]
)


@app.get("/")
def raiz():
    """Informacion de la API."""
    return {
        "api": "APIRouter Basico",
        "version": "1.0.0",
        "routers": ["/productos", "/usuarios"],
        "documentacion": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
