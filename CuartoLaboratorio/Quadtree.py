# pyright: reportOptionalSubscript=false
import random

# Esta función genera los puntos de manera uniforme y aleatoria en el mapa en metros  
def generar_N_puntos(N_puntos, ancho_ciudad, largo_ciudad, semilla = 42):             # N_puntos es la cantidad de puntos que se quieran generar y semilla es para inicializar el generador de números "aleatorios"

    generador = random.Random(semilla)   # generador guarda un generador propio con una semilla fija, esto va a ayudar a que obtenga siempre los mismos puntos sin importar cuantas veces corra el codigo o si alguien mas quiere correrlo (la semilla no necesariamente tiene que ser 42)
    lista_puntos = []

    for _ in range (N_puntos):
        punto = (generador.uniform(0, ancho_ciudad), generador.uniform(0, largo_ciudad))
        lista_puntos.append(punto)

    return lista_puntos

# Esta función calcula la distancia entre dos puntos (distancia euclidiana) en Metros
def distancia_2_puntos(a, b):
    return (((b[0] - a[0])**2) + ((b[1] - a[1])**2))**(1/2)   # esta es la ecuacion para la distancia entre dos puntos, retorna el resultado


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


# # # #   El Quadtree 2D    # # # #
# Cada nodo representa un rectangulo del mapa. Si el nodo es una hoja, guarda puntos, sino entonces, reparte a los 4 hijos (NO, NE, SO, SE)

