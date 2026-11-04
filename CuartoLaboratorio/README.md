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

## 3. `Test.py`
En este archivo están las pruebas para verificar que el Quadtree funciona bien y las gráficas de la búsqueda por radio y del vecino más cercano. Se generan 10.000 puntos en una ciudad de 10.000 m × 10.000 m, se construye el Quadtree y se generan 100 puntos de consulta con otra semilla, para que no coincidan con los puntos del árbol.

- ### Pruebas unitarias:
  Se hicieron con `assert`: si el resultado no coincide, el programa para e indica en cuál prueba falló. Las pruebas realizadas fueron:

  * `prueba_puntos_indices_correctos`: verifica que cada punto vaya al cuadrante que le corresponde. Se usa un nodo que no empieza en 0, porque si el centro se calculara mal, en un nodo que empieza en 0 no se notaría.
  * `prueba_verificar_puntos_completos`: verifica que no se perdió ningún punto. Una búsqueda con un radio que cubre toda la ciudad debe devolver los 10.000 puntos.
  * `prueba_verificar_busqueda_por_rango`: con las 100 consultas y un radio de **500 m**, compara los puntos que encuentra el Quadtree con los de la fuerza bruta. Tienen que ser los mismos.
  * `prueba_verificar_busqueda_vecino_mas_cercano`: con las 100 consultas, compara el vecino más cercano y la distancia del Quadtree con los de la fuerza bruta.
 
  **Resultado en consola:**

  <img width="1036" height="97" alt="image" src="https://github.com/user-attachments/assets/9ced14c8-666a-41af-8630-1ee9f9790940" />

- ### Visualizaciones:
  En el zoom de cada gráfica, los cuadros verdes son las hojas del Quadtree.

  ### visualización de la búsqueda por rango (usando como centro de búsqueda (5000,5000) y radio **500 m**)
    
    <img width="2100" height="1050" alt="image" src="https://github.com/user-attachments/assets/5fe81666-8d52-4207-b711-564bbafd3637" />

  > Se buscaron los puntos a un radio de 500 metros del punto `(5000, 5000)` y se encontraron **69 puntos de entrega** (los rojos). Todos quedan dentro del círculo y no hay ningún punto gris adentro.

  ### Visualización de la búsqueda del vecino más cercano (usando como punto a consultar (4000, 6000))
    
    <img width="2100" height="1050" alt="image" src="https://github.com/user-attachments/assets/94f19c16-dd16-43c8-9e0e-67b64b51f579" />

  > El punto de entrega más cercano a `(4000, 6000)` está a **35,74** metros. El círculo punteado, que llega justo hasta ese vecino, no tiene ningún otro punto adentro, así que no hay uno más cerca.


## 4. `Analisis.py`
En este archivo se hacen 3 experimentos para comparar el rendimiento del Quadtree y la lista (fuerza bruta) a medida que aumenta la cantidad de puntos N: inserción, búsqueda por radio y vecino más cercano.

### Parámetros:

* **ANCHO_CIUDAD** y **LARGO_CIUDAD** = 10.000 m. El tamaño de la ciudad
* **RADIO** = 500 m. Radio para todas las búsquedas por radio
* **M_CONSULTAS** = 100. Consultas que se hacen en cada repetición
* **N_REPETICIONES** = 40. Veces que se repite la medición de cada tamaño
* **TAMANOS** = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000]. Los distintos tamaños de N

### Cómo se mide

Se usa `time.perf_counter()`. Para cada tamaño N se repite todo 40 veces: en cada repetición se generan puntos y consultas nuevos, se construyen las dos estructuras y se miden los tiempos (la generación de los puntos no se cuenta). Cada punto de las gráficas es el promedio de las 40 repeticiones, y las barras de error son ±1 desviación estándar.
 
Los dos ejes están en escala logarítmica, así que la **pendiente** de cada línea (que aparece en la leyenda) dice cómo crece el costo: cerca de 1 es lineal, y entre 0 y 1 crece menos que lineal. La línea punteada es el **cruce**: el N desde el cual el Quadtree es más rápido que la lista.

### Experimento #1: Inserción de N puntos (lista - fuerza bruta VS Quadtree)

Se insertan los N puntos, uno por uno, en una lista vacía (con `append`) y en un Quadtree vacío, y se mide el tiempo de cada una.

<img width="1350" height="975" alt="image" src="https://github.com/user-attachments/assets/fc345971-e0f9-405f-a9a1-8463b181c174" />

- ### Interpretación:
  
