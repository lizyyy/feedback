"""Wall-clock watchdog: close the spider once it has run longer than
``DPIPE_WATCHDOG_LIMIT`` (a timeout spec, default 10 minutes)."""

from __future__ import annotations

from functools import partial

from scrapy import signals
from scrapy.exceptions import NotConfigured

from dpipe import parse_timeout

DEFAULT_LIMIT_SECONDS = 600

_parse_limit = partial(parse_timeout, default=DEFAULT_LIMIT_SECONDS)


def limit_from_settings(settings) -> float:
    """Seconds the spider may run before the watchdog closes it."""
    return float(_parse_limit(settings.get("DPIPE_WATCHDOG_LIMIT")))


class WatchdogExtension:
    def __init__(self, limit_seconds: float, crawler):
        self.limit_seconds = limit_seconds
        self.crawler = crawler
        self._call = None

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool("DPIPE_WATCHDOG_ENABLED", True):
            raise NotConfigured
        ext = cls(limit_from_settings(crawler.settings), crawler)
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        return ext

    def spider_opened(self, spider):
        from twisted.internet import reactor

        self._call = reactor.callLater(self.limit_seconds, self._expire, spider)

    def spider_closed(self, spider):
        if self._call is not None and self._call.active():
            self._call.cancel()

    def _expire(self, spider):
        spider.logger.warning("watchdog: %.0fs limit reached, closing spider", self.limit_seconds)
        self.crawler.engine.close_spider(spider, reason="dpipe_watchdog")
