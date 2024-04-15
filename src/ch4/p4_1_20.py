"""
Start with one white ball and one red ball.
Randomly choose a ball from the urn and double it.
Find limit of proportion of balls in urn
"""

from random import random
from src.utils.sim import run_sims_and_report


def run_sim_max(num_draws=10000) -> float:
    w, r = 1, 1
    for _ in range(num_draws):
        if random() < w / (w + r):
            w += 1
        else:
            r += 1
    return max(w, r) / (w + r)


def run_sim_red(num_draws=10000) -> float:
    w, r = 1, 1
    for _ in range(num_draws):
        if random() < w / (w + r):
            w += 1
        else:
            r += 1
        return r / (w + r)


run_sims_and_report(fn=run_sim_max, num_samples=100, trials_per_sample=100)
run_sims_and_report(fn=run_sim_red, num_samples=100, trials_per_sample=100)
