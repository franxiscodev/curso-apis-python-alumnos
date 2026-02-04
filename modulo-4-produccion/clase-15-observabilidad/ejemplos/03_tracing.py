"""
Ejemplo 03: Tracing y Correlation IDs
=======================================
Seguir una request a través de múltiples operaciones.

Ejecutar:
    uvicorn ejemplos.03_tracing:app --reload
"""

import asyncio
import logging
import time
import uuid

from fastapi import FastAPI, Request

app = FastAPI(title="Tracing", version="1.0.0")
logger = logging.getLogger("tracing")
logging.basicConfig(level=logging.INFO, format="%(message)s")


# === CONTEXTO DE TRACING ===


class TraceContext:
    """Contexto de tracing para una request."""

    def __init__(self, trace_id: str | None = None):
        self.trace_id = trace_id or str(uuid.uuid4())[:8]
        self.spans: list[dict] = []

    def start_span(self, nombre: str) -> dict:
        span = {
            "trace_id": self.trace_id,
            "span": nombre,
            "inicio": time.perf_counter(),
        }
        self.spans.append(span)
        return span

    def end_span(self, span: dict):
        span["duracion"] = round(time.perf_counter() - span["inicio"], 4)
        logger.info(
            f"[{span['trace_id']}] {span['span']}: {span['duracion']}s"
        )

    def resumen(self) -> dict:
        return {
            "trace_id": self.trace_id,
            "spans": [
                {"nombre": s["span"], "duracion": s.get("duracion", 0)}
                for s in self.spans
            ],
            "total_spans": len(self.spans),
        }


# === MIDDLEWARE ===


@app.middleware("http")
async def tracing_middleware(request: Request, call_next):
    trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4())[:8])
    ctx = TraceContext(trace_id)
    request.state.trace = ctx

    span = ctx.start_span(f"{request.method} {request.url.path}")
    response = await call_next(request)
    ctx.end_span(span)

    response.headers["X-Trace-ID"] = trace_id
    return response


# === FUNCIONES CON SPANS ===


async def consultar_base_datos(ctx: TraceContext) -> list:
    span = ctx.start_span("db.query")
    await asyncio.sleep(0.1)  # Simula query
    ctx.end_span(span)
    return [{"id": 1, "dato": "valor"}]


async def llamar_servicio_externo(ctx: TraceContext) -> dict:
    span = ctx.start_span("http.external")
    await asyncio.sleep(0.2)  # Simula llamada HTTP
    ctx.end_span(span)
    return {"status": "ok"}


async def procesar_datos(ctx: TraceContext, datos: list) -> dict:
    span = ctx.start_span("process.transform")
    await asyncio.sleep(0.05)
    ctx.end_span(span)
    return {"procesados": len(datos)}


# === ENDPOINTS ===


@app.get("/operacion", tags=["Tracing"])
async def operacion_completa(request: Request):
    """Operación con múltiples spans de tracing."""
    ctx = request.state.trace

    datos = await consultar_base_datos(ctx)
    externo = await llamar_servicio_externo(ctx)
    resultado = await procesar_datos(ctx, datos)

    return {
        "resultado": resultado,
        "externo": externo,
        "trace": ctx.resumen(),
    }


@app.get("/simple", tags=["Tracing"])
async def operacion_simple(request: Request):
    """Operación simple con un solo span."""
    ctx = request.state.trace
    datos = await consultar_base_datos(ctx)
    return {"datos": datos, "trace": ctx.resumen()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
