# Laboratorio #2
---

## Descripción
En este laboratorio se realizó la implementación de un árbol de Merkle con las siguientes especificaciones:
- Cada hoja contiene el hash SHA-256 de un bloque de datos
- Cada nodo interno contiene el hash SHA-256 de la concatenación de sus dos hijos
- Si el número de hojas es impar, la última hoja se duplica
- La raíz (Merkle Root) es el hash que representa todo el conjunto

En este trabajo, un bloque de datos se manejo como una transacción.

---

## Archivos del Repositorio

### `ArbolMerkel.py`
Contiene la implementación del árbol de Merkel, mediante el uso de:
- Una clase Nodo (con atributos: hash, izquierdo, derecho)
- Una función para calcular hash que usa como parámetro la transacción a hashear
- Una función para generar transacciones
- Una función para generar los nodos con los hashes (retorna una lista de nodos)
- Una función para construir los niveles del árbol (aquí es donde si el numero de hojas es impar, la última se duplica)
- Una función para construir el árbol, la cual llama a la función de los niveles y finalmente, retorna la raíz del árbol
- Una función para convertir el árbol para usar anytree
Al final:
- Se define una lista de nombres predeterminados (hacen parte de las transacciones)
- Se define el número de transacciones ( = 5)
- Se llama a la función para generar los nodos y se guarda la lista en una variable
- Se llama a la función para construir el árbol (se usa la lista de nodos) y se guarda la raíz en una variable
- Se llama a la función para convertir el árbol
- Se muestra en pantalla el árbol de Merkel

### `VerificacionesArbolMerkel.py`
