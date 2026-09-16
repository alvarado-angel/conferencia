from nodos import BinOp, NodoCST, Numero, UnaryOp


class ErrorSintactico(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def _actual(self):
        return self.tokens[self.pos]

    def _avanzar(self):
        tok = self.tokens[self.pos]
        if tok.tipo != "EOF":
            self.pos += 1
        return tok

    def parsear(self):
        cst, ast = self._expresion()
        if self._actual().tipo != "EOF":
            raise ErrorSintactico(f"Token inesperado: {self._actual()}")
        return cst, ast

    def _expresion(self):
        cst_izq, ast = self._termino()
        hijos_cst = [cst_izq]
        while self._actual().tipo in ("MAS", "MENOS"):
            op_tok = self._avanzar()
            hijos_cst.append(NodoCST(op_tok.valor))
            cst_der, ast_der = self._termino()
            hijos_cst.append(cst_der)
            ast = BinOp(ast, op_tok.valor, ast_der)
        return NodoCST("expresion", hijos_cst), ast

    def _termino(self):
        cst_izq, ast = self._factor()
        hijos_cst = [cst_izq]
        while self._actual().tipo in ("POR", "DIV"):
            op_tok = self._avanzar()
            hijos_cst.append(NodoCST(op_tok.valor))
            cst_der, ast_der = self._factor()
            hijos_cst.append(cst_der)
            ast = BinOp(ast, op_tok.valor, ast_der)
        return NodoCST("termino", hijos_cst), ast

    def _factor(self):
        if self._actual().tipo == "MENOS":
            self._avanzar()
            cst_operando, ast_operando = self._factor()
            cst = NodoCST("factor", [NodoCST("-"), cst_operando])
            ast = UnaryOp(ast_operando)
            return cst, ast
        cst_primario, ast_primario = self._primario()
        return NodoCST("factor", [cst_primario]), ast_primario

    def _primario(self):
        tok = self._actual()
        if tok.tipo == "NUMERO":
            self._avanzar()
            cst = NodoCST("primario", [NodoCST(f"NUMERO: {tok.valor}")])
            return cst, Numero(tok.valor)
        if tok.tipo == "PAREN_IZQ":
            self._avanzar()
            cst_expr, ast_expr = self._expresion()
            if self._actual().tipo != "PAREN_DER":
                raise ErrorSintactico("se esperaba ')'")
            self._avanzar()
            cst = NodoCST("primario", [NodoCST("("), cst_expr, NodoCST(")")])
            return cst, ast_expr
        raise ErrorSintactico(f"se esperaba un número o '(', se encontró: {tok}")
