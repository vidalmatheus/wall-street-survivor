from datetime import datetime

from commons import dateutils


def test_to_tz():
    d = datetime.now()
    tz = "US/Eastern"
    d_tz = dateutils.to_tz(d, tz)
    assert d_tz.tzinfo.zone == tz


def test_to_tz_with_none_datetime():
    d = None
    tz = "US/Eastern"
    d_tz = dateutils.to_tz(d, tz)
    assert d_tz is None


def test_to_tz_datetime_with_tz():
    d = datetime.now()
    tz_1 = "US/Eastern"
    d_tz_1 = dateutils.to_tz(d, tz_1)
    tz_2 = "America/Sao_Paulo"
    d_tz_2 = dateutils.to_tz(d_tz_1, tz_2)
    assert d_tz_2.tzinfo.zone == tz_2

