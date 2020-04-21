from typing import List


def build() -> List:
    return [2, 2, 3, 4, 5, 5, 6, 7, 8, 9, 9, 12, 13, 15, 16, 19, 23, 24, 29]


def search(data: List, val: int) -> int:
    """Runs a binary search to find the index of the item, returning -1 if index not found"""

    if not data:
        print('{} not found'.format(val))
        return -1

    # Figure out if we want to search the earlier portion or the next portion.
    mid = len(data) // 2
    mid_val = data[mid]
    print('pivot={}, pivot_val={}, data={}'.format(mid, mid_val, data))
    if mid_val == val:
        return mid
    elif mid_val > val:
        return search(data[:mid], val)
    else:
        return search(data[mid + 1:], val)
