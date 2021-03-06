from src.consts import *

class Lexer:
    def __init__(self):
        self._state = 'S'
        self._buffer = ''
        self._index = 0
        self._current_char = ''
        self._brackets_count = 0
        self._is_function = False
        self._result = []

        self._machine = {
            'S': self._state_s,
            'I': self._state_i,
            'R': self._state_r,
            'B': self._state_b,
            'F': self._state_f,
            'X': self._state_x
        }
        self._expectations = {
            'S': 'number, letter, unary minus or opening bracket',
            'I': 'number, operator, comma or closing bracket',
            'R': 'number, operator or closing bracket',
            'B': 'operator or closing bracket',
            'F': 'letter or opening bracket',
            'X': 'closing bracket or operator',
            'B_ERR': 'right brackets count'
        }

        assert all(item in self._expectations for item in self._machine.keys())

    def _flush_buffer(self):
        if self._buffer:
            self._result.append(self._buffer)
            self._buffer = ''

        else:
            pass

    def _append_current_char(self):
        self._buffer += self._current_char

    def _flush_current_char(self):
        self._result.append(self._current_char)

    def _reset(self):
        self._state = 'S'
        self._buffer = ''
        self._index = 0
        self._current_char = ''
        self._brackets_count = 0
        self._is_function = False
        self._result = []

    def _state_s(self):
        if self._current_char.isdigit():
            self._append_current_char()
            return 'I'

        if self._current_char == BRACKET_OPEN:
            self._brackets_count += 1
            self._flush_current_char()
            return 'S'
        if self._current_char == MINUS:
            self._append_current_char()
            return 'S'

        if self._current_char in ALPHABET and self._current_char != VAR:
            self._append_current_char()
            return 'F'

        if self._current_char == VAR:
            self._append_current_char()
            self._flush_buffer()
            return 'X'

    def _state_i_r_shared(self):
        if self._current_char.isdigit():
            self._append_current_char()
            return 'I'

        if self._current_char == BRACKET_CLOSE:
            self._brackets_count -= 1
            self._flush_buffer()
            self._flush_current_char()
            return 'B'

        if self._current_char in OPERATORS:
            self._flush_buffer()
            self._flush_current_char()
            return 'S'

    def _state_i(self):
        if self._current_char == COMM:
            self._append_current_char()
            return 'R'

        return self._state_i_r_shared()

    def _state_r(self):
        return self._state_i_r_shared()

    def _state_b(self):
        if self._current_char == BRACKET_CLOSE:
            self._brackets_count -= 1
            self._flush_current_char()
            return 'B'

        if self._current_char in OPERATORS:
            self._flush_buffer()
            self._flush_current_char()
            return 'S'

    def _state_f(self):
        if self._current_char in ALPHABET:
            self._append_current_char()
            return 'F'

        if self._current_char == BRACKET_OPEN:
            self._brackets_count += 1
            self._flush_buffer()
            self._flush_current_char()
            return 'S'

    def _state_x(self):
        self._is_function = True

        if self._current_char == BRACKET_CLOSE:
            self._brackets_count -= 1
            self._flush_current_char()
            return 'B'

        if self._current_char in OPERATORS:
            self._flush_buffer()
            self._flush_current_char()
            return 'S'

    def _raise_exception(self):
        expected = self._expectations[self._state]
        index = self._index

        self._reset()

        return

    def parse(self, s: str):
        if not s:
            exit('Nothing...')

        for i, ch in enumerate(s):
            if ch == ' ':
                continue

            self._index = i
            self._current_char = ch

            state = self._machine[self._state]()
            if state is None:
                self._raise_exception()

            self._state = state

        self._flush_buffer()

        if self._brackets_count != 0:
            # todo: wtf
            self._state = 'B_ERR'
            self._current_char = self._brackets_count

            self._raise_exception()

        if self._result[-1] in OPERATORS:
            self._state = 'S'

            self._raise_exception()

        res = self._result
        is_function = self._is_function
        self._reset()

        return res, is_function
