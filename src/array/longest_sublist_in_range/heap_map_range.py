import heapq
from typing import List, Dict


def longest_sublist_in_range(data: List[int], max_range: int) -> List[int]:
    if len(data) <= 1:
        return data

    start_idx = 0
    end_idx = 1

    # All of these structures cost O(n) space.
    range_min_heap = [data[0]]
    range_max_heap = [-data[0]]
    counter = {data[0]: 1}

    solution_start_idx = 0
    solution_end_idx = 1

    while True:
        # If we satisfy the max_diff requirement, expand, otherwise contract.
        if _meets_range_requirement(range_min_heap, range_max_heap, max_range):
            better_solution = (end_idx - start_idx) > (solution_end_idx - solution_start_idx)
            if better_solution:
                solution_start_idx = start_idx
                solution_end_idx = end_idx

            # If we are already at the end, stop. This happens after the check for better solutions to ensure that we
            # never forget to update the solutions.
            if len(data) == end_idx:
                break

            to_add = data[end_idx]
            if not counter.get(to_add):
                # O(log_n)
                heapq.heappush(range_min_heap, to_add)
                heapq.heappush(range_max_heap, -to_add)
                counter[to_add] = 1
            else:
                counter[to_add] += 1
            end_idx += 1
        else:
            to_remove = data[start_idx]
            counter[to_remove] -= 1
            if counter[to_remove] == 0:
                # Aligning won't ever cause more operations than the number of times we modify the counter.
                _align_min_heap_with_counter(range_min_heap, counter)
                _align_max_heap_with_counter(range_max_heap, counter)
            start_idx += 1

    return data[solution_start_idx: solution_end_idx]


def _meets_range_requirement(range_min_heap: List[int], range_max_heap: List[int], max_range: int) -> bool:
    min_val = range_min_heap[0]
    max_val = -range_max_heap[0]
    return max_val - min_val <= max_range


def _align_min_heap_with_counter(min_heap: List[int], counter: Dict[int, int]):
    while True:
        min_val = min_heap[0]
        if not counter.get(min_val):
            heapq.heappop(min_heap)
        else:
            break


def _align_max_heap_with_counter(max_heap: List[int], counter: Dict[int, int]):
    while True:
        max_val = -max_heap[0]
        if not counter.get(max_val):
            # O(log_n)
            heapq.heappop(max_heap)
        else:
            break
