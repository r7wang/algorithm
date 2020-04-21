import heapq
from typing import List, Set

from src.graph import Node


def find_path(nodes: List[List[Node]]):
    """Run Djikstra's algorithm, starting from start node

    Heuristic to pick the best path is by finding the unvisited node of lowest path length.
    """
    start_node = nodes[0][0]
    start_node.path_length = 0
    end_node = nodes[2][2]

    unvisited = []
    for nodes_x in nodes:
        for node in nodes_x:
            heapq.heappush(unvisited, node)
    visited = set()

    while _keep_going(unvisited, visited, end_node):
        current = heapq.heappop(unvisited)
        print('Visiting {}'.format(current.name))
        for neighbor in current.neighbors:
            if neighbor not in visited:
                new_path_length = current.path_length + current.neighbors[neighbor]
                if neighbor.path_length > new_path_length:
                    neighbor.path_length = new_path_length
                    print('Setting {} path_length to {}'.format(neighbor.name, neighbor.path_length))
                else:
                    print('Skipping {} path_length update to {}'.format(neighbor, new_path_length))
        visited.add(current)
        heapq.heapify(unvisited)


def _keep_going(unvisited: List, visited: Set, end_node: Node) -> bool:
    if end_node in visited:
        # Success!
        print('Success: length is {}'.format(end_node.path_length))
        return False

    if unvisited[0].path_length == 9999:
        # Failure!
        print('Failed')
        return False

    return True
