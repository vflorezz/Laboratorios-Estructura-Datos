# Laboratorio #3: Sistema de Búsqueda de Estudiantes

---
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
