"""
See the link below for details.

https://en.wikipedia.org/wiki/Convex_hull

Building up an artificial problem can be difficult, so we'll try to draw the diagram first. Empty spaces are
represented by periods (.) and points are represented by O.

9    .     .     .     .     O     .     .     .     O     .

8    .     O     .     O     O     .     .     .     .     .

7    .     O     O     .     .     .     .     .     .     .

6    .     .     .     .     O     .     O     .     .     O

5    .     O     O     .     .     .     .     .     .     .

4    O     O     .     .     O     O     .     O     .     .

3    .     .     O     .     .     .     .     .     .     .

2    .     .     .     O     .     .     O     .     .     .

1    .     O     .     .     .     .     .     .     .     .

0    .     .     O     .     .     O     .     .     .     .

     0     1     2     3     4     5     6     7     8     9

"""
from typing import Tuple, List


class Point:
    def __init__(self, coordinate: Tuple[int, int]):
        self.x = coordinate[0]
        self.y = coordinate[1]


sample_points = map(lambda coordinate: Point(coordinate), [
    (4, 9), (8, 9),
    (1, 8), (3, 8), (4, 8),
    (1, 7), (2, 7),
    (4, 6), (6, 6), (9, 6),
    (1, 5), (2, 5),
    (0, 4), (1, 4), (4, 4), (5, 4), (7, 4),
    (2, 3),
    (3, 2), (6, 2),
    (1, 1),
    (2, 0), (5, 0),
])


def convex_hull(points: List[Point]) -> List[Point]:
    pass
