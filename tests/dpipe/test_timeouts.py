import pytest

from dpipe.timeouts import Timeout, TimeoutSpecError, parse_timeout


@pytest.mark.parametrize(
    ("spec", "seconds"),
    [(30, 30.0), (2.5, 2.5), ("30", 30.0), ("30s", 30.0), ("500ms", 0.5), ("2m", 120.0), ("1h", 3600.0), (" 15 s ", 15.0)],
)
def test_parse_valid(spec, seconds):
    t = parse_timeout(spec)
    assert isinstance(t, Timeout)
    assert t.seconds == seconds


@pytest.mark.parametrize("spec", [None, "", "abc", "-5", -1, True, "30x", object()])
def test_parse_invalid_raises(spec):
    with pytest.raises(TimeoutSpecError):
        parse_timeout(spec)


def test_timeout_passthrough_and_deadline():
    t = parse_timeout("90s")
    assert parse_timeout(t) is t
    assert t.deadline_from(1000.0) == 1090.0
    assert str(t) == "90s"
