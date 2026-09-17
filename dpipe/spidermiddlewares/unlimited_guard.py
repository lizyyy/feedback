"""Retry cap for requests spawned under an unlimited budget.

A response fetched with an unlimited budget (``dpipe_budget`` of ``0``) may spawn
follow-up requests; those must not retry forever, so they get ``max_retry_times = 1``
unless the spider set something explicitly.
"""

from __future__ import annotations

from scrapy import Request


class UnlimitedGuardSpiderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_spider_output(self, response, result, spider):
        unlimited = response.meta.get("dpipe_budget") == 0
        for element in result:
            if unlimited and isinstance(element, Request):
                element.meta.setdefault("max_retry_times", 1)
            yield element
