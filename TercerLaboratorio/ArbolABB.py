class NodoABB:
    def __init__(self, estudiante):
        self.estudiante = estudiante
        self.izquierdo = None
        self.derecho = None


# Inserta un estudiante (tupla) en el ABB y retorna la raiz. Si el ID ya existe, no hace nada.
# Es ITERATIVA (con while) para que no falle con arboles muy profundos (IDs ordenados).
def insertar_estudiante_ABB(raiz, estudiante_insertar):
    nuevo = NodoABB(estudiante_insertar)
    if raiz is None:
        return nuevo

    id_nuevo = estudiante_insertar[0]
    actual = raiz
    while True:
        if id_nuevo < actual.estudiante[0]:        # Va a la izquierda
            if actual.izquierdo is None:
                actual.izquierdo = nuevo           # Hay un hueco: se coloca aqui
                break
            actual = actual.izquierdo
        elif id_nuevo > actual.estudiante[0]:      # Va a la derecha
            if actual.derecho is None:
                actual.derecho = nuevo
                break
            actual = actual.derecho
        else:                                      # ID repetido: no se inserta
            break

    return raiz


# Busca un estudiante por ID. Retorna la tupla del estudiante o None si no esta.
def buscar_id_estudiante_ABB(raiz, id_buscar):
    actual = raiz
    while actual is not None:
        id_actual = actual.estudiante[0]
        if id_buscar == id_actual:                 # Se encontro al estudiante
            return actual.estudiante
        if id_buscar < id_actual:
            actual = actual.izquierdo              # Menor: se busca a la izquierda
        else:
            actual = actual.derecho                # Mayor: se busca a la derecha
    return None                                    # El id no esta en el arbol


# Retorna la lista de estudiantes en orden ascendente de ID (recorrido inorden, iterativo con pila).
def listar_orden_id_estudiantes_ABB(raiz):
    estudiantes_ordenados = []
    pila = []
    actual = raiz

    while actual is not None or pila:
        while actual is not None:                  # Bajamos todo lo que se pueda a la izquierda
            pila.append(actual)
            actual = actual.izquierdo
        actual = pila.pop()                        # Visitamos el nodo
        estudiantes_ordenados.append(actual.estudiante)
        actual = actual.derecho                    # Y luego pasamos a su derecha

    return estudiantes_ordenados


# Altura del ABB, medida como el NUMERO DE NIVELES (arbol vacio = 0, solo la raiz = 1).
# Es iterativa (recorre nivel por nivel).
def altura_ABB(raiz):
    if raiz is None:
        return 0

    altura = 0
    nivel = [raiz]
    while nivel:
        altura += 1
        siguiente = []
        for nodo in nivel:
            if nodo.izquierdo is not None:
                siguiente.append(nodo.izquierdo)
            if nodo.derecho is not None:
                siguiente.append(nodo.derecho)
        nivel = siguiente
    return altura


# Busqueda por rango: retorna los estudiantes con id_min <= ID <= id_max, ya ordenados por ID.
# Recorrido inorden iterativo que se salta lo que queda por debajo de id_min y se detiene al pasar id_max.
def buscar_rango_ABB(raiz, id_min, id_max):
    resultado = []
    pila = []
    actual = raiz

    while actual is not None or pila:
        if actual is not None:
            if actual.estudiante[0] < id_min:
                actual = actual.derecho            # Este nodo y todo su lado izquierdo son menores que id_min: se saltan
            else:
                pila.append(actual)
                actual = actual.izquierdo          # Puede haber mas nodos del rango a la izquierda
        else:
            nodo = pila.pop()
            if nodo.estudiante[0] > id_max:
                break                              # Los demas son mayores (recorrido en orden): se termina
            resultado.append(nodo.estudiante)
            actual = nodo.derecho

    return resultado