"""Per-request throttling hints.

A request may carry ``request.meta["dpipe_throttle"]`` (a timeout spec).  The middleware
turns it into ``request.meta["download_slot_delay"]`` scaled by ``DPIPE_THROTTLE_FACTOR``;
requests without a hint get ``DEFAULT_DELAY``.
"""

from __future__ import annotations

from dpipe.timeouts import parse_timeout as _parse


class ThrottleMiddleware:
    DEFAULT_DELAY = 0.5

    def __init__(self, factor: float = 2.0):
        self.factor = factor

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getfloat("DPIPE_THROTTLE_FACTOR", 2.0))

    def delay_for(self, meta: dict) -> float:
        return _parse(meta.get("dpipe_throttle"), self.DEFAULT_DELAY) * self.factor

    def process_request(self, request, spider=None):
        request.meta["download_slot_delay"] = self.delay_for(request.meta)
        return None
