class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"{self.tipo}({self.valor})" if self.valor != "" else self.tipo


from reservadas import simbolos


def tokenizar(texto):
    tokens = []
    pos = 0

    while pos < len(texto):
        c = texto[pos]

        if c in (" ", "\t", "\r", "\n"):
            pos += 1
            continue

        if c.isdigit():
            inicio = pos
            while pos < len(texto) and texto[pos].isdigit():
                pos += 1
            token = Token("NUMERO", int(texto[inicio:pos]))
            tokens.append(token)
            continue

        if c in simbolos:
            token = Token(simbolos[c], c)
            tokens.append(token)
            pos += 1
            continue

        raise ValueError(f"Carácter no reconocido: '{c}'")

    tokens.append(Token("EOF", ""))
    return tokens


def imprimir_tokens(tokens):
    ancho_tipo = max(len(tok.tipo) for tok in tokens) + 2
    ancho_valor = max(len(str(tok.valor)) for tok in tokens) + 2
    ancho_pos = max(len(str(i)) for i in range(len(tokens))) + 2

    print(f"{'#':<{ancho_pos}}{'TIPO':<{ancho_tipo}}{'VALOR':<{ancho_valor}}")
    print("-" * (ancho_pos + ancho_tipo + ancho_valor))

    for i, tok in enumerate(tokens):
        valor = tok.valor if tok.valor != "" else ""
        print(f"{i:<{ancho_pos}}{tok.tipo:<{ancho_tipo}}{str(valor):<{ancho_valor}}")
