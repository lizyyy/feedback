from docmill.cache.fingerprint import source_fingerprint

FILES = {"index.rst": b"welcome\n", "guide/install.rst": b"pip install\n", "conf.py": b"project = 'x'\n"}


def test_fingerprint_is_stable_and_order_independent():
    reversed_files = dict(reversed(list(FILES.items())))
    assert source_fingerprint(FILES) == source_fingerprint(reversed_files)


def test_fingerprint_changes_with_contents():
    other = dict(FILES, **{"index.rst": b"welcome!\n"})
    assert source_fingerprint(FILES) != source_fingerprint(other)


def test_fingerprint_survives_a_restart(in_fresh_worker):
    expression = "__import__('docmill.cache.fingerprint', fromlist=['x']).source_fingerprint({'a.rst': b'1', 'b.rst': b'2'})"
    workers = {in_fresh_worker(expression) for _ in range(3)}
    assert len(workers) == 1, "workers started independently must address the same artifact"
