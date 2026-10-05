from scanner import Token

from .nodos import *


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.errores = []
        self.pos = 0

    # token actual
    def _actual(self) -> Token:
        return self.tokens[self.pos]

    # avanzar al siguiente token
    def _avanzar(self) -> Token:
        token = self.tokens[self.pos]
        if token.tipo != "EOF":
            self.pos += 1
        return token

    # errores
    def _error(self, err: Exception) -> None:
        if not self.errores:
            self.errores.append(err)

    def _sincronizar(self) -> None:
        while self._actual().tipo != "EOF":
            self._avanzar()

    # gramática
    # S -> E 'EOF'
    # E -> E '+'/'-' T
    #   | T
    # T -> T '*'/'/' F
    #   | F
    # F -> '-' F
    #   | P
    # P -> V ** F
    #   | V
    # V -> '(' E ')'
    #   | numero

    def _E(self):
        cst_izq, ast = self._T()
        cst = Nodo("E", [cst_izq])

        while self._actual().tipo in ("MAS", "MENOS"):
            operador = self._avanzar()
            cst_der, ast_der = self._T()
            cst = Nodo("E", [cst, Nodo(operador.valor), cst_der])
            ast = OpBinario(ast, operador.valor, ast_der)

        return cst, ast

    def _T(self):
        cst_izq, ast = self._F()
        cst = Nodo("T", [cst_izq])

        while self._actual().tipo in ("POR", "DIV"):
            operador = self._avanzar()
            cst_der, ast_der = self._F()
            cst = Nodo("T", [cst, Nodo(operador.valor), cst_der])
            ast = OpBinario(ast, operador.valor, ast_der)

        return cst, ast

    def _F(self):
        if self._actual().tipo == "MENOS":
            self._avanzar()
            cst_operando, ast_operando = self._F()
            cst = Nodo("F", [Nodo("-"), cst_operando])
            ast = OpUnario(ast_operando)
            return cst, ast

        cst_P, ast_P = self._P()
        return Nodo("F", [cst_P]), ast_P

    def _P(self):
        cst_base, ast = self._V()

        if self._actual().tipo == "EXPO":
            self._avanzar()
            cst_exp, ast_exp = self._F()
            cst = Nodo("P", [cst_base, Nodo("**"), cst_exp])
            ast = OpBinario(ast, "**", ast_exp)
            return cst, ast

        cst = Nodo("P", [cst_base])
        return cst, ast

    def _V(self):
        token = self._actual()

        if token.tipo == "NUMERO":
            self._avanzar()
            cst = Nodo("V", [Nodo(token.valor)])
            ast = Numero(token.valor)
            return cst, ast

        if token.tipo == "PAR_IZQ":
            self._avanzar()
            cst_E, ast_E = self._E()

            if self._actual().tipo == "PAR_DER":
                self._avanzar()
                return Nodo("V", [Nodo("("), cst_E, Nodo(")")]), ast_E

            # si no viene par der, hay error
            self._error(
                ErrorSintactico(f'Se esperaba ")", se encontró {self._actual()}')
            )
            self._sincronizar()
            return None, None

        # si no viene número o (
        self._error(
            ErrorSintactico(f'Se esperaba un número o "(", se encontró: {token}')
        )
        self._sincronizar()
        return None, None

    def parsear(self):
        # aquí empieza todo
        cst, ast = self._E()

        # si el token actual no es EOF entonces tenemos un error
        if self._actual().tipo != "EOF":
            err = ErrorSintactico(f"Token inesperado: {self._actual()}")
            self._error(err)
            self._sincronizar()

        if self.errores:
            return None, None

        return cst, ast
