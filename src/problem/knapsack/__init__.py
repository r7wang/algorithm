"""
Find the optimal value that can be fit in side a knapsack of size n.
"""
from typing import Dict


class Item:
    def __init__(self, name: str, weight: int, value: int):
        self.name = name
        self.weight = weight
        self.value = value


item_types = [
    Item('XS', 7, 1),
    Item('S', 10, 2),
    Item('M', 16, 4),
    Item('L', 25, 6),
    Item('XL', 100, 30),
]


def knapsack(max_weight: int) -> int:
    # For each of the items, find the greatest common divisor of those items, and start by incrementing the steps.
    gcd_weight = _gcd_weight_for_all_items()

    # Maps weight to optimal value.
    optimal_values = {}

    cur_weight = 0
    while cur_weight <= max_weight:
        optimal_values[cur_weight] = _get_optimal_value(cur_weight, optimal_values)
        print('weight={} value={}'.format(cur_weight, optimal_values[cur_weight]))
        cur_weight += gcd_weight
    return optimal_values[cur_weight-gcd_weight]


def _get_optimal_value(weight: int, optimal_values: Dict[int, int]) -> int:
    if weight == 0:
        return 0

    optimal_value = 0
    for item_type in item_types:
        prev_weight = weight - item_type.weight
        if prev_weight < 0:
            continue

        optimal_value = max(optimal_value, item_type.value + optimal_values[prev_weight])
    return optimal_value


def _gcd_weight_for_all_items() -> int:
    cur_gcd = item_types[0].weight
    for i in range(1, len(item_types)):
        cur_gcd = _gcd(cur_gcd, item_types[i].weight)
    return cur_gcd


def _gcd(a: int, b: int) -> int:
    min_val = min(a, b)
    max_val = max(a, b)

    if min_val == 0:
        return max_val

    return _gcd(b % a, a)
