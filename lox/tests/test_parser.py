import pytest

from lox import s_had_error
from lox.ast.printer import AstPrinter
from lox.scanner import Scanner
from lox.parser import Parser


@pytest.mark.parametrize("text,expected", [
    ("1", "1"),
    ("1 + 2", "(+ 1 2)"),
    ("1 + 2 * 3", "(+ 1 (* 2 3))"),
    ("(1 + 2) * 3", "(* (group (+ 1 2)) 3)"),
])
def test_arithmetic_expressions(text: str, expected: str):
    scanner = Scanner(text)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    expr = parser.parse()
    assert not s_had_error
    printed = AstPrinter().visit(expr)
    assert printed == expected
