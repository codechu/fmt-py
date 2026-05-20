"""Tests for codechu_fmt.bitrate."""

from __future__ import annotations

from codechu_fmt import format_bitrate


def test_zero():
    assert format_bitrate(0) == "0 bps"


def test_bps_floor():
    assert format_bitrate(500) == "500 bps"


def test_kbps():
    assert format_bitrate(1500) == "1.5 Kbps"


def test_mbps():
    assert format_bitrate(1_500_000) == "1.5 Mbps"


def test_gbps():
    assert format_bitrate(2_500_000_000) == "2.5 Gbps"


def test_tbps():
    assert format_bitrate(3_000_000_000_000) == "3.0 Tbps"


def test_pbps_cap():
    # Way past the ladder — should stay at the top unit, not crash.
    s = format_bitrate(5e18)
    assert s.endswith("Pbps")


def test_precision():
    assert format_bitrate(1_234_567, precision=2) == "1.23 Mbps"
    assert format_bitrate(1_500_000, precision=0) == "2 Mbps"


def test_negative():
    assert format_bitrate(-1_500_000) == "-1.5 Mbps"
    assert format_bitrate(-500) == "-500 bps"


def test_nan():
    assert format_bitrate(float("nan")) == "NaN bps"


def test_inf():
    assert format_bitrate(float("inf")) == "Inf bps"
    assert format_bitrate(float("-inf")) == "-Inf bps"


def test_float_input():
    assert format_bitrate(1.5e6) == "1.5 Mbps"


def test_very_small():
    assert format_bitrate(1) == "1 bps"
