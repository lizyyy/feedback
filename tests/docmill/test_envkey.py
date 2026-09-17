from docmill.cache.envkey import build_env_key, relevant_settings

ENV = {"builder": "html", "language": "en", "theme": "alabaster", "sphinx_version": "9.1.1", "jobs": 8}


def test_relevant_settings_drops_noise():
    assert "jobs" not in relevant_settings(ENV)
    assert relevant_settings(ENV)["builder"] == "html"


def test_env_key_is_twelve_hex_digits():
    key = build_env_key(ENV)
    assert len(key) == 12 and all(c in "0123456789abcdef" for c in key)


def test_env_key_changes_with_the_theme():
    assert build_env_key(ENV) != build_env_key(dict(ENV, theme="furo"))
