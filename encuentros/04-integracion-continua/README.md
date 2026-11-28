# Encuentro 4 · Integración continua, calidad y regresión

**Pregunta del día:** cuando el pipeline dice verde, ¿qué se ejecutó de verdad?

También puedes ver el material en el navegador, con las salidas preparadas: https://live.maikoldiaz.dev/backend-python/04/material/

Continuamos con el Producto del encuentro 3. Python 3.11 o posterior.

| Carpeta | Uso |
| --- | --- |
| `ci_inventario/` | Un proyecto pequeño con pruebas, `requirements.txt`, `pytest.ini` y un workflow en `.github/workflows/ci.yml` |
| `ci_cero_pruebas/` | El mismo proyecto con un workflow que sale verde sin ejecutar ninguna prueba: ¿por qué? |
| `cobertura_y_aserciones/` | Dos archivos de pruebas del Producto, y mutantes para comparar qué detecta cada uno |
| `hallazgo_ruff/` | Código con tres hallazgos de Ruff |
| `hallazgo_ruff_gemelo/` | Otro archivo con tres hallazgos, para repetir el ejercicio con datos nuevos |
| `practica_domicilios/` | La práctica: una función con muchas ramas, sus pruebas y el reporte de cobertura |
| `plantilla_ci/` | `ci.yml` para copiar a tu repositorio, una versión de nivel reto y una configuración de pre-commit |

Cada carpeta funciona sola. Los comandos de abajo se ejecutan **desde dentro de la carpeta** que se indica.

## Preparar el entorno

Desde esta carpeta, crea y activa un entorno local:

```sh
python3 -m venv .venv
```

En macOS/Linux: `source .venv/bin/activate`. En PowerShell: `.venv\Scripts\Activate.ps1`
(si la política impide activarlo, usa `.venv\Scripts\python.exe` en lugar de `python`).
En Windows puedes crearlo con `py -3 -m venv .venv`.

```sh
python -m pip install -r ci_inventario/requirements-dev.txt
```

Eso instala pytest, pytest-cov, Ruff y unidecode. Los comandos con `$?` y `| tee` son de macOS/Linux o Git Bash; en PowerShell, el código de salida está en `$LASTEXITCODE`.

## 1. Pasa en mi computador, ¿por qué falla en uno limpio?

```sh
cd ci_inventario
python -m pytest -v
```

Pasan **7**. Ahora un entorno limpio, como el que crea GitHub en cada ejecución: solo lo que dice `requirements.txt`. El `requirements.txt` de esta carpeta ya está completo; para reproducir el problema **simulamos un archivo incompleto**, que solo dijera `pytest`, instalando solo esa línea:

```sh
python3 -m venv ../venv
../venv/bin/python -m pip install pytest
../venv/bin/python -m pytest -v
```

Antes de ejecutar, escribe qué esperas ver. Lee el log y escribe **la causa y la corrección exacta**. La corrección: el `requirements.txt` incompleto necesita la línea `unidecode` (aquí ya la tiene) y, en un entorno limpio, se vuelve a instalar y a correr lo mismo que el workflow:

```sh
python3 -m venv ../venv2
../venv2/bin/python -m pip install -r requirements.txt
../venv2/bin/python -m pytest -v
```

Segunda causa frecuente: sin `pytest.ini` con `pythonpath = src`, los `import` de las pruebas no encuentran el código. Compruébalo copiando la carpeta sin ese archivo y escribiendo de nuevo la causa y la corrección exacta.

## 2. Verde con cero pruebas

```sh
cd ../ci_cero_pruebas
python -m pytest -v; echo "código de salida: $?"
python -m pytest -v | tee salida_pytest.txt; echo "código de salida: $?"
```

Pytest sin pruebas termina con código **5**. Pero el workflow guarda la salida con `| tee`, y en este workflow, que no declara `shell`, GitHub ejecuta en Linux cada `run:` con `bash -e` (sin `pipefail`): el código que queda es el de `tee`, que es 0. Clasifica cada log (verde real, verde mentiroso, rojo porque no corrió ninguna prueba, rojo porque una prueba falló) y encuentra **la línea que lo prueba**. Después mira el archivo `tests/`: ¿por qué pytest no encontró nada? Propón dos cambios exactos y compara.

```sh
mv tests/prueba_producto.py tests/test_producto.py
python -m pytest -v | tee salida_pytest.txt
```

Eso hace que corran las pruebas. Para que un paso no esconda el código de pytest detrás de un pipe, declara `shell: bash` en el paso (GitHub lo ejecuta con `bash -eo pipefail`) o escribe `set -o pipefail;` antes del comando: así el verde con cero pruebas se pone rojo. `pipefail` evita que el job mienta, pero no hace que corran pruebas.

Otras formas de llegar a verde sin ejecutar pruebas: `python -m unittest discover` con pruebas escritas como funciones de pytest (en Python 3.11 termina con código 0 y «Ran 0 tests»; desde 3.12 termina con 5) o un `|| true` al final del comando. **En el log, busca siempre la línea con el número de pruebas que pasaron.**

## 3. Tres herramientas, tres preguntas

```sh
cd ../hallazgo_ruff
ruff check .
```

Antes de ejecutar Ruff, sé el linter: en 2 minutos, encuentra a ojo los defectos de los dos archivos y anótalos con su línea. Después compara con la salida real y repite el ejercicio con otro archivo (`hallazgo_ruff_gemelo/alertas_con_hallazgo.py`): encuentra a ojo los defectos y compáralos con `ruff check .` dentro de esa carpeta. Ruff dice si el código tiene errores que se ven sin ejecutarlo: un `import` sin usar, una variable que se calcula y nunca se usa (¿qué pretendía hacer el autor?) y una prueba que se define dos veces con el mismo nombre (la primera nunca corre).

