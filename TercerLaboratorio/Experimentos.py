"""
experimentos.py

Mide el tiempo de Lista, ABB y B+ al variar N, con IDs aleatorios y ordenados.
Cada medicion se guarda como una fila en resultados/resultados.csv (tiempos en SEGUNDOS).

Como correrlo (en la misma carpeta que los otros archivos .py):
    python experimentos.py  en la terminal
"""
import csv
import gc
import os
import platform
import sys
import time

from GenerarEstudiantes import generar_N_estudiantes, generar_M_busquedas, generar_M_rangos
from Lista import (insertar_estudiantes_lista, buscar_estudiante_id_lista, listar_orden_id_lista, buscar_rango_lista)
from ArbolABB import (insertar_estudiante_ABB, buscar_id_estudiante_ABB, listar_orden_id_estudiantes_ABB, buscar_rango_ABB, altura_ABB)
from ArbolBMas import ArbolBMas

# ----------------------------------------------------------------------------------------
# PARAMETROS DEL EXPERIMENTO 
# ----------------------------------------------------------------------------------------
if len(sys.argv) > 1 and sys.argv[1] == "rapido":
    TAMANOS_N = [100, 500, 1000, 2000]
    REPETICIONES = 2
    LIMITE_N = {}                                   # sin limites en la prueba rapida
else:
    TAMANOS_N = [100, 500, 1000, 5000, 10000, 20000]    # N maximo = 20.000
    REPETICIONES = 10
    LIMITE_N = {}                                       # sin limites: las tres estructuras llegan hasta N = 20.000

M_BUSQUEDAS = 1000          # M: cantidad de busquedas por ID en cada prueba
PORCENTAJE_EXISTENTES = 0.5 # de las M busquedas, la mitad son IDs que existen y la mitad no
M_RANGOS = 100              # cantidad de busquedas por rango en cada prueba
RANGOS = {                  # nombre -> parte de todos los IDs que abarca el rango
    "muy_chico": 0.001,     # 0,1%
    "chico": 0.01,          # 1%
    "mediano": 0.10,        # 10%
    "enorme": 0.50,         # 50%
}
GRADO_BMAS = 50
ORDENES = ["aleatorio", "ordenado"]
CARPETA = "resultados"

# ----------------------------------------------------------------------------------------
# ADAPTADORES: las tres estructuras con la misma interfaz
# ----------------------------------------------------------------------------------------
def construir_lista(estudiantes):
    lista = []
    for e in estudiantes:
        insertar_estudiantes_lista(lista, e)
    return lista


def construir_abb(estudiantes):
    raiz = None
    for e in estudiantes:
        raiz = insertar_estudiante_ABB(raiz, e)
    return raiz


def construir_bmas(estudiantes):
    arbol = ArbolBMas(GRADO_BMAS)
    for e in estudiantes:
        arbol.insertar_estudiante_BMas(e)
    return arbol


ESTRUCTURAS = {
    "Lista": dict(construir=construir_lista,
                  buscar=buscar_estudiante_id_lista,
                  listar=listar_orden_id_lista,
                  rango=buscar_rango_lista,
                  altura=lambda s: ""),                      # la lista no tiene altura
    "ABB":   dict(construir=construir_abb,
                  buscar=buscar_id_estudiante_ABB,
                  listar=listar_orden_id_estudiantes_ABB,
                  rango=buscar_rango_ABB,
                  altura=altura_ABB),
    "B+":    dict(construir=construir_bmas,
                  buscar=lambda s, i: s.buscar_id_estudiante_BMas(i),
                  listar=lambda s: s.listar_orden_id_estudiantes_BMas(),
                  rango=lambda s, a, b: s.buscar_rango_BMas(a, b),
                  altura=lambda s: s.altura()),
}

# ----------------------------------------------------------------------------------------
# MEDICION
# ----------------------------------------------------------------------------------------
def medir(funcion):
    """Ejecuta funcion() y retorna (segundos, resultado).
    Se usa time.perf_counter (reloj de alta resolucion). Se apaga el recolector de basura
    solo durante la medicion para que no meta pausas al azar."""
    gc.collect()
    gc.disable()
    inicio = time.perf_counter()
    resultado = funcion()
    tiempo = time.perf_counter() - inicio
    gc.enable()
    return tiempo, resultado


