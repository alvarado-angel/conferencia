import argparse
import os
import sys

from parser import (
    Parser,
    evaluar,
    exportar_dot,
    imprimir_ast,
    imprimir_cst,
)
from scanner.lexer import imprimir_tokens, tokenizar


def exportar_errores_md(errores, nombre_archivo="errores.md"):
    filas = [
        "| # | Tipo | Mensaje |",
        "|---|---|---|",
    ]
    for i, e in enumerate(errores, start=1):
        tipo = "Léxico" if type(e).__name__ == "ErrorLexico" else "Sintáctico"
        mensaje = str(e).replace("|", "\\|").replace("\n", " ")
        filas.append(f"| {i} | {tipo} | {mensaje} |")

    os.makedirs("output", exist_ok=True)
    ruta = os.path.join("output", nombre_archivo)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(filas) + "\n")
    print(f" Errores exportados en '{ruta}'")


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

    # entrada
    print(f" {'==' * 4} CADENA DE ENTRADA {'==' * 4} ")
    print(f'"{entrada}"')
    print()

    # scanner
    tokens, errores = tokenizar(entrada)
    print(f" {'==' * 4} TOKENS {'==' * 4} ")
    imprimir_tokens(tokens)
    print()

    # parser
    parser = Parser(tokens)
    cst, ast = parser.parsear()

    # errores del parser
    if len(parser.errores) != 0:
        errores.extend(parser.errores)
        exportar_errores_md(errores)

        print(f" {'==' * 4} ERRORES {'==' * 4} ")
        print(
            "Se han detectado errores que no permiten continuar la ejecución del programa."
        )
        print()
        sys.exit(1)  # detenemos

    # generación del árbol y exportación
    if args.arbol == "cst":
        print(f" {'==' * 4} ÁRBOL DE ANÁLISIS SINTÁCTICO (CST)  {'==' * 4} ")
        imprimir_cst(cst)
        print()
        if args.exportar:
            exportar_dot(cst, "cst", "cst.dot")
    else:
        print(f" {'==' * 4} ÁRBOL DE SINTAXIS ABSTRACTA (AST)  {'==' * 4} ")
        imprimir_ast(ast)
        print()
        if args.exportar:
            exportar_dot(ast, "ast", "ast.dot")

    # resultado final
    resultado = evaluar(ast)
    print(f" {'==' * 4} RESULTADO  {'==' * 4} ")
    print(resultado)
    print()


if __name__ == "__main__":
    main()
