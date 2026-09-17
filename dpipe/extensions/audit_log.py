"""Optional JSON-lines audit trail of every request that reaches the downloader.

Enabled by ``DPIPE_AUDIT_LOG = "<path>"``; off by default (the platform enables it for
compliance crawls only).
"""

from __future__ import annotations

import json

from scrapy import signals
from scrapy.exceptions import NotConfigured


class AuditLogExtension:
    def __init__(self, path: str):
        self.path = path
        self._fh = None

    @classmethod
    def from_crawler(cls, crawler):
        path = crawler.settings.get("DPIPE_AUDIT_LOG")
        if not path:
            raise NotConfigured
        ext = cls(path)
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.request_reached_downloader, signal=signals.request_reached_downloader)
        return ext

    def spider_opened(self, spider):
        self._fh = open(self.path, "a", encoding="utf-8")

    def spider_closed(self, spider):
        if self._fh is not None:
            self._fh.close()
            self._fh = None

    @staticmethod
    def record(request) -> str:
        return json.dumps({
            "url": request.url,
            "budget": request.meta.get("dpipe_budget"),
            "started": request.meta.get("dpipe_started"),
        }, sort_keys=True)

    def request_reached_downloader(self, request, spider=None):
        if self._fh is not None:
            self._fh.write(self.record(request) + "\n")