def una_estructura(nombre, estudiantes, busquedas, rangos_por_tipo):
    """Mide todas las operaciones para UNA estructura con los datos dados."""
    e = ESTRUCTURAS[nombre]

    t_insercion, estructura = medir(lambda: e["construir"](estudiantes))

    def hacer_busquedas():
        encontrados = 0
        for id_buscar in busquedas:
            if e["buscar"](estructura, id_buscar) is not None:
                encontrados += 1
        return encontrados
    t_busqueda, encontrados = medir(hacer_busquedas)

    t_listado, listado = medir(lambda: e["listar"](estructura))

    fila = {"t_insercion_s": t_insercion, "t_busqueda_s": t_busqueda, "t_listado_s": t_listado,
            "altura": e["altura"](estructura), "encontrados": encontrados, "n_listado": len(listado)}

    for tipo, lista_rangos in rangos_por_tipo.items():
        def hacer_rangos():
            total = 0
            for a, b in lista_rangos:
                total += len(e["rango"](estructura, a, b))
            return total
        t_rango, total_devueltos = medir(hacer_rangos)
        fila[f"t_rango_{tipo}_s"] = t_rango
        fila[f"k_rango_{tipo}"] = total_devueltos / len(lista_rangos)   # estudiantes devueltos por rango (promedio)
    return fila


def guardar_info_sistema():
    os.makedirs(CARPETA, exist_ok=True)
    with open(os.path.join(CARPETA, "info_sistema.txt"), "w", encoding="utf-8") as f:
        f.write(f"Sistema operativo: {platform.platform()}\n")
        f.write(f"Procesador: {platform.processor()}\n")
        f.write(f"Nucleos logicos: {os.cpu_count()}\n")
        f.write(f"Python: {sys.version}\n")
        f.write(f"Parametros: N={TAMANOS_N}, repeticiones={REPETICIONES}, M={M_BUSQUEDAS}, "
                f"M_rangos={M_RANGOS}, rangos={RANGOS}, grado B+={GRADO_BMAS}, limites={LIMITE_N}\n")


def main():
    guardar_info_sistema()
    columnas = (["estructura", "orden", "N", "M", "repeticion",
                 "t_insercion_s", "t_busqueda_s", "t_listado_s"]
                + [f"t_rango_{t}_s" for t in RANGOS]
                + [f"k_rango_{t}" for t in RANGOS]
                + ["altura", "encontrados", "n_listado"])

    ruta = os.path.join(CARPETA, "resultados.csv")
    inicio_total = time.time()
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()

        for orden in ORDENES:
            for N in TAMANOS_N:
                estructuras_a_medir = [s for s in ESTRUCTURAS if N <= LIMITE_N.get((s, orden), float("inf"))]
                omitidas = [s for s in ESTRUCTURAS if s not in estructuras_a_medir]
                if omitidas:
                    print(f"  (N={N}, {orden}: se omite {', '.join(omitidas)} por tiempo)")

                for rep in range(1, REPETICIONES + 1):
                    # Los datos se generan UNA vez por repeticion y se usan en las tres estructuras
                    estudiantes = generar_N_estudiantes(N, ordenado=(orden == "ordenado"))
                    busquedas = generar_M_busquedas(estudiantes, M_BUSQUEDAS, PORCENTAJE_EXISTENTES)
                    rangos = {t: generar_M_rangos(N, M_RANGOS, fr) for t, fr in RANGOS.items()}

                    hits = set()
                    for nombre in estructuras_a_medir:
                        fila = una_estructura(nombre, estudiantes, busquedas, rangos)
                        hits.add((fila["encontrados"], fila["n_listado"]))
                        fila.update({"estructura": nombre, "orden": orden, "N": N,
                                     "M": M_BUSQUEDAS, "repeticion": rep})
                        escritor.writerow(fila)
                        archivo.flush()             # se guarda de inmediato: si se corta, no se pierde nada

                    # Chequeo de correctitud: las estructuras deben encontrar lo mismo y listar N estudiantes
                    assert len(hits) == 1 and list(hits)[0][1] == N, f"Las estructuras no coinciden: {hits}"

                    print(f"[{time.time() - inicio_total:7.1f}s] {orden:9s} N={N:<7d} repeticion {rep}/{REPETICIONES} lista")

    print(f"\nTerminado en {(time.time() - inicio_total) / 60:.1f} minutos. Resultados en {ruta}")


if __name__ == "__main__":
    main()