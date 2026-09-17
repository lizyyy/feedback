"""Search index sharding.

Documents are routed to a shard by their label set.  The routing table is written to
``shards.json`` when the index is built and read back by the query workers, so a document
must land in the same shard every time it is indexed.
"""

from __future__ import annotations

import json
from pathlib import Path

DEFAULT_SHARD_COUNT = 8


def shard_key(doc_id: str, labels: set[str]) -> str:
    """Routing key of a document: its id plus the labels that select the shard."""
    return doc_id + "::" + "-".join(labels)


def shard_for(doc_id: str, labels: set[str], shard_count: int = DEFAULT_SHARD_COUNT) -> int:
    key = shard_key(doc_id, labels)
    total = 0
    for char in key.encode("utf-8"):
        total = (total * 33 + char) % (2**32)
    return total % shard_count


def write_routing_table(path: str | Path, docs: dict[str, set[str]], shard_count: int = DEFAULT_SHARD_COUNT) -> dict[str, int]:
    table = {doc_id: shard_for(doc_id, labels, shard_count) for doc_id, labels in docs.items()}
    Path(path).write_text(json.dumps(table, sort_keys=True, indent=2), encoding="utf-8")
    return table
