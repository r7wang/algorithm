def num_occurrences_in_dict(text: str, search_letter: str) -> int:
    num_occurrences = {}
    for letter in text:
        if letter not in num_occurrences:
            num_occurrences[letter] = 0
        num_occurrences[letter] += 1

    return num_occurrences[search_letter]


def num_occurrences_in_charmap(text: str, search_letter: str) -> int:
    num_occurrences = [0] * 256
    for letter in text:
        num_occurrences[ord(letter)] += 1

    return num_occurrences[ord(search_letter)]
