"""Per-second rate formatter."""

from __future__ import annotations

from typing import Literal, Union

from ._helpers import _isnan, _scale_to_unit

__all__ = ["format_rate"]

# Legacy 'KB/MB/GB' presentation (1024-based but SI-style suffix) is what
# downstream progress bars expect — see test_bytes_mb / test_bytes_gb.
_BYTES_PER_SEC_UNITS = ("B/s", "KB/s", "MB/s", "GB/s", "TB/s", "PB/s", "EB/s")
_DECIMAL_PREFIXES = ("", "k", "M", "G", "T", "P")

Precision = Union[int, Literal["auto"]]


def _adaptive_precision(value: float) -> int:
    """Magnitude-adaptive decimal places for rate display.

    Mirrors the convention progress bars use: small rates need more
    decimals to be informative, large rates show as integers.

    - ``>= 100`` → 0 decimals  (``"123 items/s"``)
    - ``>= 10``  → 1 decimal   (``"42.5 items/s"``)
    - ``< 10``   → 2 decimals  (``"1.50 items/s"``)
    """
    av = abs(value)
    if av >= 100:
        return 0
    if av >= 10:
        return 1
    return 2


def format_rate(
    units_per_sec: float,
    *,
    unit: str = "items",
    precision: Precision = 1,
    bare_items: bool = True,
) -> str:
    """Per-second rate.

    ``unit='items'`` → ``"123.4/s"`` (or ``"123.4 items/s"`` when
      ``bare_items=False``).
    ``unit='bytes'`` → binary-scaled bytes/sec with legacy SI-style
      suffix, e.g. ``"1.5 MB/s"`` (1024-based math, ``MB`` label).
    ``unit='ops'``   → decimal-prefixed, e.g. ``"1.2k ops/s"``.

    Other ``unit`` values are treated like ``items`` but with the
    custom label, e.g. ``unit='req'`` → ``"123.4 req/s"``.

    ``precision`` defaults to ``1``. Pass ``precision="auto"`` for
    magnitude-adaptive decimals — the convention used by terminal
    progress bars:

    - ≥ 100 → 0 decimals
    - ≥ 10  → 1 decimal
    - < 10  → 2 decimals

    ``bare_items=False`` keeps the ``items`` label visible (useful when
    the caller has set ``unit='items'`` explicitly and wants the word
    to appear). For non-``items`` units this flag has no effect.

    NaN renders as ``"?"``. Negative inputs render with a leading
    ``-`` (e.g. ``-5.0/s``, ``-1.5 MB/s``).
    """
    if _isnan(units_per_sec):
        return "?"

    sign = ""
    if units_per_sec < 0:
        sign = "-"
        units_per_sec = -units_per_sec

    if unit == "bytes":
        v, idx = _scale_to_unit(units_per_sec, _BYTES_PER_SEC_UNITS, 1024.0)
        p = _adaptive_precision(v) if precision == "auto" else precision
        if idx == 0:
            return f"{sign}{int(v)} {_BYTES_PER_SEC_UNITS[idx]}"
        return f"{sign}{v:.{p}f} {_BYTES_PER_SEC_UNITS[idx]}"

    if unit == "ops":
        v, idx = _scale_to_unit(units_per_sec, _DECIMAL_PREFIXES, 1000.0)
        prefix = _DECIMAL_PREFIXES[idx]
        p = _adaptive_precision(v) if precision == "auto" else precision
        if idx == 0:
            return f"{sign}{v:.{p}f} ops/s"
        return f"{sign}{v:.{p}f}{prefix} ops/s"

    p = _adaptive_precision(units_per_sec) if precision == "auto" else precision

    if unit == "items":
        if bare_items:
            return f"{sign}{units_per_sec:.{p}f}/s"
        return f"{sign}{units_per_sec:.{p}f} items/s"

    return f"{sign}{units_per_sec:.{p}f} {unit}/s"
