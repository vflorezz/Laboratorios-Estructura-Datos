# pyright: reportOptionalSubscript=false
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
# Cada nodo representa un rectangulo del mapa. Si el nodo es una hoja, guarda puntos, sino entonces, reparte a los 4 hijos (NO, NE, SO, SE)

class Quadtree:

    def __init__(self, x_min, y_min, x_max, y_max, capacidad = 8, profundidad = 0, profundidad_max = 20):

        # Estos son los límites del rectángulo que representa (cubre) este nodo (la base y la altura)
        self.x_min = x_min
        self.y_min = y_min

        self.x_max = x_max
        self.y_max = y_max

        self.capacidad = capacidad              # Cuantos puntos le caben a una hoja antes de dividirse en 4 cuadrantes
        self.profundidad = profundidad          # En qué nivel esta el nodo (la raiz tiene profundidad o nivel = 0)
        self.profundidad_max = profundidad_max  # Este es un límite para evitar divisiones infinitas, por eso se delimita un tope para proteger contra los puntos duplicados

        self.puntos = []        # son los puntos guardados (solo se usa si es una hoja)
        self.hijos = None       # None indica que es una hoja, si se divide la hoja, entonces se vuelve una lista de 4 nodos (NO, NE, SO, SE)


    # Este método dice si un punto cae dentro del rectángulo de este nodo (incluye los bordes tmb). True si esta.
    def contiene_punto(self, punto_verificar):
        if ((self.x_min <= punto_verificar[0] <= self.x_max) and (self.y_min <= punto_verificar[1] <= self.y_max)):  # Primero se verfica la coordenada en x (por eso el punto se mira en 0) y luego la y (por es el punto se mira en 1)
            return True
        else:
            return False

    # Este método dice a cuál de los 4 cuadrantes (hijos), pertenece un punto: 0 (NO), 1 (NE), 2 (SO) y 3 (SE)
    def indice_hijo(self, punto):

        # Se calcula primero el centro del rectangulo
        x_medio_nodo = (self.x_max + self.x_min) / 2
        y_medio_nodo = (self.y_max + self.y_min) / 2

        indice = 0   # Se inicializa en cero o sea NO (Noroeste) arriba a la izquierda

        if (punto[0] >= x_medio_nodo and punto[1] >= y_medio_nodo):
            indice = 1  # NE (Noreste)
        elif (punto[0] >= x_medio_nodo):   # Se sabe que ya arriba es el caso de y arriba en la derecha, entonces este es y abajo en la derecha
            indice = 3  # SE (Sureste)
        elif (punto[0] < x_medio_nodo and punto[1] < y_medio_nodo):    # Abajo a la izquierda
            indice = 2  # SO (Suroeste)

        return indice

    def subdividir(self):

        # Se calcula primero el centro del rectangulo
        x_medio_nodo = (self.x_max + self.x_min) / 2
        y_medio_nodo = (self.y_min + self.y_max) / 2
        profun = self.profundidad + 1    # el nivel al que esta el nodo (los hijos: padre + 1)

        # Ahora se vuelve una lista de 4 nodos porque el nodo dejo de ser una hoja. Son los 4 hijos (cuadrantes)
        self.hijos = [
            Quadtree(self.x_min, y_medio_nodo, x_medio_nodo, self.y_max, self.capacidad, profun, self.profundidad_max),    # NO: Noroeste (arriba a la izquierda) 
            Quadtree(x_medio_nodo, y_medio_nodo, self.x_max, self.y_max, self.capacidad, profun, self.profundidad_max),    # NE: Noreste  (arriba a la derecha)
            Quadtree(self.x_min, self.y_min, x_medio_nodo, y_medio_nodo, self.capacidad, profun, self.profundidad_max),    # SO: Suroeste (abajo a la izquierda)
            Quadtree(x_medio_nodo, self.y_min, self.x_max, y_medio_nodo, self.capacidad, profun, self.profundidad_max)     # SE: Sureste (abajo a la derecha)
        ]

        for punto in self.puntos:       # Se va insertando cada punto en el cuadrante correspondiente usando el metodo indice_hijo e insertar
            self.hijos[self.indice_hijo(punto)].insertar(punto)

        self.puntos = []   # Queda vacia porque un nodo interno no guarda puntos

    # Inserta un punto dentro de un rectangulo (nodo), True si se insertó, False si ese punto no pertencia a ese rectangulo (nodo)
    def insertar(self, punto_insertar):

        # Se verifica que ese punto si pertenezca al rectangulo donde lo quiero ingresar
        if (not self.contiene_punto(punto_insertar)):
            return False                               # No lo contiene (no esta dentro de los límites)

        # Si es una hoja, o sea, si NO es un nodo interno que contendria los 4 cuadrantes (nodos)
        if (self.hijos is None):
            if (len(self.puntos) < self.capacidad or self.profundidad >= self.profundidad_max):
                self.puntos.append(punto_insertar)
                return True

            self.subdividir()   # Esto es cuando se llena la lista de puntos, entonces se subdivide el nodo (rectangulo)
        
        # Esto es cuando o era un nodo interno con 4 cuadrantes, o cuando se llena y se subdivide y despues hay que insertarlo en el nodo (cuadrante/rectangulo) correspondiente
        return self.hijos[self.indice_hijo(punto_insertar)].insertar(punto_insertar)