def longest_common_substring(text_a: str, text_b: str) -> int:
    matrix = []
    for i in range(0, len(text_a)):
        matrix.append([0] * len(text_b))

    longest_substr_idx_i = -1
    longest_substr_len = 0
    for i in range(0, len(text_a)):
        for j in range(0, len(text_b)):
            if text_a[i] == text_b[j]:
                prev_match = 0
                if i != 0 and j != 0:
                    prev_match = matrix[i-1][j-1]
                match_len = 1 + prev_match
                matrix[i][j] = match_len
                if match_len > longest_substr_len:
                    longest_substr_idx_i = i
                    longest_substr_len = match_len

    print(text_a[longest_substr_idx_i + 1 - longest_substr_len:longest_substr_idx_i + 1])

    return longest_substr_len
