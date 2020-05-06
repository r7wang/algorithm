"""
Find index of 0 to be replaced with 1 to get longest continuous sequence of 1s in a binary array

Given an array of 0s and 1s, find the position of 0 to be replaced with 1 to get longest continuous sequence of 1s.
Expected time complexity is O(n) and auxiliary space is O(1).

Test cases:
    [0,0,1,0,1,1,1,0,1,1]
    [0,1,1,1,0]
    [1,1,1,1,0]
    [1,1,1,1,1]
    []
"""
from typing import List


def find_replace_index(data: List[int]) -> int:
    # If we never encounter any 0s, then we just return 0 (has no significance).
    last_run_count = 0
    cur_run_count = 0
    best_solution_score = 0
    best_solution_idx = 0
    cur_solution_idx = 0

    # At the end, finalize the current temporary solution.
    for i in range(len(data) + 1):
        print(i)
        if i == len(data) or data[i] == 0:
            # Update the best solution if we found a better one.
            score = last_run_count + cur_run_count + int(data[cur_solution_idx] == 0)
            print('Score {}, curidx {}'.format(score, cur_solution_idx))
            if score > best_solution_score:
                best_solution_score = score
                best_solution_idx = cur_solution_idx
            cur_solution_idx = i

            # Replace the oldest run with the newest run and re-initialize the newest run to 0.
            last_run_count = cur_run_count
            cur_run_count = 0
            continue

        # Assume that the data can only be 0 or 1, so it must be 1 in this case.
        cur_run_count += 1

    return best_solution_idx
