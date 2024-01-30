"""
Beer Barrel II

A 120-quart beer barrel was discovered by Anna's parents. Furious, they plan to dump the barrel.
Anna begs her parents to let her keep some of the beer. They say that Anna may do so if she is
able to measure out an exact quart into each of a 7-quart and 5-quart vessel. You have exactly 
1 of each type of vessel. Note that Anna is allowed to pour beer from a vessel back into the beer
barrel. Define a transaction as a pour of liquid from one container into another. What is the
smallest number of transactions needed to accomplish the challenge? If impossible, respond with
-1.
"""

from enum import Enum
from queue import Queue
from typing import Callable, Dict, List, Tuple


DISCARD_IDX = -1


class MoveType(Enum):
    POUR_1_2 = 0
    POUR_2_1 = 1
    POUR_B_1 = 2
    POUR_B_2 = 3
    POUR_1_B = 4
    POUR_2_B = 5
    DISCARD_1 = 6
    DISCARD_2 = 7
    DISCARD_B = 8

    @staticmethod
    def get_from_to_dict() -> Dict["MoveType", Tuple[int, int]]:
        """Returns (from_idx, to_idx) for each `MoveType`, where indices are into (barrel, jug1, jug2) tuples as in `Node.get_container_tuple()`.

        @see `Node.get_container_tuple()`

        Returns:
            Dict["MoveType", Tuple[int, int]]: Dict of MoveType to (from, to) indices for Node tuples.
        """
        return {
            MoveType.POUR_1_2: (1, 2),
            MoveType.POUR_2_1: (2, 1),
            MoveType.POUR_B_1: (0, 1),
            MoveType.POUR_B_2: (0, 2),
            MoveType.POUR_1_B: (1, 0),
            MoveType.POUR_2_B: (2, 0),
            MoveType.DISCARD_1: (1, DISCARD_IDX),
            MoveType.DISCARD_2: (2, DISCARD_IDX),
            MoveType.DISCARD_B: (0, DISCARD_IDX),
        }


class Container:
    amt: int
    cap: int

    def __init__(self, amt: int, cap: int):
        """Create new Container.

        Args:
            amt (int): Amount currently in container.
            cap (int): Capacity of container.
        """
        self.amt = amt
        self.cap = cap

    def __str__(self) -> str:
        return f"Container[{self.amt} / {self.cap}]"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Container):
            return False
        return self.amt == __value.amt and self.cap == __value.cap

    def __hash__(self) -> int:
        return hash((self.amt, self.cap))

    def copy(self) -> "Container":
        return Container(amt=self.amt, cap=self.cap)

    @staticmethod
    def pour(
        from_c: "Container", to_c: "Container"
    ) -> Tuple["Container", "Container", int]:
        """Pour contents from one container into another. Copy both containers: does not modify either original container.

        Args:
            from_c (Container): Container from which to pour.
            to_c (Container): Container into which to pour.

        Returns:
            Tuple[Container, Container, int]: (new from container, new to container, amount poured).
        """
        from_c, to_c = from_c.copy(), to_c.copy()
        to_space = to_c.cap - to_c.amt
        pour_amt = min(from_c.amt, to_space)
        from_c.amt -= pour_amt
        to_c.amt += pour_amt
        return from_c, to_c, pour_amt


