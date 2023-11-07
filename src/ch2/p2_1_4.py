import math

from typing import Tuple

from utils.sim import choose_point, run_sims_and_report

"""
2.1.4

Alter the program MonteCarlo to estimate the area under the graph of
y = sin(pi x) inside the unit square by choosing 10,000 points at random. Now
calculate the true value of this area and use your results to estimate the value
of pi. How accurate is your estimate?
"""


def is_under_sin(pt: Tuple[float, float]) -> bool:
    x, y = pt
    sin_val = math.sin(math.pi * x)
    return y < sin_val


run_sims_and_report(
    fn=lambda: is_under_sin(pt=choose_point()),
    samples=1000,
    trials=10000,
    sample_res_map=lambda x: 2 / x,
)
