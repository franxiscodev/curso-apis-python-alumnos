"""
Ejercicio 02: Refactorizar API de Contactos
============================================
Tienen una API monolitica de contactos con CRUD y utilidades.
Refactoricenla usando APIRouter y agreguen una dependencia compartida.

OBJETIVO:
Practicar la separacion en routers y el uso de dependencias a nivel de router.

INSTRUCCIONES:
1. Crear `router_contactos` con prefix="/contactos", tags=["Contactos"]
   - Agregar dependencia compartida `log_peticion` a nivel de router
2. Crear `router_utilidades` con prefix="/utilidades", tags=["Utilidades"]
3. Mover endpoints CRUD al router de contactos (rutas relativas)
4. Mover el endpoint de estadisticas al router de utilidades
5. Montar ambos routers en la app
6. Verificar que cada peticion a /contactos imprime el log en consola

PRUEBAS:
    uvicorn ejercicio_02:app --reload

    # Probar con curl o navegador:
    POST http://localhost:8000/contactos  (body: {"nombre": "Ana", "email": "ana@test.com"})
    GET  http://localhost:8000/contactos
    GET  http://localhost:8000/utilidades/estadisticas

PISTAS:
- Dependencia a nivel de router: APIRouter(dependencies=[Depends(log_peticion)])
- La dependencia se ejecuta en CADA endpoint del router automaticamente
- from fastapi import Depends
"""

from fastapi import FastAPI, HTTPException, APIRouter, Depends, status
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="Contactos API")

# --- Base de datos en memoria (no modificar) ---
contactos_db = {}
contador = 0


# --- Modelos (no modificar) ---
class ContactoCrear(BaseModel):
    nombre: str = Field(min_length=1)
    email: EmailStr
    telefono: str | None = None


class ContactoResponse(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: str | None = None


# =============================================================================
# TODO: Crear la dependencia log_peticion
# Debe imprimir: ">> Peticion recibida en router de contactos"
# =============================================================================

# def log_peticion():
#     print(">> Peticion recibida en router de contactos")


# =============================================================================
# TODO: Crear router_contactos con prefix, tags y dependencia compartida
# =============================================================================

# router_contactos = APIRouter(
#     prefix="/contactos",
#     tags=["Contactos"],
#     dependencies=[Depends(log_peticion)],
# )


# =============================================================================
# TODO: Crear router_utilidades con prefix y tags
# =============================================================================

# router_utilidades = APIRouter(...)


# =============================================================================
# ENDPOINTS CRUD DE CONTACTOS
# TODO: Cambiar @app por @router_contactos y ajustar rutas a relativas
# =============================================================================

@app.get("/contactos", response_model=list[ContactoResponse])
def listar_contactos():
    return list(contactos_db.values())


@app.post("/contactos", response_model=ContactoResponse, status_code=status.HTTP_201_CREATED)
def crear_contacto(contacto: ContactoCrear):
    global contador
    contador += 1
    nuevo = {"id": contador, **contacto.model_dump()}
    contactos_db[contador] = nuevo
    return nuevo


@app.get("/contactos/{contacto_id}", response_model=ContactoResponse)
def obtener_contacto(contacto_id: int):
    if contacto_id not in contactos_db:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    return contactos_db[contacto_id]


@app.put("/contactos/{contacto_id}", response_model=ContactoResponse)
def actualizar_contacto(contacto_id: int, contacto: ContactoCrear):
    if contacto_id not in contactos_db:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    actualizado = {"id": contacto_id, **contacto.model_dump()}
    contactos_db[contacto_id] = actualizado
    return actualizado


@app.delete("/contactos/{contacto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_contacto(contacto_id: int):
    if contacto_id not in contactos_db:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    del contactos_db[contacto_id]


# =============================================================================
# ENDPOINT DE UTILIDADES
# TODO: Cambiar @app por @router_utilidades y ajustar ruta a relativa
# =============================================================================

@app.get("/utilidades/estadisticas")
def estadisticas():
    return {
        "total_contactos": len(contactos_db),
        "contactos_con_telefono": sum(
            1 for c in contactos_db.values() if c.get("telefono")
        ),
    }


# =============================================================================
# TODO: Montar los routers en la app
# app.include_router(router_contactos)
# app.include_router(router_utilidades)
# =============================================================================


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
