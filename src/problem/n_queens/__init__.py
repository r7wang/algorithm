"""
Return all of the different ways to place n queens on a chessboard of size n*n where none of the queens can attack each
other.
"""
from typing import List


class Placement:
    # What is an empty solution? Just a list. Every time we place a queen, we add a coordinate to that list.
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


Solution = List[Placement]


def place_queens(n: int, current_solution: Solution) -> List[Solution]:
    if len(current_solution) == n:
        return [list(current_solution)]

    solutions = []
    x = len(current_solution)
    for y in range(n):
        if _can_place_queen(current_solution, x, y):
            current_solution.append(Placement(x, y))
            solutions.extend(place_queens(n, current_solution))
            current_solution.pop()

    return solutions


def _can_place_queen(current_solution: Solution, x: int, y: int) -> bool:
    # This is an O(n) operation.
    for placement in current_solution:
        # We don't need to check the x because we're putting the queen in a new column.
        # if placement.x == x:
        #     return False
        if placement.y == y:
            return False
        diff_y = abs(y - placement.y)
        diff_x = abs(x - placement.x)
        if diff_y == diff_x:
            return False
    return True
