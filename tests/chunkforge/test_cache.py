from chunkforge.cache import SlabCache
from tests.chunkforge.conftest import NOW


def test_second_read_is_a_hit(filled):
    cache = SlabCache(filled)
    ref = filled.ref("p1", NOW)
    assert cache.get(ref, "a", NOW) == b"v1-a"
    assert cache.get(ref, "a", NOW) == b"v1-a"
    assert (cache.hits, cache.misses) == (1, 1)


def test_expired_reference_is_not_served(filled):
    cache = SlabCache(filled)
    assert cache.get(filled.ref("p1", NOW, ttl=1.0), "a", NOW + 2.0) is None


def test_invalidate_only_drops_that_pack(filled):
    filled.append("p2", "a", b"other")
    cache = SlabCache(filled)
    cache.get(filled.ref("p1", NOW), "a", NOW)
    cache.get(filled.ref("p2", NOW), "a", NOW)
    assert cache.invalidate("p1") == 1
    assert cache.get(filled.ref("p2", NOW), "a", NOW) == b"other"
