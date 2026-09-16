# Conferencia Lenguajes Formales y de Programación

Ejemplo práctico de una calculadora con suma, resta, multiplicación, división y negación.
Tomando en cuenta análisis léxico y sintáctico.

# Funcionalidades disponibles

el programa evalua expresiones aritméticas respetando la jerarquía de operadores, con las
siguientes operaciones:

1. agrupaciones
2. negación
3. producto y división
4. sumar y resta

> Nota la presedencia de operadores nos dice qué operador binario o unário se visita primero en el árbol.

# Ejecución

tomar en cuenta que la mínima instrucción posible es:

```bash
python3 src/main.py archivo.txt --arbol parametro
```

donde:

- **archivo.txt:** corresponde al archivo que contiene la expresión matemática.
- **parametro** : puede ser `ast` o `cst` , dependiendo del tipo de árbol que queremos visualizar

Adicionalmente podemos tener un tercer argumento:

```bash
python3 src/main.py archivo.txt --arbol parametro --exportar
```

> Nota:`--exportar` genera un archivo graphviz con el árbol ast o cst para visualizarlo en [graphviz sandbox](https://dreampuf.github.io/GraphvizOnline/?engine=dot#digraph%20G%20%7B%0A%0A%20%20subgraph%20cluster_0%20%7B%0A%20%20%20%20style%3Dfilled%3B%0A%20%20%20%20color%3Dlightgrey%3B%0A%20%20%20%20node%20%5Bstyle%3Dfilled%2Ccolor%3Dwhite%5D%3B%0A%20%20%20%20a0%20-%3E%20a1%20-%3E%20a2%20-%3E%20a3%3B%0A%20%20%20%20label%20%3D%20%22process%20%231%22%3B%0A%20%20%7D%0A%0A%20%20subgraph%20cluster_1%20%7B%0A%20%20%20%20node%20%5Bstyle%3Dfilled%5D%3B%0A%20%20%20%20b0%20-%3E%20b1%20-%3E%20b2%20-%3E%20b3%3B%0A%20%20%20%20label%20%3D%20%22process%20%232%22%3B%0A%20%20%20%20color%3Dblue%0A%20%20%7D%0A%20%20start%20-%3E%20a0%3B%0A%20%20start%20-%3E%20b0%3B%0A%20%20a1%20-%3E%20b3%3B%0A%20%20b2%20-%3E%20a3%3B%0A%20%20a3%20-%3E%20a0%3B%0A%20%20a3%20-%3E%20end%3B%0A%20%20b3%20-%3E%20end%3B%0A%0A%20%20start%20%5Bshape%3DMdiamond%5D%3B%0A%20%20end%20%5Bshape%3DMsquare%5D%3B%0A%7D)
