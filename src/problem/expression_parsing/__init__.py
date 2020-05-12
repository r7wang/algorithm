"""
Implement an expression parser that will solve an expression continue numbers and the following symbols:
    - '('
    - ')'
    - '+'
    - '-'
    - '*'
    - '/'
"""
from typing import Callable, Dict, Optional


class ExpressionFormatException(ValueError):
    """
    Indicates that the expression is incorrectly formatted.
    """
    pass


class ExpressionSolver:
    def __init__(self):
        self.operations: Dict[str, Callable[[int, int], int]] = {
            '+': self._add,
            '-': self._sub,
            '*': self._mult,
            '/': self._div,
        }

    def solve(self, expr: str) -> int:
        self._validate_expression(expr)

        # We want to scan through the text to see if there is an operator of lowest precedence that is not in
        # parentheses. If so, then we build the expression tree using that operator as a base.
        operator_idx = self._get_lowest_precedence_operator(expr)

        # If there is no operator, then just return the value.
        if operator_idx is None:
            # If this expression is redundantly enclosed in parentheses, remove the parentheses.
            if self._is_lparen(expr[0]) and self._is_rparen(expr[-1]):
                return self.solve(expr[1:-1])

            return int(expr)

        left_expr = expr[:operator_idx]
        right_expr = expr[operator_idx+1:]
        operator = expr[operator_idx]
        operation_func = self.operations[operator]
        return operation_func(self.solve(left_expr), self.solve(right_expr))

    def _validate_expression(self, expr: str) -> None:
        # Validate that the expression has length > 0.
        if len(expr) == 0:
            raise ExpressionFormatException()

        # Validate that the expression has correct parenthesis matching.
        paren_depth = 0
        for char in expr:
            if self._is_lparen(char):
                paren_depth += 1
            if self._is_rparen(char):
                paren_depth -= 1
        if paren_depth != 0:
            raise ExpressionFormatException()

    def _get_lowest_precedence_operator(self, expr: str) -> Optional[int]:
        operator = None
        operator_idx = None
        paren_depth = 0
        for i in range(len(expr)):
            char = expr[i]
            if self._is_lparen(char):
                paren_depth += 1
            elif self._is_rparen(char):
                paren_depth -= 1
            else:
                if paren_depth > 0:
                    continue

                if not self._is_operator(char):
                    continue

                if operator is None or self._lower_precedence(char, operator):
                    operator = char
                    operator_idx = i
        return operator_idx

    def _is_lparen(self, char: str) -> bool:
        return char == '('

    def _is_rparen(self, char: str) -> bool:
        return char == ')'

    def _is_operator(self, char: str) -> bool:
        return char == '+' or char == '-' or char == '*' or char == '/'

    def _lower_precedence(self, left: str, right: str):
        if left == '+' or left == '-':
            return right == '*' or right == '/'
        return False

    def _add(self, left: int, right: int) -> int:
        return left + right

    def _sub(self, left: int, right: int) -> int:
        return left - right

    def _mult(self, left: int, right: int) -> int:
        return left * right

    def _div(self, left: int, right: int) -> int:
        return int(left / right)
