"""
Find probability that when a random walk around a circle reaches the opposite end,
the walk has visited every other node at least once.

Probability is uniform for all target target nodes not equal to start!
"""

import random

from src.utils.sim import run_sims_and_report


N = 100
TARGET = 50


def run_frog_once() -> bool:
    x = 0

    visited_l, visited_r = False, False
    while x != TARGET:
        if x == TARGET + 1:
            visited_r = True
        elif x == TARGET - 1:
            visited_l = True

        if random.random() < 0.5:
            if x == N:
                x = 0
            x += 1
        else:
            if x == 0:
                x = N
            x -= 1
    return visited_l and visited_r


run_sims_and_report(fn=run_frog_once, num_samples=100, trials_per_sample=100)
