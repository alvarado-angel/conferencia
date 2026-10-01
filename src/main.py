import argparse
import sys

from parser import (
    ErrorSintactico,
    Parser,
    evaluar,
    exportar_dot,
    imprimir_ast,
    imprimir_cst,
)
from scanner.lexer import ErrorLexico, imprimir_tokens, tokenizar


def main():
    # argumentos y parametros
    args = argparse.ArgumentParser(
        description="Procesa expresiones y genera árbol CST o AST."
    )
    args.add_argument("archivo", help="archivo que contiene la expresión a analizar.")
    args.add_argument(
        "--arbol",
        choices=["cst", "ast"],
        required=True,
        help="Tipo de árbol que queremos generar (cst o ast).",
    )
    args.add_argument(
        "--exportar",
        action="store_true",
        help="Genera un archivo con código graphviz del árbol generado.",
    )
    args = args.parse_args()

    # abriendo el archivo
    try:
        with open(args.archivo, "r", encoding="utf-8") as contenido:
            entrada = contenido.read().strip()
    except FileNotFoundError:
        print(f"[ERROR]: No se ha encontrado el archivo {args.archivo}.")
        sys.exit(1)

    # entrada recibida
    print(f" {'==' * 4} CADENA DE ENTRADA {'==' * 4} ")
    print(f'"{entrada}"')
    print()

    try:
        # scanner
        tokens = tokenizar(entrada)
        print(f" {'==' * 4} TOKENS {'==' * 4} ")
        imprimir_tokens(tokens)
        print()
        # parser
        cst, ast = Parser(tokens).parsear()
    except (ErrorLexico, ErrorSintactico) as e:
        print(e)
        sys.exit(1)

    # generación del árbol y exportación
    if args.arbol == "cst":
        print(f" {'==' * 4} ÁRBOL DE ANÁLISIS SINTÁCTICO (CST)  {'==' * 4} ")
        imprimir_cst(cst)
        if args.exportar:
            exportar_dot(cst, "cst", "cst.dot")
    else:
        print(f" {'==' * 4} ÁRBOL DE SINTAXIS ABSTRACTA (AST)  {'==' * 4} ")
        imprimir_ast(ast)
        if args.exportar:
            exportar_dot(ast, "ast", "ast.dot")
    print()

    # resultado final
    resultado = evaluar(ast)
    print(f" {'==' * 4} RESULTADO  {'==' * 4} ")
    print(resultado)
    print()


if __name__ == "__main__":
    main()
