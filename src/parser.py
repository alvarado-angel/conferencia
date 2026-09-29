from nodos import BinOp, Nodo, Numero, UnaryOp


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

    # Expresion -> Termino ((+|-) Termino)*
    def _expresion(self):
        cst_izq, ast = self._termino()
        hijos_cst = [cst_izq]
        while self._actual().tipo in ("MAS", "MENOS"):
            op_tok = self._avanzar()
            hijos_cst.append(Nodo(op_tok.valor))
            cst_der, ast_der = self._termino()
            hijos_cst.append(cst_der)
            ast = BinOp(ast, op_tok.valor, ast_der)
        return Nodo("expresion", hijos_cst), ast

    # Termino -> Factor ((*|/) Factor)*
    def _termino(self):
        cst_izq, ast = self._factor()
        hijos_cst = [cst_izq]
        while self._actual().tipo in ("POR", "DIV"):
            op_tok = self._avanzar()
            hijos_cst.append(Nodo(op_tok.valor))
            cst_der, ast_der = self._factor()
            hijos_cst.append(cst_der)
            ast = BinOp(ast, op_tok.valor, ast_der)
        return Nodo("termino", hijos_cst), ast

    # Factor -> (- Factor) | Primario
    def _factor(self):
        if self._actual().tipo == "MENOS":
            self._avanzar()
            cst_operando, ast_operando = self._factor()
            cst = Nodo("factor", [Nodo("-"), cst_operando])
            ast = UnaryOp(ast_operando)
            return cst, ast
        cst_primario, ast_primario = self._primario()
        return Nodo("factor", [cst_primario]), ast_primario

    # Primario -> NUMERO | '(' Expresion ')'
    def _primario(self):
        tok = self._actual()
        if tok.tipo == "NUMERO":
            self._avanzar()
            cst = Nodo("primario", [Nodo(f"NUMERO: {tok.valor}")])
            return cst, Numero(tok.valor)
        if tok.tipo == "PAREN_IZQ":
            self._avanzar()
            cst_expr, ast_expr = self._expresion()
            if self._actual().tipo != "PAREN_DER":
                raise ErrorSintactico("se esperaba ')'")
            self._avanzar()
            cst = Nodo("primario", [Nodo("("), cst_expr, Nodo(")")])
            return cst, ast_expr
        raise ErrorSintactico(f"se esperaba un número o '(', se encontró: {tok}")
