"""Digest of a build result.

The digest is stored with the build record and compared against the previous run to decide
whether the downstream publish step has to run at all.
"""

from __future__ import annotations

import hashlib


def changed_docs_digest(dirty: set[str]) -> str:
    """Digest of the set of documents that changed in this build."""
    return hashlib.sha256(str(dirty).encode("utf-8")).hexdigest()[:16]


def build_record(build_id: str, dirty: set[str]) -> dict[str, str]:
    return {"build": build_id, "changed": changed_docs_digest(dirty), "count": str(len(dirty))}
