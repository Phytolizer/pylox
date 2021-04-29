from typing import List, Tuple
from math import isclose
from pytest import mark

import lox
from lox.scanner import Scanner
from lox.syntax_facts import requires_separator, text_for_type
from lox.token import Token
from lox.token_type import TokenType


def scan(text: str) -> Tuple[Token, ...]:
    scanner = Scanner(text)
    lox.s_had_error = False
    tokens = scanner.scan_tokens()
    assert not lox.s_had_error
    return tokens


def check_single_token(text: str,
                       expected_type: TokenType,
                       expected_text: str = None):
    if expected_text is None:
        expected_text = text
    tokens = scan(text)
    assert len(tokens) == 2
    assert tokens[0].type == expected_type
    assert tokens[0].lexeme == expected_text.strip()
    assert tokens[1].type == TokenType.EOF
    return tokens[0]


def get_single_tokens_data():
    for type in TokenType:
        if type == TokenType.EOF or text_for_type(type) is None:
            continue
        yield (text_for_type(type), Token(type, text_for_type(type), None, 1))


@mark.parametrize("text,expected", get_single_tokens_data())
def test_single_token_scanning(text, expected):
    check_single_token(text, expected.type, expected.lexeme)


def check_string(text: str):
    token = check_single_token(text, TokenType.STRING)
    assert token.literal == text.strip("\n ")[1:-1]


def test_empty_string_literal():
    check_string('""')


def test_basic_string_literal():
    check_string('"foobar"')


def test_string_literal_with_spaces():
    check_string('"test set"')


def test_string_literal_with_newlines():
    check_string("""
    "
    test
    set
    "
    """)


def check_number(text: str):
    token = check_single_token(text, TokenType.NUMBER)
    assert isclose(token.literal, float(text.strip()))


def test_simple_number():
    check_number("1")


def test_decimal_point():
    check_number("1.2")


def test_longer_number():
    check_number("123.456")


def test_very_large_number():
    check_number("473897328957398247293")


def two_separated_tokens_data():
    for left in TokenType:
        if left == TokenType.EOF or text_for_type(left) is None:
            continue
        for right in TokenType:
            if right == TokenType.EOF or text_for_type(right) is None:
                continue
            if requires_separator(left, right):
                for separator in (" ", "\t", "\r", "\n"):
                    yield (text_for_type(left), separator, text_for_type(right))
            else:
                yield (text_for_type(left), "", text_for_type(right))


@mark.parametrize("left,sep,right", two_separated_tokens_data())
def test_two_separated_tokens(left, sep, right):
    scanner = Scanner(f"{left}{sep}{right}")
    tokens = scanner.scan_tokens()
    assert len(tokens) == 3
    assert tokens[0].lexeme == left
    assert tokens[1].lexeme == right
