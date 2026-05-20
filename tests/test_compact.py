"""Tests for codechu_fmt.compact."""

from __future__ import annotations

from codechu_fmt import format_compact


def test_zero():
    assert format_compact(0) == "0"


def test_sub_thousand():
    assert format_compact(999) == "999"


def test_thousands():
    assert format_compact(15_234) == "15.2K"


def test_thousands_round():
    assert format_compact(1500) == "1.5K"


def test_millions():
    assert format_compact(1_500_000) == "1.5M"


def test_billions():
    assert format_compact(2_500_000_000) == "2.5B"


def test_trillions():
    assert format_compact(3_400_000_000_000) == "3.4T"


def test_cap_at_top_unit():
    # Way past T — should still render with T, not crash.
    s = format_compact(5e18)
    assert s.endswith("T")


def test_precision_zero():
    assert format_compact(15_234, precision=0) == "15K"


def test_precision_three():
    assert format_compact(15_234, precision=3) == "15.234K"


def test_negative():
    assert format_compact(-15_234) == "-15.2K"
    assert format_compact(-999) == "-999"
    assert format_compact(-2_500_000_000) == "-2.5B"


def test_nan():
    assert format_compact(float("nan")) == "NaN"


def test_inf():
    assert format_compact(float("inf")) == "Inf"
    assert format_compact(float("-inf")) == "-Inf"


def test_float_input():
    assert format_compact(1500.0) == "1.5K"
