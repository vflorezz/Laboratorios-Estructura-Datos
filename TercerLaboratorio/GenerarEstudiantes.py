import random

NOMBRES = ["Ana", "Karen", "Ariel", "Tiana", "Charlotte", "Merida", "Ella", "Hugo", "Paco", "Luis"]


# Genera N estudiantes como tuplas (id, nombre, edad, promedio) y retorna la lista.
# N es la cantidad de estudiantes
# ordenado puede ser False: los IDs quedan en orden aleatorio ; o True : los IDs quedan en orden creciente (el caso malo para el ABB)
def generar_N_estudiantes(N, ordenado=False):
    # El rango de IDs crece con N (10 veces N) para poder generar N IDs unicos sin importar que tan grande sea N.
    # random.sample ya garantiza que los IDs son unicos.
    ids = random.sample(range(1, 10 * N + 1), N)

    if ordenado:
        ids.sort()                                 # IDs en orden creciente

    estudiantes = []
    for id in ids:
        nombre = random.choice(NOMBRES)
        edad = random.randint(17, 30)              # Edad entre 17 y 30 anos
        promedio = round(random.uniform(1.0, 10.0), 1)
        estudiantes.append((id, nombre, edad, promedio))

    return estudiantes


# Genera M ids para buscar. Se mezclan ids que existen y ids que no existen.
# porcentaje_existentes es la fraccion de las busquedas que seran de ids presentes (0.5 = 50%)
def generar_M_busquedas(estudiantes, M, porcentaje_existentes=0.5):
    ids_existentes = [e[0] for e in estudiantes]
    max_id = 10 * len(estudiantes)                 # Mismo rango que usa el generador de estudiantes
    conjunto = set(ids_existentes)

    busquedas = []
    for _ in range(M):
        if random.random() < porcentaje_existentes:
            busquedas.append(random.choice(ids_existentes))   # ID que si esta
        else:
            while True:                                       # ID que NO esta
                candidato = random.randint(1, max_id)
                if candidato not in conjunto:
                    busquedas.append(candidato)
                    break
    return busquedas


# Genera M rangos (id_min, id_max) para las busquedas por rango.
# N es la cantidad de estudiantes (los IDs van de 1 a 10*N, igual que en generar_N_estudiantes)
# fraccion es que parte del rango total de IDs abarca cada rango (0.01 = 1%)
# El inicio de cada rango se escoge al azar.
def generar_M_rangos(N, M, fraccion):
    max_id = 10 * N
    ancho = max(1, int(fraccion * max_id))
    rangos = []
    for _ in range(M):
        inicio = random.randint(1, max_id - ancho + 1)
        rangos.append((inicio, inicio + ancho - 1))
    return rangos