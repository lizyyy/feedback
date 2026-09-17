"""Default values for dpipe settings (merged on top of Scrapy's defaults by the platform
bootstrap; individual projects override them in their own ``settings.py``)."""

DPIPE_DEFAULT_BUDGET = "90s"          # per-request time budget (timeout spec)
DPIPE_RETRY_BACKOFF_BASE = "2s"       # base of the exponential retry back-off
DPIPE_THROTTLE_FACTOR = 2.0           # multiplier applied to request.meta["dpipe_throttle"]
DPIPE_WATCHDOG_LIMIT = "10m"          # close the spider after this wall-clock time
DPIPE_SPIDER_TIMEOUT = "30m"          # hard stop for the whole crawl
DPIPE_HEARTBEAT_INTERVAL = "15s"      # how often the heartbeat extension reports
DPIPE_TIMEOUT_PARSER_MODULE = "dpipe.timeouts"   # where ``parse_<kind>`` parsers live
DPIPE_AUDIT_LOG = None                 # path of the JSON-lines audit trail; None = disabled
