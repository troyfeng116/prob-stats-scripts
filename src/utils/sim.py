import random
import statistics

from tqdm import tqdm
from typing import Callable, Optional, Tuple


def choose_point(
    x_bd: Optional[Tuple[int, int]] = (0, 1), y_bd: Optional[Tuple[int, int]] = (0, 1)
) -> Tuple[float, float]:
    """Uniformly randomly select random variables `(x,y)` from given bounds.

    Args:
        x_bd (Optional[Tuple[int, int]], optional): Min/max bounds for `x`. Defaults to `(0, 1)`.
        y_bd (Optional[Tuple[int, int]], optional): Min/max bounds for `y`. Defaults to `(0, 1)`.

    Returns:
        Tuple[float, float]: Uniform random point in `x_bd PROD y_bd`.
    """

    x_min, x_max = x_bd
    y_min, y_max = y_bd
    return x_min + random.random() * (x_max - x_min), y_min + random.random() * (
        y_max - y_min
    )


def run_single_sample(fn: Callable[[], bool], trials: int) -> float:
    """Run `trials` trials of `fn`, tracking success rate.

    Args:
        fn (Callable[[], bool]): Single experiment trial runnable; return `True` iff success.
        trials (int): Number of trials to run.

    Returns:
        float: Success rate across run trials.
    """

    ct = 0
    for _ in range(trials):
        ct += 1 if fn() else 0
    return ct / trials


def run_sims_and_report(
    fn: Callable[[], bool],
    num_samples: Optional[int] = 100,
    trials_per_sample: Optional[int] = 100,
    sample_res_map: Optional[Callable[[float], float]] = lambda x: x,
):
    """Run `samples` rounds of `trials` trials of `fn`, compute + report sample aggregate statistics.

    Args:
        fn (Callable[[], bool]): Single experiment trial runnable; return `True` iff success.
        num_samples (Optional[int], optional): Size of sample. Defaults to 100.
        trials_per_sample (Optional[int], optional): Number of trials to run per sample. Defaults to 100.
        sample_res_map (Optional[Callable[[float], float]], optional): Additional map to apply to each sample result. Defaults to identity.
    """

    sample_results = []
    for _ in tqdm(range(num_samples)):
        sample_results.append(
            sample_res_map(run_single_sample(fn=fn, trials=trials_per_sample))
        )

    print(
        f"mean={statistics.mean(sample_results)}, stdev={statistics.stdev(sample_results)}"
    )
