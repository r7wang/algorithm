from typing import List


def merge_sort_nspace(data: List[int]) -> List[int]:
    return _recursive_merge_sort(data, 0, len(data))


# We can avoid making new arrays while splitting on the way down by passing indices.
def _recursive_merge_sort(data: List[int], start_idx: int, end_idx: int) -> List[int]:
    # Already sorted.
    num_items = end_idx - start_idx
    if num_items == 1:
        return data[start_idx: end_idx]

    # Split up into (as close as possible to) two identical sized pieces.
    split_idx = start_idx + (num_items // 2)
    left = _recursive_merge_sort(data, start_idx, split_idx)
    right = _recursive_merge_sort(data, split_idx, end_idx)
    return _join(left, right)


def _join(left_data: List[int], right_data: List[int]) -> List[int]:
    # TODO: Can we use less space by doing merge in place?
    joined = []
    left_pointer = 0
    right_pointer = 0

    while left_pointer != len(left_data) or right_pointer != len(right_data):
        left_item = None
        right_item = None
        if left_pointer != len(left_data):
            left_item = left_data[left_pointer]
        if right_pointer != len(right_data):
            right_item = right_data[right_pointer]

        # Compare both left and right. Take from whichever data source has the smaller element.
        if left_item and right_item:
            if left_item < right_item:
                joined.append(left_item)
                left_pointer += 1
            else:
                joined.append(right_item)
                right_pointer += 1
        elif left_item:
            joined.append(left_item)
            left_pointer += 1
        else:
            joined.append(right_item)
            right_pointer += 1

    return joined
