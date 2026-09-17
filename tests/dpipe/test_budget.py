from scrapy.http import Request
from scrapy.utils.test import get_crawler

from dpipe.middlewares.budget import BudgetMiddleware


def test_budget_from_setting_and_meta():
    crawler = get_crawler(settings_dict={"DPIPE_DEFAULT_BUDGET": "90s"})
    mw = BudgetMiddleware.from_crawler(crawler)
    req = Request("http://example.com")
    mw.process_request(req, None)
    assert req.meta["dpipe_budget"].seconds == 90.0
    assert "dpipe_started" in req.meta

    req = Request("http://example.com", meta={"dpipe_timeout": "2m"})
    mw.process_request(req, None)
    assert req.meta["dpipe_budget"].seconds == 120.0


def test_budget_invalid_meta_falls_back():
    crawler = get_crawler(settings_dict={"DPIPE_DEFAULT_BUDGET": "45s"})
    mw = BudgetMiddleware.from_crawler(crawler)
    req = Request("http://example.com", meta={"dpipe_timeout": "soon"})
    mw.process_request(req, None)
    assert req.meta["dpipe_budget"].seconds == 45.0
