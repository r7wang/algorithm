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
"""
