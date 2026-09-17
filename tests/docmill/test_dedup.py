from docmill.dedup.registry import payload, signature

META = {"title": "Install", "source": "guide/install.rst", "lang": "en", "author": "team", "mtime": 17}


def test_payload_keeps_only_the_identifying_fields():
    assert set(payload(META)) == {"title", "source", "lang"}


def test_signature_differs_for_different_documents():
    other = dict(META, source="guide/upgrade.rst")
    assert signature(META) != signature(other)


def test_signature_ignores_irrelevant_metadata():
    noisy = dict(META, mtime=99, author="someone else")
    assert signature(META) == signature(noisy)
