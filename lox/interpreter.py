from typing import cast

import lox
from lox.ast import BinaryExpression, Expression, GroupingExpression, LiteralExpression, UnaryExpression
from lox.runtime_error import LoxRuntimeError
from lox.token import Token
from lox.token_type import TokenType
from lox.object import LoxObject


def is_truthy(value: object) -> bool:
    return value is not None and value != False


class Interpreter(Expression.Visitor):

    def interpret(self, expr: Expression) -> None:
        try:
            value = self._evaluate(expr)
            print(str(value))
        except LoxRuntimeError as e:
            lox.runtime_error(e)

    def visit_LiteralExpression(self, expr: LiteralExpression) -> LoxObject:
        return LoxObject(expr.value)

    def visit_GroupingExpression(self, expr: GroupingExpression) -> LoxObject:
        return self._evaluate(expr.expression)

    def visit_UnaryExpression(self, expr: UnaryExpression) -> LoxObject:
        right = self._evaluate(expr.right).value

        if expr.operator.type == TokenType.BANG:
            return LoxObject(not is_truthy(right))
        elif expr.operator.type == TokenType.MINUS:
            self._check_number_operand(expr.operator, right)
            right = cast(float, right)
            return LoxObject(-right)

        raise RuntimeError("this was supposed to be unreachable")

    def visit_BinaryExpression(self, expr: BinaryExpression) -> LoxObject:
        left = self._evaluate(expr.left).value
        right = self._evaluate(expr.right).value

        if expr.operator.type == TokenType.GREATER:
            self._check_number_operands(expr.operator, left, right)
            left = cast(float, left)
            right = cast(float, right)
            return LoxObject(left > right)
        elif expr.operator.type == TokenType.GREATER_EQUAL:
            self._check_number_operands(expr.operator, left, right)
            left = cast(float, left)
            right = cast(float, right)
            return LoxObject(left >= right)
        if expr.operator.type == TokenType.LESS:
            self._check_number_operands(expr.operator, left, right)
            left = cast(float, left)
            right = cast(float, right)
            return LoxObject(left < right)
        elif expr.operator.type == TokenType.LESS_EQUAL:
            self._check_number_operands(expr.operator, left, right)
            left = cast(float, left)
            right = cast(float, right)
            return LoxObject(left <= right)
        elif expr.operator.type == TokenType.MINUS:
            self._check_number_operands(expr.operator, left, right)
            left = cast(float, left)
            right = cast(float, right)
            return LoxObject(left - right)
        elif expr.operator.type == TokenType.SLASH:
            self._check_number_operands(expr.operator, left, right)
            left = cast(float, left)
            right = cast(float, right)
            return LoxObject(left / right)
        elif expr.operator.type == TokenType.STAR:
            self._check_number_operands(expr.operator, left, right)
            left = cast(float, left)
            right = cast(float, right)
            return LoxObject(left * right)
        elif expr.operator.type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return LoxObject(left + right)
            elif isinstance(left, str) and isinstance(right, str):
                return LoxObject(left + right)
            else:
                raise LoxRuntimeError(
                    expr.operator,
                    "Operands must be two numbers or two strings.")
        elif expr.operator.type == TokenType.EQUAL_EQUAL:
            return LoxObject(left == right)
        elif expr.operator.type == TokenType.BANG_EQUAL:
            return LoxObject(left != right)

        raise RuntimeError("this was supposed to be unreachable")

    def _evaluate(self, expr: Expression) -> LoxObject:
        return self.visit(expr)

    def _check_number_operand(self, operator: Token, operand: object):
        if isinstance(operand, float):
            return
        raise LoxRuntimeError(operator, "Operand must be a number.")

    def _check_number_operands(self, operator: Token, left: object,
                               right: object):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise LoxRuntimeError(operator, "Operands must be numbers.")
