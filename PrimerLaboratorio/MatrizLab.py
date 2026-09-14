import numpy as np    # Importamos numpy para manejar arreglos y matrices
import time           # Se importa para medir cuánto tarda el programa
import os             # Nos permite interactuar con el sistema operativo


# Definimos las constantes del programa

FILAS = 100_000       # Este es el número de filas de la matriz
COLUMNAS = 100_000    # Este es el número de columnas de la matriz
TAM_BLOQUE = 1000     # Se va a ir trabajando con bloques de 1000 filas, es decir, no pone de una vez las 100.000 sino que
                      # Va trabajando de a mil filas. Serian aprox. 100 bloques porque 100.000/1000 = 100 bloques


# Estos son los nombres de los archivos

NOMBRE_ARCHIVO = "matriz.txt"                        # Se guarda en una variable el nombre del archivo que va a contener la matriz completa      
NOMBRE_ARCHIVO_PRIMERA_FILA = "primera_fila.txt"     # Se guarda en una variable el nombre del otro archivo que va a contener solo la primera fila de la matriz

inicio_tiempo = time.time()    # Se empieza a medir cuánto tarda el programa en correr, guardamos el tiempo actual (inicial)

# Por medio de np.empty, se crea un arreglo de tamaño 1000 x 100.001 (mil filas x cien mil uno columnas), se suma una más porque se va a utilizar un carácter extra para indicar la separación de las filas
buffer = np.empty((TAM_BLOQUE, COLUMNAS + 1), dtype=np.uint8)    # Cada elemento se va a guardar como un entero de 8 bits sin signo (dtype=np.uint8)
buffer[:, -1] = ord("|")      # En todas las filas al final (en la última columna) se pone el símbolo | para indicar cuando termina cada fila de la matriz
                              # ord() convierte un carácter a su código numérico, en este caso | = 124

with open(NOMBRE_ARCHIVO, "wb") as archivo:   # Abrimos el archivo (matriz.txt) para escribir datos binarios (wb) y luego, Python se encarga de cerrar el archivo cuando terminemos

    primera_fila_guardada = False    # Se crea una variable booleana para saber si ya se guardó la primera fila. Se inicializa en False porque al inicio no se ha guardado nada en esa fila

    for inicio in range(0, FILAS, TAM_BLOQUE): # la variable inicio indica donde comienza cada bloque
        # El for comienza en cero (inicio = 0), va hasta FILAS (100.000) y el incremento es del tamaño del bloque (1000), o sea va de mil en mil. Inicio va 0 - 1000 - 2000 ...


        fin = min(inicio + TAM_BLOQUE, FILAS)  # Aquí, se calcula dónde termina el bloque, se usa min() para no pasarse del bloque (si el num de filas no fuera divisible entre 1000). Cuando inicio es 99000 y se le suma el tamaño del bloque da justo 100.000
        n_filas = fin - inicio                 # Cantidad de filas del bloque actual

        
        bloque = np.random.randint(0, 2, size=(n_filas, COLUMNAS), dtype=np.uint8)    # Se va generando parte de la matriz con numeros aleatorios (1 ó 0) para n_ filas (1000) y 100.000 columnas. Esos numeros se guardan como enteros de 8 bits sin signo
        bloque += 48  # Aquí, se convierten esos números a carácteres (48 = 0 y 1 = 49), según el código ASCII

        
        vista = buffer[:n_filas]    # Se toma una "vista" de las primeras n_filas (1000) del buffer
        vista[:, :-1] = bloque      # Se copian los 0 y 1 al buffer (todas las filas, desde la primera columna, hasta antes de la última columna porque ahí ya esta |)

        
        archivo.write(vista.tobytes())   # Se escribe el bloque en el archivo (matriz.txt), pasando de un arreglo de numpy a una secuencia de bytes

        # Aquí se verifica si ya se guardó la primera fila
        if not primera_fila_guardada:
            with open(NOMBRE_ARCHIVO_PRIMERA_FILA, "wb") as archivo_fila:  # Se abre el archivo (primera_fila.txt) para escribir en binario
                archivo_fila.write(vista[0].tobytes())                     # Se esctibe la primera fila en el archivo (primera_fila.txt), pasando de un arreglo de numpy a una secuencia de bytes
            primera_fila_guardada = True                                   # Como ya se guardó la primera fila, se actualiza a True

        print(f"Filas escritas: {fin:,} / {FILAS:,}")                      # Este print indica el progreso, es una ayuda visual para saber cuanto falta para completar la matriz en términos de filas escritas


# Termina el for y se verifica la matriz
 
BYTES_POR_FILA = COLUMNAS + 1    # Es la cantidad de bytes por fila (100.000 + 1)
 
# Primero, se verifica que el archivo de la matriz tenga el tamaño que debería tener
tamaño_esperado = FILAS * BYTES_POR_FILA                         # El tamaño que se espera en total 
tamaño_real_verificacion = os.path.getsize(NOMBRE_ARCHIVO)       # Es el tamaño del archivo
verificacion_tamaño_ok = (tamaño_esperado == tamaño_real_verificacion)  # Si los tamaños coinciden, entonces el tamaño de la matriz es correcto
 
