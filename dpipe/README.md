# dpipe

Data-platform components for the internal Scrapy branch. Everything lives in this package
so that the upstream tree stays easy to rebase; the only upstream files we patch are
`scrapy/downloadermiddlewares/downloadtimeout.py` (per-request budgets) and
`scrapy/downloadermiddlewares/retry.py` (no retries once the budget is spent).

| Component | Kind | Setting(s) |
|---|---|---|
| `dpipe.middlewares.BudgetMiddleware` | downloader middleware | `DPIPE_DEFAULT_BUDGET` |
| `dpipe.middlewares.RetryBackoffMiddleware` | downloader middleware | `DPIPE_RETRY_BACKOFF_BASE` |
| `dpipe.middlewares.ThrottleMiddleware` | downloader middleware | `DPIPE_THROTTLE_FACTOR` |
| `dpipe.middlewares.BudgetSlotMiddleware` | downloader middleware | – |
| `dpipe.spidermiddlewares.DeadlineSpiderMiddleware` | spider middleware | – |
| `dpipe.spidermiddlewares.UnlimitedGuardSpiderMiddleware` | spider middleware | – |
| `dpipe.extensions.BudgetStatsExtension` | extension | – |
| `dpipe.extensions.AuditLogExtension` | extension | `DPIPE_AUDIT_LOG` |
| `dpipe.extensions.WatchdogExtension` | extension | `DPIPE_WATCHDOG_LIMIT`, `DPIPE_WATCHDOG_ENABLED` |
| `dpipe.extensions.SpiderTimeoutExtension` | extension | `DPIPE_SPIDER_TIMEOUT` |
| `dpipe.extensions.HeartbeatExtension` | extension | `DPIPE_HEARTBEAT_INTERVAL` |

All timeout-like settings take a *timeout spec*: a number of seconds or a string with a
unit (`"500ms"`, `"30s"`, `"2m"`, `"1h"`). Specs are parsed by `dpipe.timeouts.parse_timeout`.

## 2.0 migration (in progress)

`dpipe.timeouts.parse_timeout()` used to return a bare `float` (seconds) and took a
`default=` argument that was returned for missing or malformed specs. Since 2.0 it returns
a `Timeout` value object (`.seconds`, `.deadline_from(now)`) and raises
`TimeoutSpecError` instead of returning a default -- the fallback is decided by each
caller. See `tests/dpipe/test_timeouts.py` for the contract.
