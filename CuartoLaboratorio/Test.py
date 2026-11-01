# pyright: reportOptionalSubscript=false
import os
import Quadtree
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
CARPETA_GRAFICAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Graficas")
os.makedirs(CARPETA_GRAFICAS, exist_ok = True)


# Todas en metros
ANCHO_CIUDAD = 10000
LARGO_CIUDAD = 10000
N_PUNTOS = 10000      # los 10.000 puntos de entrega
RADIO = 500


# Se generan los puntos y el árbol quadtree

lista_puntos = Quadtree.generar_N_puntos(N_PUNTOS, ANCHO_CIUDAD, LARGO_CIUDAD)
quadtree = Quadtree.Quadtree(0, 0, ANCHO_CIUDAD, LARGO_CIUDAD)

for punto in lista_puntos:
    quadtree.insertar(punto)  # Se inserta cada punto

# Tambien se generan los 100 puntos a consultar
lista_puntos_consultar = Quadtree.generar_N_puntos(100, ANCHO_CIUDAD, LARGO_CIUDAD, semilla = 9)


# # # Pruebas unitarias # # #

# Primera prueba: Verificar que cada punto si vaya al cuadrante que le corresponde
def prueba_puntos_indices_correctos():
    nodo_prueba = Quadtree.Quadtree(1000, 1000, 2000, 2000)
    assert nodo_prueba.hallar_indice_hijo((1400, 1600)) == 0, f" Deberia ser NO"  # Deberia ser NO (0)
    assert nodo_prueba.hallar_indice_hijo((1700, 1600)) == 1, f" Deberia ser NE"  # Deberia ser NE (1)
    assert nodo_prueba.hallar_indice_hijo((1200, 1100)) == 2, f" Deberia ser SO"  # Deberia ser SO (2)
    assert nodo_prueba.hallar_indice_hijo((1700, 1200)) == 3, f" Deberia ser SE"  # Deberia ser SE (3)
    assert nodo_prueba.hallar_indice_hijo((1500, 1500)) == 1, f" Deberia ser NE"  # Deberia ser NE (1)  En el centro

    print("\nTodos los indices corresponden a la ubicacion de los puntos")

# Segunda prueba: Verificar que al construir el quadtree con los puntos, no se vaya a perder ninguno, que todos esten en el quadtree
def prueba_verificar_puntos_completos():
    centro = (ANCHO_CIUDAD / 2, LARGO_CIUDAD / 2)
    radio_ciudad_completa = Quadtree.distancia_2_puntos((0,0), (ANCHO_CIUDAD, LARGO_CIUDAD)) # Se halla el radio de todaa la ciudad
    puntos_encontrados = quadtree.busqueda_por_rango(centro, radio_ciudad_completa)          # Deberia contener todos los puntos (los 10.000)
    
    assert len(puntos_encontrados) == N_PUNTOS, f" Se perdieron puntos, el quadtree esta incompleto, no se insertaron todos"    # Si falla, entonces el quadtree perdio puntos

    print("El quadtree tiene todos los puntos, todos se insertaron correctamente")

# Tercera prueba: Verificar que la busqueda por rango del quadtree coincida con la de fuerza bruta
def prueba_verificar_busqueda_por_rango():
    for punto_consultar in lista_puntos_consultar:
        puntos_en_rango_esperados = Quadtree.busqueda_rango_fbruta(lista_puntos, punto_consultar, RADIO)  # Resultado con fuerza bruta
        puntos_en_rango_obtenidos = quadtree.busqueda_por_rango(punto_consultar, RADIO)   # Resultado de la busqueda con quadtree

        assert sorted(puntos_en_rango_esperados) == sorted(puntos_en_rango_obtenidos), f" Los puntos encontrados en la busqueda por rango no coinciden, fallo en la busqueda para el punto {(punto_consultar)} "

    print ("Los resultados coincidieron para las 100 consultas en la busqueda por rango (fuerza bruta y quadtree)")

# Cuarta prueba: Verificar que la busqueda del vecino mas cercano del quadtree coincida con la de fuerza bruta
def prueba_verificar_busqueda_vecino_mas_cercano():
    for punto_consultar in lista_puntos_consultar:
        vecino_mas_cercano_esperado, menor_distancia_esperada = Quadtree.busqueda_vecino_mas_cercano_fbruta(lista_puntos, punto_consultar)  # Resultado de la busqueda del vecino con fuerza bruta
        vecino_mas_cercano_obtenido, menor_distancia_obtenida = quadtree.busqueda_vecino_mas_cercano(punto_consultar)     # Resultado de la busqueda del vecino con el quadtree

        assert vecino_mas_cercano_esperado == vecino_mas_cercano_obtenido and menor_distancia_esperada == menor_distancia_obtenida, f" Los resultados para la busqueda del vecino mas cercano no coinciden. Falla en el punto a encontrar su vecino mas cercano: {punto_consultar}"

    print("Los resultados coincidieron para las 100 consultas en la busqueda del vecino mas cercano (fuerza bruta y quadtree)")




# # #  Gráficas  # # #

# Separa una lista de puntos en dos listas, una con las x y otra con las y para que matplotlib pueda dibujar las graficas
def separar_coordenadas(lista_puntos):
    lista_de_x = []
    lista_de_y = []

    for punto in lista_puntos:
        lista_de_x.append(punto[0])
        lista_de_y.append(punto[1])

    return lista_de_x, lista_de_y


