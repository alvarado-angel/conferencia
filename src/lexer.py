class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"{self.tipo}({self.valor})" if self.valor != "" else self.tipo


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
            tokens.append(Token("NUMERO", int(texto[inicio:pos])))
            continue

        simbolos = {
            "+": "MAS",
            "-": "MENOS",
            "*": "POR",
            "/": "DIV",
            "(": "PAREN_IZQ",
            ")": "PAREN_DER",
        }
        if c in simbolos:
            tokens.append(Token(simbolos[c], c))
            pos += 1
            continue

        raise ValueError(f"Carácter no reconocido: '{c}'")

    tokens.append(Token("EOF", ""))
    return tokens
