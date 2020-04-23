"""
For more information on Python's heapq library, see the link below.
https://docs.python.org/3/library/heapq.html
"""
import math
from typing import List, Optional


class Heap:
    """
    Sample:
        from src.heap import build

        heap = build()

        for _ in range(0, 2):
            item1 = heap.pop()
            item2 = heap.pop()
            print('Popped: item1={} item2={}'.format(item1, item2))
            diff = item1 - item2
            heap.insert(diff)
            print('Inserted: {}'.format(diff))
    """

    def __init__(self, items: List):
        self.items = list(items)
        # print('Before heapify: {}'.format(self.items))
        self.max_heapify()
        # print('After heapify: {}'.format(self.items))

    def max_heapify(self) -> None:
        if not self.items:
            return

        self._max_heapify_all()

    def insert(self, item: int) -> None:
        self.items.append(item)
        self._max_sift_up(len(self.items) - 1)
        print(self.items)

        # # Can re-heapify, but this is pretty inefficient, because it involves traversing all nodes.
        # self._max_heapify_all()

    def pop(self) -> Optional[int]:
        if not self.items:
            return None

        result = self.items[0]
        self.items[0] = self.items[-1]
        del self.items[-1]
        self._max_sift_down(0)
        return result

    def _max_heapify_all(self) -> None:
        # Option 1: Try to sift down each item, always check for non-leaf during sift.
        for idx in range(len(self.items) - 1, -1, -1):
            self._max_sift_down(idx)

    def _max_heapify_approx(self) -> None:
        # Option 2: Approximate how many non-leaves exist, then try to sift down each item, but not all of these will
        #           be non-leaves, so we still have to check indices.
        exp = math.floor(math.log(len(self.items), 2))
        print(len(self.items), exp)
        num_non_leaf = int(math.pow(2, exp)) - 1
        for idx in range(num_non_leaf, -1, -1):
            self._max_sift_down(idx)

    def _max_sift_up(self, child_idx: int) -> None:
        # print('Sifting up: idx={} item={}'.format(child_idx, self.items[child_idx]))
        if child_idx == 0:
            return

        parent_idx = (child_idx - 1) // 2
        if self.items[parent_idx] < self.items[child_idx]:
            self._swap(parent_idx, child_idx)
            self._max_sift_up(parent_idx)

    def _max_sift_down(self, parent_idx: int) -> None:
        # print('Sifting down: idx={} item={}'.format(parent_idx, self.items[parent_idx]))
        left_idx = parent_idx * 2 + 1
        right_idx = parent_idx * 2 + 2
        largest_idx = parent_idx

        if left_idx < len(self.items) and self.items[left_idx] > self.items[largest_idx]:
            largest_idx = left_idx

        if right_idx < len(self.items) and self.items[right_idx] > self.items[largest_idx]:
            largest_idx = right_idx

        if largest_idx != parent_idx:
            self._swap(largest_idx, parent_idx)
            self._max_sift_down(largest_idx)

    def _max_sift_down_generic(self, parent_idx: int) -> None:
        # print('Sifting: idx={} item={}'.format(parent_idx, self.items[parent_idx]))
        children_idx = [parent_idx * 2 + 1, parent_idx * 2 + 2]
        children_idx = filter(lambda idx: idx < len(self.items), children_idx)
        children_idx = filter(lambda idx: self.items[idx] > self.items[parent_idx], children_idx)
        largest_idx = None
        for idx in children_idx:
            if not largest_idx:
                largest_idx = idx
                continue
            if self.items[idx] > self.items[largest_idx]:
                largest_idx = idx

        if largest_idx:
            self._swap(largest_idx, parent_idx)
            self._max_sift_down(largest_idx)

    def _swap(self, a: int, b: int):
        temp_val = self.items[a]
        self.items[a] = self.items[b]
        self.items[b] = temp_val
        # print('After swap: {}'.format(self.items))


def build() -> Heap:
    return Heap([2, 2, 3, 4, 5, 5, 6, 7, 8, 9, 9, 12, 13, 15, 16, 19, 23, 24, 29])
