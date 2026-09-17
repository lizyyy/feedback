"""Stamp scraped items with the deadline of the request that produced them.

The deadline is ``dpipe_started + dpipe_budget`` (both keys are written to
``request.meta`` by :class:`dpipe.middlewares.budget.BudgetMiddleware`).  Downstream
exporters use ``item["deadline"]`` to drop stale records.  Requests with an unlimited
budget (``0``) get no deadline at all.
"""

from __future__ import annotations


class DeadlineSpiderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_spider_output(self, response, result, spider):
        started = response.meta.get("dpipe_started")
        budget = response.meta.get("dpipe_budget")
        for element in result:
            if started and budget and isinstance(element, dict):
                element.setdefault("deadline", started + budget)
            yield element
