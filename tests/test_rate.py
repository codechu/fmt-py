"""Tests for codechu_fmt.rate."""

from __future__ import annotations

from codechu_fmt import format_rate


def test_items_default():
    assert format_rate(123.4) == "123.4/s"


def test_items_zero():
    assert format_rate(0) == "0.0/s"


def test_items_precision():
    assert format_rate(123.456, precision=2) == "123.46/s"


def test_bytes_small():
    s = format_rate(512, unit="bytes")
    assert s == "512 B/s"


def test_bytes_mb():
    s = format_rate(1.5 * 1024 * 1024, unit="bytes")
    assert s.endswith("MB/s")
    assert "1.5" in s


def test_bytes_gb():
    s = format_rate(2 * 1024 ** 3, unit="bytes")
    assert s.endswith("GB/s")


def test_ops_small():
    s = format_rate(123.4, unit="ops")
    assert s == "123.4 ops/s"


def test_ops_scaled_k():
    s = format_rate(1500, unit="ops")
    assert s.startswith("1.5k")
    assert s.endswith("ops/s")


def test_ops_scaled_m():
    s = format_rate(2_500_000, unit="ops")
    assert s.startswith("2.5M")


def test_custom_unit():
    s = format_rate(42.0, unit="req")
    assert s == "42.0 req/s"


def test_negative_and_nan():
    assert format_rate(-1) == "?"
    assert format_rate(float("nan")) == "?"
    assert format_rate(-1, unit="bytes") == "?"
    assert format_rate(-1, unit="ops") == "?"
