# Graph problem
#   - First create the grid.
#       - x by y grid where all nodes are linked, can write an O(vertex) function to do this, taking into account edges
#       - manually define grid relationships
#       - from 2D array
#   - Run Djikstra's algorithm, starting from start node
#       - heuristic to pick the best path is by finding the unvisited node of lowest cost
#   - Run A* search with Euclidean distance, starting from source node
#       - heuristic must never overestimate, but can underestimate
#       - using priority queue
import heapq
import random
from typing import List, Dict, Set


class Node:
    def __init__(self, name: str):
        self.name = name
        self.path_length = 9999
        self.neighbors = {}

    def __str__(self) -> str:
        return 'name={} path_length={}'.format(self.name, self.path_length)

    def __lt__(self, other):
        return self.path_length < other.path_length

    def __gt__(self, other):
        return self.path_length > other.path_length


def link(node_1: Node, node_2: Node, distance: int):
    node_1.neighbors[node_2] = distance
    node_2.neighbors[node_1] = distance


def build_fixed() -> List[List[Node]]:
    nodes = build_nxn_2d(3)

    link(nodes[0][0], nodes[1][0], distance=5)
    link(nodes[1][0], nodes[2][0], distance=3)
    link(nodes[0][1], nodes[1][1], distance=10)
    link(nodes[1][1], nodes[2][1], distance=4)
    link(nodes[0][2], nodes[1][2], distance=9)
    link(nodes[1][2], nodes[2][2], distance=10)

    link(nodes[0][0], nodes[0][1], distance=10)
    link(nodes[0][1], nodes[0][2], distance=10)
    link(nodes[1][0], nodes[1][1], distance=9)
    link(nodes[1][1], nodes[1][2], distance=1)
    link(nodes[2][0], nodes[2][1], distance=1)
    link(nodes[2][1], nodes[2][2], distance=8)

    return nodes


def build_nxn_1d(size: int) -> List[Node]:
    nodes = []
    for i in range(0, size * size):
        nodes.append(Node(name=str(i)))
    return nodes


def build_nxn_2d(size: int) -> List[List[Node]]:
    nodes = []
    for i in range(0, size):
        nodes.append([])
    for x in range(0, size):
        for y in range(0, size):
            nodes[x].append(Node(name='{}-{}'.format(x, y)))
    return nodes


def build_nxn_1d_linked_default_dist(size: int, distance: int = 1) -> List[Node]:
    nodes = build_nxn_1d(size)
    for x in range(0, size):
        for y in range(0, size):
            if x != size - 1:
                link(nodes[size * y + x], nodes[size * y + x + 1], distance)
            if y != size - 1:
                link(nodes[size * y + x], nodes[size * (y + 1) + x], distance)
    return nodes


def build_nxn_2d_linked_default_dist(size: int, distance: int = 1) -> List[List[Node]]:
    nodes = build_nxn_2d(size)
    for x in range(0, size):
        for y in range(0, size):
            if x != size - 1:
                link(nodes[x][y], nodes[x + 1][y], distance)
            if y != size - 1:
                link(nodes[x][y], nodes[x][y + 1], distance)
    return nodes


def build_nxn_2d_linked_random_dist(size: int) -> List[List[Node]]:
    nodes = build_nxn_2d(size)
    for x in range(0, size):
        for y in range(0, size):
            if x != size - 1:
                link(nodes[x][y], nodes[x + 1][y], random.randint(1, 10))
            if y != size - 1:
                link(nodes[x][y], nodes[x][y + 1], random.randint(1, 10))
    return nodes


def print_1d(nodes: List[Node]):
    for node in nodes:
        neighbors = ', '.join(str(neighbor) for neighbor in node.neighbors)
        print('name={}, neighbors={}'.format(node, neighbors))


def print_2d(nodes: List[List[Node]]):
    for nodes_x in nodes:
        for node_xy in nodes_x:
            neighbors = ', '.join(
                '({} d={})'.format(
                    neighbor,
                    node_xy.neighbors[neighbor],
                )
                for neighbor in node_xy.neighbors)
            print('name={}, neighbors={}'.format(node_xy, neighbors))


def path_djikstra(nodes: List[List[Node]]):
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
