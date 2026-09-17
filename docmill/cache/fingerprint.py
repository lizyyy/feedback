"""Content fingerprint of a source tree.

The fingerprint names the artifact directory in the shared store, so two workers that see
the same sources must compute the same value -- on different machines, in different
processes, in any order.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


def source_fingerprint(files: dict[str, bytes]) -> str:
    """Return the fingerprint of ``{relative path: contents}``."""
    h = hashlib.sha256()
    for name in sorted(files):
        h.update(name.encode("utf-8"))
        h.update(b"\0")
        h.update(hashlib.sha256(files[name]).digest())
    return h.hexdigest()[:32]


def fingerprint_tree(root: str | Path, suffixes: tuple[str, ...] = (".rst", ".md", ".py")) -> str:
    root = Path(root)
    files = {}
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in suffixes:
            files[str(path.relative_to(root))] = path.read_bytes()
    return source_fingerprint(files)
