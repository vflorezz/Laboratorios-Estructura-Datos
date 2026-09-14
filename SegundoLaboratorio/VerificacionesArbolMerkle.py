from ArbolMerkle import generar_nodos_con_hashes,construir_arbol,convertir_arbol,calcular_hash, Nodo
from anytree import RenderTree

num_transacciones = 5                          # Se define el número de transacciones como 5
print("\n\n**********   Árbol de Merkle para los Experimentos\t*************\n")
lista_nodos = generar_nodos_con_hashes(num_transacciones)
transaccion_3 = "Juanito pago 50000 pesos"           # Fijo una transacción 3 para que no sea aleatoria y poder hacer el experimento 2
lista_nodos[2] = Nodo(calcular_hash(transaccion_3))
print("La transacción 3 ahora es: Juanito pago 50000 pesos")
raiz_arbol = construir_arbol(lista_nodos)      # Se construye el arbol
arbol_visual = convertir_arbol(raiz_arbol)     # Guarda la raiz de la representación del árbol en anytree
print(f"\nLa raiz del arbol es: {raiz_arbol.hash[:8]}\n")
# RenderTree recorre el arbol y ayuda a imprimirlo
for pre, _, nodo in RenderTree(arbol_visual):  # pre contiene los caracteres que usa para representar la jerarquia, nodo es el nodo de anytree que se está recorriendo
    print(f"{pre}{nodo.name}")                 # nodo.name da el nombre del nodo (es el hash hasta los 8 caracteres)

# Experimento 1 - Voy a modificar una transacción

def exp_1 ():
    transaccion_modificada = "Libardo pago 10 pesos"                # Esta va a ser la nueva transaccion (asi se modifica)
    print (f"\ntransaccion_modificada: {transaccion_modificada}\n") 

    print (f"El número de transacciones es: {num_transacciones}\n")
    num_transaccion = int (input("Ingrese el número de transacción que va a modificar (ej: 1,..., num_transacciones): "))  # Se escoge la transaccion que se quiere modificar de las 5
    hash_transaccion_modificada = calcular_hash(transaccion_modificada)  # Se calcula el hash de la transaccion modificada

    lista_nodos_copia = lista_nodos.copy()    # Trabajo sobre una copia para no dañar el árbol original
    lista_nodos_copia[num_transaccion - 1] = Nodo(hash_transaccion_modificada)  # Asigno el nuevo nodo

    raiz_arbol_nueva = construir_arbol(lista_nodos_copia)      # Se construye el arbol nuevo
    arbol_visual_nuevo = convertir_arbol(raiz_arbol_nueva)     # Se convierte
    print(f"\nnueva raiz del arbol = {raiz_arbol_nueva.hash[:8]}\n")  # Se muestra cual es la nueva raiz del arbol
    for pre, _, nodo in RenderTree(arbol_visual_nuevo):               # Se muestra el arbol completo
        print(f"{pre}{nodo.name}")



# Experimento 2 - Prueba de Inclusión para el bloque 3
def exp_2(raiz_original, transaccion_3):                # Se usa la raiz del arbol original y la transaccion 3 que me dan
    h3 = calcular_hash(transaccion_3)                   # Se calcula el hash de la transaccion 3 que me dieron
    h4 = raiz_original.izquierdo.derecho.derecho.hash   # Se guarda el hash 4 (o sea de la transaccion 4)
    h12 = raiz_original.izquierdo.izquierdo.hash        # Se guarda el hash 12 (o sea el hash del h1+h2)
    h5555 = raiz_original.derecho.hash                  # Se guarda el hash 5555 (o sea el hash de h55+h55)

    # Ahora con esos hashes puedo llegar a la raiz con la transaccion dada a ver si si es igual o si no es igual
    h34 = calcular_hash(h3 + h4)                              # Calculo el hash 3 de la transaccion que me dieron + hash 4
    h1234 = calcular_hash(h12 + h34)                          # Calculo el hash h12+h34
    raiz_con_transaccion_3 = calcular_hash(h1234 + h5555)     # llego a la raiz (del arbol que se produce a partir de la transaccion 3 que me dieron)

    if (raiz_original.hash == raiz_con_transaccion_3):        # Verifico si realmente son iguales las raices
        print ("Prueba válida: Las raíces coinciden")
    else:
        print("Prueba inválida: Las raíces no coinciden")


while True:
    numero = input("\n\nEscoga 1 para iniciar el experimento 1. Escoga 2 para el experimento 2 (para salir, presione cualquier otra tecla): ")
    match numero:
        case "1":
            print("\n\n**********    Experimento 1\t*************\n")
            exp_1()

        case "2":
            print ("\n\n**********    Experimento 2\t*************\n")
            exp_2(raiz_arbol, "Ariel pago 80000 pesos")     # Debe ser inválida
            print("La transacción 3 dada fue: Ariel pago 80000 pesos\n")
            exp_2(raiz_arbol, "Juanito pago 50000 pesos")   # Debe ser válida
            print("La transacción 3 dada fue: Juanito pago 50000 pesos\n")

        case _:
            break