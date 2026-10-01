from scanner import Token

from .nodos import Nodo, Numero, OpBinario, OpUnario


def _etiqueta_ast(nodo: Nodo):
    if isinstance(nodo, Numero):
        return str(nodo.valor)
    if isinstance(nodo, OpUnario):
        return "- (unario)"
    if isinstance(nodo, OpBinario):
        return nodo.operador
    return "?"


def _hijos_ast(nodo: Nodo):
    if isinstance(nodo, OpBinario):
        return [nodo.operando_izq, nodo.operando_der]
    if isinstance(nodo, OpUnario):
        return [nodo.operando]
    return []


def imprimir_arbol(
    nodo, obtener_etiqueta, obtener_hijos, prefijo="", es_ultimo=True, es_raiz=True
):
    conector = "" if es_raiz else ("└── " if es_ultimo else "├── ")
    print(f"{prefijo}{conector}[{obtener_etiqueta(nodo)}]")

    hijos = obtener_hijos(nodo)
    extension = "" if es_raiz else ("\t" if es_ultimo else "│\t")
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


def evaluar(nodo: Nodo):
    if isinstance(nodo, Numero):
        return nodo.valor
    if isinstance(nodo, OpUnario):
        return -evaluar(nodo.operando)
    if isinstance(nodo, OpBinario):
        izq = evaluar(nodo.operando_izq)
        der = evaluar(nodo.operando_der)
        if nodo.operador == "+":
            return izq + der
        if nodo.operador == "-":
            return izq - der
        if nodo.operador == "*":
            return izq * der
        if nodo.operador == "/":
            return izq / der
    raise TypeError(f"Nodo no reconocido: {nodo}")
