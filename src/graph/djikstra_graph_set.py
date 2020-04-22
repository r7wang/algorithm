from typing import Set

from src.graph.common import Graph, DjikstraGraphNode as Node, MAX_DIST


def build() -> Graph:
    return Graph(
        Node,
        [
            ('0,0', '1,0', 5),
            ('1,0', '2,0', 3),
            ('0,1', '1,1', 10),
            ('1,1', '2,1', 4),
            ('0,2', '1,2', 9),
            ('1,2', '2,2', 10),
            ('0,0', '0,1', 10),
            ('0,1', '0,2', 10),
            ('1,0', '1,1', 9),
            ('1,1', '1,2', 1),
            ('2,0', '2,1', 1),
            ('2,1', '2,2', 8),
        ],
    )


def find_path(graph: Graph, start_name: str = '0,0', end_name: str = '2,2'):
    """Run Djikstra's algorithm, starting from start node

    Heuristic to pick the best path is by finding the unvisited node of lowest path length.

    Sample:
        from src.graph import djikstra_graph_set as alg

        graph = alg.build()
        alg.find_path(graph)
    """

    start_node = graph.get_node(start_name)
    start_node.path_length = 0
    end_node = graph.get_node(end_name)

    unvisited = set(graph.get_nodes())
    visited = set()

    while True:
        if end_node in visited:
            print('Success: length is {}'.format(end_node.path_length))
            return

        current = _min_path_length_node(unvisited)
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
                print('Setting {} path_length to {}'.format(neighbor_name, new_path_length))
            else:
                print('Skipping {} path_length update to {}'.format(neighbor, new_path_length))
        visited.add(current)


def _min_path_length_node(nodes: Set[Node]) -> Node:
    min_node = None
    for node in nodes:
        if not min_node:
            min_node = node
            continue

        if node.path_length < min_node.path_length:
            min_node = node

    return min_node
