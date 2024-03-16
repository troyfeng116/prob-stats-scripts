"""
Each face of a cube is painted randomly one of the colors red, orange, yellow, green, blue or purple.
What is the probability that the cube has at least one pair of faces that share an edge and are the same color?
"""

from typing import List


COLORS = [i for i in range(1, 7)]


def generate_paintings() -> List[List[int]]:
    all_paintings: List[List[int]] = []

    def backtrack_paintings(painting: List[int], idx: int):
        if idx >= len(painting):
            all_paintings.append(painting.copy())
            return
        for color in COLORS:
            painting[idx] = color
            backtrack_paintings(painting=painting, idx=idx + 1)

    backtrack_paintings(painting=[0 for _ in range(len(COLORS))], idx=0)
    return all_paintings


def does_painting_share_color_edge(painting: List[int]) -> bool:
    for face in range(6):
        for other_face in range(6):
            if face == other_face or face == 6 - other_face - 1:
                continue
            if painting[face] == painting[other_face]:
                return True
    return False


all_paintings = generate_paintings()
indic = [
    1 if does_painting_share_color_edge(painting=painting) else 0
    for painting in all_paintings
]

print(sum(indic))
print(len(all_paintings))
