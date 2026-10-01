class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"<{self.tipo}, {self.tipo if self.valor != 'EOF' else ''}>"

    def __str__(self):
        return f"{self.tipo}({self.valor if self.valor != 'EOF' else ''})"


# formalidad del manejo de errores
class ErrorLexico(Exception):
    pass


# imprime la tabla de tokens
def imprimir_tokens(tokens: list[Token]) -> None:
    ancho_pos = max(len(str(i)) for i in range(len(tokens))) + 2
    ancho_tipo = max(len(tok.tipo) for tok in tokens) + 2
    ancho_valor = max(len(str(tok.valor)) for tok in tokens) + 2

    print(f"{'#':<{ancho_pos}}{'TIPO':<{ancho_tipo}}{'VALOR':<{ancho_valor}}")
    print("-" * (ancho_pos + ancho_tipo + ancho_valor))

    for i, tok in enumerate(tokens):
        valor = tok.valor if tok.valor != "" else ""
        print(f"{i:<{ancho_pos}}{tok.tipo:<{ancho_tipo}}{valor!s:<{ancho_valor}}")
