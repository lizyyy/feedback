"""Environment key: the part of the cache address that depends on build settings.

The key is appended to the fingerprint to form the artifact directory name, e.g.
``store/<fingerprint>/<env key>/``, so a worker only reuses an artifact that was produced
with the same settings.
"""

from __future__ import annotations

RELEVANT = ("builder", "language", "theme", "sphinx_version", "docmill_version")


def relevant_settings(env: dict[str, object]) -> dict[str, str]:
    """Pick the settings that influence the output out of a full build environment."""
    return {k: str(env[k]) for k in RELEVANT if k in env}


def build_env_key(env: dict[str, object]) -> str:
    """Return the environment key for ``env`` (a build settings mapping)."""
    settings = relevant_settings(env)
    return format(hash(frozenset(settings.items())) & 0xFFFFFFFFFFFF, "012x")
