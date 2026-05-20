"""Tests for codechu_fmt.duration."""

from __future__ import annotations

from codechu_fmt import format_duration


def test_zero():
    assert format_duration(0) == "0.0s"


def test_sub_second():
    assert format_duration(0.5) == "0.5s"


def test_sub_second_compact_ms():
    assert format_duration(0.5, compact=True) == "500ms"


def test_under_minute():
    assert format_duration(45.3) == "45.3s"
    assert format_duration(45.3, compact=True) == "45s"


def test_minutes():
    assert format_duration(90) == "1m 30s"
    assert format_duration(90, compact=True) == "1m30s"


def test_whole_minute_compact():
    assert format_duration(60, compact=True) == "1m"


def test_hours():
    assert format_duration(3700) == "1h 1m"
    assert format_duration(3700, compact=True) == "1h1m"
    assert format_duration(3600, compact=True) == "1h"


def test_days():
    one_day = 86400
    assert format_duration(one_day) == "1d 0h"
    assert format_duration(one_day + 3600 * 5) == "1d 5h"
    assert format_duration(one_day, compact=True) == "1d"


def test_years():
    one_year = 365 * 86400
    assert format_duration(one_year).startswith("1y")
    assert format_duration(one_year, compact=True) == "1y"
    assert "2d" in format_duration(one_year + 2 * 86400, compact=True)


def test_nan():
    assert format_duration(float("nan")) == "?"


def test_negative_seconds():
    assert format_duration(-1) == "-1.0s"
    assert format_duration(-90) == "-1m 30s"
    assert format_duration(-90, compact=True) == "-1m30s"


def test_microseconds_default():
    assert format_duration(0.0005) == "500µs"


def test_microseconds_compact():
    assert format_duration(0.0005, compact=True) == "500µs"


def test_nanoseconds_default():
    assert format_duration(0.0000001) == "100ns"


def test_nanoseconds_compact():
    assert format_duration(0.0000001, compact=True) == "100ns"


def test_microsecond_boundary():
    # 1ms exactly → still ms granularity
    assert format_duration(0.001, compact=True) == "1ms"
    # Just under 1ms → microseconds
    assert format_duration(0.0009, compact=True) == "900µs"


def test_zero_stays_seconds():
    # Zero must not fall into the µs/ns branches.
    assert format_duration(0) == "0.0s"
    assert format_duration(0, compact=True) == "0ms"
