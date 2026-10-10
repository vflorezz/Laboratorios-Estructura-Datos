# Se va a usar una lista simplemente enlazada para las hojas del arbol

class NodoBMas:                          #Esta clase representa los nodos del árbol (ya sean hojas o nodos internos)
    def __init__(self, hoja = False):    
        self.hoja = hoja                 # La variable hoja, indica si el nodo es una hoja (True) o no (False). Por defecto es falsa
        
        self.claves = []                 # Guarda los IDs, que son los que sirven para organizar y buscar dentro del árbol
        
        self.hijos =[]                   # Son los nodos a los que apunta: En nodos internos, solo guarda las referencias a otros nodos 
                                         # En hojas, se guardan los estudiantes reales  
        self.siguiente = None            # Solo se utiliza para las hojas; guarda un puntero a la siguiente hoja, formando la lista enlazada
    

class ArbolBMas:
    def __init__(self, grado = 50):        # Definimos el grado del árbol en 50, es decir que cada nodo tiene máximo 50 claves (un nodo interno puede tener hasta 51 hijos)
        self.grado = grado 
        self.raiz = NodoBMas(hoja = True)  # Al crearse el árbol, empieza con una sola hoja como raíz
        
    def buscar_id_estudiante_BMas(self, id):
        nodo = self.raiz                    # Empezamos la búsqueda por la raíz
 
        while not nodo.hoja:                # Mientras el nodo sea interno, seguimos bajando
            i = 0                            # Índice para recorrer las claves del nodo actual

            while i < len(nodo.claves) and id >= nodo.claves[i]:   # Recorremos las claves comparando el ID; avanzamos mientras el ID sea mayor o igual
                i += 1                       # El ID va más a la derecha de esta clave, seguimos avanzando

            # Este índice coincide exactamente con el hijo que maneja ese rango, porque la clave es el límite superior de los elementos del hijo.
            nodo = nodo.hijos[i]            # Bajamos al hijo que corresponde al rango donde cae el ID
 
        for j in range(len(nodo.claves)):   # Ya en la hoja, recorremos sus claves para buscar el ID exacto
            if nodo.claves[j] == id:        # Se verifica que la posición exacta y que sea el mismo ID
                return nodo.hijos[j]        # Se retorna el estudiante que está en los hijos de la hoja en la posición j
        return None                         
 
 
    def insertar_estudiante_BMas(self, estudiante):
        nodo = self.raiz                    # Empezamos desde la raíz
        padres = []                         # lista donde se guardan nodos internos recorridos
 
        while not nodo.hoja:                # Bajamos hasta llegar a la hoja donde debe ir el estudiante
            padres.append(nodo)             # Se guarda el nodo interno por el que se baje como padre
            i = 0                            # Índice para recorrer las claves del nodo actual

            while i < len(nodo.claves) and estudiante[0] >= nodo.claves[i]:   # Avanzamos mientras el ID a insertar sea mayor o igual a la clave
                i += 1                       # El ID va más a la derecha de esta clave, seguimos avanzando

            nodo = nodo.hijos[i]            # Bajamos al hijo correspondiente, ya que en esa misma posición de la clave, está el rango de los menores a esa clave (donde debe ir el id)
 
        i = 0                                # Índice para encontrar la posición donde va el ID dentro de la hoja

        while i < len(nodo.claves) and nodo.claves[i] < estudiante[0]:   # Avanzamos mientras las claves de la hoja sean menores al ID
            i += 1                          # Las claves siguen siendo menores, avanzamos una posición

        if i < len(nodo.claves) and nodo.claves[i] == estudiante[0]:    # Si en esa posición ya está el mismo ID
            return False                    # es un duplicado y no se inserta
 
        nodo.claves.insert(i, estudiante[0])    # Insertamos el ID en su posición para que las claves sigan ordenadas
        nodo.hijos.insert(i, estudiante)        # Insertamos el estudiante en la misma posición.
 
        if len(nodo.claves) > self.grado:   # Se verifica si la hoja ya se pasó de su límite
            nueva_hoja = self.dividir_hoja(nodo)    # Si es así, se divide y obtenemos la nueva hoja en la derecha de la original
            clave_subir = nueva_hoja.claves[0]      # La primera clave de la hoja derecha será el separador, entonces se sube. Porque en la hoja original quedaron todos los menores a el y en la derecha están todos los mayores o iguales a él
            self.insertar_en_padres(padres, nodo, nueva_hoja, clave_subir)      # Aquí se sube la clave al nodo padre y se conecta a las dos hojas
 
        return True                         # Inserción exitosa
 
    def dividir_hoja(self, nodo):
        mitad = len(nodo.claves) // 2       # Posición donde partimos la hoja en dos mitades
 
        nueva_hoja = NodoBMas(hoja=True)    # Creamos la nueva hoja (quedará a la derecha)
        nueva_hoja.claves = nodo.claves[mitad:]     # La nueva hoja recibe la segunda mitad de los IDs
        nueva_hoja.hijos = nodo.hijos[mitad:]       # Y los estudiantes correspondientes a esos IDs
 
        nodo.claves = nodo.claves[:mitad]   # La hoja original se queda solo con la primera mitad de los IDs
        nodo.hijos = nodo.hijos[:mitad]     # Y con sus estudiantes correspondientes
 
        nueva_hoja.siguiente = nodo.siguiente   # La nueva hoja apunta a la que antes seguía a la original
        nodo.siguiente = nueva_hoja             # La original ahora apunta a la nueva para que la lista enlazada quede bien
 
        return nueva_hoja                   # Devolvemos la hoja nueva para poder subir su primera clave
 
    def insertar_en_padres(self, padres, izquierdo, derecho, clave):
        while padres:                       # Mientras queden padres a los cuales subir la división
            padre = padres.pop()            # Sacamos el padre más cercano, porque el que ya se analice, sale de la pila
 
            i = 0                            # Índice para encontrar la posición donde va la clave dentro del padre

            while i < len(padre.claves) and clave >= padre.claves[i]:   # Avanzamos mientras la clave a subir sea mayor o igual a las del padre
                i += 1                       # La clave va más a la derecha, seguimos avanzando

            padre.claves.insert(i, clave)           # Insertamos la clave separadora en el padre
            padre.hijos.insert(i + 1, derecho)      # El nuevo nodo va justo a la derecha del nodo que se dividió. 
 
            if len(padre.claves) <= self.grado:     # Se verifica si ese nodo padre si tenía espacio suficiente
                return                      # Si es así, se termina la inserción
 
            derecho, clave = self.dividir_interno(padre)    # No, entonces dividimos el padre y obtenemos su nueva mitad derecha y la clave que sube
            izquierdo = padre               # El padre pasa a ser el nodo izquierdo de la siguiente división, que con la función dividir interno queda con la mitad de la izquierda
 
        nueva_raiz = NodoBMas(hoja=False)   # Si salimos del ciclo, se dividió la raíz: creamos una nueva raíz interna
        nueva_raiz.claves = [clave]         # La nueva raíz tiene una sola clave: el separador
        nueva_raiz.hijos = [izquierdo, derecho]     # Y dos hijos: las dos mitades resultantes de la división
        self.raiz = nueva_raiz              # La nueva raíz reemplaza a la anterior (el árbol crece un nivel)
 
    def dividir_interno(self, nodo):
        mitad = len(nodo.claves) // 2       # Posición de la clave central
        clave_subir = nodo.claves[mitad]    # La clave central sube al padre y no se queda en ninguna mitad.
 
        nuevo_nodo = NodoBMas(hoja=False)   # Creamos el nuevo nodo interno (quedará a la derecha)
        nuevo_nodo.claves = nodo.claves[mitad + 1:]     # Recibe las claves posteriores a la central
        nuevo_nodo.hijos = nodo.hijos[mitad + 1:]       # Recibe los hijos posteriores a la posición central
 
        nodo.claves = nodo.claves[:mitad]   # El nodo original conserva las claves anteriores a la central
        nodo.hijos = nodo.hijos[:mitad + 1] # Y sus hijos 
 
        return nuevo_nodo, clave_subir      # Devolvemos el nodo derecho y la clave que debe subir al padre
    
    def listar_orden_id_estudiantes_BMas(self):
        resultado = []
        nodo = self.raiz

        while not nodo.hoja:            # Bajamos hasta la hoja más a la izquierda
            nodo = nodo.hijos[0]

        while nodo:                     # Recorremos las hojas de corrido con 'siguiente'
            for estudiante in nodo.hijos:   # Agregamos los estudiantes de esta hoja uno por uno
                resultado.append(estudiante)
            nodo = nodo.siguiente

        return resultado

    # Altura del arbol, medida como el NUMERO DE NIVELES (solo una hoja como raiz = 1).
    # En un B+ todas las hojas estan al mismo nivel, asi que basta bajar por el primer hijo.
    def altura(self):
        altura = 1
        nodo = self.raiz
        while not nodo.hoja:
            nodo = nodo.hijos[0]
            altura += 1
        return altura

    # Busqueda por rango: retorna los estudiantes con id_min <= ID <= id_max, ya ordenados por ID.
    # Baja hasta la hoja donde estaria id_min y luego avanza por las hojas enlazadas (siguiente).
    def buscar_rango_BMas(self, id_min, id_max):
        resultado = []
        nodo = self.raiz

        while not nodo.hoja:                # Bajamos igual que en la busqueda normal, usando id_min
            i = 0
            while i < len(nodo.claves) and id_min >= nodo.claves[i]:
                i += 1
            nodo = nodo.hijos[i]

        while nodo:                         # Recorremos las hojas hacia la derecha
            for j in range(len(nodo.claves)):
                clave = nodo.claves[j]
                if clave > id_max:
                    return resultado        # Nos pasamos del rango: se termina
                if clave >= id_min:
                    resultado.append(nodo.hijos[j])
            nodo = nodo.siguiente

        return resultado