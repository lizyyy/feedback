"""Operational counters."""

from __future__ import annotations

from chunkforge.packs import PackStore


def pack_health(store: PackStore) -> dict:
    packs = [store.open(pid) for pid in sorted(store._packs)]
    return {
        "packs": len(packs),
        "sealed": sum(1 for p in packs if p.sealed),
        "folds": sum(p.folds for p in packs),
        "caches": len(store.caches),
    }
