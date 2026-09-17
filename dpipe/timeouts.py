"""Timeout specs for dpipe components.

A *timeout spec* is either a number of seconds (``int`` / ``float``) or a string with an
optional unit suffix: ``"30"``, ``"30s"``, ``"500ms"``, ``"2m"``, ``"1h"``.

.. versionchanged:: 2.0
   :func:`parse_timeout` returns a :class:`Timeout` value object instead of a bare
   ``float`` and raises :class:`TimeoutSpecError` for missing/invalid specs (the old
   ``default=`` argument is gone: decide the fallback at the call site).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

__all__ = ["Timeout", "TimeoutSpecError", "parse_timeout"]


class TimeoutSpecError(ValueError):
    """Raised when a timeout spec is missing, malformed or negative."""


_UNITS = {"ms": 0.001, "s": 1.0, "m": 60.0, "h": 3600.0}
_SPEC_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*(ms|s|m|h)?\s*$")


@dataclass(frozen=True)
class Timeout:
    """A parsed timeout: ``seconds`` plus the original spec for logging."""

    seconds: float
    source: str = ""

    def deadline_from(self, now: float) -> float:
        """Absolute deadline (epoch seconds) if the clock reads ``now``."""
        return now + self.seconds

    def __str__(self) -> str:
        return f"{self.seconds:g}s"


def parse_timeout(value: object) -> Timeout:
    """Parse ``value`` into a :class:`Timeout`.

    Accepts a :class:`Timeout` (returned as-is), a non-negative number of seconds, or a
    spec string with an optional unit.  Anything else -- including ``None`` and the
    empty string -- raises :class:`TimeoutSpecError`.
    """
    if isinstance(value, Timeout):
        return value
    if value is None or isinstance(value, bool):
        raise TimeoutSpecError(f"invalid timeout spec: {value!r}")
    if isinstance(value, (int, float)):
        if value < 0:
            raise TimeoutSpecError(f"negative timeout: {value!r}")
        return Timeout(float(value), source=repr(value))
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="replace")
    if isinstance(value, str):
        m = _SPEC_RE.match(value)
        if not m:
            raise TimeoutSpecError(f"invalid timeout spec: {value!r}")
        number, unit = m.groups()
        return Timeout(float(number) * _UNITS[unit or "s"], source=value.strip())
    raise TimeoutSpecError(f"invalid timeout spec: {value!r}")
