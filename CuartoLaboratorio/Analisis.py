import os
import time
import Quadtree
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator
CARPETA_GRAFICAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Graficas")
os.makedirs(CARPETA_GRAFICAS, exist_ok = True)

# Todas en metros
ANCHO_CIUDAD = 10000
LARGO_CIUDAD = 10000
RADIO = 500
M_CONSULTAS = 100        # consultas que se hacen en cada repeticion
N_REPETICIONES = 40      # veces que se repite la medicion de cada tamaño
TAMANOS = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000]     # cantidades de puntos a probar

# La carpeta Graficas queda junto a este archivo (se crea sola si no existe)
CARPETA_GRAFICAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Graficas")
os.makedirs(CARPETA_GRAFICAS, exist_ok = True)

# Textos de las graficas
SUBTITULO = (f"Puntos de entrega uniformes en una ciudad de {ANCHO_CIUDAD:,} m x {LARGO_CIUDAD:,} m").replace(",", ".")

NOTA_COMPARACION = (f"Promedio de {N_REPETICIONES} repeticiones; barras = ±1 desviación estándar; ejes en escala logarítmica.\n"
                    f"Cada repetición genera puntos nuevos y hace M = {M_CONSULTAS} consultas. Pendiente de la leyenda: recta ajustada\n"
                    "en escala log-log (≈ 1 lineal, ≈ 2 cuadrática, cerca de 0 crecimiento muy lento).\n"
                    "Línea punteada: cruce de las dos curvas; desde ese N el quadtree es más rápido que la fuerza bruta.")

NOTA_CONSTRUCCION = (f"Promedio de {N_REPETICIONES} repeticiones; barras = ±1 desviación estándar; ejes en escala logarítmica.\n"
                     "Cada repetición inserta uno a uno los N puntos en una lista vacía (append) y en un quadtree vacío; no se cuenta\n"
                     "la generación de los puntos. Pendiente de la leyenda: recta ajustada en escala log-log (≈ 1 lineal).")


# Una repeticion para un tamaño n: genera puntos y consultas nuevos, arma las dos estructuras y mide cada metodo (tiempos en segundos)
def medir_una_repeticion(n, repeticion):
    lista_puntos = Quadtree.generar_N_puntos(n, ANCHO_CIUDAD, LARGO_CIUDAD, semilla = 42 + repeticion)
    consultas = Quadtree.generar_N_puntos(M_CONSULTAS, ANCHO_CIUDAD, LARGO_CIUDAD, semilla = 1000 + repeticion)

    # Insercion en la lista (fuerza bruta): lista vacia y los n puntos uno por uno con append
    inicio = time.perf_counter()
    lista_fbruta = []
    for punto in lista_puntos:
        lista_fbruta.append(punto)
    tiempo_construccion_lista = time.perf_counter() - inicio

    # Insercion en el quadtree: crear la raiz e insertar los n puntos uno por uno
    inicio = time.perf_counter()
    quadtree = Quadtree.Quadtree(0, 0, ANCHO_CIUDAD, LARGO_CIUDAD)
    for punto in lista_puntos:
        quadtree.insertar(punto)
    tiempo_construccion = time.perf_counter() - inicio

    # Busqueda por rango con fuerza bruta
    inicio = time.perf_counter()
    for consulta in consultas:
        Quadtree.busqueda_rango_fbruta(lista_fbruta, consulta, RADIO)
    rango_fbruta = time.perf_counter() - inicio

    # Busqueda por rango con quadtree
    inicio = time.perf_counter()
    for consulta in consultas:
        quadtree.busqueda_por_rango(consulta, RADIO)
    rango_quadtree = time.perf_counter() - inicio

    # Vecino mas cercano con fuerza bruta
    inicio = time.perf_counter()
    for consulta in consultas:
        Quadtree.busqueda_vecino_mas_cercano_fbruta(lista_fbruta, consulta)
    vecino_fbruta = time.perf_counter() - inicio

    # Vecino mas cercano con quadtree
    inicio = time.perf_counter()
    for consulta in consultas:
        quadtree.busqueda_vecino_mas_cercano(consulta)
    vecino_quadtree = time.perf_counter() - inicio

    return tiempo_construccion_lista, tiempo_construccion, rango_fbruta, rango_quadtree, vecino_fbruta, vecino_quadtree


def calcular_promedio(lista):
    return sum(lista) / len(lista)


