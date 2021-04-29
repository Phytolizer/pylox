from typing import Tuple

import lox
from lox.token import Token
from lox.token_type import TokenType
from lox.ast import (
    BinaryExpression,
    Expression,
    GroupingExpression,
    LiteralExpression,
    UnaryExpression,
)


class Parser:
    _tokens: Tuple[Token, ...]
    _current: int

    class ParseError(Exception):
        pass

    def __init__(self, tokens: Tuple[Token, ...]):
        self._tokens = tokens
        self._current = 0

    def parse(self):
        try:
            return self._expression()
        except Parser.ParseError:
            return None

    def _expression(self) -> Expression:
        return self._equality()

    def _equality(self) -> Expression:
        expr = self._comparison()
        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self._previous()
            right = self._comparison()
            expr = BinaryExpression(expr, operator, right)

        return expr

    def _comparison(self) -> Expression:
        expr = self._term()
        while self._match(
                TokenType.GREATER,
                TokenType.GREATER_EQUAL,
                TokenType.LESS,
                TokenType.LESS_EQUAL,
        ):
            operator = self._previous()
            right = self._term()
            expr = BinaryExpression(expr, operator, right)

        return expr

    def _term(self) -> Expression:
        expr = self._factor()
        while self._match(TokenType.MINUS, TokenType.PLUS):
            operator = self._previous()
            right = self._factor()
            expr = BinaryExpression(expr, operator, right)

        return expr

    def _factor(self) -> Expression:
        expr = self._unary()
        while self._match(TokenType.SLASH, TokenType.STAR):
            operator = self._previous()
            right = self._unary()
            expr = BinaryExpression(expr, operator, right)

        return expr

    def _unary(self) -> Expression:
        if self._match(TokenType.BANG, TokenType.MINUS):
            operator = self._previous()
            right = self._unary()
            return UnaryExpression(operator, right)

        return self._primary()

    def _primary(self) -> Expression:
        if self._match(TokenType.FALSE):
            return LiteralExpression(False)
        if self._match(TokenType.TRUE):
            return LiteralExpression(True)
        if self._match(TokenType.NIL):
            return LiteralExpression(None)
        if self._match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpression(self._previous().literal)
        if self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return GroupingExpression(expr)
        raise self._error(self._peek(), "Expect expression.")

    def _match(self, *types) -> bool:
        for type in types:
            if self._check(type):
                self._advance()
                return True

        return False

    def _consume(self, type: TokenType, message: str) -> Token:
        if self._check(type):
            return self._advance()

        raise self._error(self._peek(), message)

    def _error(self, token: Token, message: str) -> ParseError:
        lox.error(token, message)
        return Parser.ParseError()

    def _check(self, type: TokenType) -> bool:
        if self._at_end():
            return False
        return self._peek().type == type

    def _advance(self) -> Token:
        if not self._at_end():
            self._current += 1
        return self._previous()

    def _at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _peek(self) -> Token:
        return self._tokens[self._current]

    def _previous(self) -> Token:
        return self._tokens[self._current - 1]

    def _synchronize(self) -> None:
        self._advance()

        while not self._at_end():
            if self._previous().type == TokenType.SEMICOLON:
                return

            if self._peek() in (
                    TokenType.CLASS,
                    TokenType.FUN,
                    TokenType.VAR,
                    TokenType.FOR,
                    TokenType.IF,
                    TokenType.WHILE,
                    TokenType.PRINT,
                    TokenType.RETURN,
            ):
                return

            self._advance()
