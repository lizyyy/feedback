from chunkforge.replica import Roster, decode_ref, encode_ref
from tests.chunkforge.conftest import NOW


def test_encode_marks_the_destination(filled):
    body = encode_ref(filled.ref("p1", NOW), "replica-2")
    assert body["origin"] == "replica-2" and body["pack_id"] == "p1"


def test_round_trip_keeps_the_pack_and_the_deadline(filled):
    ref = filled.ref("p1", NOW)
    back = decode_ref(encode_ref(ref, "replica-2"))
    assert back.pack_id == ref.pack_id and back.expires_at == ref.expires_at


def test_roster_is_stable_and_ignores_the_epoch(filled):
    roster = Roster(["h1", "h2", "h3"])
    ref = filled.ref("p1", NOW)
    assert roster.host_for(ref) == roster.host_for(ref.at(ref.epoch + 5))