# Desviacion estandar de la muestra (se divide entre len - 1)
def calcular_desviacion(lista):
    promedio = calcular_promedio(lista)
    suma = 0
    for valor in lista:
        suma += (valor - promedio) ** 2
    return (suma / (len(lista) - 1)) ** 0.5


# Repite la medicion N_REPETICIONES veces para un tamaño n y devuelve el promedio y la desviacion de cada metrica
def medir_tamano(n):
    tiempos_construccion_lista = []
    tiempos_construccion = []
    tiempos_rango_fbruta = []
    tiempos_rango_quadtree = []
    tiempos_vecino_fbruta = []
    tiempos_vecino_quadtree = []

    for repeticion in range(N_REPETICIONES):
        cl, c, rfb, rqt, vfb, vqt = medir_una_repeticion(n, repeticion)
        tiempos_construccion_lista.append(cl)
        tiempos_construccion.append(c)
        tiempos_rango_fbruta.append(rfb)
        tiempos_rango_quadtree.append(rqt)
        tiempos_vecino_fbruta.append(vfb)
        tiempos_vecino_quadtree.append(vqt)

    return (calcular_promedio(tiempos_construccion_lista), calcular_desviacion(tiempos_construccion_lista),
            calcular_promedio(tiempos_construccion), calcular_desviacion(tiempos_construccion),
            calcular_promedio(tiempos_rango_fbruta), calcular_desviacion(tiempos_rango_fbruta),
            calcular_promedio(tiempos_rango_quadtree), calcular_desviacion(tiempos_rango_quadtree),
            calcular_promedio(tiempos_vecino_fbruta), calcular_desviacion(tiempos_vecino_fbruta),
            calcular_promedio(tiempos_vecino_quadtree), calcular_desviacion(tiempos_vecino_quadtree))


# Calcula la pendiente de la recta que mejor se ajusta a los puntos (n, tiempo) en escala log-log (minimos cuadrados)
def calcular_pendiente(tamanos, tiempos):
    xs = []
    ys = []
    for i in range(len(tamanos)):
        xs.append(math.log10(tamanos[i]))
        ys.append(math.log10(tiempos[i]))

    x_promedio = sum(xs) / len(xs)
    y_promedio = sum(ys) / len(ys)

    arriba = 0
    abajo = 0
    for i in range(len(xs)):
        arriba += (xs[i] - x_promedio) * (ys[i] - y_promedio)
        abajo += (xs[i] - x_promedio) ** 2

    return arriba / abajo


# Devuelve el N donde se cortan las dos lineas de la grafica (el quadtree pasa de ser mas lento a ser mas rapido). None si no se cortan
def hallar_cruce(tamanos, tiempos_fbruta, tiempos_quadtree):
    for i in range(1, len(tamanos)):
        diferencia_antes = math.log10(tiempos_quadtree[i - 1]) - math.log10(tiempos_fbruta[i - 1])
        diferencia_despues = math.log10(tiempos_quadtree[i]) - math.log10(tiempos_fbruta[i])

        # Antes el quadtree era mas lento (diferencia > 0) y despues es mas rapido (diferencia <= 0): ahi se cruzan
        if (diferencia_antes > 0 and diferencia_despues <= 0):
            x_antes = math.log10(tamanos[i - 1])
            x_despues = math.log10(tamanos[i])
            x_cruce = x_antes + (0 - diferencia_antes) * (x_despues - x_antes) / (diferencia_despues - diferencia_antes)
            return 10 ** x_cruce

    return None


