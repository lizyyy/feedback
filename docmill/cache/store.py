"""Layout of the shared artifact store."""

from __future__ import annotations

from pathlib import Path

from docmill.cache.envkey import build_env_key
from docmill.cache.fingerprint import source_fingerprint


def artifact_dir(root: str | Path, files: dict[str, bytes], env: dict[str, object]) -> Path:
    """Directory that holds the build artifact for these sources and settings."""
    return Path(root) / source_fingerprint(files) / build_env_key(env)


def lookup(root: str | Path, files: dict[str, bytes], env: dict[str, object]) -> Path | None:
    d = artifact_dir(root, files, env)
    return d if (d / "MANIFEST").exists() else None
