import pytest
from taller import InscripcionRechazada, Taller


@pytest.fixture
def guitarra():
    return Taller("Guitarra en la Casa de la Cultura de Manrique", cupo=2)


def test_inscripcion_valida(guitarra):
    assert guitarra.inscribir("Valentina") == 1
    assert guitarra.inscritos == ["Valentina"]


def test_inscripcion_invalida(guitarra):
    guitarra.inscribir("Valentina")
    guitarra.inscribir("Samuel")
    with pytest.raises(InscripcionRechazada, match="no tiene cupos"):
        guitarra.inscribir("Luisa")
    assert guitarra.inscritos == ["Valentina", "Samuel"]


def test_no_repite_persona(guitarra):
    guitarra.inscribir("Valentina")
    with pytest.raises(InscripcionRechazada, match="ya está inscrita"):
        guitarra.inscribir("Valentina")
    assert guitarra.inscritos == ["Valentina"]


def test_no_reduce_cupo_ocupado(guitarra):
    guitarra.inscribir("Valentina")
    guitarra.inscribir("Samuel")
    with pytest.raises(InscripcionRechazada, match="No se puede dejar"):
        guitarra.cupo = 1
    assert guitarra.cupo == 2
    assert guitarra.inscritos == ["Valentina", "Samuel"]
