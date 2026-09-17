"""Bulk reads for the query layer."""

from __future__ import annotations

from typing import Iterator

from chunkforge.packs import PackStore
from chunkforge.refs import PackRef


def stream_entries(store: PackStore, ref: PackRef, now: float) -> Iterator[tuple[str, bytes]]:
    """Yield every entry the reference covers, cheapest path first."""
    if now >= ref.expires_at:
        return
    epoch = store.epoch_of(ref.pack_id)
    for key in store.snapshot_keys(ref.pack_id, epoch):
        payload = store.read(ref.pack_id, key, epoch)
        if payload is not None:
            yield key, payload
