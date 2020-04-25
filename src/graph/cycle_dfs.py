from typing import List, Set, Optional

adj_graph_with_cycle = {
    0: [1, 7],
    1: [0, 2, 7],
    2: [1, 8],
    6: [7, 8],
    7: [0, 1, 6, 8],
    8: [2, 6, 7],
}

adj_graph_no_cycle = {
    0: [1],
    1: [0, 2],
    2: [1, 8],
    6: [7, 8],
    7: [6],
    8: [2, 6],
}


def _get_neighbors(node: int) -> List:
    return adj_graph_with_cycle[node]


def solve() -> bool:
    """
    Detect cycles by searching and making sure that all neighbors are either the last visited node or not yet visited
    """
    visited = set()
    start_node = 0
    return _has_cycle(visited, from_node=None, node=start_node)


def _has_cycle(visited: Set, from_node: Optional[int], node: int) -> bool:
    if node in visited:
        print('Has cycle = True, node {} already visited'.format(node))
        return True
    visited.add(node)
    print('Has cycle = False, visiting node {}'.format(node))

    neighbors = _get_neighbors(node)
    for neighbor in neighbors:
        if neighbor == from_node:
            continue

        if _has_cycle(visited, node, neighbor):
            return True

    return False
