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
def test_puntos_insertados_correctamente():
    nodo_prueba = Quadtree.Quadtree(0, 0, 1000, 1000)
    assert nodo_prueba.hallar_indice_hijo((400, 600)) == 0  # Deberia ser NO (0)
    assert nodo_prueba.hallar_indice_hijo((700,600))  == 1  # Deberia ser NE (1)
    assert nodo_prueba.hallar_indice_hijo((200, 100)) == 2  # Deberia ser SO (2)
    assert nodo_prueba.hallar_indice_hijo((700, 200)) == 3  # Deberia ser SE (3)
    assert nodo_prueba.hallar_indice_hijo((500, 500)) == 1  # Deberia ser NE (1)  En el centro

# Segunda prueba: Verificar que al construir el quadtree con los puntos, no se vaya a perder ninguno, que todos esten en el quadtree
