"""
Print out all characters within a string in their binary representation, where every character's integer value is the
ordinal in the ASCII table.
"""


def to_binary(text: str) -> None:
    for letter in text:
        print(_binary(letter))


def _binary(letter: str) -> str:
    result = []
    ordinal = ord(letter)

    # O(n^2), where n is number of bits required to store a letter
    while ordinal > 0:
        if (ordinal >> 1 << 1) != ordinal:
            result.append('1')
        else:
            result.append('0')
        ordinal = ordinal >> 1

    # O(n)
    result.reverse()
    return ''.join(result)
