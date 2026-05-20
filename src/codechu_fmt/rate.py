"""Per-second rate formatter."""

from __future__ import annotations

from ._helpers import _isnan, _scale_to_unit

__all__ = ["format_rate"]

# Legacy 'KB/MB/GB' presentation (1024-based but SI-style suffix) is what
# downstream progress bars expect — see test_bytes_mb / test_bytes_gb.
_BYTES_PER_SEC_UNITS = ("B/s", "KB/s", "MB/s", "GB/s", "TB/s", "PB/s", "EB/s")
_DECIMAL_PREFIXES = ("", "k", "M", "G", "T", "P")


def format_rate(
    units_per_sec: float,
    *,
    unit: str = "items",
    precision: int = 1,
) -> str:
    """Per-second rate.

    ``unit='items'`` → ``"123.4/s"``.
    ``unit='bytes'`` → binary-scaled bytes/sec with legacy SI-style
      suffix, e.g. ``"1.5 MB/s"`` (1024-based math, ``MB`` label).
    ``unit='ops'``   → decimal-prefixed, e.g. ``"1.2k ops/s"``.

    Other ``unit`` values are treated like ``items`` but with the
    custom label, e.g. ``unit='req'`` → ``"123.4 req/s"``.

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
        if idx == 0:
            return f"{sign}{int(v)} {_BYTES_PER_SEC_UNITS[idx]}"
        return f"{sign}{v:.{precision}f} {_BYTES_PER_SEC_UNITS[idx]}"

    if unit == "ops":
        v, idx = _scale_to_unit(units_per_sec, _DECIMAL_PREFIXES, 1000.0)
        prefix = _DECIMAL_PREFIXES[idx]
        if idx == 0:
            return f"{sign}{v:.{precision}f} ops/s"
        return f"{sign}{v:.{precision}f}{prefix} ops/s"

    if unit == "items":
        return f"{sign}{units_per_sec:.{precision}f}/s"

    return f"{sign}{units_per_sec:.{precision}f} {unit}/s"
