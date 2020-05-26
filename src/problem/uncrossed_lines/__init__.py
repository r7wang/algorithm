"""
We write the integers of A and B (in the order they are given) on two separate horizontal lines.

Now, we may draw connecting lines: a straight line connecting two numbers A[i] and B[j] such that:

    A[i] == B[j];
    The line we draw does not intersect any other connecting (non-horizontal) line.

Note that a connecting lines cannot intersect even at the endpoints: each number can only belong to one connecting line.

Return the maximum number of connecting lines we can draw in this way.
"""
from typing import List


def uncrossed_lines(a: List[int], b: List[int]) -> int:
    width = len(a)
    height = len(b)

    # Build a matrix where matrix[x][y] represents the best possible solution for the subproblem a[0:x+1], b[0:y+1].
    # For example:
    #   a = [0, 2, 7, 6]
    #   b = [3, 2, 4, 9]
    #       matrix[0][0] is the best possible solution for a = [0], b = [3]
    #       matrix[2][0] is the best possible solution for a = [0, 2, 7], b = [3]
    matrix = []
    for _ in range(width):
        matrix.append([0] * height)

    for x in range(width):
        for y in range(height):
            _fill(matrix, x, y, a, b)

    return matrix[width-1][height-1]


def _fill(matrix: List[List[int]], x: int, y: int, a: List[int], b: List[int]):
    left_val = _get_value_at(matrix, x - 1, y)
    top_val = _get_value_at(matrix, x, y - 1)
    if a[x] == b[y]:
        # Case 1: Values are the same.
        # The current solution can be up to one better than what we've found so far, but most not reuse the same value,
        # more than once. On the last x, if the value from y and y - 1 were the same, then all we are doing is copying
        # the best solution so far (not using the current value). Otherwise, we are using the current value to generate
        # a better solution and can no longer use it (increment = 0).
        top_left_val = _get_value_at(matrix, x - 1, y - 1)
        increment = 1 if top_left_val == left_val else 0
        matrix[x][y] = max(left_val+increment, top_val)
    else:
        # Case 2: Values are different.
        # The current solution can't be worse than the best solution we've found so far.
        matrix[x][y] = max(left_val, top_val)


def _get_value_at(matrix: List[List[int]], x: int, y: int) -> int:
    if x < 0 or y < 0:
        return 0
    return matrix[x][y]