```sh
cd ../cobertura_y_aserciones
python -m pytest tests/test_recorre_todo.py -v --cov=producto --cov-branch --cov-report=term-missing
python cazar_mutantes.py tests/test_recorre_todo.py
python -m pytest tests/test_con_aserciones.py -v --cov=producto --cov-branch --cov-report=term-missing
python cazar_mutantes.py tests/test_con_aserciones.py
```

Antes de ejecutar: una sola prueba que recorre todo el código sin comprobar los resultados del negocio (y con `pytest.raises(Exception)`, demasiado general), ¿qué cobertura da? ¿Y las siete que sí afirman? ¿Cuál de las dos detecta un mutante? `cazar_mutantes.py` primero comprueba que el Producto original pase; un mutante «muere» cuando una prueba falla al ejecutarse (casi siempre una aserción; si fue otro error, el script lo avisa), y cualquier otro problema (importar, preparar las pruebas, argumentos, cero pruebas) se muestra como error, no como un mutante muerto.

Haz tú el mutante: en una copia de `src/producto.py`, borra la línea `self.existencias -= cantidad`, ejecuta `test_recorre_todo.py` (pasa: el mutante sobrevive), cambia `cafe.registrar_salida(3)` por `assert cafe.registrar_salida(3) == 7` (ahora falla: el mutante muere) y restaura el original. La complejidad ciclomática (cuántos caminos tiene una función) se mide en la práctica, con la regla `C901` de Ruff.

## Práctica: una función con muchas ramas

```sh
cd ../practica_domicilios
python -m pytest -v
python -m pytest --cov=tarifa --cov-branch --cov-report=term-missing
ruff check .
```

La tarifa de un domicilio en Medellín depende de la distancia, la comuna, la hora, la lluvia y el tipo de cliente; las reglas están al inicio de `src/tarifa.py`. Las pruebas actuales pasan, pero el reporte muestra ramas sin cubrir y Ruff marca la función como demasiado compleja.

1. Lean el reporte: ¿qué líneas de `tarifa.py` no se ejecutan? Elijan una rama y escriban la prueba que la cubre. **El esperado sale de las reglas, no de leer el código.**
2. Elijan **una** mejora: retornos tempranos, una tabla (diccionario) en lugar de `if`/`elif`, o extraer una función. Háganla sin cambiar el comportamiento.
   El redondeo también se conserva: Python redondea al par (7.650 → 7.600), como dice el encabezado de `tarifa.py`.
3. Repitan `python -m pytest --cov=tarifa --cov-branch --cov-report=term-missing` y `ruff check .`. Las pruebas deben seguir en verde.
4. Para ver la complejidad de cada función antes y después (con el umbral de 10, una función que baja a 5 ya no aparece en `ruff check .`), usen este comando; sale con código 1 a propósito, porque su trabajo es mostrar los números:

```sh
ruff check --isolated --select C901 --config 'lint.mccabe.max-complexity=1' --output-format concise src/tarifa.py
```

**Producto:** la complejidad antes y después, el porcentaje de cobertura antes y después, y qué prueba les habría avisado si la mejora hubiera cambiado el comportamiento.

## Solución de referencia

[`solucion/`](solucion/) es la práctica resuelta: `src/tarifa.py` refactorizado con una tabla de tramos y tres funciones pequeñas, y `tests/test_tarifa.py` con 26 pruebas.

| | Antes | Después |
|---|---|---|
| Complejidad de `calcular_tarifa` | 17 | 5 |
| Cobertura de ramas | 75 % (9 pruebas) | 100 % (26 pruebas) |

```sh
cd solucion
python -m pytest --cov=tarifa --cov-branch --cov-report=term-missing
ruff check .
python equivalencia.py
```

`equivalencia.py` compara la versión original con la nueva en 7.840 combinaciones de entradas y cuenta las que dan distinto (deben ser 0). Compárala con tu mejora: ¿qué prueba tuya habría avisado si el redondeo hubiera cambiado?

## Para tu proyecto

En tu repositorio:

1. Crea `requirements.txt` con lo que necesita tu proyecto (por ejemplo `pytest`) y comprueba que funciona en un entorno limpio: `python -m pip install -r requirements.txt`.
2. Copia `plantilla_ci/ci.yml` a `.github/workflows/ci.yml` y ajusta la versión de Python, las dependencias y el comando de pruebas.
3. Haz `git push`. En GitHub abre la pestaña **Actions** y entra a la ejecución.
4. **Comprueba en el log cuántas pruebas corrieron.** Debe ser más de cero y coincidir con tu ejecución local.
5. En tu `README.md`: el comando local con su salida, el comando del workflow, y el estado de cada parte (ejecutado, simulado o pendiente). Si no tienes acceso a Actions, conserva el YAML y tu salida local; **no los llames ejecución remota**.
6. Ejecuta `ruff check .` en tu proyecto. Elige **una** mejora de legibilidad o de complejidad, repite tus pruebas y escribe en el README qué cambiaste y por qué.

**Nivel reto:** `plantilla_ci/ci_reto.yml` (matriz de versiones de Python, Ruff y `--cov-fail-under` en el pipeline) y `plantilla_ci/pre-commit-config.yaml`. Más de cobertura no es mejor si las pruebas no afirman nada.

**Para pensar antes del próximo encuentro:** si tu proyecto guardara sus datos en documentos en vez de en la memoria, ¿qué parte de tu pipeline tendría que cambiar?
