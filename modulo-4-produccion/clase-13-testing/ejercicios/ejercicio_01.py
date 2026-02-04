"""
Ejercicio 01: Tests Unitarios de Modelos
==========================================
Testear funciones puras y modelos Pydantic.

INSTRUCCIONES:
1. Escribir tests para la función calcular_descuento
2. Escribir tests para el modelo Pydantic Usuario
3. Usar pytest.mark.parametrize para múltiples casos

Ejecutar: pytest ejercicios/ejercicio_01.py -v
"""

from pydantic import BaseModel, field_validator


class Usuario(BaseModel):
    nombre: str
    email: str
    edad: int

    @field_validator("edad")
    @classmethod
    def validar_edad(cls, v):
        if v < 0 or v > 150:
            raise ValueError("Edad debe estar entre 0 y 150")
        return v


def calcular_descuento(precio: float, porcentaje: float) -> float:
    """Calcula precio con descuento. Porcentaje entre 0 y 100."""
    if porcentaje < 0 or porcentaje > 100:
        raise ValueError("Porcentaje debe estar entre 0 y 100")
    return round(precio * (1 - porcentaje / 100), 2)


def categorizar_edad(edad: int) -> str:
    """Categoriza por rango de edad."""
    if edad < 18:
        return "menor"
    if edad < 65:
        return "adulto"
    return "senior"


# TODO: test_calcular_descuento_basico

# TODO: test_calcular_descuento_cero

# TODO: test_calcular_descuento_cien

# TODO: test_calcular_descuento_invalido (ValueError)

# TODO: test_usuario_valido

# TODO: test_usuario_edad_invalida

# TODO: test_categorizar_edad_parametrize (usar @pytest.mark.parametrize)
