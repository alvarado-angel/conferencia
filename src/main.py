import argparse
import sys

from parser import evaluar
from parser.evaluar import imprimir_ast, imprimir_cst
from parser.exportar import exportar_dot
from parser.nodos import ErrorSintactico
from parser.parser import Parser
from scanner.lexer import tokenizar
from scanner.token import ErrorLexico, imprimir_tokens


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

    try:
        # scanner
        tokens = tokenizar(entrada)
        print("=== TOKENS ===")
        imprimir_tokens(tokens)
        print()
        # parser
        cst, ast = Parser(tokens).parsear()
    except (ErrorLexico, ErrorSintactico) as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    if args.arbol == "cst":
        print("=== ÁRBOL DE ANÁLISIS SINTÁCTICO (CST) ===")
        imprimir_cst(cst)
        if args.exportar:
            exportar_dot(cst, "cst", "cst.dot")
    else:
        print("=== ÁRBOL DE SINTAXIS ABSTRACTA (AST) ===")
        imprimir_ast(ast)
        if args.exportar:
            exportar_dot(ast, "ast", "ast.dot")

    resultado = evaluar(ast)
    print("\n=== RESULTADO ===")
    print(f"  {resultado}")


if __name__ == "__main__":
    main()
