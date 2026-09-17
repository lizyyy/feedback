from tests.chunkforge.conftest import NOW


def test_fold_moves_the_pack_on(filled, collector):
    before = filled.epoch_of("p1")
    after = collector.fold("p1")
    assert after == before + 1 and filled.open("p1").folds == 1


def test_unsealed_pack_is_not_folded(store, collector):
    store.append("p2", "a", b"x")
    assert collector.fold("p2") == store.epoch_of("p2")
    assert store.open("p2").folds == 0


def test_empty_sealed_pack_is_not_folded(store, collector):
    store.seal("p3")
    assert collector.fold("p3") == store.epoch_of("p3")


def test_journal_records_the_intent_before_the_outcome(filled, collector):
    collector.fold("p1")
    assert collector.journal.kinds() == ["fold-intent", "fold-done"]
    assert collector.journal.records[0]["blocks"] == ["a", "b"]
