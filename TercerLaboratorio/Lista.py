# Esta función se encarga de insertar nuevos estudiantes a la lista
def insertar_estudiantes_lista(estudiantes, estudiante):  # Estudiantes es la lista de estudiantes y estudiante es el nuevo a agregar
    for est in estudiantes:
        if (est[0] == estudiante[0]):
            return False
    
    estudiantes.append(estudiante)
    return True

# Esta función se encarga de buscar a un estudiante de la lista de estudiantes usando su ID
def buscar_estudiante_id_lista(estudiantes, id_buscar):
    for est in estudiantes:
        if (est[0] == id_buscar):
            return est

    return None

# Esta función se encarga de ordenar a los estudiantes de la lista por id y los retorna
def listar_orden_id_lista(estudiantes):
    estudiantes_ordenados = sorted(estudiantes)   # En una tupla, sorted ordena con el primer elemento, en este caso es perfecto porque el id es el primer elemento de la tupla
    return estudiantes_ordenados

# Busqueda por rango: retorna los estudiantes con id_min <= ID <= id_max, ordenados por ID.
# La lista no esta ordenada, asi que debe revisar TODOS los estudiantes (O(N)), y luego ordenar el resultado.
def buscar_rango_lista(estudiantes, id_min, id_max):
    resultado = []
    for est in estudiantes:
        if id_min <= est[0] <= id_max:
            resultado.append(est)
    resultado.sort()                               # Se ordena por ID (el id es el primer elemento de la tupla)
    return resultado