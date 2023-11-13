import math
import random

from typing import Tuple

from utils.sim import run_sims_and_report

"""
For Buffon's needle problem, Laplace considered a grid with horizontal and
vertical lines one unit apart. He showed that the probability that a needle of
length `L ≤ 1` crosses at least one line is
`p = (4L - L^2) / π`
To simulate this experiment we choose at random an angle θ between 0 and
π/2 and independently two numbers `d1` and `d2` between 0 and 1/2. (The two
numbers represent the distance from the center of the needle to the nearest
horizontal and vertical line.) The needle crosses a line if either `d1 ≤ (L/2) sin θ`
or `d2 ≤ (L/2) cos θ`. We do this a large number of times and estimate π as
`π = (4L - L^2) / a`,
where `a` is the proportion of times that the needle crosses at least one line.
Write a program to estimate π by this method, run your program for 100,
1000, and 10,000 experiments, and compare your results with Buffon's method
described in Exercise 6. (Take `L = 1`.)
"""

L = 1


def sample_laplace_point() -> Tuple[float, float, float]:
    return (
        random.random() / 2,
        random.random() / 2,
        random.random() * math.pi / 2,
    )


def does_intersect_grid(d1: float, d2: float, theta: float) -> bool:
    return d1 <= (L / 2) * math.sin(theta) or d2 <= (L / 2) * math.cos(theta)


run_sims_and_report(
    fn=lambda: does_intersect_grid(*sample_laplace_point()),
    num_samples=1000,
    trials_per_sample=10000,
    sample_res_map=lambda a: (4 * L - L**2) / a,
)
