# Laboratorio #2


## Descripción
En este laboratorio se realizó la implementación de un árbol de Merkle con las siguientes especificaciones:
- Cada hoja contiene el hash SHA-256 de un bloque de datos
- Cada nodo interno contiene el hash SHA-256 de la concatenación de sus dos hijos
- Si el número de hojas es impar, la última hoja se duplica
- La raíz (Merkle Root) es el hash que representa todo el conjunto

En este trabajo, un bloque de datos se manejó como una transacción.

---

## Archivos del Repositorio

### `ArbolMerkle.py`
Contiene la implementación del árbol de Merkle, mediante el uso de:
- Una clase Nodo (con atributos: hash, izquierdo, derecho)
- Una función para calcular hash que usa como parámetro la transacción a hashear
- Una función para generar transacciones
- Una función para generar los nodos con los hashes (retorna una lista de nodos)
- Una función para construir los niveles del árbol (aquí es donde si el número de hojas es impar, la última se duplica)
- Una función para construir el árbol, la cual llama a la función de los niveles y finalmente, retorna la raíz del árbol
- Una función para convertir el árbol para usar anytree

Al final:
- Se define una lista de nombres predeterminados (hacen parte de las transacciones)
- Se define el número de transacciones (= 5)
- Se llama a la función para generar los nodos y se guarda la lista en una variable
- Se llama a la función para construir el árbol (se usa la lista de nodos) y se guarda la raíz en una variable
- Se llama a la función para convertir el árbol
- Se muestra en pantalla el árbol de Merkle

### `VerificacionesArbolMerkle.py`
Contiene los experimentos:
- Crear 5 bloques de datos (pueden ser transacciones simuladas)
- Construir el árbol y mostrar la raíz
- Modificar un bloque y demostrar que la raíz cambia (Experimento 1)
- Generar una prueba de inclusión para el bloque 3 y verificar que es válida. Al intentar verificar con un dato incorrecto, debe ser inválida (Experimento 2)

Los experimentos 1 y 2 se encuentran como funciones llamadas `exp_1` y `exp_2`, respectivamente.

---

## Sobre el Uso de IA
En este laboratorio se utilizó la inteligencia artificial como apoyo para:
- Comprender cómo realizar la función `construir_arbol` y entender cómo ayuda la recursión en ella para construir el árbol
- Comprender y desarrollar algunas partes de la función `construir_nivel_arbol`
- Mostrar el árbol usando la librería `anytree`, específicamente `Node` y `RenderTree`, y desarrollar la función `convertir_arbol` para adaptar mi árbol a la representación visual de la librería
- Descubrir y aplicar la función `choice()` para poder seleccionar un elemento de manera aleatoria de una lista

---

## Pantallazos de las Verificaciones

### Experimento 1
<img width="681" height="632" alt="image" src="https://github.com/user-attachments/assets/b8063bc0-cb72-48b8-82e4-4dce99bb935e" />
<img width="797" height="610" alt="image" src="https://github.com/user-attachments/assets/503197a8-3445-4796-bafb-e2bdd254b693" />



### Experimento 2

<img width="512" height="205" alt="image" src="https://github.com/user-attachments/assets/f78f0d64-a6cc-4e30-892d-e72a54a3b4e9" />

