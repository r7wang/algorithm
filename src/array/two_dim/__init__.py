"""
The way you build a 2D array should really depend on how you intend to query it.
    - Are you going to index it like arr[x][y] or like arr[y][x]?
    - Is the shape of the 2D array rectangular or not uniform?
"""
import itertools
from typing import List, Any, Iterator


def seed_2d_array_xy(width: int, height: int) -> List:
    arr_x = []
    for _ in range(0, width):
        arr_x.append([-1] * height)
    return arr_x


def seed_2d_array_yx(width: int, height: int) -> List:
    arr = []
    for _ in range(0, height):
        # List generation is a pretty neat trick.
        arr.append([-1] * width)
    return arr


def copy_2d_array(arr: List) -> List:
    return [list(sub_arr) for sub_arr in arr]


def mult_2d_array(arr: List, factor: int) -> List:
    """Multiplies all elements in a 2d array by a given factor (not in-place)
    No restriction on array dimensions.
    """
    return [map(lambda item: item * factor, sub_arr) for sub_arr in arr]


def mult_2d_array_in_place(arr: List, factor: int) -> None:
    """Multiplies all elements in a 2d array by a given factor (in-place)
    No restriction on array dimensions.
    """
    len_1 = len(arr)
    for idx_1 in range(0, len_1):
        len_2 = len(arr[idx_1])
        for idx_2 in range(0, len_2):
            arr[idx_1][idx_2] *= factor


def make_2d_array_yx_seeded_row_order_using_iter(items: List, width: int, height: int) -> List:
    """
    Properties:
        - initially seeded with None
        - applies items in row order, left to right
        - uses an iterator to apply as many items as possible
    """

    arr = seed_2d_array_yx(width, height)
    items_iter = iter(items)
    try:
        for y in range(0, height):
            for x in range(0, width):
                arr[y][x] = next(items_iter)
    except StopIteration:
        pass
    return arr


def make_2d_array_yx_seeded_col_order_using_iter(items: List, width: int, height: int) -> List:
    """
    Properties:
        - initially seeded with None
        - applies items in column order, top to bottom
        - uses an iterator to apply as many items as possible
    """

    arr = seed_2d_array_yx(width, height)
    items_iter = iter(items)
    try:
        for x in range(0, width):
            for y in range(0, height):
                arr[y][x] = next(items_iter)
    except StopIteration:
        pass
    return arr


def make_2d_array_yx_seeded_col_order_alternating_using_iter(items: List, width: int, height: int) -> List:
    """
    Properties:
        - initially seeded with None
        - applies items in column order, alternating top to bottom and bottom to top
        - uses an iterator to apply as many items as possible
    """

    arr = seed_2d_array_yx(width, height)
    items_iter = iter(items)
    try:
        for x in range(0, width):
            for y in range(0, height):
                if x % 2 == 0:
                    arr[y][x] = next(items_iter)
                else:
                    arr[width - y - 1][x] = next(items_iter)
    except StopIteration:
        pass
    return arr


def make_2d_array_yx_seeded_col_order_alternating_using_inf(width: int, height: int) -> List:
    """
    Properties:
        - initially seeded with None
        - applies items in column order, alternating top to bottom and bottom to top
        - uses an infinite sequence to apply as many items as possible
    """

    arr = seed_2d_array_yx(width, height)
    items_iter = _infinite_sequence()
    for x in range(0, width):
        for y in range(0, height):
            if x % 2 == 0:
                arr[y][x] = next(items_iter)
            else:
                arr[height - y - 1][x] = next(items_iter)
    return arr


def make_2d_array_yx_unseeded_col_order_alternating_using_inf(width: int, height: int) -> List:
    """
    Properties:
        - not initially seeded
        - applies items in column order, alternating top to bottom and bottom to top
        - uses an infinite sequence to apply as many items as possible
    """

    arr = []
    items_iter = _infinite_sequence()
    for x in range(0, width):
        for y in range(0, height):
            if x % 2 == 0:
                idx = y
                while idx >= len(arr):
                    arr.append([])
                arr[y].append(next(items_iter))
            else:
                idx = height - y - 1
                while idx >= len(arr):
                    arr.append([])
                arr[height - y - 1].append(next(items_iter))
    return arr


def print_2d_yx(arr: List) -> None:
    height = len(arr)
    for y in range(0, height):
        arr_x = arr[y]
        row_str = '   '.join(map(_format_item, arr_x))
        full_str = '{}{}{}'.format(
            '[ ' if y == 0 else '  ',
            row_str,
            ' ]' if y == height - 1 else '',
        )
        print(full_str)


def slice_infinite_sequence(num_items: int):
    return itertools.islice(_infinite_sequence(), num_items)


def _format_item(item: Any) -> str:
    return '{:4}'.format(str(item))


def _infinite_sequence() -> Iterator[int]:
    num = 0
    while True:
        yield num
        num += 1
