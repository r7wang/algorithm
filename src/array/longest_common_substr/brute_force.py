"""
Find the longest common substring across two strings.
"""


def longest_common_substring(text_a: str, text_b: str) -> int:
    """
    There are a substrings of length 1, a-1 substrings of length 2, ..., 1 substring of length a, for a total of up to
    a^2 substrings, each of which can be up to length a, hence the cost to build all substrings is O(a^3).
    """

    substr_a = set()
    for i in range(0, len(text_a)):
        for j in range(i + 1, len(text_a) + 1):
            substr_a.add(text_a[i: j])

    substr_b = set()
    for i in range(0, len(text_b)):
        for j in range(i + 1, len(text_b) + 1):
            substr_b.add(text_b[i: j])

    # Average case: O(a) or O(b).
    common_substr = substr_a.intersection(substr_b)
    if not common_substr:
        return 0

    largest_substr = ''
    for substr in common_substr:
        if len(substr) > len(largest_substr):
            largest_substr = substr

    print('Largest substring: {}'.format(largest_substr))
    return len(largest_substr)
