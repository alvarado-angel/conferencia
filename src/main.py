import argparse
import sys
from parser import ErrorSintactico, Parser

from evaluar import evaluar, imprimir_ast, imprimir_cst
from exportar import exportar_dot
from lexer import tokenizar


def main():
    argp = argparse.ArgumentParser(description="Procesa expresiones y genera AST/CST.")
    argp.add_argument("archivo", help="Ruta al archivo con la expresión")
    argp.add_argument(
        "--arbol",
        choices=["cst", "ast"],
        required=True,
        help="Tipo de árbol: 'cst' o 'ast'",
    )
    argp.add_argument(
        "--exportar",
        action="store_true",
        help="Exporta el árbol a un archivo .dot (cst.dot o ast.dot)",
    )
    args = argp.parse_args()

    try:
        with open(args.archivo, "r", encoding="utf-8") as f:
            expresion_texto = f.read().strip()
    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo '{args.archivo}'")
        sys.exit(1)

    print(f"Expresión leída de '{args.archivo}': {expresion_texto}\n")

    try:
        tokens = tokenizar(expresion_texto)
        cst, ast = Parser(tokens).parsear()
    except (ValueError, ErrorSintactico) as e:
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
