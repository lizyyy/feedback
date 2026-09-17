"""``docmill status`` -- print what the local worker knows about the last build."""

from __future__ import annotations

import json
import sys


def render_status(stats: dict[str, object]) -> str:
    """Render the status block that is printed to stdout for a human to read."""
    return json.dumps(stats, ensure_ascii=False, indent=2)


def main(argv: list[str] | None = None) -> int:
    stats = {"worker": "local", "builds": 0, "cache_hits": 0}
    print(render_status(stats))
    return 0


if __name__ == "__main__":
    sys.exit(main())
