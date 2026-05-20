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
    s = format_rate(2 * 1024**3, unit="bytes")
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


def test_nan_all_units():
    assert format_rate(float("nan")) == "?"
    assert format_rate(float("nan"), unit="bytes") == "?"
    assert format_rate(float("nan"), unit="ops") == "?"
    assert format_rate(float("nan"), unit="req") == "?"


def test_negative_items():
    assert format_rate(-5) == "-5.0/s"


def test_negative_bytes():
    assert format_rate(-1024, unit="bytes") == "-1.0 KB/s"
    assert format_rate(-512, unit="bytes") == "-512 B/s"


def test_negative_ops():
    assert format_rate(-1500, unit="ops") == "-1.5k ops/s"


def test_negative_custom():
    assert format_rate(-42, unit="req") == "-42.0 req/s"


# ---------------------------------------------------------------------------
# precision="auto" + bare_items (added in v0.4.0)
# ---------------------------------------------------------------------------


def test_auto_precision_below_10():
    assert format_rate(1.5, precision="auto") == "1.50/s"
    assert format_rate(9.99, precision="auto") == "9.99/s"


def test_auto_precision_between_10_and_100():
    assert format_rate(10.0, precision="auto") == "10.0/s"
    assert format_rate(42.5, precision="auto") == "42.5/s"
    assert format_rate(99.9, precision="auto") == "99.9/s"


def test_auto_precision_above_100():
    assert format_rate(100, precision="auto") == "100/s"
    assert format_rate(123.4, precision="auto") == "123/s"


def test_auto_precision_with_custom_unit():
    assert format_rate(1.5, unit="req", precision="auto") == "1.50 req/s"
    assert format_rate(42.5, unit="req", precision="auto") == "42.5 req/s"
    assert format_rate(150, unit="req", precision="auto") == "150 req/s"


def test_auto_precision_with_bytes_scales_then_picks():
    # 1.5 MiB/s → v ≈ 1.5 in MB column → 2 decimals at auto
    s = format_rate(1.5 * 1024 * 1024, unit="bytes", precision="auto")
    assert s == "1.50 MB/s"


def test_bare_items_default_true():
    assert format_rate(42.0, unit="items") == "42.0/s"


def test_bare_items_false_shows_label():
    assert format_rate(42.0, unit="items", bare_items=False) == "42.0 items/s"


def test_bare_items_false_with_auto_precision():
    assert format_rate(1.5, unit="items", bare_items=False, precision="auto") == "1.50 items/s"
    assert format_rate(42.5, unit="items", bare_items=False, precision="auto") == "42.5 items/s"
    assert format_rate(150, unit="items", bare_items=False, precision="auto") == "150 items/s"


def test_bare_items_no_effect_on_other_units():
    # bare_items only changes the "items" branch; "req" is unaffected
    assert (
        format_rate(42.0, unit="req", bare_items=False)
        == format_rate(42.0, unit="req", bare_items=True)
        == "42.0 req/s"
    )
