from nodos import BinOp, Numero, UnaryOp


def _etiqueta_ast(nodo):
    if isinstance(nodo, Numero):
        return str(nodo.valor)
    if isinstance(nodo, UnaryOp):
        return "- (unario)"
    if isinstance(nodo, BinOp):
        return nodo.operador
    return "?"


def _hijos_ast(nodo):
    if isinstance(nodo, BinOp):
        return [nodo.izquierda, nodo.derecha]
    if isinstance(nodo, UnaryOp):
        return [nodo.operando]
    return []


def imprimir_arbol(
    nodo, obtener_etiqueta, obtener_hijos, prefijo="", es_ultimo=True, es_raiz=True
):
    conector = "" if es_raiz else ("└── " if es_ultimo else "├── ")
    print(f"{prefijo}{conector}[{obtener_etiqueta(nodo)}]")

    hijos = obtener_hijos(nodo)
    extension = "" if es_raiz else ("    " if es_ultimo else "│   ")
    nuevo_prefijo = prefijo + extension
    for i, hijo in enumerate(hijos):
        imprimir_arbol(
            hijo,
            obtener_etiqueta,
            obtener_hijos,
            nuevo_prefijo,
            i == len(hijos) - 1,
            es_raiz=False,
        )


def imprimir_cst(nodo_cst):
    imprimir_arbol(nodo_cst, lambda n: n.etiqueta, lambda n: n.hijos)


def imprimir_ast(nodo_ast):
    imprimir_arbol(nodo_ast, _etiqueta_ast, _hijos_ast)


def evaluar(nodo):
    if isinstance(nodo, Numero):
        return nodo.valor
    if isinstance(nodo, UnaryOp):
        return -evaluar(nodo.operando)
    if isinstance(nodo, BinOp):
        izq = evaluar(nodo.izquierda)
        der = evaluar(nodo.derecha)
        if nodo.operador == "+":
            return izq + der
        if nodo.operador == "-":
            return izq - der
        if nodo.operador == "*":
            return izq * der
        if nodo.operador == "/":
            return izq / der
    raise TypeError(f"Nodo no reconocido: {nodo}")
