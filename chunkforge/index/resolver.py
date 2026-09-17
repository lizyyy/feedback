"""Reads against packs the writers are still appending to.

A pack that has not been sealed yet is not a fold candidate, so a reader of one wants the
bytes that are there when it looks rather than the bytes that were there when it asked.
"""

from __future__ import annotations

from chunkforge.packs import DEFAULT_TTL, PackStore
from chunkforge.refs import PackRef


def resolve_growing(store: PackStore, pack_id: str, now: float, ttl: float = DEFAULT_TTL) -> PackRef:
    if store.open(pack_id).sealed:
        raise ValueError(f"pack {pack_id} is sealed; take a reference through the catalog")
    return PackRef(pack_id, now + ttl)
