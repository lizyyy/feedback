"""What the HTTP layer hands back to callers."""

from __future__ import annotations

from dataclasses import asdict

from chunkforge.refs import CURRENT_EPOCH, PackRef

DEFAULTS = {"origin": "local", "epoch": CURRENT_EPOCH}


def ref_payload(ref: PackRef, **overrides) -> dict:
    """Render a reference as the JSON body the API returns."""
    body = asdict(ref)
    body.update({**DEFAULTS, **overrides})
    return body
