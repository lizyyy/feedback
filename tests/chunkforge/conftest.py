import pytest

from chunkforge.collector import Collector
from chunkforge.packs import PackStore

NOW = 1_000.0


@pytest.fixture
def store():
    return PackStore()


@pytest.fixture
def collector(store):
    return Collector(store)


@pytest.fixture
def filled(store):
    """A sealed pack with two entries."""
    store.append("p1", "a", b"v1-a")
    store.append("p1", "b", b"v1-b")
    store.seal("p1")
    return store
