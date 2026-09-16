class NodoCST:
    def __init__(self, etiqueta, hijos=None):
        self.etiqueta = etiqueta
        self.hijos = hijos or []


class BinOp:
    def __init__(self, izquierda, operador, derecha):
        self.izquierda = izquierda
        self.operador = operador
        self.derecha = derecha


class UnaryOp:
    def __init__(self, operando):
        self.operando = operando


class Numero:
    def __init__(self, valor):
        self.valor = valor
