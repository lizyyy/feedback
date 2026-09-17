"""Append-only record of what the collector intends to do and what it did.

Recovery replays the journal, so an intent has to name the blocks it covers before the
bytes move and the matching outcome has to land after them.
"""

from __future__ import annotations


class Journal:
    def __init__(self) -> None:
        self.records: list[dict] = []

    def intent(self, pack_id: str, epoch: int, blocks: list[str]) -> None:
        self.records.append({"kind": "fold-intent", "pack": pack_id, "epoch": epoch, "blocks": list(blocks)})

    def done(self, pack_id: str, epoch: int) -> None:
        self.records.append({"kind": "fold-done", "pack": pack_id, "epoch": epoch})

    def kinds(self) -> list[str]:
        return [r["kind"] for r in self.records]
