from typing import Dict, Set, Optional, List

from src.graph.common import Graph, PrimNode as Node, MAX_DIST


def build():
    return Graph(
        Node,
        [
            ('0', '1', 4),
            ('0', '7', 8),
            ('1', '7', 11),
            ('1', '2', 8),
            ('7', '8', 7),
            ('7', '6', 1),
            ('2', '8', 2),
            ('8', '6', 6),
            ('2', '3', 7),
            ('2', '5', 4),
            ('6', '5', 2),
            ('3', '5', 14),
            ('3', '4', 9),
            ('5', '4', 10),
            ('9', '10', 1),  # 9, 10 disconnected from other nodes
        ],
    )


def solve_basic_node_non_recursive():
    graph = build()

    start_node_name = '0'
    node_dists = {}
    node_origins = {}
    for node in graph.get_nodes():
        node_dists[node.name] = MAX_DIST
        node_origins[node.name] = None
    node_dists[start_node_name] = 0
    node_origins[start_node_name] = None

    visited = set()
    while True:
        next_node_name = _get_next_node_name(node_dists, node_origins, visited)
        if not next_node_name:
            return

        for neighbor_name, neighbor_dist in graph.get_neighbors(next_node_name):
            if node_dists[neighbor_name] > neighbor_dist:
                node_dists[neighbor_name] = neighbor_dist
                node_origins[neighbor_name] = next_node_name
        visited.add(next_node_name)


def solve_extended_node_recursive():
    graph = build()
    all_nodes = graph.get_nodes()
    while all_nodes:
        visited_nodes = _solve_for_tree(graph, all_nodes)
        all_nodes = all_nodes.difference(visited_nodes)


def _solve_for_tree(graph: Graph, all_nodes: List) -> Set:
    start_node = next(iter(all_nodes))
    start_node.min_dist = 0
    visited = set()
    while True:
        next_node = _get_next_node(all_nodes, visited)
        if not next_node:
            return visited

        for neighbor, neighbor_dist in graph.get_neighbor_nodes(next_node.name):
            if neighbor.min_dist > neighbor_dist:
                neighbor.min_dist = neighbor_dist
                neighbor.parent = next_node
        visited.add(next_node)


def _get_next_node(all_nodes: List, visited: Set) -> Optional[Node]:
    not_visited = list(filter(lambda node: node not in visited, all_nodes))
    if not not_visited:
        return None

    next_node = min(not_visited, key=lambda node: node.min_dist)
    if next_node.min_dist == MAX_DIST:
        return None

    print('{} to {}'.format(next_node.parent.name if next_node.parent else None, next_node.name))
    return next_node


def _get_next_node_name(node_dists: Dict, node_origins: Dict, visited: Set) -> Optional[str]:
    not_visited = {k: v for (k, v) in node_dists.items() if k not in visited}
    if not not_visited:
        return None

    next_node_name = min(not_visited.keys(), key=lambda k: not_visited[k])
    if node_dists[next_node_name] == MAX_DIST:
        return None

    print('{} to {}'.format(node_origins[next_node_name], next_node_name))
    return next_node_name

