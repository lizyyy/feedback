from chunkforge.api import pack_health, ref_payload
from tests.chunkforge.conftest import NOW


def test_payload_carries_the_pack_and_deadline(filled):
    body = ref_payload(filled.ref("p1", NOW))
    assert body["pack_id"] == "p1" and body["expires_at"] > NOW


def test_payload_overrides_win(filled):
    assert ref_payload(filled.ref("p1", NOW), origin="edge-1")["origin"] == "edge-1"


def test_health_counts_packs_and_folds(filled, collector):
    collector.fold("p1")
    assert pack_health(filled) == {"packs": 1, "sealed": 1, "folds": 1, "caches": 0}


def test_health_counts_attached_caches(filled, collector):
    from chunkforge.cache import SlabCache

    SlabCache(filled)
    assert pack_health(filled)["caches"] == 1
