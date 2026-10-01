from .nodos import Nodo, Numero, OpBinario, OpUnario


def exportar_dot(raiz, tipo, nombre_archivo):
    lineas = [
        "digraph G {",
        '\tlabel="titulo del diagrama";',
        '\tlabelloc="t";',
        "\tfontsize=20;",
        '\tfontname="Arial";',
        "\tnode [shape=circle];",
        '\tnode [shape=circle, style="filled", fillcolor="#EBF5FB", color="#2980B9", fontname="Helvetica",',
        '\t\tfontcolor="#2C3E50", penwidth=2, width=0.8];',
        '\tedge [color="#7F8C8D", penwidth=1.5];',
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

    def _recorrer_ast(nodo: Nodo):
        nonlocal contador
        id_actual = f"node{contador}"
        contador += 1

        if isinstance(nodo, Numero):
            etiqueta = str(nodo.valor)
            hijos = []
        elif isinstance(nodo, OpUnario):
            etiqueta = "-"
            hijos = [nodo.operando]
        elif isinstance(nodo, OpBinario):
            etiqueta = nodo.operador
            hijos = [nodo.operando_izq, nodo.operando_der]
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
    print(f" Archivo DOT exportado exitosamente como '{nombre_archivo}'")
