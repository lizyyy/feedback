"""Shared download slots for requests with the same budget.

Requests to the same host with an identical budget are throttled together (one Scrapy
download slot per ``(host, budget)`` pair) so that per-slot delays and concurrency limits
apply to the whole budget class instead of every request individually.
"""

from __future__ import annotations

from urllib.parse import urlparse


class BudgetSlotMiddleware:
    def __init__(self):
        self._slot_ids: dict = {}

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def slot_for(self, request) -> str | None:
        budget = request.meta.get("dpipe_budget")
        if budget is None:
            return None
        key = (urlparse(request.url).netloc, budget)
        slot_id = self._slot_ids.setdefault(key, len(self._slot_ids))
        return f"{key[0]}#budget{slot_id}"

    def process_request(self, request, spider=None):
        slot = self.slot_for(request)
        if slot is not None:
            request.meta.setdefault("download_slot", slot)
        return None
