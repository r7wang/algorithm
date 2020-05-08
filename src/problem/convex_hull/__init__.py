"""
See the link below for details.

https://en.wikipedia.org/wiki/Convex_hull

Building up an artificial problem can be difficult, so we'll try to draw the diagram first. Empty spaces are
represented by periods (.) and points are represented by O.

9    .     .     .     .     O     .     .     .     O     .

8    .     O     .     O     O     .     .     .     .     .

7    .     O     O     .     .     .     .     .     .     .

6    .     .     .     .     O     .     O     .     .     .

5    .     O     O     .     .     .     .     .     .     .

4    O     O     .     .     O     O     .     O     .     O

3    .     .     O     .     .     .     .     .     .     .

2    .     .     .     O     .     .     O     O     .     .

1    .     O     .     .     .     .     O     .     .     .

0    .     .     O     .     .     O     .     .     .     .

     0     1     2     3     4     5     6     7     8     9

"""
from enum import IntEnum
from typing import List, Set, Tuple


class Point:
    def __init__(self, coordinate: Tuple[int, int]):
        self.x = coordinate[0]
        self.y = coordinate[1]


class Quadrant(IntEnum):
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_LEFT = 2
    BOTTOM_RIGHT = 3


sample_points = list(map(lambda coordinate: Point(coordinate), [
    (4, 9), (8, 9),
    (1, 8), (3, 8), (4, 8),
    (1, 7), (2, 7),
    (4, 6), (6, 6),
    (1, 5), (2, 5),
    (0, 4), (1, 4), (4, 4), (5, 4), (7, 4), (9, 4),
    (2, 3),
    (3, 2), (6, 2), (7, 2),
    (1, 1), (6, 1),
    (2, 0), (5, 0),
]))


def convex_hull(points: List[Point]) -> Set[Point]:
    """
    Return the set of points that form the border of the convex hull problem.
    """
    if not points:
        return set()

    # Find the min/max x and the min/max y as an O(n) operation.
    min_x = points[0].x
    max_x = points[0].x
    min_y = points[0].y
    max_y = points[0].y

    for point in points:
        min_x = min(min_x, point.x)
        max_x = max(max_x, point.x)
        min_y = min(min_y, point.y)
        max_y = max(max_y, point.y)

    # Add all points that satisfy min/max properties to different arrays as an O(n) operation. Note that points may
    # exist in more than one array.
    min_x_points = []
    max_x_points = []
    min_y_points = []
    max_y_points = []

    for point in points:
        if point.x == min_x:
            min_x_points.append(point)
        if point.x == max_x:
            max_x_points.append(point)
        if point.y == min_y:
            min_y_points.append(point)
        if point.y == max_y:
            max_y_points.append(point)

    # Sort the points as an O(n_log_n) operation because we need to know which points to initially connect.
    min_x_points = sorted(min_x_points, key=lambda item: item.y)
    max_x_points = sorted(max_x_points, key=lambda item: item.y)
    min_y_points = sorted(min_y_points, key=lambda item: item.x)
    max_y_points = sorted(max_y_points, key=lambda item: item.x)

    solution = set()
    solution.update(
        min_x_points,
        max_x_points,
        min_y_points,
        max_y_points,
        _solve_quadrant(points, min_x_points[-1], max_y_points[0], Quadrant.TOP_LEFT),
        _solve_quadrant(points, max_y_points[-1], max_x_points[-1], Quadrant.TOP_RIGHT),
        _solve_quadrant(points, min_x_points[0], min_y_points[0], Quadrant.BOTTOM_LEFT),
        _solve_quadrant(points, min_y_points[-1], max_x_points[0], Quadrant.BOTTOM_RIGHT),
    )
    return solution


def _solve_quadrant(points: List[Point], point_a: Point, point_b: Point, quadrant: Quadrant) -> List[Point]:
    """
    point_a and point_b must be two points that we can initially assume will be connected. We can then build on that
    solution. They may actually be the same point, in which case there's no work to do.

    Returns any points that form the quadrant.
    """
    if point_a == point_b:
        return [point_a]

    # Calculate our baseline slope.
    slope = (point_b.y - point_a.y) / (point_b.x - point_a.x)
    base_y_intercept = point_a.y - (slope * point_a.x)

    # Determine which points we need to look at.
    if quadrant == Quadrant.TOP_LEFT:
        to_check = filter(lambda item: item.x < point_b.x and item.y > point_a.y, points)
    elif quadrant == Quadrant.TOP_RIGHT:
        to_check = filter(lambda item: item.x > point_a.x and item.y > point_b.y, points)
    elif quadrant == Quadrant.BOTTOM_LEFT:
        to_check = filter(lambda item: item.x < point_b.x and item.y < point_a.y, points)
    else:
        to_check = filter(lambda item: item.x > point_a.x and item.y < point_b.y, points)

    # Check all points and update the baseline slope as necessary.
    to_add = []
    for point in to_check:
        if point is point_a or point is point_b:
            continue

        base_y = (slope * point.x) + base_y_intercept
        if quadrant == Quadrant.TOP_LEFT or quadrant == Quadrant.TOP_RIGHT:
            if point.y > base_y:
                to_add.clear()
                base_y_intercept = point.y - (slope * point.x)
            if point.y >= base_y:
                to_add.append(point)
        else:
            if point.y < base_y:
                to_add.clear()
                base_y_intercept = point.y - (slope * point.x)
            if point.y <= base_y:
                to_add.append(point)

    to_add = sorted(to_add, key=lambda item: item.x)
    if to_add:
        left_solution = _solve_quadrant(points, point_a, to_add[0], quadrant)
        right_solution = _solve_quadrant(points, to_add[-1], point_b, quadrant)
        to_add.extend(left_solution)
        to_add.extend(right_solution)

    return [point_a, point_b, *to_add]


