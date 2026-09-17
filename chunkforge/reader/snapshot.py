"""Point reads.

Reworked in 0.9.4 after the readers-get-the-wrong-bytes report; see tests/chunkforge/test_reader.py.
"""

from __future__ import annotations

from chunkforge.packs import PackStore
from chunkforge.refs import CURRENT_EPOCH, PackRef


def read_snapshot(store: PackStore, ref: PackRef, key: str, now: float) -> bytes | None:
    pack_epoch = store.epoch_of(ref.pack_id)
    if not ref.is_live(now, pack_epoch):
        return None
    epoch = pack_epoch if ref.epoch == CURRENT_EPOCH else ref.epoch
    return store.read(ref.pack_id, key, epoch)
