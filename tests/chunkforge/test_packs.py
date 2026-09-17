import pytest

from tests.chunkforge.conftest import NOW


def test_append_then_read(store):
    store.append("p1", "a", b"x")
    assert store.read("p1", "a", store.epoch_of("p1")) == b"x"


def test_sealed_pack_refuses_appends(filled):
    with pytest.raises(ValueError):
        filled.append("p1", "c", b"y")


def test_snapshot_keys_are_sorted(filled):
    assert filled.snapshot_keys("p1", filled.epoch_of("p1")) == ["a", "b"]


def test_ref_carries_the_current_epoch(filled):
    ref = filled.ref("p1", NOW)
    assert ref.pack_id == "p1" and ref.epoch == filled.epoch_of("p1")
    assert ref.expires_at > NOW