class Quadtree:

    def __init__(self, x_min, y_min, x_max, y_max, capacidad = 8, nivel_nodo = 0, profundidad_max = 20):

        # Estos son los límites del rectángulo que representa (cubre) este nodo (la base y la altura)
        self.x_min = x_min
        self.y_min = y_min

        self.x_max = x_max
        self.y_max = y_max

        self.capacidad = capacidad              # Cuantos puntos le caben a una hoja antes de dividirse en 4 cuadrantes
        self.nivel_nodo = nivel_nodo          # En qué nivel esta el nodo (la raiz tiene profundidad o nivel = 0)
        self.profundidad_max = profundidad_max  # Este es un límite para evitar divisiones infinitas, por eso se delimita un tope para proteger contra los puntos duplicados. Es un limite en el nivel del nodo

        self.puntos = []        # son los puntos guardados (SOLO se usa si es una HOJA)
        self.hijos = None       # None indica que es una hoja, si se divide la hoja, entonces se vuelve una lista de 4 nodos (NO, NE, SO, SE)


    # Este método dice si un punto cae dentro del rectángulo de este nodo (incluye los bordes tmb). True si esta.
    def contiene_punto(self, punto_verificar):
        if ((self.x_min <= punto_verificar[0] <= self.x_max) and (self.y_min <= punto_verificar[1] <= self.y_max)):  # Primero se verfica la coordenada en x (por eso el punto se mira en 0) y luego la y (por es el punto se mira en 1)
            return True
        else:
            return False

    # Este método dice a cuál de los 4 cuadrantes (hijos), pertenece un punto: 0 (NO), 1 (NE), 2 (SO) y 3 (SE)
    def hallar_indice_hijo(self, punto):

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
        nivel_nodo = self.nivel_nodo + 1    # el nivel al que esta el nodo (los hijos: padre + 1)

        hijo_NO = Quadtree(self.x_min, y_medio_nodo, x_medio_nodo, self.y_max, self.capacidad, nivel_nodo, self.profundidad_max) # NO: Noroeste (arriba a la izquierda) 
        hijo_NE = Quadtree(x_medio_nodo, y_medio_nodo, self.x_max, self.y_max, self.capacidad, nivel_nodo, self.profundidad_max) # NE: Noreste  (arriba a la derecha)
        hijo_SO = Quadtree(self.x_min, self.y_min, x_medio_nodo, y_medio_nodo, self.capacidad, nivel_nodo, self.profundidad_max) # SO: Suroeste (abajo a la izquierda)
        hijo_SE = Quadtree(x_medio_nodo, self.y_min, self.x_max, y_medio_nodo, self.capacidad, nivel_nodo, self.profundidad_max) # SE: Sureste (abajo a la derecha)

        # Ahora se vuelve una lista de 4 nodos porque el nodo dejo de ser una hoja. Son los 4 hijos (cuadrantes)
        self.hijos = [hijo_NO, hijo_NE, hijo_SO, hijo_SE]

        for punto in self.puntos:       # Se va insertando cada punto en el cuadrante correspondiente usando el metodo indice_hijo e insertar
            self.hijos[self.hallar_indice_hijo(punto)].insertar(punto)

        self.puntos = []   # Queda vacia porque un nodo interno no guarda puntos

    # Inserta un punto dentro de un rectangulo (nodo), True si se insertó, False si ese punto no pertencia a ese rectangulo (nodo)
    def insertar(self, punto_insertar):

        # Se verifica que ese punto si pertenezca al rectangulo donde lo quiero ingresar
        if (not self.contiene_punto(punto_insertar)):
            return False                               # No lo contiene (no esta dentro de los límites)

        # Si es una hoja, o sea, si NO es un nodo interno (que contendria los 4 cuadrantes (nodos))
        if (self.hijos is None):
            if (len(self.puntos) < self.capacidad or self.nivel_nodo >= self.profundidad_max):
                self.puntos.append(punto_insertar)
                return True

            self.subdividir()   # Esto es cuando se llena la lista de puntos, entonces se subdivide el nodo (rectangulo)
        
        # Esto es cuando o era un nodo interno con 4 cuadrantes, o cuando se llena y se subdivide y despues hay que insertarlo en el nodo (cuadrante/rectangulo) correspondiente
        return self.hijos[self.hallar_indice_hijo(punto_insertar)].insertar(punto_insertar)

    # Este método ayuda a saber la distancia minima a un rectangulo (uno de los nodos o cuadrantes) de un punto determinado, esto sirve para saber si vale la pena visitarlo o si de por si ya esta muy lejos/se pasa del rango cuando se busca por rango
    def distancia_minima_a_rectangulo(self, punto):

        # Se guardan las coordenadas x e y del punto a mirar
        x_punto = punto[0]
        y_punto = punto[1]

        # Primero se halla la coordenada en x del rectangulo mas cercano a mi punto (es un punto, pero es la coordenada en x de donde empieza ese rectangulo)
        if (x_punto < self.x_min):
            x_rect_cercano = self.x_min      # Si el punto con su coordenada en x esta a la izq del rectangulo, entonces el punto del rectangulo en x va a estar en self.x_min (el borde del rect esta a su derecha)
        elif (x_punto > self.x_max):
            x_rect_cercano = self.x_max      # Si el punto con su coordenada en x esta a la der del rectangulo, entonces el punto del rectangulo en x va a estar en self.x_max (el borde del rect esta a su izquierda)
        else:
            x_rect_cercano = x_punto         # Esto ocurre si el punto ya esta dentro de ese rectangulo, el punto en su x es el mismo x_punto

        # Ahora en y, la coordenada del punto del rectangulo mas cercano a mi punto

        if (y_punto < self.y_min):
            y_rect_cercano = self.y_min     # En y el punto esta debajo del rectangulo, el punto coordenada en y mas cercano es self.y_min
        elif (y_punto > self.y_max):
            y_rect_cercano = self.y_max     # En y el punto esta arriba del rectangulo, el punto coordenada en y mas cercano es self.y_max
        else:
            y_rect_cercano = y_punto        # En y el punto esta dentro del rectangulo, el punto coordenada en y mas cercano es el mismo y_punto

        punto_mas_cercano_del_rectangulo = (x_rect_cercano, y_rect_cercano)

        return distancia_2_puntos(punto, punto_mas_cercano_del_rectangulo)    # La distancia entre esos dos puntos (el punto que se estaba mirando y el punto del rectangulo que esta mas cercano al punto que se esta mirando). Si se esta dentro del rectangulo la distancia es 0

    # Este metodo es la busqueda por rango del quadtree, centro (es el punto), radio es el radio de busqueda y la lista de encontrados que es None pero cambia en el primer llamado de la función
    def busqueda_por_rango(self, centro, radio, lista_encontrados = None):

        # Esto ocurre solo en la primera llamada, donde como la lista esta en None, se inicializa como vacía
        if (lista_encontrados is None):
            lista_encontrados = []

        #  Mira si vale la pena visitar ese rectangulo (si el punto (centro) esta mas lejos del rectangulo (nodo actual), superando el radio de busqueda. Pero si el punto ya esta dentro del rectangulo, esa distancia es cero porque esta dentro) 
        if (self.distancia_minima_a_rectangulo(centro) > radio):
            return lista_encontrados  # la devuelve sin agregar nada porque esta muy lejos el rectangulo

        # Si el nodo es una hoja (y pasa la prueba, si vale la pena revisar el rectangulo o nodo, que en este caso es hoja)
        if (self.hijos is None):
            for punto in self.puntos:     # Se recorren los puntos almacenados en la lista de puntos de esa hoja
                if (distancia_2_puntos(punto, centro) <= radio):         # Si el punto esta dentro de ese radio
                    lista_encontrados.append(punto)

            return lista_encontrados

        # Si el nodo es interno (no hoja, sino que tiene 4 hijos, los 4 cuadrantes NO, NE, SE, SO)
        for hijo in self.hijos:
            hijo.busqueda_por_rango(centro, radio, lista_encontrados)   # Se mira en ese hijo, por eso se vuelve a llamar a la función

        return lista_encontrados  # Retorna la lista de puntos encontrados