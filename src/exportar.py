from nodos import BinOp, Numero, UnaryOp


def exportar_dot(raiz, tipo, nombre_archivo):
    lineas = [
        "digraph G {",
        '\tlabel="titulo del diagrama";',
        '\tlabelloc="t";',
        "\tfontsize=20;",
        '\tfontname="Arial";',
        "\tnode [shape=box];",
    ]
    contador = 0

    def _recorrer_cst(nodo):
        nonlocal contador
        id_actual = f"node{contador}"
        contador += 1
        etiqueta_limpia = str(nodo.etiqueta).replace('"', '\\"')
        lineas.append(f'\t{id_actual} [label="{etiqueta_limpia}"];')

        for hijo in nodo.hijos:
            id_hijo = _recorrer_cst(hijo)
            lineas.append(f"\t{id_actual} -> {id_hijo};")
        return id_actual

    def _recorrer_ast(nodo):
        nonlocal contador
        id_actual = f"node{contador}"
        contador += 1

        if isinstance(nodo, Numero):
            etiqueta = str(nodo.valor)
            hijos = []
        elif isinstance(nodo, UnaryOp):
            etiqueta = "-"
            hijos = [nodo.operando]
        elif isinstance(nodo, BinOp):
            etiqueta = nodo.operador
            hijos = [nodo.izquierda, nodo.derecha]
        else:
            etiqueta = "?"
            hijos = []

        lineas.append(f'\t{id_actual} [label="{etiqueta}"];')
        for hijo in hijos:
            id_hijo = _recorrer_ast(hijo)
            lineas.append(f"\t{id_actual} -> {id_hijo};")
        return id_actual

    if tipo == "cst":
        lineas[1] = '\tlabel="Árbol de análisis de sintaxis";'
        _recorrer_cst(raiz)
    else:
        lineas[1] = '\tlabel="Árbol de sintaxis";'
        _recorrer_ast(raiz)

    lineas.append("}\n")

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))
    print(f" A[rchivo DOT exportado exitosamente como '{nombre_archivo}'")
