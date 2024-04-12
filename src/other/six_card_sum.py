"""
3 aces and 3 jacks in a pile, drawn one at a time without replacement.
At each turn, correct guess -> $1.
Find expected winnings under optimal strategy.
"""

ACES = 3
JACKS = 3


def solve_dp(aces: int, jacks: int) -> float:
    dp = [[0 for _ in range(jacks + 1)] for _ in range(aces + 1)]
    for j in range(1, jacks + 1):
        dp[0][j] = j
    for a in range(1, aces + 1):
        dp[a][0] = a

    for a in range(1, aces + 1):
        for j in range(1, jacks + 1):
            t = a + j
            dp[a][j] = max(a, j) / t + (a / t) * dp[a - 1][j] + (j / t) * dp[a][j - 1]

    return dp[aces][jacks]


print(solve_dp(aces=ACES, jacks=JACKS))
