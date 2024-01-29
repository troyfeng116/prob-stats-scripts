from itertools import permutations
from random import randint
from typing import List, Dict, Set

from src.utils.sim import run_sims_and_report

"""
3.1.20

At a mathematical conference, ten participants are randomly seated around
a circular table for meals. Using simulation, estimate the probability that no
two people sit next to each other at both lunch and dinner. Can you make an
intelligent conjecture for the case of n participants when n is large?
"""

N = 10

all_seatings = list(permutations(range(1, N)))
for place in range(len(all_seatings)):
    all_seatings[place] = (0,) + all_seatings[place]


def get_neighbors(seating: List[int]) -> Dict[int, Set[int]]:
    """Generate dict of (person, neighbors) for each person in given seating arrangement."""
    return {
        m: set((seating[(place - 1 + N) % N], seating[(place + 1) % N]))
        for place, m in enumerate(seating)
    }


def has_no_shared_neighbors(neighbors: Dict[int, Set[int]], seating: List[int]) -> bool:
    """Given neighbors map from first seating, determine if anyone has repeat neighbors in second seating.

    Args:
        neighbors (Dict[int, Set[int]]): Map of person to neighbors from first seating.
        seating (List[int]): Second seating.

    Returns:
        bool: `True` iff no person has the same neighbors as in the first seating.
    """

    for place, m in enumerate(seating):
        l, r = seating[(place - 1 + N) % N], seating[(place + 1) % N]
        if l in neighbors[m] or r in neighbors[m]:
            return False
    return True


def run_once() -> bool:
    ri, rj = randint(0, len(all_seatings) - 1), randint(0, len(all_seatings) - 1)
    seating1, seating2 = all_seatings[ri], all_seatings[rj]
    neighbors1 = get_neighbors(seating=seating1)
    return has_no_shared_neighbors(neighbors=neighbors1, seating=seating2)


"""
======== simulations========
"""

run_sims_and_report(fn=run_once, num_samples=100, trials_per_sample=1000)


"""
======== compute exact probability ========
"""

# symmetry -> use identity as first seating
first_seating = list(range(N))
first_neighbors = get_neighbors(seating=first_seating)

good_seating_indic = [
    1 if has_no_shared_neighbors(neighbors=first_neighbors, seating=seating) else 0
    for seating in all_seatings
]
good_seatings, total = sum(good_seating_indic), len(good_seating_indic)

print(f"good_seatings={good_seatings}, total={total}, p={good_seatings / total}")
