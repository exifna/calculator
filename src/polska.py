from src.consts import *
from typing import *

def parse_width(s: str) -> int:
    try:
        temp = float(s)
        return Token.INTEGER

    except:
        if s.lower() == 'x':
            return Token.VARIABLE

        if s in OPERATORS:
            return Token.OPERATOR

        if s in FUNCTIONS:
            return Token.FUNCTION

        if s == BRACKET_OPEN:
            return Token.BRACKET_OPEN

        if s == BRACKET_CLOSE:
            return Token.BRACKET_CLOSE


class Converter:
    def __init__(self):
        self._priority = {
            BRACKET_OPEN: 1,
            PLUS: 2,
            MINUS: 2,
            MULTIPLY: 3,
            DIVIDE: 3,
            DEGREE: 4,
            BRACKET_CLOSE: 5
        }

    def _get_priority(self, item: Tuple[str, Token]):
        if item[1] == Token.FUNCTION:
            return 4

        return self._priority.get(item[0]) or 0

    def convert(self, tokenizer_result: List[str]):

        stack = []
        result = []

        for item in tokenizer_result:
            item = [item, parse_width(item)]

            if item[1] in (Token.INTEGER, Token.VARIABLE):
                result.append(item)

            elif item[1] == Token.FUNCTION:
                stack.append(item)

            elif item[1] == Token.OPERATOR:
                priority = self._get_priority(item)

                if stack and self._get_priority(stack[-1]) >= priority:
                    while stack and self._get_priority(stack[-1]) >= priority:
                        result.append(stack.pop())

                stack.append(item)

            elif item[1] == Token.BRACKET_OPEN:
                stack.append(item)

            elif item[1] == Token.BRACKET_CLOSE:
                while stack[-1][1] != Token.BRACKET_OPEN:
                    result.append(stack.pop())

                stack.pop()  # remove open bracket
            else:
                pass

        if stack:
            while stack:
                result.append(stack.pop())

        return result