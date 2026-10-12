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

### Lista (``Lista.py``)

Una lista de Python con los estudiantes, en el orden en que llegan.

* Insertar: primero recorre la lista para comprobar que el ID no exista y luego agrega el estudiante al final.
* Buscar: revisa los estudiantes uno por uno hasta encontrar el ID.
* Listar: usa ``sorted()`` para ordenar por ID.
* Rango: recorre todos los estudiantes, se queda con los que están en el rango y los ordena.

### Árbol binario de búsqueda, ABB (``ArbolABB.py``)

Cada nodo guarda un estudiante, y tiene un hijo izquierdo (IDs menores) y un hijo derecho (IDs mayores). Las funciones son iterativas (con ``while``), porque con la recursión Python falla cuando el árbol queda muy profundo.

* Insertar y buscar: bajan por el árbol, comparando el ID en cada nodo. Su costo depende de la altura del árbol.
* Listar: recorrido "inorden" (izquierda, nodo, derecha), que ya sale ordenado.
* Rango: recorrido inorden que se salta lo que está por debajo de ``a`` y se detiene al pasar ``b``.
* Altura: cuenta los niveles del árbol.
* Si los IDs se insertan ordenados, el árbol queda como una cadena (altura = N) y se comporta como una lista.

### Árbol B+ (``ArbolBMas.py``)

Árbol balanceado de **grado 50**: cada nodo guarda hasta 50 claves. Los nodos internos solo guardan claves que sirven de guía; los estudiantes están solo en las hojas, y las hojas están enlazadas entre sí.

* Insertar: baja hasta la hoja que corresponde. Si la hoja se pasa de 50 claves, se divide en dos y sube una clave al nodo padre; si el padre también se pasa, se divide igual, y así hasta la raíz.
* Buscar: baja por el árbol y revisa las claves de cada nodo.
* Listar: baja a la primera hoja y recorre la cadena de hojas.
* Rango: baja hasta la hoja donde empieza el rango y avanza por las hojas enlazadas.
* Altura: cuenta los niveles (todas las hojas están siempre al mismo nivel).

### Complejidad que predice la teoría

| Operación | Lista | ABB (IDs aleatorios) | ABB (IDs ordenados) | Árbol B+ |
|---|---|---|---|---|
| Buscar un ID | lineal | logarítmica | lineal | logarítmica |
| Insertar los N estudiantes | cuadrática | N log N | cuadrática | N log N |
| Listar ordenado | N log N | lineal | lineal | lineal |
| Buscar por rango | lineal (siempre revisa todos) | logarítmica + k | lineal | logarítmica + k |

k = cantidad de estudiantes que devuelve el rango.

---
## 3. Diseño Experimental y Forma de Medir

### Qué se mide
Se hacen cinco experimentos, cada uno con **IDs aleatorios** y con **IDs ordenados**:
 
| # | Experimento | Qué se mide |
|---|---|---|
| 1 | Búsqueda por ID | Tiempo total de M búsquedas |
| 2 | Inserción | Tiempo total de insertar los N estudiantes, uno por uno, partiendo de una estructura vacía |
| 3 | Listado | Tiempo de listar los N estudiantes en orden ascendente de ID |
| 4 | Búsqueda por rango | Tiempo total de 100 consultas de rango, con cuatro tamaños de rango |
| 5 | Altura | Número de niveles del ABB y del B+ (no se mide tiempo) |

### Cómo se generan los datos (``GenerarEstudiantes.py``)

* Los IDs son números únicos elegidos al azar entre 1 y 10·N. Con IDs ordenados, esos mismos IDs se ordenan de menor a mayor. El rango llega hasta 10·N para que existan IDs que no están guardados, y así poder probar búsquedas que no encuentran nada.
* El nombre, la edad (entre 17 y 30) y el promedio (entre 1,0 y 10,0) se eligen al azar.
* Cada ejecución genera datos distintos, por eso cada prueba se repite varias veces.

### Cómo se generan las búsquedas

* **Por ID:** M IDs; cada uno, con probabilidad 50%, es un ID que existe, y si no, un ID que no existe.
* **Por rango:** el ancho es una fracción del total de IDs (0,1%, 1%, 10% o 50%) y el inicio se elige al azar.

