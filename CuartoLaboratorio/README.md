# Laboratorio #4: Sistema de Logística de Entregas

## 1. Descripción del Problema y Objetivo

Se tienen las coordenadas (x, y) de **10.000 puntos de entrega** en una ciudad, y se necesita un sistema que pueda responder dos cosas: qué puntos de entrega están a un radio de **500 metros** de un punto dado, y cuál es el punto de entrega **más cercano** a una ubicación dada. Los datos son estáticos (no cambian).
 
Los puntos se generan al azar con una semilla, en una ciudad de 10.000 m × 10.000 m. Todo está en metros.

### Objetivos

- Implementar un Quadtree desde cero (en 2D) que responda las necesidades del sistema de entregas.
- Comparar el rendimiento del Quadtree con la fuerza bruta (una lista).
- Visualizar y verificar los resultados de las búsquedas.
- Responder desde qué tamaño de datos el Quadtree empieza a ser más rápido que la fuerza bruta.

## Estructuras de Datos y Algoritmos

### `Quadtree.py`

Se implementaron las funciones de fuerza bruta y la función para generar los datos, y el Quadtree para dos dimensiones.