# Dibuja el rectangulo de cada hoja del quadtree
def dibujar_cuadrantes(nodo, dibujo):

    # Si es una hoja, se dibuja su rectangulo
    if (nodo.hijos is None):
        ancho = nodo.x_max - nodo.x_min
        alto =  nodo.y_max - nodo.y_min
        rectangulo = Rectangle((nodo.x_min, nodo.y_min), ancho, alto, fill = False, edgecolor = "green", linewidth = 0.6, zorder = 0)
        dibujo.add_patch(rectangulo)

    # Si es un nodo interno, se llama la función recursivamente a los hijos
    else:
        for hijo in nodo.hijos:
            dibujar_cuadrantes(hijo, dibujo)

def grafica_busqueda_por_rango():
    centro = (5000, 5000)
    puntos_encontrados = quadtree.busqueda_por_rango(centro, RADIO)

    todas_las_x, todas_las_y = separar_coordenadas(lista_puntos)
    las_x_encontradas, las_y_encontradas = separar_coordenadas(puntos_encontrados)

    # Una figura con dos dibujos lado a lado: la ciudad completa y un zoom al circulo
    figura, (dibujo_ciudad, dibujo_con_zoom) = plt.subplots(1, 2, figsize = (14, 7))

    for dibujo in (dibujo_ciudad, dibujo_con_zoom):
        dibujo.scatter(todas_las_x, todas_las_y, s = 4, color = "lightgray", label = "Puntos de entrega")
        dibujo.scatter(las_x_encontradas, las_y_encontradas, s = 30, color = "red", label = f"Dentro del radio ({len(puntos_encontrados)})")
        dibujo.scatter(centro[0], centro[1], s = 100, color = "blue", marker = "x", label = "Centro de la busqueda")
        dibujo.add_patch(Circle(centro, RADIO, fill = False, color = "blue", linewidth = 2))   # el circulo con radio de 500
        dibujo.set_aspect("equal")          # mismo tamaño en x e y, para que el circulo se vea circulo
        dibujo.set_xlabel("x (metros)")
        dibujo.set_ylabel("y (metros)")
        dibujo.legend(loc = "upper right")

    dibujo_ciudad.set_title("Ciudad completa")

    # El acercamiento muestra solo la zona alrededor del circulo
    dibujo_con_zoom.set_xlim(centro[0] - 1.5 * RADIO, centro[0] + 1.5 * RADIO)
    dibujo_con_zoom.set_ylim(centro[1] - 1.5 * RADIO, centro[1] + 1.5 * RADIO)
    dibujo_con_zoom.set_title("Zoom al circulo")

    # Se dibujan los cuadrantes (las hojas del quadtree) en el acercamiento
    dibujar_cuadrantes(quadtree, dibujo_con_zoom)

    figura.suptitle(f"Busqueda por rango con el quadtree: radio de {RADIO} m")
    plt.savefig(os.path.join(CARPETA_GRAFICAS, "grafica_busqueda_por_rango.png"), dpi = 150)     # se guarda la imagen para el repositorio
    plt.close()

def grafica_vecino_mas_cercano():
    punto_consultar = (4000, 6000)
    vecino_mas_cercano, menor_distancia = quadtree.busqueda_vecino_mas_cercano(punto_consultar)

    todas_las_x, todas_las_y = separar_coordenadas(lista_puntos)

    # Una figura con dos dibujos lado a lado: la ciudad completa y un acercamiento
    figura, (dibujo_ciudad, dibujo_con_zoom) = plt.subplots(1, 2, figsize = (14, 7))

    for dibujo in (dibujo_ciudad, dibujo_con_zoom):
        dibujo.scatter(todas_las_x, todas_las_y, s = 4, color = "lightgray", label = "Puntos de entrega")
        dibujo.scatter(punto_consultar[0], punto_consultar[1], s = 100, color = "blue", marker = "x", label = "Punto consultado")
        dibujo.scatter(vecino_mas_cercano[0], vecino_mas_cercano[1], s = 60, color = "red", label = f"Vecino mas cercano ({round(menor_distancia, 2)} m)")          # type: ignore
        dibujo.plot([punto_consultar[0], vecino_mas_cercano[0]], [punto_consultar[1], vecino_mas_cercano[1]], color = "red", linewidth = 1)   # linea entre la consulta y su vecino
        dibujo.add_patch(Circle(punto_consultar, menor_distancia, fill = False, color = "blue", linestyle = "--"))   # circulo de comprobacion     # type: ignore
        dibujo.set_aspect("equal")
        dibujo.set_xlabel("x (metros)")
        dibujo.set_ylabel("y (metros)")
        dibujo.legend(loc = "upper right")

    dibujo_ciudad.set_title("Ciudad completa")

    # El acercamiento se ajusta a la distancia: se ve una zona 10 veces mas grande que la distancia al vecino
    margen = 10 * menor_distancia                                                                                                       # type: ignore
    dibujo_con_zoom.set_xlim(punto_consultar[0] - margen, punto_consultar[0] + margen)
    dibujo_con_zoom.set_ylim(punto_consultar[1] - margen, punto_consultar[1] + margen)
    dibujo_con_zoom.set_title("Zoom al circulo")

    dibujar_cuadrantes(quadtree, dibujo_con_zoom)

    figura.suptitle("Vecino mas cercano con el quadtree")
    plt.savefig(os.path.join(CARPETA_GRAFICAS, "grafica_vecino_mas_cercano.png"), dpi = 150)
    plt.close()



if __name__ == "__main__":

    # Primero las pruebas
    prueba_puntos_indices_correctos()
    prueba_verificar_puntos_completos()
    prueba_verificar_busqueda_por_rango()
    prueba_verificar_busqueda_vecino_mas_cercano()

    # Luego, las graficas
    grafica_busqueda_por_rango()
    grafica_vecino_mas_cercano()