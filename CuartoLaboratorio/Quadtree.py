import math
import random

# El mapa es un cuadrado de 10km por 10km, pero como las coordenadas están en metros, se escriben esas cantidades en metros
ANCHO_MAPA = 10_000    # 10.000 metros o 10 km
ALTO_MAPA = 10_000     # 10.000 metros o 10 km


# Esta función genera los puntos de manera uniforme y aleatoria en el mapa en metros  
def generar_N_puntos(N_puntos, semilla = 42):             # N_puntos es la cantidad de puntos que se quieran generar y semilla es para inicializar el generador de números "aleatorios"

    generador = random.Random(semilla)   # generador guarda un generador propio con una semilla fija, esto va a ayudar a que obtenga siempre los mismos puntos sin importar cuantas veces corra el codigo o si alguien mas quiere correrlo (la semilla no necesariamente tiene que ser 42)
    lista_puntos = []

    for _ in range (N_puntos):
        punto = (generador.uniform(0, ANCHO_MAPA), generador.uniform(0, ALTO_MAPA))
        lista_puntos.append(punto)

    return lista_puntos

# Esta función calcula la distancia entre dos puntos (distancia euclidiana) en Metros
def distancia_2_puntos(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])   # La función math.hypot hace el calculo de la ecuacion para la distancia entre dos puntos


# # #   Fuerza Bruta!  # # #

# busqueda dentro de un radio (Range Search) con fuerza bruta, devuelve todos los puntos que esten a una distancia <= al radio del centro. Como es fuerza bruta, revisa TODOS
def busqueda_rango_fbruta(lista_puntos, centro, radio):        # El centro es el punto dado y el radio es el radio en metros a buscar otros puntos cercanos
    resultado_puntos = []
    for punto in lista_puntos:
        if (distancia_2_puntos(punto, centro) <= radio):
            resultado_puntos.append(punto)

    return resultado_puntos

# busqueda del vecino más cercano con fuerza bruta, se miran todos los puntos y el punto a encontrarle su vecino más cercano. Devuelve el vecino más cercano de ese punto
def busqueda_vecino_mas_cercano_fbruta(lista_puntos, punto_consultar_vecino_cercano):
    vecino_mas_cercano = lista_puntos[0]
    menor_distancia = distancia_2_puntos(lista_puntos[0], punto_consultar_vecino_cercano)

    for punto in lista_puntos:
        distancia = distancia_2_puntos(punto, punto_consultar_vecino_cercano)
        if (distancia < menor_distancia):
            vecino_mas_cercano = punto
            menor_distancia = distancia

    return vecino_mas_cercano, menor_distancia


# # # #   El Quadtree (Point Region) 2D    # # # #
# Cada nodo representa un rectangulo del mapa. Si el nodo es una hoja, guarda puntos, sino entonces, reparte a los 4 hijos (N, S, E, O)

class Quadtree:

    def __init__(self, x_min, y_min, x_max, y_max, capacidad = 4, profundidad = 0, profundidad_max = 20):

        # Estos son los límites del rectángulo que representa (cubre) este nodo (la base y la altura)
        self.x_min = x_min
        self.y_min = y_min

        self.x_max = x_max
        self.y_max = y_max

        self.capacidad = capacidad              # Cuantos puntos le caben a una hoja antes de dividirse en 4 cuadrantes
        self.profundidad = profundidad          # En qué nivel esta el nodo (la raiz tiene profundidad o nivel = 0)
        self.profundidad_max = profundidad_max  # Este es un límite para evitar divisiones infinitas, por eso se delimita un tope para proteger contra los puntos duplicados

        self.puntos = []        # son los puntos guardados (solo se usa si es una hoja)
        self.hijos = None       # None indica que es una hoja, si se divide la hoja, entonces se vuelve una lista de 4 nodos (N, S, E, O)


    # Este método dice si un punto cae dentro del rectángulo de este nodo (incluye los bordes tmb)
    def contiene_punto(self, punto_verificar):
        if ((self.x_min <= punto_verificar[0] <= self.x_max) and (self.y_min <= punto_verificar[1] <= self.y_max)):  # Primero se verfica la coordenada en x (por eso el punto se mira en 0) y luego la y (por es el punto se mira en 1)
            return True
        else:
            return False