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


def find_df(val: int, node: Node) -> Optional[Node]:
    """Finds a node by value given a root, using pre-order traversal"""

    print('In {}'.format(node.val))
    if node.val == val:
        return node
    for child in [node.left, node.right]:
        if not child:
            continue

        result = find_df(val, child)
        if result:
            return result
    return None


def bf(val: int, root: Node) -> Optional[Node]:
    queue = deque([root])
    while queue:
        result = find_bf(val, queue.popleft(), queue)
        if result:
            return result


def find_bf(val: int, node: Node, queue: Deque) -> Optional[Node]:
    """Finds a node by value, using breadth-first traversal"""

    print('In {}, queue={}'.format(node.val, ','.join(map(str, queue))))
    if node.val == val:
        return node
    for child in [node.left, node.right]:
        # Push both left and right on a queue.
        if child:
            queue.append(child)
    return None
