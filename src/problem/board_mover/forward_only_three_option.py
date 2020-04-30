"""
A piece starts at S, can only move to positions marked X1, before moving again with the same pattern.

    (X) 0   1   2   3
(Y)     .   .   .   .
 3      .   .   .   .
 2      .   .   .   .
 1      .   S1  .   .
 0      S   S1  .   .
-1      .   S1  .   .
-2      .   .   .   .
-3      .   .   .   .
-4      .   .   .   .

How many unique ways can a piece move from S (0, 0) to (n, 0)?
"""
from collections import defaultdict
from typing import Dict


def solve(n: int) -> int:
    """
     - Can approach this problem recursively, but it may require too deep of a stack for high n.
     - Can approach this problem in layers, calculating all necessary values for X=1, then X=2, etc.
    """
    # Map of y to number of ways to visit coordinate (layer, y) from (0, 0)
    ways_to_visit = defaultdict(lambda: defaultdict(int))
    ways_to_visit[0][0] = 1
    calculations = 0
    for layer in range(1, n + 1):
        calculations += _solve_layer(n, layer, ways_to_visit)
        del ways_to_visit[0]
    print('calculations: {}'.format(calculations))
    return ways_to_visit[n][0]


def _solve_layer(n: int, layer: int, ways_to_visit: Dict[int, Dict[int, int]]) -> int:
    # Optimization 1: Only calculate the positive y.
    # Optimization 2: Don't calculate y that are too far out to generate any solutions.
    max_y = min(layer, n - layer)
    for y in range(max_y + 1):
        # Need to flip the index on negative y queries because we only store positive results (should be identical)
        ways_to_visit[layer][y] = (
            ways_to_visit[layer-1][abs(y+1)] +
            ways_to_visit[layer-1][abs(y)] +
            ways_to_visit[layer-1][abs(y-1)]
        )
        print('ways_{}_{}: {}'.format(layer, y, ways_to_visit[layer][y]))
    return max_y