### Cómo se mide el tiempo

* Se usa ``time.perf_counter()`` de Python, que es un cronómetro de alta precisión.
* Antes de medir se ejecuta ``gc.collect()`` y el recolector de basura se apaga solo durante la medición, para que no meta pausas al azar.
* Las búsquedas se miden en bloque (M seguidas), porque una sola dura apenas unos microsegundos y sería difícil medirla bien.
* No se mide la generación de los datos, solo las operaciones de cada estructura.
* En cada repetición los datos se generan una sola vez y se usan en las tres estructuras, para que la comparación sea justa. El programa comprueba además que las tres encuentren la misma cantidad de IDs y listen N estudiantes.
* Cada medición se guarda de inmediato como una fila en ``resultados/resultados.csv``.

---

## 4. Parámetros del Experimento

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

---

## 5. Estadísticas y Gráficas

Las estadísticas y las gráficas las produce el archivo ``graficas.py``, a partir de ``resultados/resultados.csv``.

### Qué hace ``graficas.py``

1. Lee ``resultados.csv`` (una fila por repetición).
2. Agrupa las 10 repeticiones de cada combinación (orden, estructura, N).
3. Calcula para cada grupo el promedio, la desviación estándar, la mediana y cuántos valores atípicos hay, y los guarda en ``resultados/tabla_resumen.csv``.
4. Calcula la pendiente de cada curva y la guarda en ``resultados/pendientes.csv``.
5. Dibuja las 6 gráficas y las guarda en ``resultados/graficas/``.

### De dónde sale cada cosa

| Qué | De dónde sale |
|---|---|
| **Tiempo** (en segundos) | Directo del CSV. Búsqueda: tiempo total de las 1.000 búsquedas. Inserción: tiempo total de insertar los N. Listado: tiempo de listar los N. Rango: tiempo total de las 100 consultas. |
| **Promedio** (cada punto de las gráficas) | Suma de las 10 repeticiones dividida entre 10. |
| **Desviación estándar** (las barras) | Mide cuánto se separan las 10 repeticiones de su promedio. Se calcula con `n − 1` (desviación muestral). |
| **Mediana** | El valor central de las 10 repeticiones ordenadas. Se usa como comprobación en la tabla. |
| **Valores atípicos** | Se marcan con la **regla de Tukey**: un valor es atípico si está por debajo de `Q1 − 1,5·IQR` o por encima de `Q3 + 1,5·IQR` (Q1 y Q3 son los cuartiles; IQR = Q3 − Q1). **No se elimina ningún dato**: solo se cuentan en la columna `atipicos_IQR` de la tabla. |
| **Pendiente** | Se ajusta una recta a `log10(promedio)` contra `log10(N)` (con `numpy.polyfit`, usando todos los N medidos). Aparece en la leyenda de las curvas. |

### Por qué se eligió la escala log-log

Se usó escala logarítmica en **los dos ejes** (cada marca vale 10 veces la anterior) por dos razones:

1. N va de 100 a 20.000 y los tiempos van de milésimas de segundo a varios segundos. En una escala normal, las curvas del ABB y del B+ quedarían pegadas abajo, casi planas, junto a la de la lista.
2. En log-log la **pendiente** de una curva indica cómo crece el tiempo, y con eso se compara contra la complejidad teórica.

### Cómo leer la pendiente

La tabla muestra la pendiente que daría una función perfecta con los N usados (100 a 20.000):

| Pendiente | Complejidad | Si N se duplica... |
|---:|---|---|
| cerca de 0,14 | logarítmica | el tiempo casi no cambia |
| cerca de 1 | lineal | el tiempo se duplica |
| cerca de 1,14 | N log N (casi lineal) | el tiempo se duplica y un poco más |
| cerca de 2 | cuadrática | el tiempo se cuadruplica |

La pendiente es una pista, no una prueba. Lineal (1,00) y N log N (1,14) están muy cerca y con ruido de medición no siempre se pueden distinguir; ahí se usa también lo que dice la teoría sobre el algoritmo.

### Cómo leer las gráficas

