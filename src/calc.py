from src.consts import *
from typing import *


class Evaluator:
    def __init__(self):
        self._operations = {
            PLUS: lambda left, right: left + right,
            MINUS: lambda left, right: left - right,
            MULTIPLY: lambda left, right: left * right,
            DIVIDE: lambda left, right: left / right,
            DEGREE: lambda left, right: left ** right
        }


    def eval(self, converter_result, x: float = 0):
        assert converter_result

        try:
            return self._eval(converter_result, x)
        except ZeroDivisionError:
            return None
        except ValueError:
            pass

    def _eval(self, expression: List[Tuple[Union[str, int], Token]], x: float):
        stack = []

        for item in expression:
            if item[1] == Token.INTEGER:
                stack.append(item)

            elif item[1] == Token.VARIABLE:
                stack.append((self._eval_x(item, x), Token.INTEGER))

            elif item[1] == Token.OPERATOR:

                right = stack.pop()[0]
                left = stack.pop()[0]

                stack.append((self._eval_operator(item, left, right), Token.INTEGER))

            elif item[1] == Token.FUNCTION:
                value = stack.pop()[0]

                stack.append((self._eval_function(item, value), Token.INTEGER))
            else:
                pass

        res = stack.pop()

        return res[0]

    def _eval_x(self, item: Tuple[Union[str, int], Token], x: float):
        assert item[1] == Token.VARIABLE

        if item[0].startswith('-'):
            return -x

        return x

    def _eval_operator(self, item: Tuple[Union[str, int], Token], left: str, right: str):
        assert item[1] == Token.OPERATOR

        func = self._operations.get(item[0])
        if not func:
            exit(f'Unknown operation {item}')

        return func(float(left), float(right))

    def _eval_function(self, item: Tuple[str, Token], value: str):
        assert item[1] == Token.FUNCTION

        name = item[0]
        pos = True

        if name.startswith(MINUS):
            name = item[0][1:]
            pos = False

        if name not in FUNCTIONS:
            exit(f'Unknown function {name}')

        func = FUNCTIONS.get(name)


        res = func(float(value))

        return res if pos else -res