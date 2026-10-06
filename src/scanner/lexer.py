from tkinter import N

from .reservadas import *
from .token import *


def tokenizar(cadena: str) -> tuple[list[Token], list[Exception]]:
    tokens = []
    errores = []
    pos = 0

    while pos < len(cadena):
        caracter = cadena[pos]

        # quitar ruido blanco
        if caracter in ruido:
            pos += 1
            continue

        # validar reservadas
        if caracter in reservadas:
            # potencia es un caso especial
            if caracter == "*" and pos + 1 < len(cadena) and cadena[pos + 1] == "*":
                token = Token(reservadas["**"], "**")
                tokens.append(token)
                pos += 2
                continue

            token = Token(reservadas[caracter], caracter)
            tokens.append(token)
            pos += 1
            continue

        # validar digitos
        if caracter.isdigit():
            inicio = pos
            while pos < len(cadena) and cadena[pos].isdigit():
                pos += 1
            token = Token("NUMERO", int(cadena[inicio:pos]))
            tokens.append(token)
            continue

        # manejar errores
        errores.append(
            ErrorLexico(f'El caracter "{caracter}" no pertenece al lenguaje.')
        )
        pos += 1

    tokens.append(Token("EOF", None))
    return tokens, errores
