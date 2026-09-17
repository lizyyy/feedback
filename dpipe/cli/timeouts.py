"""Argument helpers for the ``dpipe`` command line.

Nothing here is related to :mod:`dpipe.timeouts`: the CLI takes ``--timeout NAME=SECONDS``
pairs used to override per-stage limits of the *platform scheduler*, not Scrapy settings.
"""

from __future__ import annotations


def parse_timeout(text: str) -> tuple[str, float]:
    """Parse one ``NAME=SECONDS`` argument into ``(name, seconds)``."""
    name, sep, seconds = text.partition("=")
    if not sep or not name.strip():
        raise SystemExit(f"--timeout expects NAME=SECONDS, got {text!r}")
    try:
        value = float(seconds)
    except ValueError:
        raise SystemExit(f"--timeout {text!r}: seconds must be a number") from None
    if value < 0:
        raise SystemExit(f"--timeout {text!r}: seconds must be >= 0")
    return name.strip(), value
