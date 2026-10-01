# Conferencia Lenguajes Formales y de Programación

Calculadora capaz de sumar, restar, multiplicar, dividir y negar.

# Funcionalidades disponibles

el programa evalua expresiones aritméticas tomando en cuenta la jerarquía entre ellos, con los siguientes operadores:

1. agrupaciones
2. potencia
3. negación
4. producto y división
5. sumar y resta

> Nota: Los números son operandos, por ello no tienen precedencia ni asociatividad.

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

El argumento `--exportar` genera un archivo graphviz con el árbol seleccionado.

# Recursos

Herramientas utilizadas durante el desarrollo del ejemplo:

- [graphviz sandbox](https://dreampuf.github.io/GraphvizOnline/?engine=dot#digraph%20G%20%7B%0A%0A%20%20subgraph%20cluster_0%20%7B%0A%20%20%20%20style%3Dfilled%3B%0A%20%20%20%20color%3Dlightgrey%3B%0A%20%20%20%20node%20%5Bstyle%3Dfilled%2Ccolor%3Dwhite%5D%3B%0A%20%20%20%20a0%20-%3E%20a1%20-%3E%20a2%20-%3E%20a3%3B%0A%20%20%20%20label%20%3D%20%22process%20%231%22%3B%0A%20%20%7D%0A%0A%20%20subgraph%20cluster_1%20%7B%0A%20%20%20%20node%20%5Bstyle%3Dfilled%5D%3B%0A%20%20%20%20b0%20-%3E%20b1%20-%3E%20b2%20-%3E%20b3%3B%0A%20%20%20%20label%20%3D%20%22process%20%232%22%3B%0A%20%20%20%20color%3Dblue%0A%20%20%7D%0A%20%20start%20-%3E%20a0%3B%0A%20%20start%20-%3E%20b0%3B%0A%20%20a1%20-%3E%20b3%3B%0A%20%20b2%20-%3E%20a3%3B%0A%20%20a3%20-%3E%20a0%3B%0A%20%20a3%20-%3E%20end%3B%0A%20%20b3%20-%3E%20end%3B%0A%0A%20%20start%20%5Bshape%3DMdiamond%5D%3B%0A%20%20end%20%5Bshape%3DMsquare%5D%3B%0A%7D)

# Anexos

## Gramática Utilizada durante

teóricamente: 

```py
S ->  E 'EOF'
E ->  E '+' T
    | E '-' T
    | T
T ->  T '*' F
    | T '/' F
    | F
F ->  '-' F
    | P
P ->  V ** F
    | V
V ->  '(' E ')'
    | numero
```

### Características
- Es ambigua
- Es recursiva por izquierda
- No está factorizada por izquierda

### Supuestos

- Solo se requiere ejecutar una expresión matemática.
- Nuestra estrategia de manejo de errores es el modo pánico.
    - El token de sincronización durante el parseo es el final del documento (EOF).
- Detectar errores lexicos no implica detener el programa.
- la asociatividad y la precedencia de operadores están basadas en las convenciones comúnmente utilizadas en los lenguajes de programación.


