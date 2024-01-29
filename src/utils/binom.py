def binom(n: int, k: int) -> int:
    """Compute binomial coefficient `n CHOOSE k`."""
    k = min(k, n - k)
    res = 1
    for i in range(1, k + 1):
        res = (res * (n - k + i)) // i
    return res
