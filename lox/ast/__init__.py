from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
import visitor

from lox.token import Token


class Expression(ABC):

    class Visitor(ABC, visitor.Visitor):

        @abstractmethod
        def visit_BinaryExpression(self, expr):
            pass

        @abstractmethod
        def visit_GroupingExpression(self, expr):
            pass

        @abstractmethod
        def visit_LiteralExpression(self, expr):
            pass

        @abstractmethod
        def visit_UnaryExpression(self, expr):
            pass


@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: Token
    right: Expression


@dataclass
class GroupingExpression(Expression):
    expression: Expression


@dataclass
class LiteralExpression(Expression):
    value: Any


@dataclass
class UnaryExpression(Expression):
    operator: Token
    right: Expression