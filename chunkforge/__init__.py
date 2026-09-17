"""chunkforge -- batched chunk staging for the internal zarr branch.

Writers stage chunks into packs instead of touching the store one chunk at a time; a
background collector later folds the packs it finds worth folding.  The store, the
replicas and the read paths all address data through :class:`chunkforge.refs.PackRef`.
"""

from chunkforge.refs import PackRef

__all__ = ["PackRef"]
__version__ = "0.9.4.dev2"
