"""
Start at n, at each step, +1 w/ prob p, -1 w/ prob 1-p.
Ruin once hit 0. Find prob ruin at exactly n+2k steps
"""

N = 5
K = 3
P = 1 / 3


def gamblers_ruin_dp(n: int, k: int, p: float) -> float:
    # opt[i][t] = probability ruin in exactly n+2k steps, given have i at step t
    # opt[i][t] = p*opt[i+1][t+1] + q*opt[i-1][t+1]
    steps = n + 2 * k
    opt = [[0.0 for _ in range(steps + 1)] for _ in range(steps + 1)]
    opt[0][steps] = 1.0
    for t in range(steps - 1, -1, -1):
        for i in range(steps):
            opt[i][t] += p * opt[i + 1][t + 1]
            if i - 1 != 0 or t == steps - 1:
                opt[i][t] += (1 - p) * opt[i - 1][t + 1]

    return opt[n][0]


print(gamblers_ruin_dp(n=N, k=K, p=P))
