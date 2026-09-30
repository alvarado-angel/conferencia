class Nodo:
    def __init__(self, etiqueta, hijos=None):
        self.etiqueta = etiqueta
        self.hijos = hijos


class OpBinario:
    def __init__(self, operando_izq, operador, operando_der):
        self.operando_izq = operando_izq
        self.operador = operador
        self.operando_der = operando_der


class OpUnario:
    def __init__(self, operando):
        self.operando = operando


class Numero:
    def __init__(self, operando):
        self.operando = operando


# formalidad del manejo de errores
class ErrorSintactico(Exception):
    pass
