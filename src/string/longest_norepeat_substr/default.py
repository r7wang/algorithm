def longest_norepeat_substr(text: str) -> int:
    """
    Don't need to traverse string more than twice: O(n).
    In the worst case, we will add to the map n times and delete from the map n times: O(n) average.
    In the worst case, we will calculate the substring 1 time: O(n).
    """

    start_ptr = 0
    end_ptr = 0
    max_len = 0
    max_substr_start_ptr = 0
    counter = {}

    for letter in text:
        # Shift start_ptr until we've deleted the repeated letter.
        while letter in counter:
            start_ptr_letter = text[start_ptr]
            del counter[start_ptr_letter]
            start_ptr += 1
            if start_ptr_letter == letter:
                break

        # Shift end_ptr to include new letter.
        counter[letter] = 1
        end_ptr += 1

        # Determine size of the substring.
        cur_len = end_ptr - start_ptr
        if cur_len > max_len:
            max_len = cur_len
            max_substr_start_ptr = start_ptr

    print(text[max_substr_start_ptr: max_substr_start_ptr + max_len])
    return max_len
