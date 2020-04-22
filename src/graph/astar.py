from typing import Set

from src.graph.common import Graph, AStarNode as Node, MAX_DIST


def build() -> Graph:
    """
    * --- * --- * --- *
    |           |     |
    *           *     *
    |           |     |
    * --- * --- *     *
                      |
    * --- * --- * --- *
    """
    return Graph(
        Node,
        [
            ('0,0', '1,0', 1),
            ('1,0', '2,0', 1),
            ('0,0', '0,1', 1),
            ('0,1', '0,2', 1),
            ('0,2', '1,2', 1),
            ('1,2', '2,2', 1),
            ('2,0', '2,1', 1),
            ('2,1', '2,2', 1),
            ('2,0', '3,0', 1),
            ('3,0', '3,1', 1),
            ('3,1', '3,2', 1),
            ('3,2', '3,3', 1),
            ('3,3', '2,3', 1),
            ('2,3', '1,3', 1),
            ('1,3', '0,3', 1),
        ],
    )


def find_path(graph: Graph, start_name: str = '0,0', end_name: str = '0,3'):
    """Run A* search, starting from start node

    Heuristic is Manhattan distance. Heuristic must never overestimate, but can underestimate.

    Sample:
        from src.graph import astar as alg

        graph = alg.build()
        alg.find_path(graph)
    """

    start_node = graph.get_node(start_name)
    start_node.path_length = 0
    end_node = graph.get_node(end_name)

    # Works for static heuristics such as Manhattan distance.
    nodes = graph.get_nodes()
    for node in nodes:
        node.set_remaining_estimate(end_node)

    unvisited = set(nodes)
    visited = set()

    while True:
        if end_node in visited:
            print('Success: length is {}'.format(end_node.path_length))
            return

        current = _min_cost_node(unvisited)
        if current.path_length == MAX_DIST:
            print('Failed')
            return

        unvisited.remove(current)
        print('Visiting {}'.format(current.name))
        for neighbor_name, distance in graph.get_neighbors(current.name):
            neighbor = graph.get_node(neighbor_name)
            if neighbor in visited:
                continue

            new_path_length = current.path_length + distance
            if neighbor.path_length > new_path_length:
                neighbor.path_length = new_path_length
                print('Setting {} path_length to {}, best cost is {}'.format(
                    neighbor_name,
                    new_path_length,
                    neighbor.get_best_cost(),
                ))
            else:
                print('Skipping {} path_length update to {}'.format(neighbor, new_path_length))
        visited.add(current)


def _min_cost_node(nodes: Set[Node]) -> Node:
    min_node = None
    for node in nodes:
        if not min_node:
            min_node = node
            continue

        if node.get_best_cost() < min_node.get_best_cost():
            min_node = node

    return min_node
