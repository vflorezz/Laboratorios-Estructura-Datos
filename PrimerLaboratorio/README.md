# Laboratorio1ED

**Estudiante:** Valentina Flórez Acosta

## Descripción
Este repositorio presenta la solución al problema planteado en clase para el laboratorio #1 de Estructuras de Datos y Laboratorio.

Este proyecto consiste en la generación de una matriz de gran tamaño compuesta únicamente por los valores `0` y `1`. La matriz tiene **100.000 filas y 100.000 columnas**, por lo que contiene un total de 10.000 millones de elementos.

Debido al gran tamaño de la matriz, no es posible trabajar con ella completa en memoria de manera eficiente. Por esta razón, se decidió generar y escribir la matriz por bloques de **1.000 filas**, lo que permite controlar mejor el uso de memoria durante la ejecución del programa.

Además de generar la matriz, el programa realiza una serie de verificaciones para comprobar que el archivo generado tenga el tamaño esperado, que cada fila contenga únicamente `0` y `1` y termine con el carácter `|`, y que la primera fila almacenada en un archivo independiente coincida con la primera fila de la matriz.

Para el manejo de los bloques se utilizan **1.000 filas × 100.001 columnas**. La columna adicional corresponde al carácter `|`, que se agrega al final de cada fila para indicar dónde termina. De esta manera, cada fila contiene los 100.000 valores de la matriz más el carácter utilizado como separador. La matriz completa ocupa aproximadamente **10 GB (9,31 GB)**, por lo que trabajar por bloques permite realizar el proceso sin tener que cargar toda la matriz en memoria al mismo tiempo.

## Objetivos
El código debe resolver los siguientes problemas planteados:

- Consumo excesivo de RAM
- Escritura lenta a disco
- Optimización en la manipulación, creación, almacenamiento y lectura de datos.

## Tecnologías y herramientas utilizadas

- **Python:** Lenguaje utilizado para desarrollar el programa.
- **NumPy:** Utilizado para generar y manejar los datos de la matriz.
- **Time:** Utilizado para medir el tiempo de ejecución del programa.
- **OS:** Utilizado para consultar el tamaño y la ubicación de los archivos generados.

## Archivos del Repositorio

### `MatrizLab.py`
- Se genera la matriz de `100.000 × 100.000`.
- Se generan los datos por bloques de 1.000 filas.
- Se convierten los valores `0` y `1` a bytes para poder escribirlos en el archivo.
- Se agrega el carácter `|` al final de cada fila.
- Se guarda la matriz completa en `matriz.txt`.
- Se guarda la primera fila de la matriz en `primera_fila.txt`.
- Se verifica que la matriz sea válida (tamaño y elementos).
- Se muestra información sobre el tiempo que tardó el proceso y el tamaño de los archivos generados.

Los archivos `matriz.txt` y `primera_fila.txt` no se incluyen en el repositorio, ya que son generados automáticamente al ejecutar el programa.
