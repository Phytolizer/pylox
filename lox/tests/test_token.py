import pytest

from lox.token_type import TokenType
from lox.token import Token


@pytest.mark.parametrize("type", TokenType)
def test_string(type: TokenType):
    tok = Token(type, "blah", 3, 123)
    assert str(tok) == f"{type} blah 3"
