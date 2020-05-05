"""
Merge k sorted linked lists and return it as one sorted list.

Example:
    Input:
        [
          1->4->5,
          1->3->4,
          2->6
        ]
    Output:
        1->1->2->3->4->4->5->6
"""
import heapq
from typing import List, Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class ListMinimumNode:
    def __init__(self, cur_node: ListNode):
        self.cur_node = cur_node

    def __lt__(self, other: 'ListMinimumNode'):
        return self.cur_node.val < other.cur_node.val


def merge_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    if not lists:
        return None

    # Build a heap that always contains the next node in all lists.
    min_nodes_heap = []
    for list_idx in range(len(lists)):
        list_node = lists[list_idx]
        if list_node:
            heapq.heappush(min_nodes_heap, ListMinimumNode(list_node))

    # At this stage, start nodes has already been moved forward 1 step, and the min_nodes_heap has been populated with
    # data from all lists.
    first_node = None
    result = None
    while min_nodes_heap:
        min_node = heapq.heappop(min_nodes_heap)
        result_node = min_node.cur_node
        next_node = result_node.next
        if next_node:
            # There is another node after this, so add it back to the heap.
            heapq.heappush(min_nodes_heap, ListMinimumNode(next_node))

        # Get lowest node from heap and add to cumulative result. Wipe the next pointer because we want to reuse the
        # node in the result.
        result_node.next = None
        if not first_node:
            first_node = result_node
        else:
            result.next = result_node
        result = result_node

    return first_node
