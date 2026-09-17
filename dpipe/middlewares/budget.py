"""Per-request time budgets.

``BudgetMiddleware`` attaches ``request.meta["dpipe_budget"]`` (the parsed budget) and
``request.meta["dpipe_started"]`` (epoch seconds) to every request.  Other dpipe
components derive deadlines from these two keys.  A budget of ``0`` means *unlimited*:
consumers must not derive a deadline from it.
"""

from __future__ import annotations

import time

from scrapy.exceptions import NotConfigured

from dpipe.timeouts import TimeoutSpecError, parse_timeout


class BudgetMiddleware:
    def __init__(self, default_budget: str):
        self.default_budget = default_budget

    @classmethod
    def from_crawler(cls, crawler):
        raw = crawler.settings.get("DPIPE_DEFAULT_BUDGET")
        if not raw:
            raise NotConfigured("DPIPE_DEFAULT_BUDGET is not set")
        return cls(raw)

    def process_request(self, request, spider=None):
        spec = request.meta.get("dpipe_timeout", self.default_budget)
        try:
            budget = parse_timeout(spec)
        except TimeoutSpecError:
            budget = parse_timeout(self.default_budget)
        request.meta["dpipe_budget"] = budget
        request.meta.setdefault("dpipe_started", time.time())
        return None
