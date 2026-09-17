"""dpipe -- data-platform components layered on the internal Scrapy branch.

Components are plain Scrapy middlewares / extensions / pipelines; enable them through
``settings.py`` the usual way.  Timeout-like settings accept a *timeout spec* (see
:mod:`dpipe.timeouts`).
"""

from dpipe.timeouts import Timeout, TimeoutSpecError, parse_timeout

__all__ = ["Timeout", "TimeoutSpecError", "parse_timeout"]
__version__ = "2.0.0.dev3"
