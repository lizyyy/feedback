from docmill.index.shards import shard_for, shard_key


def test_shard_is_within_range():
    for doc in ("index", "guide/install", "api/ref"):
        assert 0 <= shard_for(doc, {"public"}, 8) < 8


def test_shard_key_contains_the_doc_id():
    assert shard_key("guide/install", {"public"}).startswith("guide/install::")


def test_documents_with_different_labels_may_differ():
    keys = {shard_key("index", {"public"}), shard_key("index", {"internal"})}
    assert len(keys) == 2