if not verificacion_tamaño_ok:
    print(f"ERROR: el archivo pesa {tamaño_real_verificacion} bytes, se esperaban {tamaño_esperado} bytes")  # Si no, entonces se indica que el tamaño no coincidió

 
# Segundo, verificar que todas las filas tengas solo unos o ceros y terminen en |

# Se inicializa un contador de errores para la siguiente verificación
errores_encontrados = 0

# Si el tamaño es correcto, se continúa con la segunda verificación
if verificacion_tamaño_ok:
    with open(NOMBRE_ARCHIVO, "rb") as archivo_verificacion:          # Se abre de nuevo el archivo (matriz.txt) y lo vamos a leer como bytes
 
        for inicio_v in range(0, FILAS, TAM_BLOQUE):    # Se crea un ciclo for que va a ayudar a leer y revisar los bloques
            # El for comienza en cero (inicio = 0), va hasta FILAS (100.000) y el incremento es del tamaño del bloque (1000), o sea va de mil en mil. Inicio va 0 - 1000 - 2000 ...
            
            fin_v = min(inicio_v + TAM_BLOQUE, FILAS)    # Aquí, se calcula dónde termina el bloque, se usa min() para no pasarse del bloque (si el num de filas no fuera divisible entre 1000). Cuando inicio es 99000 y se le suma el tamaño del bloque da justo 100.000
            n_filas_v = fin_v - inicio_v                 # Cantidad de filas del bloque actual
 
            bytes_bloque = archivo_verificacion.read(n_filas_v * BYTES_POR_FILA)   # Se lee el bloque (1000 * 100000), lee los bytes correspondientes a 1000 filas
 
            tabla = np.frombuffer(bytes_bloque, dtype=np.uint8).reshape(n_filas_v, BYTES_POR_FILA) # Convierte los bytes que se acaban de leer y los organiza en forma de una tabla

            separadores = tabla[:, -1]       # Se toma la última columna de todas las filas, donde está el separador |
            filas_con_separador_malo = np.where(separadores != ord("|"))[0]     # Se buscan las filas que no tienen | al final con su código de carácter (124)

            # Se recorren las filas malas y muestra cuales tienen el error
            for i in filas_con_separador_malo:
                print(f"Fila {inicio_v + i}: no termina en '|'") 
                errores_encontrados += 1    # Aumenta el contador

            cuerpo = tabla[:, :-1]                               # Se guardan todas las filas y columnas menos la última columna (|)
            valido = (cuerpo == 48) | (cuerpo == 49)             # Se comprueba cada número de la tabla que sean 0 o 1
            filas_invalidas = np.where(~valido.all(axis=1))[0]   # Se buscan las filas invalidas

            # Se recorren las filas con errores
            for i in filas_invalidas:
                if i not in filas_con_separador_malo:  # Si la fila no tuvo un error con el separador
                    print(f"Fila {inicio_v + i}: contiene un carácter distinto de 0/1")
                    errores_encontrados += 1  # Se aumenta el contador
 
            print(f"Filas verificadas: {fin_v:,} / {FILAS:,}")             # Progreso en verificación, ayuda visual por filas verificadas
 
 
# Si todas las verificaciones pasaron, se confirma que la matriz quedó bien
matriz_verificada_ok = (
    verificacion_tamaño_ok
    and errores_encontrados == 0
)

# Si no, entonces se informa que se encontraron problemas
if not matriz_verificada_ok:
    print("\nLa verificación encontró problemas. La matriz NO quedó como se esperaba.")
    raise SystemExit(1)   # Se detiene el programa porque la matriz está mal

# Se muestra un mensaje de éxito en caso de que todo haya salido bien
print("Verificación superada: el archivo tiene el formato y contenido esperado.\n")



# Ahora, se calcula cuánto tiempo tomó
tiempo = time.time() - inicio_tiempo    # Tiempo actual - tiempo en que inicio


print("\nMatriz creada correctamente")     # Se indica que la matriz se creó sin problemas
print("Filas:", FILAS)                     # Se muestra la cantidad de filas que tiene la matriz
print("Columnas:", COLUMNAS)               # Se muestra la cantidad de columnas que tiene la matriz

print("Archivo:", NOMBRE_ARCHIVO)          # Se muestra el nombre del archivo de la matriz (matriz.txt)
print(f"Tiempo de escritura: {tiempo:.2f} segundos")   # Se muestra el tiempo que demoró en segundos

print("\nEl archivo de la matriz completa está en:")
print(os.path.abspath(NOMBRE_ARCHIVO))                 # Muestra la ubicación del archivo de la matriz

print("\nEl archivo de la primera fila de la matriz está en:")  # Se añadió por si se desea observar cómo se ve 1 fila de la matriz
print(os.path.abspath(NOMBRE_ARCHIVO_PRIMERA_FILA))           # Muestra la ubicación del archivo de la primera fila de la matriz 
