from src.utils.binom import binom


N, M = 20, 13


def bertrand_ballot_dp(n: int, m: int) -> int:
    if n < m:
        raise ValueError(f"n={n} votes for A cannot be less than m={m} votes for B")

    # dp[a][b] = num paths starting from a votes for A, b votes for B
    opt = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
    for a in range(n, -1, -1):
        # must have a >= b
        for b in range(min(a, m), -1, -1):
            if a == n:
                opt[a][b] = 1
            else:
                opt[a][b] += opt[a + 1][b]
                if b + 1 <= m and b + 1 <= a:
                    opt[a][b] += opt[a][b + 1]
    return opt[0][0]


print(bertrand_ballot_dp(n=N, m=M))
print((binom(n=N + M, k=M) * (N + 1 - M)) // (N + 1))

assert bertrand_ballot_dp(n=N, m=M) == (binom(n=N + M, k=M) * (N + 1 - M)) // (N + 1)
