# docmill

Incremental build cache for the internal Sphinx branch. Builds run in short-lived worker
processes on a fleet of machines; artifacts, search shards and the duplicate registry are
shared between them through the store at `DOCMILL_STORE`.

| Module | Decides |
|---|---|
| `docmill.cache.fingerprint` | artifact address from the source contents |
| `docmill.cache.envkey` | artifact address from the build settings |
| `docmill.cache.store` | store layout and lookup |
| `docmill.assets.bundler` | identity of a shared asset bundle (`assets.manifest`) |
| `docmill.index.shards` | which search shard a document is routed to (`shards.json`) |
| `docmill.dedup.registry` | whether a document was already built in an earlier run (`dedup.jsonl`) |
| `docmill.report.digest` | whether the publish step has to run again |
| `docmill.report.summary` | end-of-run summary printed to the console |
| `docmill.util.memo` | in-process memoisation of pure helpers |
| `docmill.cli.status` | `docmill status` output |

The only upstream file the branch patches is `sphinx/builders/html/__init__.py`, which asks
docmill for the cache tag it stores next to the doctrees.

## 3.2 in progress

A worker was rebuilding everything from scratch on every start. `source_fingerprint()` used
to be built with the builtin `hash()`; it now hashes the sorted entries with
`hashlib.sha256`. See `tests/docmill/test_fingerprint.py` for the contract that the value
must be identical in a fresh interpreter.