* **Eje horizontal:** la cantidad de estudiantes N (en el panel derecho de la gráfica 6 es la cantidad de estudiantes que devuelve cada consulta de rango).
* **Eje vertical:** el tiempo en segundos (en la gráfica 3, la altura). Los dos en escala logarítmica.
* Cada **línea** es una estructura (Lista, ABB, Árbol B+), con su color.
* Cada **punto** es el promedio de 10 repeticiones.
* Las **barras verticales** son ± 1 desviación estándar: barra corta, medición muy repetible; barra larga, el tiempo varió mucho entre repeticiones. Si las barras de dos líneas se tocan, no se puede asegurar que sean realmente distintas.
* La **leyenda** trae la pendiente de cada curva.
* En las gráficas con dos paneles (2, 3, 4 y 5) el de la izquierda es con **IDs aleatorios** y el de la derecha con **IDs ordenados**. Los dos paneles comparten el eje vertical para poder compararlos.
* La gráfica 3 no mide tiempo, mide la **altura** de los árboles (número de niveles). La línea punteada negra es una referencia: log₂(N).

---

## 6. Análisis de Resultados

### Gráfica #1: Búsqueda por ID (aleatorios)

<img width="1200" height="825" alt="image" src="https://github.com/user-attachments/assets/c1cc9e66-66e9-4908-9163-bf3108be185d" />

* **Lista:**
  * Pendiente: 0.91 (casi 1).
  * El costo es lineal O(N).
  * La teoría dice que es lineal, porque para buscar un ID, la lista revisa los estudiantes uno por uno.
  * La lista funciona bien con pocos datos, pero cuando estos aumentan, el tiempo lo hace también de forma lineal. Por ello, la lista no escala bien.
    
* **ABB:** 
  * Pendiente: 0.14 (cerca de 0).
  * El costo es logarítmico.
  * La teoría dice que es logarítmico, porque en cada paso del árbol se descarta más o menos la mitad de los estudiantes que quedan.
  * El ABB con IDs en orden aleatorio para la búsqueda escala muy bien.
    
* **Árbol B+:** 
  * Pendiente: 0.10 (cerca de 0).
  * El costo es logarítmico O(log N).
  * La teoría dice que es logaritmico, porque es un árbol y baja por niveles. Además, como sus nodos son grandes (aquí 50) tiene muy pocos niveles.

#### Comparación general para IDs aleatorios
El ABB es el mejor, le sigue el B+ y el peor es la Lista para el caso de IDs aleatorios.

Puede parecer extraño que el B+ no sea el más veloz porque tiene pocos niveles, pero esto ocurre porque en cada nivel revisa **hasta 50 claves**, mientras que el ABB compara una sola. En este caso, menos niveles no significa menos trabajo.

---
### Gráfica #2: Búsqueda por ID (IDs aleatorios vs IDs Ordenados)

<img width="1950" height="825" alt="image" src="https://github.com/user-attachments/assets/9840c51f-f2ba-435d-aedd-bc11147f140a" />


Analizando el caso de IDs ordenados:

* **Lista:**
  * Pendiente: 1.03 (casi 1).
  * El costo es lineal O(N).
  * La teoría dice que es lineal, porque para buscar un ID, la lista revisa los estudiantes uno por uno y eso no depende de cómo estén ordenados. Por ello, el orden de inserción no afecta al costo de la lista.
    
* **ABB:** 
  * Pendiente: 1.02 (casi 1).
  * El costo es lineal O(N).
  * La teoría dice que es lineal para este caso, porque con IDs ordenados cada estudiante nuevo es mayor que todos, así que se ubica a la derecha y el árbol queda como una cadena de N niveles.
  * El orden de inserción **rompe** el ABB.
    
* **Árbol B+:** 
  * Pendiente: 0.16 (cerca de 0).
  * El costo es logarítmico O(log N).
  * La teoría dice que es logarítmico sin importar el orden de los IDs, porque el B+ se organiza al insertar, dividiendo los nodos que se llenan y por eso, siempre queda balanceado.
  * El orden de inserción no afecta al costo del B+.

#### Comparación general para IDs ordenados:
El mejor es el B+, seguido de la Lista y el peor es el ABB.

