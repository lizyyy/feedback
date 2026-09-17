"""The catalog maps user-visible names to the pack that currently holds them."""

from __future__ import annotations

from chunkforge.packs import DEFAULT_TTL, PackStore
from chunkforge.refs import PackRef


class Catalog:
    def __init__(self, store: PackStore) -> None:
        self.store = store
        self._by_name: dict[str, str] = {}

    def publish(self, name: str, pack_id: str) -> None:
        self._by_name[name] = pack_id

    def lookup(self, name: str, now: float, ttl: float = DEFAULT_TTL) -> PackRef | None:
        """Hand out a reference to whatever ``name`` points at."""
        pack_id = self._by_name.get(name)
        if pack_id is None:
            return None
        return PackRef(pack_id, now + ttl)

    def names(self) -> list[str]:
        return sorted(self._by_name)
