from lox.token_type import TokenType


def text_for_type(type: TokenType) -> str:
    return {
        TokenType.LEFT_PAREN: "(",
        TokenType.RIGHT_PAREN: ")",
        TokenType.LEFT_BRACE: "{",
        TokenType.RIGHT_BRACE: "}",
        TokenType.COMMA: ",",
        TokenType.DOT: ".",
        TokenType.MINUS: "-",
        TokenType.PLUS: "+",
        TokenType.SEMICOLON: ";",
        TokenType.SLASH: "/",
        TokenType.STAR: "*",
        TokenType.BANG: "!",
        TokenType.BANG_EQUAL: "!=",
        TokenType.EQUAL: "=",
        TokenType.EQUAL_EQUAL: "==",
        TokenType.GREATER: ">",
        TokenType.GREATER_EQUAL: ">=",
        TokenType.LESS: "<",
        TokenType.LESS_EQUAL: "<=",
        TokenType.IDENTIFIER: None,
        TokenType.STRING: None,
        TokenType.NUMBER: None,
        TokenType.AND: "and",
        TokenType.CLASS: "class",
        TokenType.ELSE: "else",
        TokenType.FALSE: "false",
        TokenType.FOR: "for",
        TokenType.FUN: "fun",
        TokenType.IF: "if",
        TokenType.NIL: "nil",
        TokenType.OR: "or",
        TokenType.PRINT: "print",
        TokenType.RETURN: "return",
        TokenType.SUPER: "super",
        TokenType.THIS: "this",
        TokenType.TRUE: "true",
        TokenType.VAR: "var",
        TokenType.WHILE: "while",
    }[type]


def is_keyword(type: TokenType) -> bool:
    return type in (
        TokenType.AND,
        TokenType.CLASS,
        TokenType.ELSE,
        TokenType.FALSE,
        TokenType.FOR,
        TokenType.FUN,
        TokenType.IF,
        TokenType.NIL,
        TokenType.OR,
        TokenType.PRINT,
        TokenType.RETURN,
        TokenType.SUPER,
        TokenType.THIS,
        TokenType.TRUE,
        TokenType.VAR,
        TokenType.WHILE,
    )


def requires_separator(left: TokenType, right: TokenType) -> bool:
    return (is_keyword(left) and is_keyword(right) or
            left == TokenType.IDENTIFIER and is_keyword(right) or
            is_keyword(left) and right == TokenType.IDENTIFIER or
            left == TokenType.BANG and
            right in (TokenType.EQUAL, TokenType.EQUAL_EQUAL) or
            left == TokenType.EQUAL and
            right in (TokenType.EQUAL, TokenType.EQUAL_EQUAL) or
            left == TokenType.LESS and
            right in (TokenType.EQUAL, TokenType.EQUAL_EQUAL) or
            left == TokenType.GREATER and
            right in (TokenType.EQUAL, TokenType.EQUAL_EQUAL) or
            left == TokenType.SLASH and right == TokenType.SLASH)
