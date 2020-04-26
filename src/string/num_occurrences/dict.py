def num_occurrences(text: str, search_letter: str) -> int:
    occurrences = {}
    for letter in text:
        if letter not in occurrences:
            occurrences[letter] = 0
        occurrences[letter] += 1

    return occurrences[search_letter]
