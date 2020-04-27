from typing import List, Set, Tuple


def find_unique_3sum_triplets(data: List[int]) -> Set[Tuple[int, int, int]]:
    if len(data) < 3:
        return []

    # For every single item, in the array, fix one value and solve 2sum on the
    # remaining values.
    solutions_3sum = set()
    for i in range(0, len(data)):
        solutions_2sum = _2sum(data, i)
        solutions_3sum.update(solutions_2sum)

    return solutions_3sum


# Solutions must all be ordered to avoid duplicates. It's easier for us to do
# this when generating the solution.
def _2sum(data: List[int], fixed_idx: int) -> Set[Tuple[int, int, int]]:
    solutions = set()

    # Build a counter so we can easily determine whether or not a 2sum solution
    # exists.
    counter = {}
    fixed_val = data[fixed_idx]
    for i in range(0, len(data)):
        if i == fixed_idx:
            continue
        # We don't care if there is more than one item.
        if data[i] not in counter:
            counter[data[i]] = 0
        counter[data[i]] += 1

    # Collect all 2sum solutions.
    for key in counter:
        to_search = -fixed_val - key
        to_search_exists = to_search in counter
        has_sufficient_quantity = key != to_search or counter[to_search] > 1
        if to_search_exists and has_sufficient_quantity:
            solution = tuple(sorted([fixed_val, key, to_search]))
            solutions.add(solution)

    return solutions
