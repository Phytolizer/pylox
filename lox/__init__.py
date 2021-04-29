import sys
from typing import Union

from lox.ast.printer import AstPrinter
from lox.scanner import Scanner
from lox.parser import Parser
from lox.token import Token
from lox.token_type import TokenType

LOX_VERSION = "0.1.0"

s_had_error = False


def report(line: int, where: str, message: str) -> None:
    print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
    global s_had_error
    s_had_error = True


def error(location: Union[int, Token], message: str) -> None:
    if isinstance(location, int):
        report(location, "", message)
    elif isinstance(location, Token):
        if location.type == TokenType.EOF:
            report(location.line, " at end", message)
        else:
            report(location.line, f" at '{location.lexeme}'", message)


def run(source: str) -> None:
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    expr = parser.parse()

    if s_had_error:
        return

    print(AstPrinter().visit(expr))


def run_file(file_name: str) -> None:
    with open(file_name) as source_file:
        contents = source_file.read()
    run(contents)
    if s_had_error:
        exit(65)


def run_prompt() -> None:
    print(f"lox.py, version {LOX_VERSION}.")
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        run(line)

        # Ignore errors in REPL.
        global s_had_error
        s_had_error = False
