"""The pack store itself."""

from __future__ import annotations

from chunkforge.refs import PackRef, PackState

DEFAULT_TTL = 3600.0


class PackStore:
    def __init__(self) -> None:
        self._packs: dict[str, PackState] = {}
        self._bytes: dict[tuple[str, int], dict[str, bytes]] = {}
        self.caches: list = []

    def attach_cache(self, cache) -> None:
        """Register a cache that decodes bytes out of this store."""
        self.caches.append(cache)

    # -- writing ---------------------------------------------------------------
    def open(self, pack_id: str) -> PackState:
        state = self._packs.setdefault(pack_id, PackState(pack_id))
        self._bytes.setdefault((pack_id, state.epoch), {})
        return state

    def append(self, pack_id: str, key: str, payload: bytes) -> None:
        state = self.open(pack_id)
        if state.sealed:
            raise ValueError(f"pack {pack_id} is sealed")
        state.entries.append(key)
        self._bytes[(pack_id, state.epoch)][key] = payload

    def seal(self, pack_id: str) -> None:
        self.open(pack_id).sealed = True

    # -- reading ---------------------------------------------------------------
    def epoch_of(self, pack_id: str) -> int:
        return self.open(pack_id).epoch

    def read(self, pack_id: str, key: str, epoch: int) -> bytes | None:
        return self._bytes.get((pack_id, epoch), {}).get(key)

    def ref(self, pack_id: str, now: float, ttl: float = DEFAULT_TTL) -> PackRef:
        """Take a reference to ``pack_id`` as it stands right now."""
        return PackRef(pack_id, now + ttl, self.epoch_of(pack_id))

    def snapshot_keys(self, pack_id: str, epoch: int) -> list[str]:
        return sorted(self._bytes.get((pack_id, epoch), {}))
