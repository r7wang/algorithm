"""
Find the maximum sublist sum of an array containing positive and negative integers.
"""
from typing import List


def max_sublist_sum(data: List[int]) -> int:
    # return _solve_brute_force(data)
    return _solve_iterative(data)


def _solve_iterative(data: List[int]) -> int:
    max_sum = 0
    for i in range(0, len(data)):
        cumulative_sum = 0
        for j in range(i, len(data)):
            cumulative_sum += data[j]
            if cumulative_sum > max_sum:
                max_sum = cumulative_sum
    return max_sum


def _solve_brute_force(data: List[int]) -> int:
    # O(n^3) because for each of n^2 sublists, we have to pull up to n items from the list.
    max_sum = 0
    for i in range(0, len(data)):
        for j in range(i + 1, len(data) + 1):
            cur_sum = sum(data[i:j])
            print('{}-{}: {}'.format(i, j, cur_sum))
            if cur_sum > max_sum:
                max_sum = cur_sum
    return max_sum
