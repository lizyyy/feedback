"""docmill -- incremental build cache layer for the internal Sphinx branch.

The platform runs Sphinx builds in short-lived worker processes on a fleet of machines and
shares build artifacts through a content-addressed store.  Everything under ``docmill/``
decides *identity*: which artifact a build may reuse, which shard a document lands in and
which documents count as duplicates.
"""

from docmill.cache.fingerprint import source_fingerprint

__all__ = ["source_fingerprint"]
__version__ = "3.2.0.dev7"
