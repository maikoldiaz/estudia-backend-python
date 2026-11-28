"""Tarifa de un domicilio en Medellín, en pesos colombianos.

Reglas, en este orden:
1. Distancia: hasta 2 km, 4.000; hasta 5 km, 6.000; hasta 10 km, 9.000; más de 10 km,
   9.000 más 1.200 por cada km adicional (se cobra completo). Más de 25 km no se atiende.
2. Comuna: El Poblado y Laureles, +1.500; Santa Elena, +3.000; Belén, +500.
3. Lluvia: +2.000.
4. Hora: de 10 p. m. a 6 a. m., +25 %; de 12 a 2 p. m. y de 6 a 8 p. m., +10 %.
5. Cliente: frecuente, -10 %; empresa, -15 % hasta 10 km y -5 % si es más lejos;
   nuevo, gratis hasta 2 km.
El valor final se redondea a la centena; si queda justo a la mitad, a la centena par (7.650 → 7.600).
"""
from math import ceil

MAXIMO_KM = 25
TRAMOS = [(2, 4000), (5, 6000), (10, 9000)]  # (hasta cuántos km, valor)
RECARGO_COMUNA = {"El Poblado": 1500, "Laureles": 1500, "Santa Elena": 3000, "Belén": 500}
RECARGO_LLUVIA = 2000


class FueraDeCobertura(Exception):
    """El domicilio queda más lejos de lo que se atiende."""


def _tarifa_base(distancia_km):
    for limite, valor in TRAMOS:
        if distancia_km <= limite:
            return valor
    return 9000 + 1200 * ceil(distancia_km - 10)


def _factor_horario(hora):
    if hora >= 22 or hora < 6:
        return 1.25
    if 12 <= hora < 14 or 18 <= hora < 20:
        return 1.10
    return 1.0


def _factor_cliente(cliente, distancia_km):
    if cliente == "frecuente":
        return 0.90
    if cliente == "empresa":
        return 0.85 if distancia_km <= 10 else 0.95
    return 1.0


def calcular_tarifa(distancia_km, comuna, hora, cliente, llueve=False):
    if distancia_km <= 0:
        raise ValueError(f"Distancia inválida: {distancia_km}. Debe ser positiva")
    if distancia_km > MAXIMO_KM:
        raise FueraDeCobertura(f"{distancia_km} km queda fuera de cobertura (máximo {MAXIMO_KM})")
    if cliente == "nuevo" and distancia_km <= 2:
        return 0

    tarifa = _tarifa_base(distancia_km) + RECARGO_COMUNA.get(comuna, 0)
    if llueve:
        tarifa += RECARGO_LLUVIA
    tarifa = tarifa * _factor_horario(hora) * _factor_cliente(cliente, distancia_km)
    return int(round(tarifa / 100.0) * 100)
