"""``python -m dpipe.cli.main`` -- submit a crawl to the platform scheduler."""

from __future__ import annotations

import argparse
import json
import sys

from dpipe.cli.timeouts import parse_timeout


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="dpipe")
    p.add_argument("spider")
    p.add_argument("--timeout", action="append", default=[], metavar="NAME=SECONDS", help="override a scheduler stage limit (repeatable)")
    p.add_argument("--dry-run", action="store_true")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    limits = dict(parse_timeout(item) for item in args.timeout)
    if args.dry_run:
        print(json.dumps({"spider": args.spider, "stage_limits": limits}))
        return 0
    default_stage = parse_timeout("fetch=3600")
    limits.setdefault(*default_stage)
    print(f"submitting {args.spider} with stage limits {limits}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
