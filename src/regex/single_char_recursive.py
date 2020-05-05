"""
Given an input text and a pattern, implement regular expression matching with support for '.' and '*'.

'.' Matches any single character.
'*' Matches zero or more of the preceding element.

Single char recursive is a simplification for more elegant code that minimally increments the solution.
"""


def is_match(text: str, pattern: str) -> bool:
    # Case 1: No pattern left, and has text (FALSE)
    # Case 2: No pattern left, and no text (TRUE)
    if not pattern:
        return not text

    # Case 3: Has pattern left, and no string:
    #   - Is end of pattern? Cannot be * (FALSE)
    #   - Not end of pattern?
    #       - Is pattern[i+1] *? Recurse
    #       - Is pattern[i+1] non-*? (FALSE)
    end_of_pattern = len(pattern) == 1
    if len(text) == 0:
        if end_of_pattern or pattern[1] != '*':
            return False
        return is_match(text, pattern[2:])

    # Case 4: Has pattern left, and has string:
    #   - Is end of pattern? Match text and recurse
    #   - Not end of pattern?
    #       - Is pattern[i+1] *? Generate subproblems and recurse
    #       - Is pattern[i+1] non-*? Match text and recurse
    if end_of_pattern or pattern[1] != '*':
        if not _match_char(text[0], pattern[0]):
            return False
        return is_match(text[1:], pattern[1:])

    # We know that we have a repeat character and a * coming up.
    subproblems = []
    i = 0
    while True:
        subproblems.append(i)
        if i == len(text) or not _match_char(text[i], pattern[0]):
            break
        i += 1
    for text_start_idx in subproblems:
        if is_match(text[text_start_idx:], pattern[2:]):
            return True
    return False


def _match_char(text: str, pattern: str) -> bool:
    # Must guarantee that there is a first char for each.
    return text == pattern or pattern == '.'
