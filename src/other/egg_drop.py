"""
Egg drop problem

Note: if given that there does exist `x \in [1, floors]`
s.t. dropping below x is safe but dropping at or above x is unsafe,
can pass `floors - 1` into `min_egg_drops`
-> determines number of drops to determine if there is a cutoff floor in `[1, floors-1]`
-> this tells us whether floor `floor` is safe, if every floor in `[1, floors-1]` is safe.

ex. if one floor, it takes one drop to determine whether floor is safe
IF not given existence of breaking floor `x`.
If given existence of breaking floor, would take 0 drops.
"""


def min_egg_drops(eggs: int, floors: int) -> int:
    """Given `eggs` and `floors`, find min drops needed to determine cutoff `x \in [1, floors]`
    s.t. it is safe to drop an egg from below floor `x`, but not from floors `x` and above.
    Assume it is possible that egg may not break for any `x \in [1, floors]`.

    Args:
        eggs (int): Number of remaining eggs.
        floors (int): Number of floors to test.

    Returns:
        int: Minimum drops needed to find safe floor cutoff for dropping eggs.
    """

    # opt[e][f] = (best floor to drop from, min drops to find cutoff floor) with e eggs, f floors to search
    opt = [[(None, None) for _ in range(floors + 1)] for _ in range(eggs + 1)]

    # base case: if 1 egg left, must linearly drop one floor at a time worst-case
    for f in range(1, floors + 1):
        opt[1][f] = (1, f)

    # base case: if 0 floors left, no more drops needed
    for e in range(1, eggs + 1):
        opt[e][0] = (None, 0)
        opt[e][1] = (None, 1)

    for e in range(2, eggs + 1):
        for f in range(2, floors + 1):
            best_f, best_ct = 0, float("inf")
            # for every floor drop_f we could drop from: find drop_f that minimizes worst-case drops
            for drop_f in range(1, f + 1):
                # if break at drop_f, (e-1) eggs left and (drop_f - 1) floors left to check
                ct_if_break = 1 + opt[e - 1][drop_f - 1][1]
                # if safe at drop_f, e eggs left and (f - drop_f) floors left to check
                ct_if_safe = 1 + opt[e][f - drop_f][1]
                # egg could break or not break if drop from drop_f -> use worst-case
                worst_case_ct = max(ct_if_break, ct_if_safe)
                if worst_case_ct < best_ct:
                    best_f, best_ct = drop_f, worst_case_ct
            opt[e][f] = (best_f, best_ct)

    for e in range(1, eggs + 1):
        s_list = list(
            map(
                lambda x: f"{e} eggs, {x[0]} floors -> drop from {x[1][0]}, worst-case drops = {x[1][1]}",
                enumerate(opt[e]),
            )
        )
        print("\n".join(s_list))
    return opt[eggs][floors][1]


eggs = 3
floors = 131
print(min_egg_drops(eggs=eggs, floors=floors - 1))
