"""References into the pack store.

A reference names a pack and the moment its holder stops being entitled to it.  Packs grow
until a writer seals them and a sealed pack is a fold candidate; folding rewrites a pack
where it lies, so the bytes under a pack id are the bytes of whichever epoch that pack has
reached by then, a reference pinned to an epoch stands for that epoch's bytes for as long
as the store keeps them, and an unpinned one stands for the pack rather than for anything
that was in it.  Epochs only move forward.
"""

from __future__ import annotations

from dataclasses import dataclass, field

CURRENT_EPOCH = -1


@dataclass(frozen=True)
class PackRef:
    pack_id: str
    expires_at: float
    epoch: int = CURRENT_EPOCH
    origin: str = "local"

    def is_live(self, now: float, pack_epoch: int) -> bool:
        """Whether this reference still stands for what its holder asked for."""
        if now >= self.expires_at:
            return False
        if self.epoch == CURRENT_EPOCH:
            return True
        return 0 <= self.epoch <= pack_epoch

    def pinned(self) -> bool:
        return self.epoch != CURRENT_EPOCH

    def at(self, pack_epoch: int) -> "PackRef":
        return PackRef(self.pack_id, self.expires_at, pack_epoch, self.origin)


@dataclass
class PackState:
    pack_id: str
    epoch: int = 0
    sealed: bool = False
    folds: int = 0
    entries: list = field(default_factory=list)
