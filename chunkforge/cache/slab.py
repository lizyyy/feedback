"""Decoded payloads held in front of the pack store."""

from __future__ import annotations

from chunkforge.packs import PackStore
from chunkforge.refs import PackRef


class SlabCache:
    def __init__(self, store: PackStore) -> None:
        self.store = store
        self._slabs: dict[tuple, bytes] = {}
        self.hits = 0
        self.misses = 0
        store.attach_cache(self)

    def key_for(self, ref: PackRef, key: str) -> tuple:
        return (ref.pack_id, key)

    def get(self, ref: PackRef, key: str, now: float) -> bytes | None:
        if now >= ref.expires_at:
            return None
        slot = self.key_for(ref, key)
        if slot in self._slabs:
            self.hits += 1
            return self._slabs[slot]
        self.misses += 1
        epoch = ref.epoch if ref.pinned() else self.store.epoch_of(ref.pack_id)
        payload = self.store.read(ref.pack_id, key, epoch)
        if payload is not None:
            self._slabs[slot] = payload
        return payload

    def invalidate(self, pack_id: str) -> int:
        dropped = [slot for slot in self._slabs if slot[0] == pack_id]
        for slot in dropped:
            del self._slabs[slot]
        return len(dropped)
