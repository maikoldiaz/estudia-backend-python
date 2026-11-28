import pytest
from tarifa import FueraDeCobertura, calcular_tarifa


def test_distancia_no_positiva():
    with pytest.raises(ValueError, match="Debe ser positiva"):
        calcular_tarifa(0, "Robledo", 10, "regular")


def test_fuera_de_cobertura():
    with pytest.raises(FueraDeCobertura, match="fuera de cobertura"):
        calcular_tarifa(26, "Robledo", 10, "regular")


@pytest.mark.parametrize("distancia, esperado", [(1.5, 4000), (4, 6000), (8, 9000)])
def test_tramos_de_distancia(distancia, esperado):
    assert calcular_tarifa(distancia, "Robledo", 10, "regular") == esperado


def test_recargo_el_poblado():
    assert calcular_tarifa(3, "El Poblado", 10, "regular") == 7500


def test_hora_pico_del_almuerzo():
    assert calcular_tarifa(3, "Robledo", 12, "regular") == 6600


def test_cliente_frecuente():
    assert calcular_tarifa(3, "Robledo", 10, "frecuente") == 5400


def test_cliente_nuevo_cerca_no_paga():
    assert calcular_tarifa(1.5, "Robledo", 10, "nuevo") == 0


# Ramas que el reporte de cobertura marcaba sin cubrir. El esperado sale de las reglas.
def test_recargo_laureles():
    assert calcular_tarifa(3, "Laureles", 10, "regular") == 7500


def test_recargo_santa_elena():
    assert calcular_tarifa(3, "Santa Elena", 10, "regular") == 9000


def test_recargo_belen():
    assert calcular_tarifa(3, "Belén", 10, "regular") == 6500


def test_lluvia_suma_dos_mil():
    assert calcular_tarifa(3, "Robledo", 10, "regular", llueve=True) == 8000


@pytest.mark.parametrize("hora", [22, 23, 0, 5])
def test_recargo_nocturno(hora):
    assert calcular_tarifa(3, "Robledo", hora, "regular") == 7500


@pytest.mark.parametrize("hora", [6, 21, 14, 11])
def test_sin_recargo_fuera_de_las_horas_especiales(hora):
    assert calcular_tarifa(3, "Robledo", hora, "regular") == 6000


def test_hora_pico_de_la_tarde():
    assert calcular_tarifa(3, "Robledo", 18, "regular") == 6600


def test_distancia_mayor_a_diez_cobra_km_adicional_completo():
    assert calcular_tarifa(12.3, "Robledo", 10, "regular") == 12600


def test_cliente_empresa_cerca():
    assert calcular_tarifa(8, "El Poblado", 10, "empresa") == 8900


def test_cliente_empresa_lejos():
    assert calcular_tarifa(12, "Robledo", 10, "empresa") == 10800


def test_cliente_nuevo_lejos_paga_completo():
    assert calcular_tarifa(3, "Robledo", 10, "nuevo") == 6000
