from scanner import Token

from .nodos import *


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def _actual(self) -> Token:
        return self.tokens[self.pos]

    def _avanzar(self) -> Token:
        token = self.tokens[self.pos]
        if token.tipo != "EOF":
            self.pos += 1
        return token

    # expr -> term '+'/'-' term
    #     | term
    # term -> fact '*'/'/' fact
    #     | fact
    # fact -> '-' fact
    #     | prim
    # prim -> '(' expr ')'
    #     | numero

    def _expr(self):
        hijos_cst = []

        cst_izq, ast = self._term()
        hijos_cst.append(cst_izq)

        while self._actual().tipo in ("MAS", "MENOS"):
            operador = self._avanzar()
            nodo = Nodo(operador.valor)
            hijos_cst.append(nodo)

            cst_der, ast_der = self._term()
            hijos_cst.append(cst_der)
            ast = OpBinario(ast, operador.valor, ast_der)

        return Nodo("expr", hijos_cst), ast

    def _term(self):
        hijos_cst = []

        cst_izq, ast = self._fact()
        hijos_cst.append(cst_izq)

        while self._actual().tipo in ("POR", "DIV"):
            operador = self._avanzar()
            nodo = Nodo(operador.valor)
            hijos_cst.append(nodo)

            cst_der, ast_der = self._fact()
            hijos_cst.append(cst_der)
            ast = OpBinario(ast, operador.valor, ast_der)

        return Nodo("term", hijos_cst), ast

    def _fact(self):
        if self._actual().tipo == "MENOS":
            self._avanzar()
            cst_operando, ast_operando = self._fact()
            cst = Nodo("fact", [Nodo("-"), cst_operando])
            ast = OpUnario(ast_operando)
            return cst, ast

        cst_prim, ast_prim = self._prim()
        return Nodo("fact", [cst_prim]), ast_prim

    def _prim(self):
        token = self._actual()

        if token.tipo == "NUMERO":
            self._avanzar()
            cst = Nodo("prim", [Nodo(token.valor)])
            return cst, Numero(token.valor)

        if token.tipo == "PAR_IZQ":
            self._avanzar()
            cst_expr, ast_expr = self._expr()
            if self._actual().tipo != "PAR_DER":
                raise ErrorSintactico(
                    f'[ERROR SINTACTICO]: Se esperaba un ")", se encontró {token}'
                )

            self._avanzar()
            cst = Nodo("prim", [Nodo("("), cst_expr, Nodo(")")])
            return cst, ast_expr

        raise ErrorSintactico(
            f'[ERROR SINTACTICO]: se esperaba un número o "(", se encontró: {token}'
        )

    def parsear(self):
        cst, ast = self._expr()
        if self._actual().tipo != "EOF":
            raise ErrorSintactico(f"Token inesperado: {self._actual()}")
        return cst, ast
