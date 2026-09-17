import pytest

from chunkforge.index import Catalog, resolve_growing
from tests.chunkforge.conftest import NOW


def test_catalog_hands_out_a_reference(filled):
    catalog = Catalog(filled)
    catalog.publish("daily", "p1")
    ref = catalog.lookup("daily", NOW)
    assert ref is not None and ref.pack_id == "p1"


def test_catalog_misses_are_none(filled):
    assert Catalog(filled).lookup("nope", NOW) is None


def test_growing_pack_reference_follows_the_writer(store):
    store.append("p2", "a", b"one")
    ref = resolve_growing(store, "p2", NOW)
    store.append("p2", "b", b"two")
    assert store.snapshot_keys(ref.pack_id, store.epoch_of("p2")) == ["a", "b"]


def test_growing_resolver_refuses_a_sealed_pack(filled):
    with pytest.raises(ValueError):
        resolve_growing(filled, "p1", NOW)
