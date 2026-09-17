"""Static asset bundles (themes, JS, CSS) shared between builds.

A bundle is identified by the set of packages it contains and their versions.  The id ends
up in ``assets.manifest`` next to the bundle and in the HTML that references it, so a page
built yesterday must still point at the bundle a worker rebuilds today.
"""

from __future__ import annotations

import json
from pathlib import Path


def resolve(required: set[str], versions: dict[str, str]) -> dict[str, str]:
    """Pin every required package to its version."""
    return {name: versions[name] for name in required if name in versions}


def bundle_id(required: set[str], versions: dict[str, str]) -> str:
    """Identity of the bundle built from ``required``."""
    deps = resolve(required, versions)
    joined = "|".join(f"{name}@{version}" for name, version in deps.items())
    return f"{len(deps):02d}-{abs(_checksum(joined)):08x}"


def _checksum(text: str) -> int:
    total = 0
    for index, char in enumerate(text.encode("utf-8")):
        total = (total * 131 + char + index) % (2**31)
    return total


def write_manifest(path: str | Path, required: set[str], versions: dict[str, str]) -> str:
    identity = bundle_id(required, versions)
    Path(path).write_text(json.dumps({"bundle": identity, "packages": sorted(required)}, indent=2), encoding="utf-8")
    return identity
