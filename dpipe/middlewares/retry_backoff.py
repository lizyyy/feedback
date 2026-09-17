"""Exponential back-off hints for retried requests (429 / 503)."""

from __future__ import annotations

from dpipe.timeouts import TimeoutSpecError, parse_timeout


class RetryBackoffMiddleware:
    def __init__(self, base_seconds: float):
        self.base_seconds = base_seconds

    @classmethod
    def from_crawler(cls, crawler):
        try:
            base = parse_timeout(crawler.settings.get("DPIPE_RETRY_BACKOFF_BASE", "2s")).seconds
        except TimeoutSpecError:
            base = 2.0
        return cls(base)

    def backoff_for(self, retry_times: int) -> float:
        return self.base_seconds * (2**retry_times)

    def process_response(self, request, response, spider=None):
        if response.status in (429, 503):
            request.meta["dpipe_backoff"] = self.backoff_for(request.meta.get("retry_times", 0))
        return response
