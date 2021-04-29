import sys
from typing import Tuple

from lox.token import Token
from lox.scanner import Scanner

LOX_VERSION: str = "0.1.0"

s_had_error: bool = False


def report(line: int, where: str, message: str) -> None:
    print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
    global s_had_error
    s_had_error = True


def error(line: int, message: str) -> None:
    report(line, "", message)


def run(source: str) -> None:
    scanner = Scanner(source)
    tokens: Tuple[Token] = scanner.scan_tokens()

    for token in tokens:
        print(token)


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
