"""Compara la versión original con la refactorizada en una malla de entradas."""
import importlib.util
import itertools
import sys
from pathlib import Path


def cargar(nombre, ruta):
    ficha = importlib.util.spec_from_file_location(nombre, ruta)
    modulo = importlib.util.module_from_spec(ficha)
    ficha.loader.exec_module(modulo)
    return modulo


aqui = Path(__file__).resolve().parent
candidatos = [aqui.parent / "practica_domicilios/src/tarifa.py",
              aqui.parent.parent / "E04_demo/practica_domicilios/src/tarifa.py"]
ruta_original = Path(sys.argv[1]) if len(sys.argv) > 1 else next(c for c in candidatos if c.exists())
original = cargar("tarifa_original", ruta_original)
nueva = cargar("tarifa_nueva", aqui / "src/tarifa.py")

distancias = [0.5, 1.5, 2, 2.1, 4, 5, 5.5, 8, 10, 10.1, 12.3, 12, 20, 25]
comunas = ["Robledo", "El Poblado", "Laureles", "Santa Elena", "Belén"]
horas = [0, 5, 6, 11, 12, 13, 14, 17, 18, 19, 20, 21, 22, 23]
clientes = ["regular", "frecuente", "empresa", "nuevo"]
lluvia = [False, True]

total = distintos = 0
for d, c, h, cl, ll in itertools.product(distancias, comunas, horas, clientes, lluvia):
    total += 1
    if original.calcular_tarifa(d, c, h, cl, ll) != nueva.calcular_tarifa(d, c, h, cl, ll):
        distintos += 1
        print("DIFIERE", d, c, h, cl, ll)
print(f"{total} combinaciones comparadas; {distintos} distintas")
sys.exit(1 if distintos else 0)
