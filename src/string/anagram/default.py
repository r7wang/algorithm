from typing import List


def is_anagram(text_a: str, text_b: str) -> bool:
    """
    Add all the letter counts to a char map for both strings.
    Make sure that all of the counts are equal.
    """

    counter_a = _build_counter(text_a)
    counter_b = _build_counter(text_b)
    return counter_a == counter_b


def _build_counter(text: str) -> List:
    counter = [0] * 256
    for letter in text:
        counter[ord(letter)] += 1
    return counter
