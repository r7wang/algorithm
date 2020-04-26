def is_palindrome(text: str) -> bool:
    """
    Keep two pointers, one at start of string, and one at the end, and move them in opposite directions.
    """

    if len(text) <= 1:
        return True

    start_ptr = 0
    end_ptr = len(text) - 1
    while start_ptr < end_ptr:
        if text[start_ptr] != text[end_ptr]:
            return False

        start_ptr += 1
        end_ptr -= 1

    return True
