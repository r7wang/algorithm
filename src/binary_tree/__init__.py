from collections import deque
from typing import Optional, Deque


class Node:
    def __init__(self, val: int, left: 'Node' = None, right: 'Node' = None):
        self.val = val
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.val)


def build() -> Node:
    return Node(
        5,
        left=Node(
            3,
            left=Node(
                1,
                right=Node(2)),
            right=Node(4),
        ),
        right=Node(
            9,
            left=Node(6),
            right=Node(11),
        ),
    )


def df_pre_order(node: Node) -> None:
    """Uses pre-order traversal to traverse a tree"""

    print('In {}'.format(node))
    for child in [node.left, node.right]:
        if not child:
            continue
        df_pre_order(child)


def df_in_order(node: Node) -> None:
    """Uses in-order traversal to traverse a tree"""

    if node.left:
        df_in_order(node.left)
    print('In {}'.format(node))
    if node.right:
        df_in_order(node.right)


def df_post_order(node: Node) -> None:
    """Uses post-order traversal to traverse a tree"""

    for child in [node.left, node.right]:
        if not child:
            continue
        df_post_order(child)
    print('In {}'.format(node))


def bf(node: Node) -> None:
    """Uses breadth-first traversal to traverse a tree"""
    queue = deque([node])
    while queue:
        _bf(queue.popleft(), queue)


def _bf(node: Node, queue: Deque) -> None:
    print('In {}, queue={}'.format(node, ','.join(map(str, queue))))
    for child in [node.left, node.right]:
        if child:
            queue.append(child)


def find_df(val: int, node: Node) -> Optional[Node]:
    """Finds a node by value given a root, using depth-first traversal"""

    print('In {}'.format(node))
    if node.val == val:
        return node
    for child in [node.left, node.right]:
        if not child:
            continue

        result = find_df(val, child)
        if result:
            return result
    return None


def find_bf(val: int, root: Node) -> Optional[Node]:
    """Finds a node by value given a root, using breadth-first traversal"""
    queue = deque([root])
    while queue:
        result = _find_bf(val, queue.popleft(), queue)
        if result:
            return result


def _find_bf(val: int, node: Node, queue: Deque) -> Optional[Node]:
    print('In {}, queue={}'.format(node, ','.join(map(str, queue))))
    if node.val == val:
        return node
    for child in [node.left, node.right]:
        if child:
            queue.append(child)
    return None
