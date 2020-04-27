def num_occurrences(text: str, search_letter: str) -> int:
    occurrences = [0] * 256
    for letter in text:
        occurrences[ord(letter)] += 1

    return occurrences[ord(search_letter)]
