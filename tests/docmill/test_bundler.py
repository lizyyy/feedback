from docmill.assets.bundler import bundle_id, resolve

VERSIONS = {"alabaster": "1.0.0", "pygments": "2.18.0", "jquery": "3.7.1", "basic-theme": "9.1.1"}


def test_resolve_pins_known_packages():
    assert resolve({"pygments", "jquery"}, VERSIONS) == {"pygments": "2.18.0", "jquery": "3.7.1"}


def test_resolve_skips_unknown_packages():
    assert resolve({"pygments", "nope"}, VERSIONS) == {"pygments": "2.18.0"}


def test_bundle_id_reflects_the_package_count():
    assert bundle_id({"pygments"}, VERSIONS).startswith("01-")
    assert bundle_id({"pygments", "jquery"}, VERSIONS).startswith("02-")


def test_different_bundles_get_different_ids():
    assert bundle_id({"pygments"}, VERSIONS) != bundle_id({"jquery"}, VERSIONS)
