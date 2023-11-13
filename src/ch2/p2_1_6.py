import math
import random

from typing import Tuple

from utils.sim import run_sims_and_report

"""
2.1.6

To simulate the Buffon's needle problem we choose independently the distance
`d` and the angle `θ` at random, with `0 ≤ d ≤ 1/2` and `0 ≤ θ ≤ π/2`,
and check whether `d ≤ (1/2)sin θ`. Doing this a large number of times, we
estimate π as `2/a`, where `a` is the fraction of the times that `d ≤ (1/2)sin θ`.
Write a program to estimate π by this method. Run your program several
times for each of 100, 1000, and 10,000 experiments. Does the accuracy of
the experimental approximation for π improve as the number of experiments
increases?
"""


def sample_buffon_point() -> Tuple[float, float]:
    return random.random() * 0.5, random.random() * math.pi / 2


def does_intersect_line(d: float, theta: float) -> bool:
    return d <= 0.5 * math.sin(theta)


run_sims_and_report(
    fn=lambda: does_intersect_line(*sample_buffon_point()),
    num_samples=1000,
    trials_per_sample=10000,
    sample_res_map=lambda a: 2 / a,
)
