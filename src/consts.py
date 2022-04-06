import math
import string
from enum import Enum

PLUS = '+'
MINUS = '-'
MULTIPLY = '*'
DIVIDE = '/'
DEGREE = '^'

COMM = '.'
VAR = 'x'

BRACKET_OPEN = '('
BRACKET_CLOSE = ')'

OPERATORS = [PLUS, MINUS, MULTIPLY, DIVIDE, DEGREE]
BRACKETS = [BRACKET_OPEN, BRACKET_CLOSE]
ALPHABET = string.ascii_letters

FUNCTIONS = {
    'sin': math.sin,
    'cos': math.cos,
    'log': math.log,
    'exp': math.exp,
    'tg' : math.tan,
    'ctg': lambda x: 1 / math.tan(x)
}

class Token:
    INTEGER = 1
    VARIABLE = 2
    OPERATOR = 3
    FUNCTION = 4
    BRACKET_OPEN = 5
    BRACKET_CLOSE = 6