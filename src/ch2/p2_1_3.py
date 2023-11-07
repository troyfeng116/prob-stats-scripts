from typing import Tuple

from utils.sim import choose_point, run_sims_and_report

"""
2.1.3

Alter the program MonteCarlo to estimate the area of the circle of radius
1/2 with center at (1/2, 1/2) inside the unit square by choosing 1000 points
at random. Compare your results with the true value of pi/4. Use your results
to estimate the value of pi. How accurate is your estimate?
"""

CENTER = (0.5, 0.5)
RADIUS = 0.5


def is_in_circle(pt: Tuple[float, float], c_pt: Tuple[float, float], r: float) -> bool:
    x, y = pt
    cx, cy = c_pt
    (x - cx) ** 2 + (y - cy) ** 2
    return (x - cx) ** 2 + (y - cy) ** 2 < r**2


run_sims_and_report(
    fn=lambda: is_in_circle(pt=choose_point(), c_pt=CENTER, r=RADIUS),
    samples=1000,
    trials=10000,
    sample_res_map=lambda x: 4 * x,
)
