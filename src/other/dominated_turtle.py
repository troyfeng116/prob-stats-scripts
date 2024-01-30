"""
Dominated Turtle

Two turtles, Tort and Bort, are going to perform independent simple symmetric random walks
on the integers starting at positions 0 and 4, respectively. Compute the probability after 
10 steps, Tort and Bort are back at their initial positions and that Tort was strictly behind
Bort at all 10 steps.
"""

from typing import List

T_START = 0
B_START = 4
MOVES = 10


def generate_possible_moves(li: List[int], forward_ct) -> List[List[int]]:
    if len(li) == MOVES and forward_ct == MOVES // 2:
        return [[*li]]

    if forward_ct > MOVES // 2 or len(li) - forward_ct > MOVES // 2:
        return []

    return generate_possible_moves(
        li=li + [1], forward_ct=forward_ct + 1
    ) + generate_possible_moves(li=li + [-1], forward_ct=forward_ct)


def does_bort_stay_ahead(t_moves: List[int], b_moves: List[int]) -> bool:
    t_pos, b_pos = T_START, B_START
    for m in range(MOVES):
        t_pos += t_moves[m]
        b_pos += b_moves[m]
        if t_pos >= b_pos:
            return False
    return True


move_sequences = generate_possible_moves(li=[], forward_ct=0)
successes = 0
for t_moves in move_sequences:
    for b_moves in move_sequences:
        successes += 1 if does_bort_stay_ahead(t_moves=t_moves, b_moves=b_moves) else 0

print(f"successes={successes}, diff={len(move_sequences) ** 2 - successes}")
