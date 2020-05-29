"""
A cache object can be instantiated in memory. It requires the max number of records as an argument:
cache = Cache.new(max_size: 100)

An object may be written to a string cache key:
cache.write("key", value)

That object may be retrieved by a key, or nil is returned if it is not found:
cache.read("key")

A cached value may be deleted by key:
cache.delete("key")

All values may be deleted:
cache.clear

The number of records can be fetched at any time:
Cache.count
"""
from collections import deque
from typing import Any, Optional, Dict, Deque


class CacheSizeInvalidError(ValueError):
    def __init__(self, max_size: int):
        self.max_size = max_size


class LruCache:
    """
    The LruCache does not support concurrent access.
    """

    def __init__(self, max_size: int):
        self._max_size = max_size
        if max_size <= 0:
            raise CacheSizeInvalidError(max_size)

        self._data: Dict[str, Any] = {}
        self._eviction_priority: Deque[str] = deque()

    def write(self, key: str, val: Any) -> Any:
        """Write a record to the cache.

        This will also set the key to the lowest priority for eviction from the cache. If we already have max_size
        records, then the least recently used record must be evicted.

        :param key: Key for record to be written.
        :param val: Value for the given key.
        :return: Value written to cache. If nothing was written to the cache, return None.
        """

        if key in self._data:
            # Shuffle eviction priority.
            self._deprioritize(key)
            self._data[key] = val
            return val

        if self.count() == self._max_size:
            next_eviction = self._eviction_priority.popleft()
            del self._data[next_eviction]

        self._eviction_priority.append(key)
        self._data[key] = val
        return val

    def read(self, key: str) -> Optional[Any]:
        """Read the record corresponding to the key.

        This will also deprioritize the key from being evicted from the cache.

        :param key: Key for record to be read.
        :return: The value for the given key. If the key does not exist, return None.
        """

        if key not in self._data:
            return None

        self._deprioritize(key)
        return self._data[key]

    def delete(self, key: str) -> Optional[Any]:
        """Delete the record corresponding to the key.

        :param key: Key for the record to be deleted.
        :return: The value that was deleted. If the key does not exist, return None.
        """

        if key not in self._data:
            return None

        cur_val = self._data[key]
        self._eviction_priority.remove(key)
        del self._data[key]
        return cur_val

    def clear(self) -> int:
        """Deletes all records in the cache.

        :return: Number of records that were deleted.
        """

        count = self.count()
        self._data.clear()
        self._eviction_priority.clear()
        return count

    def count(self) -> int:
        """Returns the number of records currently in the cache."""

        return len(self._data)

    def to_h(self) -> Dict[str, Any]:
        """Return the full data set in the cache.

        We should be careful that we don't give others the ability to modify the cache.
        """

        return dict(self._data)

    def _deprioritize(self, key: str):
        self._eviction_priority.remove(key)
        self._eviction_priority.append(key)
