from lox.token_type import TokenType
from lox.token import Token
from lox.ast import BinaryExpression, Expression, GroupingExpression, LiteralExpression, UnaryExpression


class AstPrinter(Expression.Visitor):

    def _parenthesize(self, name, *exprs):
        builder = f"({name}"
        for expr in exprs:
            builder += f" {self.visit(expr)}"
        return builder + ")"

    def visit_BinaryExpression(self, expr):
        return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_GroupingExpression(self, expr):
        return self._parenthesize("group", expr.expression)

    def visit_LiteralExpression(self, expr):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_UnaryExpression(self, expr):
        return self._parenthesize(expr.operator.lexeme, expr.right)


if __name__ == "__main__":
    expression = BinaryExpression(
        UnaryExpression(
            Token(TokenType.MINUS, "-", None, 1),
            LiteralExpression(123),
        ), Token(TokenType.STAR, "*", None, 1),
        GroupingExpression(LiteralExpression(45.67)))

    print(AstPrinter().visit(expression))
