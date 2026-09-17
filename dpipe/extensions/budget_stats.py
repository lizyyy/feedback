"""Budget histogram in crawler stats (feeds the platform dashboard).

Every request that reaches the downloader is counted into a bucket by its budget
(``request.meta["dpipe_budget"]``, attached by :class:`dpipe.middlewares.budget.BudgetMiddleware`).
"""

from __future__ import annotations

from scrapy import signals

BUCKETS = ((60, "le_60s"), (600, "le_10m"), (float("inf"), "gt_10m"))


class BudgetStatsExtension:
    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler.stats)
        crawler.signals.connect(ext.request_reached_downloader, signal=signals.request_reached_downloader)
        return ext

    def request_reached_downloader(self, request, spider=None):
        budget = request.meta.get("dpipe_budget")
        if not isinstance(budget, (int, float)):
            # requests scheduled before BudgetMiddleware ran (or legacy spiders) carry no budget
            return
        for limit, label in BUCKETS:
            if budget <= limit:
                self.stats.inc_value(f"dpipe/budget_bucket/{label}")
                break
