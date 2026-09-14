import hashlib
import random
from anytree import Node, RenderTree    # Node ayudará a crear un nodo compatible con anytree, mientras que RenderTree ayudará a recorrer ese árbol e imprimirlo (Se usan es para la visualización del árbol al final)

# Se crea una clase Nodo para poder hacer el árbol
class Nodo:
    def __init__(self, hash):  #Se usa el hash de la transacción para crear el nodo
        self.hash = hash
        self.izquierdo = None
        self.derecho = None

# Esta función calcula es hash de la transacción que es la "clave a hashear"
def calcular_hash(clave_a_hashear):
    return hashlib.sha256(clave_a_hashear.encode()).hexdigest()

# Esta función genera una transacción
def generar_transacciones():
    nombre = random.choice(nombres)     # Escoge un elemento aleatorio de la lista de nombres (esta abajo)
    valor = random.randint(1,1000000000) # Escoge un entero aleatorio entre 1 y 1000000000
    print (f"{nombre} pago {valor} pesos")

    return  f"{nombre} pago {valor} pesos"   # Retorna siempre una frase con ese nombre aleatorio y valor

# Esta función crea los nodos para todas las transacciones
def generar_nodos_con_hashes(numero_transacciones):
    lista_nodos = []     # Los nodos de las transacciones (hasheadas) se van guardando en esta lista

    for _ in range (numero_transacciones):      # Aqui se piden tantas transacciones indique el numero de transacciones
        hash_transaccion = calcular_hash(generar_transacciones())   # Se usa la funcion de calcular el hash y se guarda en una variable
        nodo = Nodo(hash_transaccion)           # Se crea un objeto tipo Nodo que se crea con el hash de la transacción
        lista_nodos.append(nodo)                # Se añade el nuevo nodo de la transacción (hasheada) a la lista

    print ("\n")
    return lista_nodos    # Retorna la lista de nodos completa

# Esta función se encarga de construir los niveles del árbol
def construir_nivel_arbol(nodos_nivel_actual):       # Con nodos_nivel_actual se refiere a las transacciones hasheadas que se obtuvieron de generar_nodos_con_hashes
    nivel_siguiente = []                             # Aquí se guarda los nodos que queden para el nivel siguiente del arbol (por ejemplo cuando queda sobrando uno que no tiene para hacer pareja o cuando hay un nuevo papa)

    for i in range (0, len(nodos_nivel_actual), 2):  # En este for va yendo de dos en dos (parejitas) y el que se quede sin pareja tambien entra pero esto ocurriria en el ultimo ciclo
        if (i + 1 < len(nodos_nivel_actual)):        # Aqui verifica que el siguiente al nodo en que yo estoy parado exista (es una verificacion para saber si voy en parejita o si voy solo porque si va solo al hacer la verificación daría falso) 
            nodo_izquierda = nodos_nivel_actual[i]   # Se guarda el nodo en el que estoy parado como izquierdo en una variable
            nodo_derecha = nodos_nivel_actual[i+1]   # Se guarda el nodo siguiente al que estoy parado como derecho en una variable

            hash_nodo_papa = calcular_hash(nodo_izquierda.hash + nodo_derecha.hash)   # Se calcula el hash para el nodo papa que va a sacar el hash de (hash izq + hash derecha)
            nodo_papa = Nodo(hash_nodo_papa)    # Y aqui ya se crea el nodo papa con su hash

            nodo_papa.izquierdo = nodo_izquierda  # Se conectan los nodos izq y derecho del papa 
            nodo_papa.derecho = nodo_derecha

            nivel_siguiente.append(nodo_papa)     # Se añade el papa al siguiente nivel
        else:
            # Esto es cuando queda un nodo sin pareja (esto ocurre al final del ciclo)
            nodo_izquierda = nodos_nivel_actual[i]
            nodo_derecha = nodos_nivel_actual[i]   # Duplico mi nodo que quedó solito

            hash_nodo_papa = calcular_hash(nodo_izquierda.hash + nodo_derecha.hash)  # Se saca el hash del hash de el mismo con el mismo para el nodo papa
            nodo_papa = Nodo(hash_nodo_papa)   # Aqui se crea el nodo papa

            nodo_papa.izquierdo = nodo_izquierda  # Se conecta con los nodos izq y derecho
            nodo_papa.derecho = nodo_derecha

            nivel_siguiente.append(nodo_papa)     # Se añade el papa al siguietne nivel

    return nivel_siguiente    # Se retorna la lista del siguiente nivel del arbol

# Esta función construye el árbol
def construir_arbol(lista_nodos):    # Se usa la lista de nodos (esta es inicialmente, la primera lista de nodos de las transacciones hasheadas)
    while (len(lista_nodos) > 1):    # Se repite hasta que quede 1 solo elemento (cuando quede 1 solo, no entra al ciclo) 
        lista_nodos = construir_nivel_arbol(lista_nodos)  # Esa lista se va actualizando con la de nodos_nivel_actual hasta llegar a la raiz donde habria solo 1 elemento, por eso > 1

    return lista_nodos[0]           # Como al final esa lista de nodos queda con un solo elemento, retorna ese elemento que es la raiz del arbol

# Esta función convierte el arbol en un arbol anytree
def convertir_arbol(nodo, padre = None):         # nodo, es un nodo de mi arbol, este caso, cuando se llama la funcion se usa la raiz (esto ocurre en la primera llamada, en las llamadas recursivas será cada hijo)
    # El padre = None es el nodo padre en anytree, como estamos en la raiz, es None (no tiene papa)
    nodo_any = Node(nodo.hash[:8], parent=padre)   # Se crea un nodo de ANYTREE, se toman los primeros 8 caracteres del hash del nodo y asisgna como papa de ese nodo a padre
    if (nodo.izquierdo):                           # Si hay un nodo a la izquierda de mi nodo actual
        convertir_arbol(nodo.izquierdo, nodo_any)  # Convierte el hijo izquierdo, su padre (en anytree) es nodo_any
    if (nodo.derecho):                             # Si hay un nodo a la derecha de mi nodo actual
        convertir_arbol(nodo.derecho, nodo_any)    # Convierte el hijo derecho, su padre en (anytree) es nodo_any
    return nodo_any  # Cada llamada devuelve el nodo_any que se creo, no se guardan pero los nodos ya quedan conectados por el vinculo parent. El último return de esta función es la raiz del arbol en representacion anytree



nombres = ["Pedrito","Juanito","Ivone","Karmen","Sara","Carlos","David","Felipe","Tiana","Vanessa","Luisa"]
num_transacciones = 5

print("\n\n************\t Árbol de Merkle \t*************\n")
lista_nodos = generar_nodos_con_hashes(num_transacciones)
raiz_arbol = construir_arbol(lista_nodos)      # Se construye el arbol
arbol_visual = convertir_arbol(raiz_arbol)     # Guarda la raiz de la representación del árbol en anytree
print(f"\nLa raiz del arbol es: {raiz_arbol.hash[:8]}\n")
# RenderTree recorre el arbol y ayuda a imprimirlo
for pre, _, nodo in RenderTree(arbol_visual):  # pre contiene los caracteres que usa para representar la jerarquia, nodo es el nodo de anytree que se está recorriendo
    print(f"{pre}{nodo.name}")                 # nodo.name da el nombre del nodo (es el hash hasta los 8 caracteres)