class Node:
    barrel: Container
    jug1: Container
    jug2: Container

    def __init__(self, barrel: Container, jug1: Container, jug2: Container):
        """Node state is determined by state of three containers.

        Args:
            barrel (Container): Original barrel.
            jug1 (Container): First container.
            jug2 (Container): Second container.
        """
        self.barrel = barrel
        self.jug1 = jug1
        self.jug2 = jug2

    @classmethod
    def from_tuple(cls, containers: Tuple[Container, Container, Container]) -> "Node":
        barrel, jug1, jug2 = containers
        return Node(barrel=barrel, jug1=jug1, jug2=jug2)

    def get_container_tuple(self) -> Tuple[Container, Container, Container]:
        return self.barrel, self.jug1, self.jug2

    def get_neighbors(self) -> List[Tuple["Node", MoveType, int]]:
        """Generate all reachable distinct states from this node.

        Returns:
            List[Tuple[Node, MoveType, int]]: List of (neighbor, move_type to reach, amt_poured to reach) tuples.
        """
        neighbors: List[Tuple["Node", MoveType]] = []
        container_list = list(self.get_container_tuple())
        move_type_dict = MoveType.get_from_to_dict()
        for move_type, (from_idx, to_idx) in move_type_dict.items():
            from_c = container_list[from_idx]
            if to_idx == DISCARD_IDX:
                # dummy container to discard into
                to_c = Container(0, from_c.cap)
            else:
                to_c = container_list[to_idx]

            new_from_c, new_to_c, amt_poured = Container.pour(from_c=from_c, to_c=to_c)
            if amt_poured > 0:
                # create new node, updating containers at from/to indices
                new_container_list = container_list.copy()
                new_container_list[from_idx] = new_from_c
                if to_idx != DISCARD_IDX:
                    new_container_list[to_idx] = new_to_c
                neighbors.append(
                    (
                        Node.from_tuple(containers=tuple(new_container_list)),
                        move_type,
                        amt_poured,
                    )
                )

        return neighbors

    def __str__(self) -> str:
        return f"Node[barrel={self.barrel}, jug1={self.jug1}, jug2={self.jug2}]"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Node):
            return False
        return self.get_container_tuple() == __value.get_container_tuple()

    def __hash__(self) -> int:
        return hash((self.barrel, self.jug1, self.jug2))


def reconstruct_path(
    pred: Dict[Node, Tuple[Node, MoveType, int]], end_node: Node
) -> List[Tuple[Node, MoveType, int]]:
    """Generate path from search result predecessor dict, given as a list of states and the move taken to reach each state.

    Args:
        pred (Dict[Node, Tuple[Node, MoveType, int]]): Predecessor dict from graph search.
        end_node (Node): Terminating node from search.

    Returns:
        List[Tuple[Node, MoveType, int]]: List of (state, move type to reach state, amt_poured to reach state) tuples.
    """
    path = []
    while end_node in pred and pred[end_node] is not None:
        prev_node, move_type, amt_poured = pred[end_node]
        path = [(end_node, move_type, amt_poured)] + path
        end_node = prev_node
    path = [(end_node, None, 0)] + path
    return path


def search(
    initial_state: Node, is_target: Callable[[Node], bool]
) -> List[Tuple[Node, MoveType, int]]:
    """BFS from initial state to find shortest path to state satisfying `is_target` condition.
    Path generated using `reconstruct_path()`.

    @see `reconstruct_path()`

    Args:
        initial_state (Node): Initial state.
        is_target (Callable[[Node], bool]): Callback for search terminating condition.

    Returns:
        List[Tuple[Node, MoveType, int]]: Shortest path to state satisfying `is_target`, or `[]` if none exists.
    """
    q: "Queue[Node]" = Queue(-1)
    q.put(initial_state)
    pred: Dict[Node, Tuple[Node, MoveType, int]] = {initial_state: None}
    while not q.empty():
        node = q.get()
        if is_target(node):
            print(f"found {node} (visited {len(pred)})")
            return reconstruct_path(pred=pred, end_node=node)

        neighbors = node.get_neighbors()
        for neighbor_node, move_type, amt_poured in neighbors:
            # print(neighbor_node)
            if neighbor_node in pred:
                continue
            pred[neighbor_node] = (node, move_type, amt_poured)
            q.put(neighbor_node)

    print(f"not found (visited {len(pred)})")
    return []


initial_state = Node(Container(120, 120), Container(0, 5), Container(0, 7))
path = search(
    initial_state=initial_state,
    is_target=lambda node: node.jug1.amt == 1 and node.jug2.amt == 1,
)

path = list(
    map(
        lambda step: (
            step[0],
            step[1].name if step[1] is not None else "START",
            step[2],
        ),
        path,
    )
)
for node, move_type, amt_poured in path:
    print(f"{move_type}: pour {amt_poured} -> {node}")
print(f"num steps: {len(path) - 1}")
