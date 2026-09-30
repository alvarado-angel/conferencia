from .reservadas import *
from .token import *


def tokenizar(cadena: str):
    tokens = []
    pos = 0

    while pos < len(cadena):
        caracter = cadena[pos]

        # quitar ruido blanco
        if caracter in ruido:
            pos += 1
            continue

        # validar reservadas
        if caracter in reservadas:
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
        raise ErrorLexico(
            f'[ERROR LEXICO]: El caracter "{caracter}" no pertenece al lenguaje.'
        )

    tokens.append(Token("EOF", ""))
    return tokens
