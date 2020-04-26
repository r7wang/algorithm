from typing import List


def is_anagram(text_a: str, text_b: str) -> bool:
    """
    Add all the letter counts to a char map for both strings.
    Make sure that all of the counts are equal.
    """

    # O(n) to build each counter
    counter_a = _build_counter(text_a)
    counter_b = _build_counter(text_b)

    # O(1) to verify counter equality
    return counter_a == counter_b


def all_anagrams(text_a: str, text_b: str) -> List:
    if len(text_b) == 0:
        return []

    if len(text_a) < len(text_b):
        return []

    # O(b)
    counter_b = _build_counter(text_b)

    # We need O(a) comparisons, each of which cost O(1)
    results = []
    counter_a = _build_counter('')
    for i in range(0, len(text_a)):
        start_ptr = i - len(text_b)
        end_ptr = i

        end_ptr_letter = text_a[end_ptr]
        counter_a[ord(end_ptr_letter)] += 1
        if start_ptr < 0:
            continue

        start_ptr_letter = text_a[start_ptr]
        counter_a[ord(start_ptr_letter)] -= 1
        if counter_a == counter_b:
            results.append(start_ptr + 1)

    return results


def _build_counter(text: str) -> List:
    counter = [0] * 256
    for letter in text:
        counter[ord(letter)] += 1
    return counter