#### Cuál es la mejor estructura en general según la gráfica #2:
El B+ porque funciona bien para ambos casos (IDs aleatorios o IDs en orden).

#### Por qué el ABB ordenado es peor que la lista:
Ambos son lineales O(N), pero cada paso por un nodo del árbol cuesta más que revisar un elemento de la lista.

---
### Gráfica #3: Altura del Árbol vs N (IDs aleatorios e IDs ordenados)
<img width="1950" height="825" alt="image" src="https://github.com/user-attachments/assets/b9ada27b-d908-46a8-87f4-b3c291d9bdbd" />

* **ABB (IDs aleatorios):** 
  * Pendiente: 0.18 (cerca de 0).
  * La altura crece de forma logarítmica O(log N).
  * La teoría dice que es logarítmica, porque con árbol construido con IDs al azar queda relativamente repartido.
 
* **ABB (IDs ordenados):** 
  * Pendiente: 1
  * La altura crece de forma lineal O(N).
  * La teoría dice que es lineal, porque con IDs ordenados cada estudiante nuevo es mayor que todos los anteriores, así que se ubica a la derecha y el árbol queda como una cadena de N niveles.
    
* **Árbol B+:**  
  * Pendiente: 0.10 (cerca de 0).
  * La altura crece de forma logarítmica O(log N) y también, esta casi no crece.
  * La teoría dice que es logarítmica porque cada nodo guarda **hasta 50 claves** y el árbol sólo gana un nivel cuando se divide la raíz, que pasa a veces.
  * Es igual con IDs aleatorios u ordenados, el orden no le afecta.

#### Comparación general:
* El árbol de menor altura es el B+
* El ABB aleatorio y el B+ son logarítmicos en tiempo porque su altura es logarítmica.

#### Relación con las gráficas #1 y #2:
La altura influye en los tiempos. El ABB ordenado es lineal en tiempo porque su altura es lineal. En cambio, el ABB aleatorio y el B+ son logarítmicos en tiempo porque su altura es logarítmica.

---
## Gráfica #4: Inserción de los N estudiantes (IDs aleatorios y IDs ordenados)

<img width="1950" height="825" alt="image" src="https://github.com/user-attachments/assets/89fc27ed-fb94-4ecd-9054-9ef6b5319002" />

* **Lista:**
  * Pendiente (aleatorios): 1.89 (casi 2).
  * Pendiente (aleatorios): 2.01 (casi 2).
  * El costo es cuadrático O(N^2) para ambos casos.
  * La teoría dice que es cuadrático, porque antes de insertar cada estudiante la lista revisa que su ID no exista, recorriendo los elementos existentes ene ella. El primer estudiante cuesta 1 revisión, el segundo 2, ... , hasta N. La suma total es del orden de N^2.
  * Es la peor estructura para insertar, el orden no la afecta.
    
