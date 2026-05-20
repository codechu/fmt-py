"""Tests for codechu_fmt.percent."""

from __future__ import annotations

from codechu_fmt import format_percent


def test_zero():
    assert format_percent(0) == "0.0%"


def test_simple_en():
    assert format_percent(0.42) == "42.0%"


def test_simple_tr():
    assert format_percent(0.42, locale="tr") == "%42,0"


def test_one_hundred():
    assert format_percent(1.0) == "100.0%"


def test_above_one():
    assert format_percent(1.5) == "150.0%"


def test_negative_en():
    assert format_percent(-0.05) == "-5.0%"


def test_negative_tr():
    assert format_percent(-0.05, locale="tr") == "%-5,0"


def test_precision_zero():
    assert format_percent(0.4267, precision=0) == "43%"


def test_precision_three():
    assert format_percent(0.42678, precision=3) == "42.678%"


def test_precision_tr():
    assert format_percent(0.4267, precision=2, locale="tr") == "%42,67"


def test_unknown_locale_falls_back_to_en():
    assert format_percent(0.42, locale="de") == "42.0%"


def test_nan_en():
    assert format_percent(float("nan")) == "NaN%"


def test_nan_tr():
    assert format_percent(float("nan"), locale="tr") == "%NaN"


def test_inf_en():
    assert format_percent(float("inf")) == "Inf%"
    assert format_percent(float("-inf")) == "-Inf%"


def test_inf_tr():
    assert format_percent(float("inf"), locale="tr") == "%Inf"


def test_very_small():
    assert format_percent(0.00001, precision=3) == "0.001%"


def test_very_large():
    assert format_percent(1000.0) == "100000.0%"
