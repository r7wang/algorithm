"""
https://medium.com/hackernoon/google-interview-questions-deconstructed-the-knights-dialer-f780d516f029
    * there are a max of 3 neighbors for any given node
    * the num of combinations for n hops is equal to the sum of the number of combinations for (n-1) hops for all
      of its neighbors
    * we don't know which node we're going to traverse, so it probably makes sense to precalculate results for all
      nodes for a given hop (n-1) before we move to calculating results for hop n

    Sample:
        result = solve(num_hops=150, node=3)
"""
from typing import List, Dict, Optional

adj_graph = {
    0: [4, 6],
    1: [6, 8],
    2: [7, 9],
    3: [4, 8],
    4: [0, 3, 9],
    5: [],
    6: [0, 1, 7],
    7: [2, 6],
    8: [1, 3],
    9: [2, 4],
}


def _get_neighbors(node: int) -> List:
    return adj_graph[node]


def _validate_node(node: int) -> bool:
    return 0 <= node <= 9


def solve(num_hops: int, node: int) -> Optional[int]:
    if not _validate_node(node):
        return None

    return solve_dp(num_hops, node)


def solve_dp(num_hops: int, node: int) -> int:
    results = {}
    for hop in range(1, num_hops + 1):
        _dp_solve_hop(results, hop)

    return results[node]


def _dp_solve_hop(results: Dict, hop: int):
    if hop < 1:
        return

    old_results = results.copy()
    results.clear()
    for node in range(0, 10):
        if hop == 1:
            results[node] = len(adj_graph[node])
        else:
            result = 0
            for neighbor in _get_neighbors(node):
                result += old_results[neighbor]
            results[node] = result


def solve_memo(num_hops: int, node: int) -> int:
    results = {}
    for hop in range(1, num_hops + 1):
        _memo_solve_hop(results, hop)

    return results[(num_hops, node)]


def _memo_solve_hop(results: Dict, hop: int):
    if hop < 1:
        return

    for node in range(0, 10):
        if hop == 1:
            results[(hop, node)] = len(adj_graph[node])
        else:
            result = 0
            for neighbor in _get_neighbors(node):
                result += results[(hop - 1, neighbor)]
            results[(hop, node)] = result
