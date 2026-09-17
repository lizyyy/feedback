"""Handing references to the replicas."""

from __future__ import annotations

from dataclasses import asdict

from chunkforge.refs import PackRef

WIRE_FIELDS = ("pack_id", "expires_at", "origin")


def encode_ref(ref: PackRef, host: str) -> dict:
    """Serialise a reference for the replica on ``host``."""
    body = {k: v for k, v in asdict(ref).items() if k in WIRE_FIELDS}
    body["origin"] = host
    return body


def decode_ref(body: dict) -> PackRef:
    return PackRef(**{k: body[k] for k in body if k in PackRef.__dataclass_fields__})
