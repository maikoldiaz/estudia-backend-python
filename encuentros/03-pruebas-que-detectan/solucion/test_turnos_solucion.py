from unittest.mock import Mock
from urllib.error import URLError
import pytest
from producto import MovimientoInvalido, Producto
from reabastecimiento import ProveedorHTTP, Reabastecimiento


def test_existencias_negativas():
    with pytest.raises(MovimientoInvalido, match="Existencias inválidas"):
        Producto("panela-1kg", "Panela de Barbosa 1 kg", -1)


@pytest.mark.parametrize("error", [TimeoutError, ConnectionError, URLError])
def test_proveedor_cae(error):
    proveedor = Mock(spec=ProveedorHTTP)
    proveedor.pedir.side_effect = error("Sin respuesta")
    panela = Producto("panela-1kg", "Panela de Barbosa 1 kg", 2)
    assert Reabastecimiento(proveedor).revisar(panela) == "pendiente"
    proveedor.pedir.assert_called_once_with("panela-1kg", 12)
