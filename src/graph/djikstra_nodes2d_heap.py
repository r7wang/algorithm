import heapq
from typing import List, Set

from src.graph.common import DjikstraNeighborsNode as Node, MAX_DIST


def build() -> List[List[Node]]:
    nodes = _build_nxn_2d(3)

    _link(nodes[0][0], nodes[1][0], distance=5)
    _link(nodes[1][0], nodes[2][0], distance=3)
    _link(nodes[0][1], nodes[1][1], distance=10)
    _link(nodes[1][1], nodes[2][1], distance=4)
    _link(nodes[0][2], nodes[1][2], distance=9)
    _link(nodes[1][2], nodes[2][2], distance=10)

    _link(nodes[0][0], nodes[0][1], distance=10)
    _link(nodes[0][1], nodes[0][2], distance=10)
    _link(nodes[1][0], nodes[1][1], distance=9)
    _link(nodes[1][1], nodes[1][2], distance=1)
    _link(nodes[2][0], nodes[2][1], distance=1)
    _link(nodes[2][1], nodes[2][2], distance=8)

    return nodes


def _link(node_1: Node, node_2: Node, distance: int):
    node_1.neighbors[node_2] = distance
    node_2.neighbors[node_1] = distance


def _build_nxn_2d(size: int) -> List[List[Node]]:
    """Build 2d array of nodes, without any relationships"""
    nodes = []
    for i in range(0, size):
        nodes.append([])
    for x in range(0, size):
        for y in range(0, size):
            nodes[x].append(Node(name='{}-{}'.format(x, y)))
    return nodes


def find_path(nodes: List[List[Node]]):
    """Run Djikstra's algorithm, starting from start node

    Heuristic to pick the best path is by finding the unvisited node of lowest path length.

    Sample:
        from src.graph import djikstra_nodes2d_heap as alg

        nodes = alg.build()
        alg.find_path(nodes)
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
        # Using heappop to maintain the heap invariant -- O(log_n).
        current = heapq.heappop(unvisited)
        print('Visiting {}'.format(current.name))
        for neighbor in current.neighbors:
            if neighbor in visited:
                continue

            new_path_length = current.path_length + current.neighbors[neighbor]
            if neighbor.path_length > new_path_length:
                neighbor.path_length = new_path_length
                # If we want to keep track of the path, we have to track the parent relationship for every node.
                print('Setting {} path_length to {}'.format(neighbor.name, neighbor.path_length))
            else:
                print('Skipping {} path_length update to {}'.format(neighbor, new_path_length))
        visited.add(current)
        # Require heapify to maintain the heap invariant -- O(n_log_n).
        heapq.heapify(unvisited)


def _keep_going(unvisited: List, visited: Set, end_node: Node) -> bool:
    if end_node in visited:
        print('Success: length is {}'.format(end_node.path_length))
        return False

    if unvisited[0].path_length == MAX_DIST:
        print('Failed')
        return False

    return True
