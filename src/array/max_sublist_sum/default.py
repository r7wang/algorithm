"""
Find the maximum sublist sum of an array containing positive and negative integers.
"""
from typing import List, Optional

NO_SOLUTION = -999


def max_sublist_sum(data: List[int]) -> Optional[int]:
    # return _solve_brute_force(data)
    # return _solve_iterative(data)
    return _solve_linear(data)


def _solve_linear(data: List[int]) -> Optional[int]:
    # For the whole array from 0 -> (n-1):
    #   - If index 0 is negative, we don't want that element.
    #   - If index 0 is positive, and sum(index 0 -> k) is negative, then item k must be sufficiently negative to wipe
    #     out positivity from 0 -> k-1.
    #
    # Index: 0                    k
    #        P------------------>PN
    #        ----------------------
    #
    # Notes:
    #   - There is no way for sum(index 1 -> k-1) to be more positive than what k would wipe out, because that would
    #     imply index 0 to be negative, and if index 0 is negative, there's no reason to start accumulating from that
    #     index.
    #   - During the time when we're traversing the array, we should record our best solution.
    #
    # If we want to track the indices of the best solution:
    #   - Track the start index of the current solution.
    #   - Every time we update the best solution, the best solution goes from start index of the current solution to
    #     current index.
    best_solution = NO_SOLUTION
    cur_solution = 0
    for val in data:
        cumulative_sum = cur_solution + val

        # Update the best solution.
        best_solution = max(best_solution, cumulative_sum)

        # Decide whether or not to reset the current solution.
        if cumulative_sum < 0:
            cur_solution = 0
        else:
            cur_solution = cumulative_sum

    return best_solution if best_solution != NO_SOLUTION else None


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
