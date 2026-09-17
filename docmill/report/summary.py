"""Human-readable build summary printed at the end of a run."""

from __future__ import annotations


def format_summary(dirty: set[str], warnings: list[str]) -> str:
    lines = [f"{len(dirty)} document(s) rebuilt"]
    for name in dirty:                      # display order does not matter here
        lines.append(f"  - {name}")
    if warnings:
        lines.append(f"{len(warnings)} warning(s)")
    return "\n".join(lines)
