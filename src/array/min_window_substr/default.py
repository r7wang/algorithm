from typing import List


def min_window_substring(text: str, substr: str) -> str:
    if len(text) < len(substr):
        return ''

    start_ptr = 0
    end_ptr = 0

    result_start_ptr = None
    result_end_ptr = None

    counter_text = _build_counter('')
    counter_substr = _build_counter(substr)

    while True:
        if _contains(counter_text, counter_substr):
            diff = end_ptr - start_ptr
            if result_start_ptr is None or diff < (result_end_ptr - result_start_ptr):
                result_start_ptr = start_ptr
                result_end_ptr = end_ptr
                print('result = {}'.format(text[start_ptr: end_ptr]))
            if diff == len(substr) - 1:
                break

            # Try to increment start_ptr to reduce the window.
            start_ptr_letter = text[start_ptr]
            counter_text[ord(start_ptr_letter)] -= 1
            start_ptr += 1
            print('start ptr = {}'.format(start_ptr))
        else:
            if end_ptr == len(text):
                break

            # Try to increment end_ptr to satisfy the condition.
            end_ptr_letter = text[end_ptr]
            counter_text[ord(end_ptr_letter)] += 1
            end_ptr += 1
            print('end ptr = {}'.format(end_ptr))

    if result_start_ptr is None:
        return ''

    return text[result_start_ptr: result_end_ptr]


def _build_counter(text: str) -> List:
    counter = [0] * 256
    for letter in text:
        counter[ord(letter)] += 1
    return counter


def _contains(counter: List, counter_substr: List) -> bool:
    for i in range(0, len(counter_substr)):
        if counter_substr[i] != 0 and counter[i] < counter_substr[i]:
            return False
    return True
