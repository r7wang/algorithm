"""
Given a string that contains the following alphabet ('0', '1', '?'), return all valid expansions of the string, where
the wildcard character ('?') can be one of ('0', '1').

For example:
    - Input: '10'
    - Output: ['10']

    - Input: '010?'
    - Output: ['0100', '0101']
"""
from typing import List


def expand_wildcard(pattern: str) -> List[str]:
    # Tokenize the string.
    tokens = pattern.split('?')
    if len(tokens) == 1:
        return [tokens[0]]

    # If there are n tokens, there are n-1 wildcards, and each wildcard doubles the solution size.
    solutions = []
    num_wildcards = len(tokens) - 1
    for i in range(1 << num_wildcards):
        bitmask = i
        accumulator = [tokens[0]]

        for j in range(num_wildcards):
            # Remainder is going to be either 0 or 1. Note that this will not return the values in sorted order.
            remainder = bitmask % 2
            bitmask = bitmask >> 1

            accumulator.append(str(remainder))
            accumulator.append(tokens[j + 1])

        solutions.append(''.join(accumulator))

    return solutions
