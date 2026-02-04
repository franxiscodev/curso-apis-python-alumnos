"""
Ejemplo 02: Patrón Circuit Breaker
====================================
Protege contra servicios externos caídos.

Ejecutar:
    python ejemplos/02_circuit_breaker.py
"""

import asyncio
import time
from enum import Enum


# === CIRCUIT BREAKER ===


class Estado(Enum):
    CERRADO = "cerrado"          # Normal, llamadas pasan
    ABIERTO = "abierto"          # Bloqueado, falla inmediato
    SEMI_ABIERTO = "semi_abierto"  # Probando una llamada


class CircuitBreaker:
    """Circuit breaker para proteger llamadas a servicios externos."""

    def __init__(
        self,
        nombre: str,
        umbral_fallos: int = 3,
        tiempo_recuperacion: float = 10.0,
    ):
        self.nombre = nombre
        self.umbral_fallos = umbral_fallos
        self.tiempo_recuperacion = tiempo_recuperacion
        self.estado = Estado.CERRADO
        self.fallos_consecutivos = 0
        self.ultimo_fallo: float = 0

    async def ejecutar(self, coroutine):
        """Ejecuta una coroutine protegida por el circuit breaker."""
        if self.estado == Estado.ABIERTO:
            if time.time() - self.ultimo_fallo > self.tiempo_recuperacion:
                self.estado = Estado.SEMI_ABIERTO
                print(f"  [{self.nombre}] Semi-abierto: probando...")
            else:
                raise RuntimeError(f"Circuito ABIERTO para {self.nombre}")

        try:
            resultado = await coroutine
            self._exito()
            return resultado
        except Exception as e:
            self._fallo()
            raise e

    def _exito(self):
        self.fallos_consecutivos = 0
        if self.estado == Estado.SEMI_ABIERTO:
            self.estado = Estado.CERRADO
            print(f"  [{self.nombre}] Circuito CERRADO (recuperado)")

    def _fallo(self):
        self.fallos_consecutivos += 1
        self.ultimo_fallo = time.time()
        if self.fallos_consecutivos >= self.umbral_fallos:
            self.estado = Estado.ABIERTO
            print(f"  [{self.nombre}] Circuito ABIERTO ({self.fallos_consecutivos} fallos)")

    @property
    def info(self) -> dict:
        return {
            "nombre": self.nombre,
            "estado": self.estado.value,
            "fallos": self.fallos_consecutivos,
        }


# === DEMO ===


async def servicio_inestable(exito: bool) -> str:
    """Simula un servicio que a veces falla."""
    await asyncio.sleep(0.1)
    if not exito:
        raise ConnectionError("Servicio no disponible")
    return "OK"


async def main():
    cb = CircuitBreaker("api-externa", umbral_fallos=3, tiempo_recuperacion=2.0)

    # Simular 5 fallos seguidos
    print("=== Simulando fallos ===")
    for i in range(5):
        try:
            resultado = await cb.ejecutar(servicio_inestable(False))
            print(f"  Llamada {i + 1}: {resultado}")
        except (ConnectionError, RuntimeError) as e:
            print(f"  Llamada {i + 1}: {e}")
    print(f"  Estado: {cb.info}")

    # Esperar recuperación
    print("\n=== Esperando recuperación (2s) ===")
    await asyncio.sleep(2.1)

    # Intentar de nuevo (éxito)
    print("\n=== Reintentando ===")
    try:
        resultado = await cb.ejecutar(servicio_inestable(True))
        print(f"  Resultado: {resultado}")
    except RuntimeError as e:
        print(f"  Error: {e}")
    print(f"  Estado: {cb.info}")


if __name__ == "__main__":
    asyncio.run(main())