* **ABB (IDs aleatorios):** 
  * Pendiente: 1.07 (es casi lineal).
  * El costo es lineal-logarítmico O(N log N).
  * La teoría dice que es lineal-logarítmico, porque cada inserción baja por un árbol de altura logarítmica (gráfica #3), y se hacen N inserciones: N veces log N.
 
* **ABB (IDs ordenados):** 
  * Pendiente: 2.02 (cerca de 2)
  * El costo es cuadrático O(N^2).
  * La teoría dice que es cuadrático, porque el árbol es una "una cadena" (gráfica #3). El estudiante #i recorre primero i niveles antes de ubicarse. La suma total es del orden N^2.
  * El orden de inserción rompe el ABB.
  * Es peor que la lista porque bajar por un nodo del árbol, cuesta más que revisar un elemento de la lista. 
    
* **Árbol B+:**  
  * Pendiente en IDs aleatorios: 1.05 (casi lineal).
  * Pendiente en IDS ordenados: 1.18 (casi lineal).
  * En ambos casos, el costo es lineal-logarítmico O(N log N).
  * La teoría dice que es lineal-logarítmico porque cada inserción baja por unos pocos niveles y en ocasiones se divide un nodo.
 
#### Comparación general:
* Con IDs aleatorios: El mejor es el ABB, seguido del B+ y el peor la Lista.
* Con IDs ordenados:  El mejor es el B+, seguido de la Lista y el peor es el ABB.

#### Cuál es el mejor:
El B+ porque funciona bien con sus IDs aleatorios y ordenados. EL ABB solo gana con IDs aleatorios y la Lista siempre es peor por su costo cuadrático.

---
## Gráfica #5: Listado de Todos los Estudiantes en Orden Ascendente de ID
<img width="1950" height="825" alt="image" src="https://github.com/user-attachments/assets/42f1d2bd-2572-4638-9794-3b393da691d6" />

Esta es la gráfica más ruidosa de todas: Los tiempos son muy chiquitos y se miden una sola vez.

* **Lista:**
  * Pendiente (aleatorios): 0.97 (casi lineal).
  * El costo es lineal-logarítmico O(N log N).
  * La teoría dice que es lineal-logarítmico porque la lista no está ordenada y la función ``sorted()`` tiene que ordenarla, y ordenar N datos cuesta N log N.
    
  * Pendiente (ordenados): 0.92 (casi lineal).
  * El costo es lineal-logarítmico O(N log N).
  * La teoría dice que es lineal-logarítmica, pero es más rápida que en IDs aleatorios poque la lista y esta ordenada y la función ``sorted()`` lo detecta y casi no trabaja.
    
* **ABB:** 
  * Pendiente (aleatorios): 0.83 (cerca de 1).
  * Pendiente (ordenados): 0.87 (cerca de 1).
  * El costo es lineal O(N) para ambos casos.
  * La teoría dice que es lineal, porque el recorrido en orden  (INORDER) visita cada nodo exactamente una vez y ya salen ordenados, no importa la forma del árbol: N nodos = N visitas.
  * El orden de inserción casi no afecta el listado del ABB, es una de las pocas operaciones donde el ABB degenerado no se ve perjudicado.
 
    
* **Árbol B+:**  
  * Pendiente en IDs aleatorios: 0.62 (cerca de 1).
  * Pendiente en IDS ordenados: 0.69 (cerca de 1).
  * En ambos casos, el costo es lineal O(N).
  * La teoría dice que es lineal porque baja hasta la primera hoja y recorre la cadena de hojas, visitando cada estudiante una vez.
  * No le afecta el orden.


#### Comparación general:
* Con IDs aleatorios: El mejor es el B+, seguido del ABB y el peor la Lista.
* Con IDs ordenados:  Los mejores son la Lista y el B+ (quienes quedan parecidos y con barras que se tocan), y finalmente, el peor es el ABB.

---
## Gráfica #6: Búsqueda por Rango (IDs aleatorios)

<img width="1950" height="825" alt="image" src="https://github.com/user-attachments/assets/de766135-8c62-4ff7-88ec-629422682aa8" />

* **Lista (gráfica izquierda):**
  * Pendiente: 0.91 (cerca a 1).
  * El costo es lineal O(N).
  * La teoría dice que es lineal porque para cualquier rango la lista revisa todos los estudiantes.
    
* **Lista (gráfica derecha):**
  * Es casi plana con rangos pequeños y solo sube con rangos más grandes.
  * Lo que cuesta es el recorrido de los N (que son fijos N= 10.000) y lo único que crece con el rango es ordenar los resultados.
    
* **ABB (gráfica izquierda):** 
  * Pendiente: 0.70 (entre la log y la lineal).
  * La teoría dice que el costo es bajar hasta el inicio del rango (logarítmico) + recoger a los k estudiantes (proporcional a k). Como el rango es del 1% de N, k crece con N y por eso, la pendiente queda entre las 2.
  * El costo es lineal-logarítmico O(N log N).
    
 * **ABB (gráfica derecha):** 
  * crece con el tamaño del rango, crece casi en proporción a k.
    
* **Árbol B+ (gráfica izquierda):**  
  * Pendiente: 0.45 (entre log y lineal).
  * La teoría dice que el costo es bajar hasta el inicio del rango y recoger k estudiantes. Pero, baja menos y además va por las hojas enlazadas.
  * El costo es O (N log N).
 
* **Árbol B+ (gráfica derecha):** 
  * Crece en proporción a k.
 
#### Comparación general:

* Rangos pequeños: Son rápidos ABB y B+, la lista es más lenta.
* Rangos enormes: El mejor es el B+, luego el ABB y el peor, la Lista.

La ventaja contra la lista se achica porque cuando hay que devolver miles de estudiantes, hay más trabajo (en rangos enormes).

#### Cuál es mejor:
El B+ es el mejor, le sigue el ABB y el peor es la Lista.

---
## 7. Limitaciones
1. N llega solo hasta 20.000 (por el límite de tiempo del experimento). Para N mayores no hay mediciones.
2. Solo 10 repeticiones por combinación, así que la desviación estándar es una estimación aproximada.
3. Con N pequeños los tiempos son diminutos y muy ruidosos (las barras son grandes), y los costos fijos aplanan las curvas. Por eso las pendientes con N pequeños se deben leer con cuidado.
4. La pendiente se calcula con solo 6 valores de N y es una pista, no una prueba, de la complejidad.
5. El listado se mide una sola vez por repetición, así que es la medición más ruidosa.
6. Los IDs están repartidos de forma uniforme y el 50% de las búsquedas son de IDs que existen. Con otras distribuciones los resultados podrían cambiar.
7. El computador no estaba aislado: el sistema operativo y otros procesos pueden afectar las mediciones.

---
## 8. Hardware, Software y Librerías

| Componente | Detalle |
|---|---|
| Procesador | Intel Core i5-1235U de 12.ª generación (frecuencia base 1,30 GHz, 12 núcleos lógicos) |
| Memoria RAM | 16,0 GB (3200 MT/s) |
| Gráficos | Intel Iris Xe (128 MB) |
| Almacenamiento | 477 GB |
| Sistema operativo | Windows 11 (10.0.26200) |
| Lenguaje | Python 3.13.2 (64 bits) |
| Editor | Visual Studio Code |
| Librerías | `pandas` 3.0.6, `matplotlib` 3.11.2, `numpy` 2.5.2 |
 
Los experimentos (`experimentos.py`) usan solo la biblioteca estándar de Python (`time`, `gc`, `random`, `csv`). Las librerías anteriores se usan solo en `graficas.py`.
 
**Comandos para consultar las versiones** (en la terminal):
 
```
python --version
python -m pip show pandas matplotlib numpy
```
 
`experimentos.py` también guarda el sistema operativo, el procesador, la versión de Python y los parámetros en `resultados/info_sistema.txt`.

---
## 9. Cómo se Ejecutaron los Experimentos
Fecha de ejecución: 11/10/2026
Duración total del experimento completo: 5.6 minutos (el programa lo muestra al terminar: "Terminado en X minutos").
Condiciones: Tenía abierto GitHub Desktop al inicio de la ejecución y Edge.
Los datos de las tablas y gráficas salen de una misma ejecución completa (la última).

---
## 10. Cómo Repetir el Experimento

1. Instalar **Python 3** (se usó 3.13.2).
2. Poner todos los archivos `.py` en una misma carpeta y abrir una terminal en esa carpeta (por ejemplo, abriendo la carpeta en VS Code).
3. Instalar las librerías (solo la primera vez):
```
   python -m pip install pandas matplotlib
```

4. Cerrar los programas pesados y, si es un portátil, conectarlo al cargador. Ejecutar el experimento completo y anotar cuánto tarda:
```
   python experimentos.py
```
   Se crea la carpeta `resultados/` con `resultados.csv` e `info_sistema.txt`.
5. Generar las tablas y las gráficas:
```
   python graficas.py
```
   Se crean `tabla_resumen.csv`, `pendientes.csv` y las 6 gráficas en `resultados/graficas/` (el script borra las imágenes de corridas anteriores).
 
**Notas:**
- Cada ejecución genera datos distintos, así que los tiempos variarán un poco entre corridas y entre computadores. Las tendencias deberían mantenerse.
- Los parámetros (N, repeticiones, M, tamaños de rango) están al inicio de `experimentos.py` y se pueden cambiar ahí.

---
## 11. Código de Honor (Uso de la IA)

En este laboratorio se hizo uso de la inteligencia artificial para:

