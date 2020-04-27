def remove_duplicate_letters(text: str) -> str:
    """
    algorithm takes O(n) time
    counter takes O(1) space
    dedup_text takes O(n) space

    Python strings are immutable. To get constant space, you need to have built up the array using a linked list.
    The closest implementation is a deque. Then you can find a duplicate, pop it, and repeat.
    """

    counter = [0] * 256
    dedup_text = []

    for letter in text:
        counter_idx = ord(letter)
        if counter[counter_idx] == 0:
            dedup_text.append(letter)
            counter[counter_idx] = 1

    return ''.join(dedup_text)
