from src.heap import build

heap = build()

for _ in range(0, 2):
    item1 = heap.pop()
    item2 = heap.pop()
    print('Popped: item1={} item2={}'.format(item1, item2))
    diff = item1 - item2
    heap.insert(diff)
    print('Inserted: {}'.format(diff))
