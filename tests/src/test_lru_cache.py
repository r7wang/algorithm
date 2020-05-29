import pytest

from src.lru_cache import LruCache, CacheSizeInvalidError


class TestCreate:
    @pytest.mark.parametrize('max_size', [
        0,
        -3,
    ])
    def test_when_cache_size_lte_0_expect_exception(self, max_size: int):
        with pytest.raises(CacheSizeInvalidError):
            LruCache(max_size=max_size)


class TestCount:
    def test_when_empty_cache_expect_no_items(self):
        cache = LruCache(max_size=10)
        assert cache.count() == 0


class TestClear:
    def test_when_empty_cache_do_nothing(self):
        cache = LruCache(max_size=10)
        assert cache.clear() == 0
        assert cache.count() == 0


class TestRead:
    def test_tbd(self):
        # Write a key and read the key.
        # Write multiple keys and read specific key.
        # Overwrite a key and make sure it has the latest update.
        pass


class TestWrite:
    def test_when_written_returns_written_item(self):
        cache = LruCache(max_size=10)
        val = cache.write('a', 1)
        assert val == 1

    def test_when_exceeds_max_size_expect_eviction(self):
        cache = LruCache(max_size=2)
        cache.write('a', 1)
        cache.write('b', 2)
        cache.write('c', 4)

        assert cache.count() == 2
        assert cache.read('a') is None
        assert cache.read('b') == 2
        assert cache.read('c') == 4

    def test_when_multiple_writes_on_same_key_expect_no_eviction(self):
        cache = LruCache(max_size=2)
        cache.write('a', 1)
        cache.write('b', 2)
        cache.write('b', 4)
        cache.write('b', 6)

        assert cache.count() == 2
        assert cache.read('a') == 1
        assert cache.read('b') == 6

