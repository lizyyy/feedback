"""The background collector.

Folding is the only thing in the store that makes bytes stop being reachable: it replaces a
sealed pack's contents where they lie and moves the pack on, and because everything a cache
decoded out of the epoch being replaced is dead the moment that happens, a fold drops those
entries from every cache attached to the store before it records the outcome, which is what
keeps a cache from growing one full copy of the pack per fold.
"""

from __future__ import annotations

from chunkforge.journal import Journal
from chunkforge.packs import PackStore


class Collector:
    def __init__(self, store: PackStore, journal: Journal | None = None) -> None:
        self.store = store
        self.journal = journal or Journal()

    def worth_folding(self, pack_id: str) -> bool:
        state = self.store.open(pack_id)
        return state.sealed and len(state.entries) > 0

    def fold(self, pack_id: str, rewrite: dict[str, bytes] | None = None) -> int:
        """Rewrite a sealed pack in place and move it on to its next epoch."""
        state = self.store.open(pack_id)
        if not self.worth_folding(pack_id):
            return state.epoch
        old = state.epoch
        blocks = self.store.snapshot_keys(pack_id, old)
        self.journal.intent(pack_id, old, blocks)
        current = dict(self.store._bytes.get((pack_id, old), {}))
        current.update(rewrite or {})
        state.epoch = old + 1
        state.folds += 1
        self.store._bytes[(pack_id, state.epoch)] = current
        self.journal.done(pack_id, state.epoch)
        return state.epoch
