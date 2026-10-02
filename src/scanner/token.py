import os


class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"<{self.tipo}, {self.valor if self.tipo != 'EOF' else ''}>"

    def __str__(self):
        return f"<{self.tipo}, {self.valor if self.tipo != 'EOF' else ''}>"


# formalidad del manejo de errores
class ErrorLexico(Exception):
    pass


# imprime la tabla de tokens
def exportar_tokens(tokens: list[Token]) -> None:

    lineas = ["| # | TIPO | VALOR |"]
    lineas.append("|---|---|---|")

    for i, token in enumerate(tokens, start=1):
        lineas.append(f"| {i} | {token.tipo} | {token.valor} |")

    # guardar
    os.makedirs("output", exist_ok=True)
    ruta = os.path.join("output", "tokens.md")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))

    print(f" {'==' * 4} TABLA DE TOKENS {'==' * 4} ")
    print("Tabla de tokens exportada exitosamente.")
    print()
