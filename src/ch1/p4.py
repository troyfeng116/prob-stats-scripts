import random
import statistics

from tqdm import tqdm

"""
4. In raquetball, a player continues to serve as long as she is winning; a point
is scored only when a player is serving and wins the volley. The first player
to win 21 points wins the game. Assume that you serve first and have a
probability .6 of winning a volley when you serve and probability .5 when
your opponent serves. Estimate, by simulation, the probability that you will
win a game.
"""

WINNING_SCORE = 21
P1_SERVE_WIN_PROB = 0.6
P2_SERVE_WIN_PROB = 0.5


"""
======== monte carlo ========
"""


def play_game() -> int:
    p1_score, p2_score = 0, 0
    is_p1_serving = True
    while p1_score < WINNING_SCORE and p2_score < WINNING_SCORE:
        r = random.random()
        if is_p1_serving:
            if r < P1_SERVE_WIN_PROB:
                p1_score += 1
            else:
                is_p1_serving = False
        else:
            if r < P2_SERVE_WIN_PROB:
                p2_score += 1
            else:
                is_p1_serving = True
    return 1 if p1_score == WINNING_SCORE else 2


def run_sample(trials: int) -> float:
    p1_win_ct = 0
    for _ in range(trials):
        p1_win_ct += 1 if play_game() == 1 else 0
    # print(f"p1_win_ct={p1_win_ct}, trials={trials} -> p = {p1_win_ct / trials}")
    return p1_win_ct / trials


samples = 100
trials = 1000
sample_results = []
for i in tqdm(range(samples)):
    sample_results.append(run_sample(trials=trials))

print(
    f"mean={statistics.mean(sample_results)}, stdev={statistics.stdev(sample_results)}"
)


"""
======== dynamic programming ========
"""

# prob_p1[i][j] = prob P1 wins, given P1 serving, with score P1:i to P2:j
# prob_p2[i][j] = prob P1 wins, given P2 serving, with score P1:i to P2:j
# solved recurrences:
# prob_p1[i][j] = 0.6*prob_p1[i+1][j] + (1-0.6)*prob_p2[i][j]
# prob_p2[i][j] = 0.5*prob_p2[i][j+1] + (1-0.5)*prob_p1[i][j]

prob_p1 = [[0.0 for _ in range(WINNING_SCORE + 1)] for _ in range(WINNING_SCORE + 1)]
prob_p2 = [[0.0 for _ in range(WINNING_SCORE + 1)] for _ in range(WINNING_SCORE + 1)]

for losing_score in range(0, WINNING_SCORE):
    prob_p1[WINNING_SCORE][losing_score] = 1.0
    prob_p2[WINNING_SCORE][losing_score] = 1.0

mult = 1 / (1 - (1 - P1_SERVE_WIN_PROB) * (1 - P2_SERVE_WIN_PROB))
for i in range(WINNING_SCORE - 1, -1, -1):
    for j in range(WINNING_SCORE - 1, -1, -1):
        prob_p1[i][j] = mult * (
            P1_SERVE_WIN_PROB * prob_p1[i + 1][j]
            + (1 - P1_SERVE_WIN_PROB) * P2_SERVE_WIN_PROB * prob_p2[i][j + 1]
        )
        prob_p2[i][j] = mult * (
            P2_SERVE_WIN_PROB * prob_p2[i][j + 1]
            + (1 - P2_SERVE_WIN_PROB) * P1_SERVE_WIN_PROB * prob_p1[i + 1][j]
        )

print(prob_p1[0][0])
