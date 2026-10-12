# Laboratorio #3: Sistema de Búsqueda de Estudiantes


## 1. Descripción del Problema y Objetivo

### El problema

Una institución educativa necesita un sistema para administrar la información de sus estudiantes. De cada estudiante se guarda su ID (número único de matrícula), su nombre, su edad y su promedio. El sistema debe permitir:

1. Buscar un estudiante a partir de su ID.
2. Insertar un nuevo estudiante.
3. Listar todos los estudiantes en orden ascendente de ID.

Además, se agregó una cuarta operación, la búsqueda por rango: obtener todos los estudiantes cuyo ID está entre dos valores ``a`` y ``b``.

### Objetivo

Estudiar experimentalmente cómo cambia el tiempo de ejecución cuando se guardan y se buscan los estudiantes con tres estrategias distintas (Lista, ABB y Árbol B+) a medida que aumenta la cantidad de estudiantes (N), y comparar lo que se mide con lo que predice la teoría. También se estudia cómo afecta el orden en que se insertan los IDs (aleatorio u ordenado).

---
## 2. Estructuras de Datos y Algoritmos

Cada estudiante se guarda como una tupla ``(id, nombre, edad, promedio)``.

#### Lista (``Lista.py``)

Una lista de Python con los estudiantes, en el orden en que llegan.

* Insertar: primero recorre la lista para comprobar que el ID no exista y luego agrega el estudiante al final.
* Buscar: revisa los estudiantes uno por uno hasta encontrar el ID.
* Listar: usa ``sorted()`` para ordenar por ID.
* Rango: recorre todos los estudiantes, se queda con los que están en el rango y los ordena.

#### Árbol binario de búsqueda, ABB (``ArbolABB.py``)

Cada nodo guarda un estudiante, y tiene un hijo izquierdo (IDs menores) y un hijo derecho (IDs mayores). Las funciones son iterativas (con ``while``), porque con la recursión Python falla cuando el árbol queda muy profundo.

* Insertar y buscar: bajan por el árbol, comparando el ID en cada nodo. Su costo depende de la altura del árbol.
* Listar: recorrido "inorden" (izquierda, nodo, derecha), que ya sale ordenado.
* Rango: recorrido inorden que se salta lo que está por debajo de ``a`` y se detiene al pasar ``b``.
* Altura: cuenta los niveles del árbol.
* Si los IDs se insertan ordenados, el árbol queda como una cadena (altura = N) y se comporta como una lista.

#### Árbol B+ (ArbolBMas.py)

Árbol balanceado de **grado 50**: cada nodo guarda hasta 50 claves. Los nodos internos solo guardan claves que sirven de guía; los estudiantes están solo en las hojas, y las hojas están enlazadas entre sí.

* Insertar: baja hasta la hoja que corresponde. Si la hoja se pasa de 50 claves, se divide en dos y sube una clave al nodo padre; si el padre también se pasa, se divide igual, y así hasta la raíz.
* Buscar: baja por el árbol y revisa las claves de cada nodo.
* Listar: baja a la primera hoja y recorre la cadena de hojas.
* Rango: baja hasta la hoja donde empieza el rango y avanza por las hojas enlazadas.
* Altura: cuenta los niveles (todas las hojas están siempre al mismo nivel).

#### Complejidad que predice la teoría

Operación:

* **Buscar un ID:** Lista (*lineal*), ABB con IDs aleatorios (*logarítmica*), ABB con IDs ordenados (*lineal*) y Árbol B+ (*logarítmica*)
* **Insertar los N estudiantes:** Lista (*cuadrática*), ABB con IDs aleatorios (*N log N*), ABB con IDs ordenados (*cuadrática*) y Árbol B+ (*N log N*)
* **Listar ordenado:** Lista (*N log N*), ABB con IDs aleatorios (*lineal*), ABB con IDs ordenados (*lineal*) y Árbol B+ (*lineal*)
* **Buscar por rango:** Lista (*lineal*, siempre revisa todos), ABB con IDs aleatorios (*logarítmica + k*), ABB con IDs ordenados (*lineal*) y Árbol B+ (*logarítmica + k*)

k = cantidad de estudiantes que devuelve el rango.

---
## 3. Diseño Experimental y Forma de Medir

#### Qué se mide
Se hacen cinco experimentos, cada uno con **IDs aleatorios** y con **IDs ordenados**:
 
| # | Experimento | Qué se mide |
|---|---|---|
| 1 | Búsqueda por ID | Tiempo total de M búsquedas |
| 2 | Inserción | Tiempo total de insertar los N estudiantes, uno por uno, partiendo de una estructura vacía |
| 3 | Listado | Tiempo de listar los N estudiantes en orden ascendente de ID |
| 4 | Búsqueda por rango | Tiempo total de 100 consultas de rango, con cuatro tamaños de rango |
| 5 | Altura | Número de niveles del ABB y del B+ (no se mide tiempo) |

#### Cómo se generan los datos (``GenerarEstudiantes.py``)

* Los IDs son números únicos elegidos al azar entre 1 y 10·N. Con IDs ordenados, esos mismos IDs se ordenan de menor a mayor. El rango llega hasta 10·N para que existan IDs que no están guardados, y así poder probar búsquedas que no encuentran nada.
* El nombre, la edad (entre 17 y 30) y el promedio (entre 1,0 y 10,0) se eligen al azar.
* Cada ejecución genera datos distintos, por eso cada prueba se repite varias veces.

#### Cómo se generan las búsquedas

* **Por ID:** M IDs; cada uno, con probabilidad 50%, es un ID que existe, y si no, un ID que no existe.
* **Por rango:** el ancho es una fracción del total de IDs (0,1%, 1%, 10% o 50%) y el inicio se elige al azar.

#### Cómo se mide el tiempo

* Se usa ``time.perf_counter()`` de Python, que es un cronómetro de alta precisión.
* Antes de medir se ejecuta ``gc.collect()`` y el recolector de basura se apaga solo durante la medición, para que no meta pausas al azar.
* Las búsquedas se miden en bloque (M seguidas), porque una sola dura apenas unos microsegundos y sería difícil medirla bien.
* No se mide la generación de los datos, solo las operaciones de cada estructura.
* En cada repetición los datos se generan una sola vez y se usan en las tres estructuras, para que la comparación sea justa. El programa comprueba además que las tres encuentren la misma cantidad de IDs y listen N estudiantes.
* Cada medición se guarda de inmediato como una fila en ``resultados/resultados.csv``.

---

## Parámetros del Experimento

| Parámetro | Valor |
|---|---|
| **N** (cantidad de estudiantes) | 100, 500, 1.000, 5.000, 10.000 y 20.000 |
| **Orden de inserción** | Aleatorio y ordenado |
| **Repeticiones** | 10 por cada combinación (orden, estructura, N) |
| **M** (búsquedas por ID en cada repetición) | 1.000 |
| **Porcentaje de búsquedas de IDs que existen** | 50% (el otro 50% son IDs que no existen) |
| **Consultas por rango** | 100 por repetición y por tamaño de rango |
| **Tamaños de rango** | 0,1%, 1%, 10% y 50% del rango de IDs |
| **Grado del B+** | 50 |

En total hay **360 mediciones** (2 órdenes × 6 valores de N × 3 estructuras × 10 repeticiones).
