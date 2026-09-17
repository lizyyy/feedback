"""Periodic heartbeat: logs crawl progress every ``DPIPE_HEARTBEAT_INTERVAL``."""

from __future__ import annotations

from scrapy import signals
from scrapy.exceptions import NotConfigured

from dpipe.utils.load import seconds_for


class HeartbeatExtension:
    def __init__(self, interval: float, crawler):
        self.interval = interval
        self.crawler = crawler
        self._task = None

    @classmethod
    def from_crawler(cls, crawler):
        interval = seconds_for(crawler.settings, "DPIPE_HEARTBEAT_INTERVAL", 15.0)
        if interval <= 0:
            raise NotConfigured
        ext = cls(interval, crawler)
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        return ext

    def spider_opened(self, spider):
        from twisted.internet.task import LoopingCall

        self._task = LoopingCall(self._beat, spider)
        self._task.start(self.interval, now=False)

    def spider_closed(self, spider):
        if self._task is not None and self._task.running:
            self._task.stop()

    def _beat(self, spider):
        stats = self.crawler.stats.get_stats() if self.crawler.stats else {}
        spider.logger.info("heartbeat: %s items, %s responses", stats.get("item_scraped_count", 0), stats.get("response_received_count", 0))
