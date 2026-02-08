"""
Solucion Ejercicio 02: Refactorizar API de Contactos
=====================================================
API de contactos refactorizada con routers y dependencia compartida.

Ejecutar:
    uvicorn ejercicio_02_solucion:app --reload
"""

from fastapi import FastAPI, HTTPException, APIRouter, Depends, status
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="Contactos API")

# --- Base de datos en memoria ---
contactos_db = {}
contador = 0


# --- Modelos ---
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
# Dependencia compartida
# =============================================================================

def log_peticion():
    print(">> Peticion recibida en router de contactos")


# =============================================================================
# Router de Contactos (con dependencia compartida)
# =============================================================================

router_contactos = APIRouter(
    prefix="/contactos",
    tags=["Contactos"],
    dependencies=[Depends(log_peticion)],
)


@router_contactos.get("/", response_model=list[ContactoResponse])
def listar_contactos():
    return list(contactos_db.values())


@router_contactos.post("/", response_model=ContactoResponse, status_code=status.HTTP_201_CREATED)
def crear_contacto(contacto: ContactoCrear):
    global contador
    contador += 1
    nuevo = {"id": contador, **contacto.model_dump()}
    contactos_db[contador] = nuevo
    return nuevo


@router_contactos.get("/{contacto_id}", response_model=ContactoResponse)
def obtener_contacto(contacto_id: int):
    if contacto_id not in contactos_db:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    return contactos_db[contacto_id]


@router_contactos.put("/{contacto_id}", response_model=ContactoResponse)
def actualizar_contacto(contacto_id: int, contacto: ContactoCrear):
    if contacto_id not in contactos_db:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    actualizado = {"id": contacto_id, **contacto.model_dump()}
    contactos_db[contacto_id] = actualizado
    return actualizado


@router_contactos.delete("/{contacto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_contacto(contacto_id: int):
    if contacto_id not in contactos_db:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    del contactos_db[contacto_id]


# =============================================================================
# Router de Utilidades
# =============================================================================

router_utilidades = APIRouter(prefix="/utilidades", tags=["Utilidades"])


@router_utilidades.get("/estadisticas")
def estadisticas():
    return {
        "total_contactos": len(contactos_db),
        "contactos_con_telefono": sum(
            1 for c in contactos_db.values() if c.get("telefono")
        ),
    }


# =============================================================================
# Montar routers
# =============================================================================

app.include_router(router_contactos)
app.include_router(router_utilidades)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
