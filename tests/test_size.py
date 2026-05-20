"""Tests for codechu_fmt.size."""

from __future__ import annotations

from codechu_fmt import format_size


def test_zero():
    assert format_size(0) == "0 B"


def test_small_bytes():
    assert format_size(512) == "512 B"


def test_kib():
    assert format_size(2048) == "2.0 KiB"


def test_mib():
    assert format_size(int(1.5 * 1024 * 1024)) == "1.5 MiB"


def test_gib():
    assert format_size(2 * 1024 ** 3) == "2.0 GiB"


def test_tib():
    s = format_size(3 * 1024 ** 4)
    assert s.endswith("TiB")


def test_decimal_mode():
    s = format_size(1500, binary=False)
    assert s == "1.5 kB"


def test_decimal_mb():
    s = format_size(1_500_000, binary=False)
    assert s == "1.5 MB"


def test_precision():
    s = format_size(int(1.234 * 1024 * 1024), precision=2)
    assert s.startswith("1.23")
    assert s.endswith("MiB")


def test_negative_and_nan():
    assert format_size(-1) == "?"
    assert format_size(float("nan")) == "?"


def test_max_unit_cap():
    # Way bigger than EiB — should still render as EiB rather than crash.
    huge = 1024 ** 8
    s = format_size(huge)
    assert s.endswith("EiB")
