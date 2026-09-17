"""Hard stop for the whole crawl after ``DPIPE_SPIDER_TIMEOUT``.

Setting names are resolved by *kind* (``DPIPE_SPIDER_<KIND>``) and parsed by the matching
``parse_<kind>`` function so that the same extension can later serve other spider-level
limits (``DPIPE_SPIDER_DELAY`` ...) without new code.
"""

from __future__ import annotations

from scrapy import signals
from scrapy.exceptions import NotConfigured

from dpipe import timeouts as _timeouts


class SpiderTimeoutExtension:
    KIND = "timeout"
    DEFAULT_SECONDS = 1800.0

    def __init__(self, seconds: float, crawler):
        self.seconds = seconds
        self.crawler = crawler
        self._call = None

    @classmethod
    def from_crawler(cls, crawler):
        raw = crawler.settings.get(f"DPIPE_SPIDER_{cls.KIND.upper()}")
        seconds = cls._resolve(cls.KIND, raw, cls.DEFAULT_SECONDS)
        if seconds <= 0:
            raise NotConfigured
        ext = cls(seconds, crawler)
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        return ext

    @staticmethod
    def _resolve(kind: str, raw, default: float) -> float:
        parser = getattr(_timeouts, f"parse_{kind}")
        return float(parser(raw, default))

    def spider_opened(self, spider):
        from twisted.internet import reactor

        self._call = reactor.callLater(self.seconds, self._expire, spider)

    def spider_closed(self, spider):
        if self._call is not None and self._call.active():
            self._call.cancel()

    def _expire(self, spider):
        spider.logger.warning("spider timeout: %.0fs reached, closing spider", self.seconds)
        self.crawler.engine.close_spider(spider, reason="dpipe_spider_timeout")
