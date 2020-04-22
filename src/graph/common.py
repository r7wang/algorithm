from typing import List, Type, Set

MAX_DIST = 9999


class DjikstraNeighborsNode:
    def __init__(self, name: str):
        self.name = name
        self.path_length = MAX_DIST
        self.neighbors = {}

    def __str__(self) -> str:
        return 'name={} path_len={}'.format(self.name, self.path_length)

    def __lt__(self, other):
        return self.path_length < other.path_length

    def __gt__(self, other):
        return self.path_length > other.path_length


class DjikstraGraphNode:
    def __init__(self, name: str):
        self.name = name
        self.path_length = MAX_DIST

    def __str__(self) -> str:
        return 'name={} path_len={}'.format(self.name, self.path_length)


class AStarNode:
    def __init__(self, name: str):
        xy_split = name.split(',')
        self.x = int(xy_split[0])
        self.y = int(xy_split[1])
        self.name = name
        self.path_length = MAX_DIST
        self.remaining_estimate = 0

    def get_best_cost(self) -> int:
        return self.path_length + self.remaining_estimate

    def set_remaining_estimate(self, end_node: 'AStarNode'):
        self.remaining_estimate = abs(end_node.x - self.x) + abs(end_node.y - self.y)

    def __str__(self) -> str:
        return 'name={} path_len={} rem_est={}'.format(self.name, self.path_length, self.remaining_estimate)


class Graph:
    """
    This implementation uses a centralized structure to store relationship between nodes, as opposed to storing the
    relationship between nodes within a node itself. It's easier for us to create a dataset that builds this centralized
    structure, given that there are no recursive dependencies. The graph depends on nodes. The nodes do not depend on
    each other.

    This pattern doesn't work as well when we actually need to store and update data on the nodes, such as in the case
    of Djikstra or A* search. We could probably extend it so that instead of returning weights,
    """

    def __init__(self, node_cls: Type, links: List):
        # Given some specification on graph direction, build a graph.
        self.node_cls = node_cls
        self.edges = {}

        for src, dest, weight in links:
            if src not in self.edges:
                self.edges[src] = {}
            self.edges[src][dest] = weight

            if dest not in self.edges:
                self.edges[dest] = {}
            self.edges[dest][src] = weight

        # Collect all of the names for which nodes need to be created.
        node_names = set()
        for src, dest, weight in links:
            node_names.add(src)
            node_names.add(dest)

        self.nodes = {}
        for node_name in node_names:
            self.nodes[node_name] = self.node_cls(node_name)

    def get_neighbors(self, name: str):
        return self.edges[name].items()

    def get_node(self, name: str):
        return self.nodes.get(name)

    def get_nodes(self) -> Set:
        return {node for node_name, node in self.nodes.items()}


# def link(node_1: Node, node_2: Node, distance: int):
#     node_1.neighbors[node_2] = distance
#     node_2.neighbors[node_1] = distance
#
#
# def build_nxn_1d(size: int) -> List[Node]:
#     """Build 1d array of nodes, without any relationships"""
#     nodes = []
#     for i in range(0, size * size):
#         nodes.append(Node(name=str(i)))
#     return nodes
#
#
# def build_nxn_2d(size: int) -> List[List[Node]]:
#     """Build 2d array of nodes, without any relationships"""
#     nodes = []
#     for i in range(0, size):
#         nodes.append([])
#     for x in range(0, size):
#         for y in range(0, size):
#             nodes[x].append(Node(name='{}-{}'.format(x, y)))
#     return nodes
#
#
# def build_nxn_1d_linked(size: int, distance_func: Callable[[], int] = lambda: 1) -> List[Node]:
#     """Build 1d array of nodes, with relationships, using given distance function
#
#     This works best for raw interconnected grids.
#     """
#     nodes = build_nxn_1d(size)
#     for x in range(0, size):
#         for y in range(0, size):
#             if x != size - 1:
#                 link(nodes[size * y + x], nodes[size * y + x + 1], distance_func())
#             if y != size - 1:
#                 link(nodes[size * y + x], nodes[size * (y + 1) + x], distance_func())
#     return nodes
#
#
# def build_nxn_2d_linked(size: int, distance_func: Callable[[], int] = lambda: 1) -> List[List[Node]]:
#     """Build 2d array of nodes, with relationships, using given distance function
#
#     This works best for raw interconnected grids.
#     """
#     nodes = build_nxn_2d(size)
#     for x in range(0, size):
#         for y in range(0, size):
#             if x != size - 1:
#                 link(nodes[x][y], nodes[x + 1][y], distance_func())
#             if y != size - 1:
#                 link(nodes[x][y], nodes[x][y + 1], distance_func())
#     return nodes
#
#
# def build_nxn_2d_linked_random_dist(size: int) -> List[List[Node]]:
#     """Build 2d array of nodes, with relationships, using random distance
#     """
#     return build_nxn_2d_linked(size, lambda: random.randint(1, 10))
#
#
# def print_1d(nodes: List[Node]):
#     for node in nodes:
#         neighbors = ', '.join(str(neighbor) for neighbor in node.neighbors)
#         print('name={}, neighbors={}'.format(node, neighbors))
#
#
# def print_2d(nodes: List[List[Node]]):
#     for nodes_x in nodes:
#         for node_xy in nodes_x:
#             neighbors = ', '.join(
#                 '({} d={})'.format(
#                     neighbor,
#                     node_xy.neighbors[neighbor],
#                 )
#                 for neighbor in node_xy.neighbors)
#             print('name={}, neighbors={}'.format(node_xy, neighbors))
