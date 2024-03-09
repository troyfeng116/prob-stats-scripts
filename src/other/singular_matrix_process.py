"""
Starting with 2x2 identity matrix, randomly choose an entry and flip it.
Find expected steps until singular matrix.
"""

import random

from typing import List

from src.utils.sim import run_sims_and_report


def det(mat: List[int]) -> int:
    a, b, c, d = mat
    return a * c - b * d


def run_matrix_process() -> int:
    mat = [1, 0, 1, 0]
    steps = 0
    while det(mat=mat) != 0:
        idx = random.randint(0, 3)
        mat[idx] = 1 - mat[idx]
        steps += 1
    return steps


run_sims_and_report(fn=run_matrix_process, num_samples=1000, trials_per_sample=1000)
print(12 / 7)
