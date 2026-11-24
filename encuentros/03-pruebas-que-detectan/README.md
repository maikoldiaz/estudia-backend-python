# Encuentro 3 · Pruebas que detectan

**Pregunta del día:** ¿tu prueba detecta un error de la regla o solo repite lo que hace el código?

También puedes ver el material en el navegador, con las salidas preparadas: https://live.maikoldiaz.dev/backend-python/03/material/

Continuamos con el Producto y el Taller del encuentro 2. Python 3.11 o posterior.

| Archivo | Uso |
| --- | --- |
| `producto.py` | El Producto del encuentro 2, importable |
| `producto_con_defecto.py` | El mismo Producto con un defecto: ya no descuenta |
| `test_eco.py` | Dos pruebas del mismo caso: una repite el código y otra espera lo que dice el caso |
| `test_producto.py` | Arrange–Act–Assert, `raises` con `match`, fixture con `yield` y `parametrize` |
| `test_turno_rechazo.py` | Tu turno: la prueba de rechazo de otra regla del Producto, por escribir |
| `test_caja.py` | Tu turno: una fixture con `yield`; cuántas veces se imprime «Abrir caja de panela» |
| `test_orden.py` | Dos pruebas que comparten una fixture |
| `reabastecimiento.py` | Servicio con proveedor inyectado y adaptador HTTP |
| `test_reabastecimiento.py` | Mock, llamadas, el adaptador sin red y una prueba de integración omitida |
| `test_proveedor_cae.py` | Tu turno: que el proveedor se caiga, con `side_effect`, por escribir |
| `taller.py` | El Taller del encuentro 2, importable |
| `test_taller_practica.py` | Fixture lista y dos pruebas por completar |
| `mutantes/mutante_1.py` … `mutante_3.py` | Tres copias del Taller con un error escondido |
| `cazar_mutantes.py` | Ejecuta tus pruebas contra el Taller y contra cada mutante |
| `conftest.py`, `pytest.ini` | Configuración de pytest para esta carpeta |

## Preparar el entorno

Desde esta carpeta, crea y activa un entorno local:

```sh
python3 -m venv .venv
```

En macOS/Linux: `source .venv/bin/activate`. En PowerShell: `.venv\Scripts\Activate.ps1`
(si la política impide activarlo, usa `.venv\Scripts\python.exe` en lugar de `python`).
En Windows puedes crearlo con `py -3 -m venv .venv`.

```sh
python -m pip install pytest
python -m pytest -v
```

El conjunto inicial falla a propósito: **16 pasan, 5 fallan y 1 se omite**. Cuatro fallos son pruebas que vas a escribir (las dos del Taller, la de rechazo y la del proveedor que cae); el quinto, en `test_orden.py`, lo descubrimos en clase.

Ejecuta por secciones, escribiendo antes qué esperas ver:

```sh
python -m pytest test_eco.py -v
python -m pytest test_eco.py --producto-defecto -v
python -m pytest test_producto.py -v
python -m pytest test_turno_rechazo.py -v
python -m pytest test_caja.py -v -s
python -m pytest test_orden.py -v
python -m pytest test_orden.py::test_salida -v
python -m pytest test_orden.py::test_inventario_inicial -v
python -m pytest test_reabastecimiento.py -v
python -m pytest test_proveedor_cae.py -v
```

## Práctica

En tu sala, abre `test_taller_practica.py`.

1. Completen las dos pruebas: una inscripción que se acepta y una que se rechaza cuando no hay cupo. Corran `python -m pytest test_taller_practica.py -v`.
2. Si escribieron la válida en el navegador, cópienla a su `test_taller_practica.py` local (el editor no guarda en tu computador y «Descargar» trae el original). Corran `python cazar_mutantes.py`. Cada mutante es una copia del Taller con un error escondido. ¿Cuáles sobreviven?
3. Escriban la prueba que mata al que sobrevivió. Vuelvan a cazar.

**Producto:** cuántos mutantes sobrevivieron al principio y cuál prueba lo mató.

El cazador exige que tus pruebas pasen primero contra el Taller original. Código de salida 2: las pruebas originales están incompletas o hubo un error de infraestructura; 0: la comparación se hizo, aunque sobrevivan mutantes. Que un mutante muera significa que al menos una prueba falló; no demuestra por sí solo que toda la regla esté cubierta.

La solución se publica después de la clase.

## Solución de referencia

- [`solucion/test_taller_solucion.py`](solucion/test_taller_solucion.py): las pruebas del taller con una fixture, una inscripción que se acepta y una que se rechaza.
- [`solucion/test_turnos_solucion.py`](solucion/test_turnos_solucion.py): existencias negativas y el proveedor que cae, con un mock para cada error de red.

Córrelas con `python -m pytest -v solucion/` desde esta carpeta y compáralas con las tuyas: ¿qué caso probaron ellas que las tuyas no?

## Para tu proyecto

En tu repositorio:

1. Crea `pytest.ini` con dos líneas: `[pytest]` y `pythonpath = src`. Así `from modelo import …` funciona desde `tests/`.
2. Crea `tests/test_modelo.py` con una prueba de tu regla que se acepta y una que se rechaza. El esperado sale de tu caso, no de tu código.
3. Rompe tu regla a propósito (un `<` por `<=`, quita una validación). ¿Falló alguna prueba? Si no, tus pruebas todavía no detectan ese defecto: revisa el caso y las aserciones. Restaura.
4. Pasa la preparación a una fixture y escribe su alcance.
5. Si tu servicio llama algo externo (correo, pago, API, base de datos), reemplázalo con un mock y prueba qué pasa cuando falla.
6. En tu `README.md`: pega la salida de `python -m pytest -v` y escribe qué comportamiento externo aún no comprobaste.

El mock comprueba cómo reacciona tu código al contrato que supones; una prueba de integración comprueba ese contrato. La dirección `.example` de `reabastecimiento.py` está reservada: reemplázala antes de habilitar una prueba de integración y no quites el `skip` solo para ver verde.

**Para pensar antes del próximo encuentro:** ¿qué cambio en tu regla debería hacer fallar a tus pruebas? El miércoles esas pruebas corren solas en GitHub.
