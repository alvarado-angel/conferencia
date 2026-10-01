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
        hijos_cst = [cst_izq]

        while self._actual().tipo in ("MAS", "MENOS"):
            operador = self._avanzar()
            nodo = Nodo(operador.valor)
            hijos_cst.append(nodo)

            cst_der, ast_der = self._T()
            hijos_cst.append(cst_der)
            ast = OpBinario(ast, operador.valor, ast_der)

        return Nodo("E", hijos_cst), ast

    def _T(self):
        cst_izq, ast = self._F()
        hijos_cst = [cst_izq]

        while self._actual().tipo in ("POR", "DIV"):
            operador = self._avanzar()
            nodo = Nodo(operador.valor)
            hijos_cst.append(nodo)

            cst_der, ast_der = self._F()
            hijos_cst.append(cst_der)
            ast = OpBinario(ast, operador.valor, ast_der)

        return Nodo("T", hijos_cst), ast

    def _F(self):
        if self._actual().tipo == "MENOS":
            self._avanzar()
            cst_operando, ast_operando = self._F()
            cst = Nodo("F", [Nodo("-"), cst_operando])
            return cst, OpUnario(ast_operando)

        cst_P, ast_P = self._P()
        return Nodo("F", [cst_P]), ast_P

    def _P(self):
        cst_base, ast = self._V()

        if self._actual().tipo == "EXPO":
            self._avanzar()
            cst_exp, ast_exp = self._F()
            cst = Nodo("P", [cst_base, Nodo("**"), cst_exp])
            return cst, OpBinario(ast, "**", ast_exp)

        return Nodo("P", [cst_base]), ast

    def _V(self):
        token = self._actual()

        if token.tipo == "NUMERO":
            self._avanzar()
            return Nodo("V", [Nodo(token.valor)]), Numero(token.valor)

        if token.tipo == "PAR_IZQ":
            self._avanzar()
            cst_E, ast_E = self._E()

            if self._actual().tipo == "PAR_DER":
                self._avanzar()
            elif not self.errores:  # si ya hay error, no reportes en cascada
                self._error(
                    ErrorSintactico(
                        f'[ERROR SINTACTICO]: Se esperaba ")", se encontró {self._actual()}'
                    )
                )
                self._sincronizar()

            return Nodo("V", [Nodo("("), cst_E, Nodo(")")]), ast_E

        # no hay número ni "("
        self._error(
            ErrorSintactico(
                f'[ERROR SINTACTICO]: se esperaba un número o "(", se encontró: {token}'
            )
        )
        self._sincronizar()
        return None, None

    def parsear(self):
        cst, ast = self._E()

        if self._actual().tipo != "EOF":
            self._error(
                ErrorSintactico(
                    f"[ERROR SINTACTICO]: Token inesperado: {self._actual()}"
                )
            )
            self._sincronizar()

        if self.errores:
            return None, None
        return cst, ast
