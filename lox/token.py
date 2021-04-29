from dataclasses import dataclass
from typing import Any
from lox.token_type import TokenType


@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str
    literal: Any
    line: int

    def __str__(self):
        out = f"{self.type} {self.lexeme}"
        if self.literal is not None:
            out += f" {str(self.literal).replace('.0', '')}"
        return out