# Grafica con el mismo estilo para todas: una linea por metodo, en log-log, con barras de error y la pendiente en la leyenda
# lineas es una lista de tuplas: (nombre, promedios, desviaciones, color, marcador)
def graficar(tamanos, lineas, titulo, subtitulo, etiqueta_y, nota, nombre_archivo, cruce = None):
    figura, dibujo = plt.subplots(figsize = (9, 6.5))

    for nombre, promedios, desviaciones, color, marcador in lineas:
        pendiente = str(round(calcular_pendiente(tamanos, promedios), 2)).replace(".", ",")
        dibujo.errorbar(tamanos, promedios, yerr = desviaciones, marker = marcador, color = color, capsize = 4, linewidth = 2, label = f"{nombre} (pendiente {pendiente})")

    dibujo.set_xscale("log")
    dibujo.set_yscale("log")

    # Las marcas del eje x son los tamaños probados (con punto de miles: 1.000, 10.000...)
    dibujo.set_xticks(tamanos)
    dibujo.set_xticklabels([f"{n:,}".replace(",", ".") for n in tamanos], rotation = 45)
    dibujo.xaxis.set_minor_locator(NullLocator())      # quita las marcas pequeñas del eje x

    # Si las lineas se cruzan, se marca el cruce con una linea vertical punteada (aparece en la leyenda)
    if (cruce is not None):
        dibujo.axvline(cruce, color = "gray", linestyle = "--", linewidth = 1.5, label = f"Cruce: el quadtree es más rápido desde N ≈ {round(cruce)}")

    dibujo.set_xlabel("Cantidad de puntos de entrega N")
    dibujo.set_ylabel(etiqueta_y)
    dibujo.set_title(subtitulo, fontsize = 10)
    dibujo.grid(True, which = "both", linestyle = "-", alpha = 0.25)
    dibujo.legend()

    figura.suptitle(titulo, fontweight = "bold", fontsize = 13)
    figura.text(0.5, 0.01, nota, ha = "center", va = "bottom", fontsize = 8, color = "dimgray")
    figura.tight_layout(rect = [0, 0.14, 1, 0.97])                                                         # type: ignore

    plt.savefig(os.path.join(CARPETA_GRAFICAS, nombre_archivo), dpi = 150)
    plt.close()



if __name__ == "__main__":

    construccion_lista_prom, construccion_lista_desv = [], []
    construccion_prom, construccion_desv = [], []
    rango_fb_prom, rango_fb_desv = [], []
    rango_qt_prom, rango_qt_desv = [], []
    vecino_fb_prom, vecino_fb_desv = [], []
    vecino_qt_prom, vecino_qt_desv = [], []

    for n in TAMANOS:
        print(f"Midiendo n = {n} ({N_REPETICIONES} repeticiones)...")
        cl_p, cl_d, c_p, c_d, rfb_p, rfb_d, rqt_p, rqt_d, vfb_p, vfb_d, vqt_p, vqt_d = medir_tamano(n)

        construccion_lista_prom.append(cl_p)
        construccion_lista_desv.append(cl_d)
        construccion_prom.append(c_p)
        construccion_desv.append(c_d)
        rango_fb_prom.append(rfb_p)
        rango_fb_desv.append(rfb_d)
        rango_qt_prom.append(rqt_p)
        rango_qt_desv.append(rqt_d)
        vecino_fb_prom.append(vfb_p)
        vecino_fb_desv.append(vfb_d)
        vecino_qt_prom.append(vqt_p)
        vecino_qt_desv.append(vqt_d)


    # Cruces (se muestran en las graficas)
    cruce_rango = hallar_cruce(TAMANOS, rango_fb_prom, rango_qt_prom)
    cruce_vecino = hallar_cruce(TAMANOS, vecino_fb_prom, vecino_qt_prom)

    # Graficas (se guardan en la carpeta Graficas)
    graficar(TAMANOS,
             [("Fuerza bruta", rango_fb_prom, rango_fb_desv, "#457b9d", "o"),
              ("Quadtree", rango_qt_prom, rango_qt_desv, "#386641", "s")],
             "Búsqueda por rango: tiempo vs. N",
             f"Radio de {RADIO} m · " + SUBTITULO,
             f"Tiempo total de {M_CONSULTAS} consultas (segundos)",
             NOTA_COMPARACION, "analisis_rango.png", cruce = cruce_rango)

    graficar(TAMANOS,
             [("Fuerza bruta", vecino_fb_prom, vecino_fb_desv, "#457b9d", "o"),
              ("Quadtree", vecino_qt_prom, vecino_qt_desv, "#386641", "s")],
             "Vecino más cercano: tiempo vs. N",
             "Consultas en ubicaciones aleatorias · " + SUBTITULO,
             f"Tiempo total de {M_CONSULTAS} consultas (segundos)",
             NOTA_COMPARACION, "analisis_vecino.png", cruce = cruce_vecino)

    graficar(TAMANOS,
             [("Lista (fuerza bruta): inserción con append", construccion_lista_prom, construccion_lista_desv, "#457b9d", "o"),
              ("Quadtree: inserción de los N puntos", construccion_prom, construccion_desv, "#386641", "s")],
             "Inserción de N puntos: lista (fuerza bruta) vs. quadtree",
             SUBTITULO,
             "Tiempo de inserción de los N puntos (segundos)",
             NOTA_CONSTRUCCION, "analisis_construccion.png")