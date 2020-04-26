def sort_lowercase(text: str) -> str:
    # O(n)
    counter = [0] * 26
    for letter in text:
        counter[_to_ord(letter)] += 1

    # O(n) because we need to account for every character
    result = []
    for ordinal in range(0, 26):
        result.extend([_to_char(ordinal)] * counter[ordinal])

    # O(n)
    return ''.join(result)


def _to_ord(letter: str):
    return ord(letter) - ord('a')


def _to_char(ordinal: int):
    return chr(ordinal + ord('a'))
