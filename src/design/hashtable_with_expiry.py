"""
How would you design a hash table with keys that can potentially expire?

Notes:
    * Very much like DynamoDB's TTL.

Goals:
    * We want something that is fast for access and fast for writes.
    * We want something that respects the time boundaries set.

Questions:
    * Do we want to support hash table updates? Does that extend the TTL?
    * Do we have any kind of transactional or concurrency semantics?

Solution: Array of LinkedLists
    * Do the keys expire on access or do the keys expire regularly? Perhaps a mix of both?
    * Do we need locks?
    * Array[
        Partition_0 -> LinkedList[ (1, v1, ex), (2, v2, ex), (3, v3, ex), ...]
        Partition_1 -> LinkedList[ (4, v4, ex), (5, v5, ex), (6, v6, ex), ...]
      ]
      NumItems: int
      NumPartitions: int
    * To access:
        * Hash key % (num partitions).
        * Index directly into partition linked list, then search for matching entry (or none).
        * If the entry is expired during the search, discard the entry right away by manipulating one pointer and
          freeing up some memory, up to a limit of n times per operation.
        * If there are too few items, scale down by removing some partitions.
    * To write:
        * Hash key % (num partitions).
        * Index directly into partition linked list, then put the item at the beginning.
        * If there are too many items, scale up by adding some partitions.
    * To synchronize:
        * Can't rebalance while anyone else is doing anything (need rebalancer RW lock in write mode).
        * We can fix TTL by moving one pointer, but there should only be one TTL fixer at a time.
        * Any writer needs a partition lock because they are creating an item and then prepending it and potentially
          colliding with any work TTL fixing is doing. They still need to synchronize with a rebalancer RW lock in read
          mode.
        * Any reader does not need a partition lock because they can ignore what the TTL fixer is doing as it cleans up
          silently. They still need to synchronize with a rebalancer RW lock in read mode.
    * Problems:
        * The hash table can stay very large if write operations suddenly drop off.
"""
