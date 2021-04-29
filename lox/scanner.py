from typing import Any, List, Tuple

from lox.token_type import TokenType
from lox.token import Token
import lox

KEYWORDS = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


def is_digit(c: str) -> bool:
    return "0" <= c and c <= "9"


def is_alpha(c: str) -> bool:
    return "a" <= c and c <= "z" or "A" <= c and c <= "Z" or c == "_"


class Scanner:
    _source: str
    _tokens: List[Token]
    _start: int
    _current: int
    _line: int

    def _at_end(self) -> bool:
        return self._current >= len(self._source)

    def _scan_token(self) -> None:
        c: str = self._advance()
        if c == "(":
            self._add_token(TokenType.LEFT_PAREN)
        elif c == ")":
            self._add_token(TokenType.RIGHT_PAREN)
        elif c == "{":
            self._add_token(TokenType.LEFT_BRACE)
        elif c == "}":
            self._add_token(TokenType.RIGHT_BRACE)
        elif c == ",":
            self._add_token(TokenType.COMMA)
        elif c == ".":
            self._add_token(TokenType.DOT)
        elif c == "-":
            self._add_token(TokenType.MINUS)
        elif c == "+":
            self._add_token(TokenType.PLUS)
        elif c == ";":
            self._add_token(TokenType.SEMICOLON)
        elif c == "*":
            self._add_token(TokenType.STAR)
        elif c == "!":
            self._two_char_token("=", TokenType.BANG_EQUAL, TokenType.BANG)
        elif c == "=":
            self._two_char_token("=", TokenType.EQUAL_EQUAL, TokenType.EQUAL)
        elif c == "<":
            self._two_char_token("=", TokenType.LESS_EQUAL, TokenType.LESS)
        elif c == ">":
            self._two_char_token("=", TokenType.GREATER_EQUAL,
                                 TokenType.GREATER)
        elif c == "/":
            if self._match("/"):
                while self._peek() != "\n" and not self._at_end():
                    self._advance()
            else:
                self._add_token(TokenType.SLASH)
        elif c in (" ", "\r", "\t"):
            pass
        elif c == "\n":
            self._line += 1
        elif c == '"':
            self._string()
        elif is_digit(c):
            self._number()
        elif is_alpha(c):
            self._identifier()
        else:
            lox.error(self._line, "Unexpected character.")

    def _string(self) -> None:
        while self._peek() != '"' and not self._at_end():
            if self._peek() == "\n":
                self._line += 1
            self._advance()
        if self._at_end():
            lox.error(self._line, "Unterminated string.")
            return
        self._advance()
        value = self._source[self._start + 1:self._current - 1]
        self._add_token(TokenType.STRING, value)

    def _number(self) -> None:
        while is_digit(self._peek()):
            self._advance()

        if self._peek() == "." and is_digit(self._peek_next()):
            self._advance()
            while is_digit(self._peek()):
                self._advance()

        self._add_token(TokenType.NUMBER,
                        float(self._source[self._start:self._current]))

    def _identifier(self) -> None:
        while is_alpha(self._peek()) or is_digit(self._peek()):
            self._advance()

        text = self._source[self._start:self._current]
        try:
            self._add_token(KEYWORDS[text])
        except KeyError:
            self._add_token(TokenType.IDENTIFIER)

    def _peek(self) -> str:
        if self._at_end():
            return "\0"
        else:
            return self._source[self._current]

    def _peek_next(self) -> str:
        if self._current + 1 >= len(self._source):
            return "\0"
        else:
            return self._source[self._current + 1]

    def _two_char_token(self, expected: str, success_type: TokenType,
                        failure_type: TokenType) -> None:
        if self._match(expected):
            self._add_token(success_type)
        else:
            self._add_token(failure_type)

    def _advance(self) -> str:
        out = self._source[self._current]
        self._current += 1
        return out

    def _add_token(self, type: TokenType, literal: Any = None) -> None:
        lexeme = self._source[self._start:self._current]
        self._tokens.append(Token(type, lexeme, literal, self._line))

    def _match(self, expected: str) -> bool:
        if self._at_end():
            return False
        if self._source[self._current] != expected:
            return False
        self._current += 1
        return True

    def __init__(self, source: str) -> None:
        self._source = source
        self._tokens = []
        self._start = 0
        self._current = 0
        self._line = 1

    def scan_tokens(self) -> Tuple[Token, ...]:
        while not self._at_end():
            self._start = self._current
            self._scan_token()
        self._tokens.append(Token(TokenType.EOF, "", None, self._line))
        return tuple(self._tokens)
