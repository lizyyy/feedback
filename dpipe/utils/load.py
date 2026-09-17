"""Settings helpers shared by dpipe components."""

from __future__ import annotations

from scrapy.utils.misc import load_object

from dpipe.settings_defaults import DPIPE_TIMEOUT_PARSER_MODULE


def resolve_parser(kind: str, settings=None):
    """Return the ``parse_<kind>`` callable from the configured parser module.

    The module is configurable (``DPIPE_TIMEOUT_PARSER_MODULE``) so that projects can plug
    in their own spec syntax without touching the components.
    """
    module = None
    if settings is not None:
        module = settings.get("DPIPE_TIMEOUT_PARSER_MODULE")
    module = module or DPIPE_TIMEOUT_PARSER_MODULE
    return load_object(f"{module}.parse_{kind}")


def seconds_for(settings, key: str, default: float) -> float:
    """Read the interval setting ``key`` (a timeout spec) and return it in seconds.

    Falls back to ``default`` when the setting is unset or cannot be parsed.
    """
    raw = settings.get(key)
    if raw in (None, ""):
        return default
    value = resolve_parser("timeout", settings)(raw, default)
    return default if value is None else float(value)
