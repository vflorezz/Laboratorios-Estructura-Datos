# Laboratorio #4: Sistema de Logística de Entregas

## 1. Descripción del Problema y Objetivo

Se tienen las coordenadas (x, y) de **10.000 puntos de entrega** en una ciudad, y se necesita un sistema que pueda responder dos cosas: qué puntos de entrega están a un radio de **500 metros** de un punto dado, y cuál es el punto de entrega **más cercano** a una ubicación dada. Los datos son estáticos (no cambian).
 
Los puntos se generan al azar usando una semilla, para que los resultados se puedan repetir, en una ciudad de 10.000 m × 10.000 m. Todo está en metros.

### Objetivos

- Implementar un Quadtree desde cero (en 2D) que responda las necesidades del sistema de entregas.
- Comparar el rendimiento del Quadtree con la fuerza bruta (una lista).
- Visualizar y verificar los resultados de las búsquedas.
- Responder desde qué tamaño de datos el Quadtree empieza a ser más rápido que la fuerza bruta.

## Estructuras de Datos y Algoritmos

### `Quadtree.py`

Se implementaron el Quadtree para dos dimensiones, las funciones de la fuerza bruta, la función para generar los datos y la función para calcular la distancia entre dos puntos.

- ### Quadtree:
  Cada nodo es un rectángulo (cuadrante) de la ciudad. Si es una hoja, guarda puntos (hasta 8). Cuando se llena, se divide en 4 cuadrantes iguales y pasa a ser un nodo interno, que ya no guarda puntos sino que los reparte entre sus hijos.

  Cada nodo es un objeto de la clase `Quadtree` y tiene:
  * `x_min`, `y_min`, `x_max`, `y_max`: los límites del rectángulo, en metros
  * `capacidad`: cuántos puntos le caben a una hoja antes de dividirse (8)
  * `nivel_nodo`: el nivel del nodo (la raíz es el nivel 0)
  * `profundidad_max`: un tope de nivel (20) para evitar divisiones infinitas si hay puntos repetidos
  * `puntos`: los puntos guardados (solo si es hoja)
  * `hijos`: `None` si es hoja. Si se dividió, es una lista de 4 nodos en este orden: NO, NE, SO, SE
 

  Y estos métodos:
  * `contiene_punto`: verifica si un punto cae dentro del rectángulo del nodo.
  * `hallar_indice_hijo`: dice a cuál de los 4 hijos pertenece un punto, comparándolo con el centro del nodo (0 = NO, 1 = NE, 2 = SO, 3 = SE).
  * `subdividir`: crea los 4 hijos, cada uno con la mitad del ancho y del alto, reparte los puntos que tenía el nodo y deja su lista vacía.
  * `insertar`: baja por el árbol hasta la hoja que le corresponde al punto y lo guarda ahí. Si la hoja está llena, la divide primero. Devuelve `False` si el punto cae fuera de la ciudad.
  * `distancia_minima_a_rectangulo`: calcula la distancia entre un punto y la parte del rectángulo que le queda más cerca (0 si el punto está adentro). Sirve para saber si vale la pena visitar un nodo o si está muy lejos.
  * `busqueda_por_rango`: encuentra los puntos a un radio dado. Recorre el árbol y, si un rectángulo está más lejos que el radio, descarta ese nodo y todo lo que tiene adentro. En las hojas revisa cada punto con su distancia real.
  * `busqueda_vecino_mas_cercano`: guarda el mejor candidato que va encontrando. En cada nodo interno ordena los 4 hijos del más cercano al más lejano a la consulta y los visita en ese orden, y descarta los rectángulos que están igual o más lejos que la mejor distancia.

- ### Fuerza bruta:
  Se trabaja con una lista. Para buscar los puntos a un radio, se recorre toda la lista calculando la distancia de cada punto a la consulta. Y para el vecino más cercano, también se recorren todos los puntos y se guarda el de menor distancia.

- ### Generación de los datos y distancia:
  * `generar_N_puntos`: genera N puntos al azar, todos con la misma probabilidad de caer en cualquier lado de la ciudad. Recibe una semilla (por defecto 42) para que siempre salgan los mismos puntos y los resultados se puedan repetir.
  * `distancia_2_puntos`: calcula la distancia euclidiana entre dos puntos, a mano con la fórmula.

### 3. `Test.py`
