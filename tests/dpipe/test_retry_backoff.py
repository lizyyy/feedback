from scrapy.utils.test import get_crawler

from dpipe.middlewares.retry_backoff import RetryBackoffMiddleware


def test_backoff_base_from_settings():
    mw = RetryBackoffMiddleware.from_crawler(get_crawler(settings_dict={"DPIPE_RETRY_BACKOFF_BASE": "500ms"}))
    assert mw.backoff_for(0) == 0.5
    assert mw.backoff_for(3) == 4.0


def test_backoff_invalid_setting_uses_two_seconds():
    mw = RetryBackoffMiddleware.from_crawler(get_crawler(settings_dict={"DPIPE_RETRY_BACKOFF_BASE": "later"}))
    assert mw.backoff_for(1) == 4.0
