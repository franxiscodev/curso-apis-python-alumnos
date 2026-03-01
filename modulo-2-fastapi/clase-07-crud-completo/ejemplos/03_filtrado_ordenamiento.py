"""
Filtrado y Ordenamiento
========================
Query params dinámicos para filtrar y ordenar resultados.

Ejecutar:
    uvicorn ejemplos.03_filtrado_ordenamiento:app --reload

Conceptos:
    - Query params opcionales para filtrado
    - Ordenamiento con sort_by y order
    - Combinación de filtrado + paginación
"""

import math
from typing import Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Filtrado y Ordenamiento", version="1.0.0")


# =============================================================================
# MODELOS
# =============================================================================


class Empleado(BaseModel):
    """Modelo de empleado."""
    id: int
    nombre: str
    departamento: str
    salario: float
    activo: bool


class EmpleadosPaginados(BaseModel):
    """Respuesta paginada de empleados."""
    items: list[Empleado]
    total: int
    page: int
    size: int
    pages: int


# =============================================================================
# DATOS DE EJEMPLO
# =============================================================================


departamentos = ["Ingeniería", "Marketing", "Ventas", "RRHH", "Finanzas"]

empleados_db: list[dict] = [
    {
        "id": i,
        "nombre": f"Empleado {i}",
        "departamento": departamentos[i % 5],
        "salario": 30000 + (i * 1500),
        "activo": i % 7 != 0
    }
    for i in range(1, 31)  # 30 empleados
]


# =============================================================================
# ENDPOINT CON FILTRADO + ORDENAMIENTO + PAGINACIÓN
# =============================================================================


@app.get("/empleados", response_model=EmpleadosPaginados, tags=["Empleados"])
def listar_empleados(
    # Filtros
    departamento: str | None = Query(
        default=None, description="Filtrar por departamento"
    ),
    activo: bool | None = Query(
        default=None, description="Filtrar por estado activo"
    ),
    salario_min: float | None = Query(
        default=None, ge=0, description="Salario mínimo"
    ),
    salario_max: float | None = Query(
        default=None, ge=0, description="Salario máximo"
    ),
    # Ordenamiento
    sort_by: Literal["nombre", "salario", "departamento"] = Query(
        default="nombre", description="Campo para ordenar"
    ),
    order: Literal["asc", "desc"] = Query(
        default="asc", description="Dirección del orden"
    ),
    # Paginación
    page: int = Query(default=1, ge=1, description="Página"),
    size: int = Query(default=10, ge=1, le=50, description="Items por página")
):
    """
    Listar empleados con filtrado, ordenamiento y paginación.

    - **departamento**: Filtro exacto por departamento
    - **activo**: Filtrar por estado
    - **salario_min/max**: Rango de salario
    - **sort_by**: Ordenar por nombre, salario o departamento
    - **order**: asc o desc
    """
    resultados = empleados_db.copy()

    # Aplicar filtros
    if departamento:
        resultados = [
            e for e in resultados if e["departamento"] == departamento]

    if activo is not None:
        resultados = [e for e in resultados if e["activo"] == activo]

    if salario_min is not None:
        resultados = [e for e in resultados if e["salario"] >= salario_min]

    if salario_max is not None:
        resultados = [e for e in resultados if e["salario"] <= salario_max]

    # Ordenar
    reverse = order == "desc"
    resultados.sort(key=lambda e: e[sort_by], reverse=reverse)

    # Paginar
    total = len(resultados)
    pages = math.ceil(total / size) if total > 0 else 0
    start = (page - 1) * size

    return {
        "items": resultados[start:start + size],
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }


@app.get("/departamentos", response_model=list[str], tags=["Utilidades"])
def listar_departamentos():
    """Listar departamentos disponibles (para poblar filtros)."""
    return sorted(set(e["departamento"] for e in empleados_db))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
