def n_choose_k(n: int, k: int) -> int:
    largest_div = max(k, n-k)
    smallest_div = min(k, n-k)

    numerator = 1
    for multiplier in range(largest_div + 1, n + 1):
        numerator *= multiplier

    denominator = 1
    for multiplier in range(1, smallest_div + 1):
        denominator *= multiplier

    return int(numerator / denominator)
