from typing import List


def longest_sublist_in_range(data: List[int], max_range: int) -> List[int]:
    if len(data) <= 1:
        return data

    start_idx = 0
    end_idx = 1

    solution_start_idx = 0
    solution_end_idx = 1

    while True:
        # If we satisfy the max_diff requirement, expand, otherwise contract.
        if _meets_range_requirement(data[start_idx: end_idx], max_range):
            better_solution = (end_idx - start_idx) > (solution_end_idx - solution_start_idx)
            if better_solution:
                solution_start_idx = start_idx
                solution_end_idx = end_idx

            # If we are already at the end, stop. This happens after the check for better solutions to ensure that we
            # never forget to update the solutions.
            if len(data) == end_idx:
                break

            end_idx += 1
        else:
            start_idx += 1

    return data[solution_start_idx: solution_end_idx]


def _meets_range_requirement(data: List[int], max_range: int) -> bool:
    # O(2n) on data.
    return max(data) - min(data) <= max_range
