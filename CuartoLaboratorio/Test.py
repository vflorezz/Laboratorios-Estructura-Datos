import Quadtree

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
    nodo_prueba = Quadtree.Quadtree(0, 0, 1000, 1000)
    assert nodo_prueba.hallar_indice_hijo((400, 600)) == 0, f" Deberia ser NO"  # Deberia ser NO (0)
    assert nodo_prueba.hallar_indice_hijo((700, 600)) == 1, f" Deberia ser NE"  # Deberia ser NE (1)
    assert nodo_prueba.hallar_indice_hijo((200, 100)) == 2, f" Deberia ser SO"  # Deberia ser SO (2)
    assert nodo_prueba.hallar_indice_hijo((700, 200)) == 3, f" Deberia ser SE"  # Deberia ser SE (3)
    assert nodo_prueba.hallar_indice_hijo((500, 500)) == 1, f" Deberia ser NE"  # Deberia ser NE (1)  En el centro

    print("\nTodos los indices corresponden a la ubicacion de los puntos")

# Segunda prueba: Verificar que al construir el quadtree con los puntos, no se vaya a perder ninguno, que todos esten en el quadtree
def prueba_verificar_puntos_completos():
    centro = (ANCHO_CIUDAD / 2, LARGO_CIUDAD / 2)
    radio_ciudad_completa = Quadtree.distancia_2_puntos((0,0), (ANCHO_CIUDAD, LARGO_CIUDAD)) # Se halla el radio de todaa la ciudad
    puntos_encontrados = quadtree.busqueda_por_rango(centro, radio_ciudad_completa)          # Deberia contener todos los puntos (los 10.000)
    
    assert len(puntos_encontrados) == N_PUNTOS, f" Se perdieron puntos, el quadtree esta incompleto, no se insertaron todos"    # Si falla, entonces el quadtree perdio puntos

    print("\nEl quadtree tiene todos los puntos, todos se insertaron correctamente")

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