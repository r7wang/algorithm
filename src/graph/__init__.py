import random
from typing import List


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
