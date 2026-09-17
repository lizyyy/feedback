"""Cross-run duplicate detection.

Every built document appends its signature to ``dedup.jsonl``.  A later run that computes
the same signature skips the document instead of rebuilding and re-uploading it, so the
signature has to survive process restarts.
"""

from __future__ import annotations

import json
from pathlib import Path

WANTED = {"title", "source", "lang", "toctree_parent"}


def payload(meta: dict[str, object]) -> dict[str, object]:
    """Reduce document metadata to the fields that make a document unique."""
    return {key: meta[key] for key in meta.keys() & WANTED}


def signature(meta: dict[str, object]) -> str:
    """Signature used to recognise a document that was already built."""
    return json.dumps(payload(meta), ensure_ascii=False, default=str)


def append(path: str | Path, meta: dict[str, object]) -> str:
    sig = signature(meta)
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(sig + "\n")
    return sig


def seen(path: str | Path, meta: dict[str, object]) -> bool:
    p = Path(path)
    if not p.exists():
        return False
    return signature(meta) in set(p.read_text(encoding="utf-8").splitlines())
