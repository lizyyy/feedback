from chunkforge.reader import read_snapshot, stream_entries
from tests.chunkforge.conftest import NOW


def test_read_snapshot_returns_the_payload(filled):
    ref = filled.ref("p1", NOW)
    assert read_snapshot(filled, ref, "a", NOW) == b"v1-a"


def test_read_snapshot_refuses_an_expired_reference(filled):
    ref = filled.ref("p1", NOW, ttl=1.0)
    assert read_snapshot(filled, ref, "a", NOW + 2.0) is None


def test_read_snapshot_holds_its_epoch_across_a_fold(filled, collector):
    ref = filled.ref("p1", NOW)
    collector.fold("p1", rewrite={"a": b"v2-a"})
    assert read_snapshot(filled, ref, "a", NOW) == b"v1-a"


def test_stream_yields_every_entry(filled):
    ref = filled.ref("p1", NOW)
    assert dict(stream_entries(filled, ref, NOW)) == {"a": b"v1-a", "b": b"v1-b"}


def test_stream_stops_once_the_reference_is_done(filled):
    ref = filled.ref("p1", NOW, ttl=1.0)
    assert list(stream_entries(filled, ref, NOW + 2.0)) == []
