import random
import statistics

from tqdm import tqdm
from typing import Callable, Optional, Tuple


def choose_point(
    x_bd: Optional[Tuple[int, int]] = (0, 1), y_bd: Optional[Tuple[int, int]] = (0, 1)
) -> Tuple[float, float]:
    x_min, x_max = x_bd
    y_min, y_max = y_bd
    return x_min + random.random() * (x_max - x_min), y_min + random.random() * (
        y_max - y_min
    )


def run_sample(fn: Callable[[], bool], trials: int) -> float:
    ct = 0
    for _ in range(trials):
        ct += 1 if fn() else 0
    return ct / trials


def run_sims_and_report(
    fn: Callable[[], bool],
    samples: Optional[int] = 100,
    trials: Optional[int] = 100,
    sample_res_map: Optional[Callable[[float], float]] = lambda x: x,
):
    sample_results = []
    for _ in tqdm(range(samples)):
        sample_results.append(sample_res_map(run_sample(fn=fn, trials=trials)))

    print(
        f"mean={statistics.mean(sample_results)}, stdev={statistics.stdev(sample_results)}"
    )
