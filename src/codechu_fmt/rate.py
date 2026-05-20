"""Per-second rate formatter."""

from __future__ import annotations

from .size import format_size

__all__ = ["format_rate"]

_DECIMAL_SUFFIXES = ("", "k", "M", "G", "T", "P")


def _isnan(x: float) -> bool:
    return x != x  # noqa: PLR0124


def format_rate(
    units_per_sec: float,
    *,
    unit: str = "items",
    precision: int = 1,
) -> str:
    """Per-second rate.

    ``unit='items'`` → ``"123.4/s"``.
    ``unit='bytes'`` → binary-prefixed bytes/sec, e.g. ``"1.2 MB/s"``
      (uses :func:`codechu_fmt.format_size` internally with binary scaling).
    ``unit='ops'``   → decimal-prefixed, e.g. ``"1.2k ops/s"``.

    Other ``unit`` values are treated like ``items`` but with the
    custom label, e.g. ``unit='req'`` → ``"123.4 req/s"``.

    Negative values and NaN render as ``"?"``.
    """
    if _isnan(units_per_sec) or units_per_sec < 0:
        return "?"

    if unit == "bytes":
        sized = format_size(units_per_sec, binary=True, precision=precision)
        # format_size returns e.g. '1.5 MiB' — convert to bytes/sec form.
        # Use the legacy 'KB/MB/GB' presentation that matches downstream
        # progress bars; we substitute the IEC suffix for an SI-style one.
        return _iec_to_legacy_bps(sized)

    if unit == "ops":
        return _decimal_scaled(units_per_sec, suffix="ops/s", precision=precision)

    if unit == "items":
        return f"{units_per_sec:.{precision}f}/s"

    return f"{units_per_sec:.{precision}f} {unit}/s"


def _iec_to_legacy_bps(sized: str) -> str:
    """Convert ``'1.5 MiB'`` → ``'1.5 MB/s'``.

    The trailing ``iB`` becomes ``B/s``; bare ``B`` becomes ``B/s``.
    """
    if sized == "?":
        return "?"
    if sized.endswith(" B"):
        return sized + "/s"
    # Strip 'iB' → 'B', append '/s'.
    if sized.endswith("iB"):
        return sized[:-2] + "B/s"
    return sized + "/s"


def _decimal_scaled(value: float, *, suffix: str, precision: int) -> str:
    v = float(value)
    idx = 0
    while v >= 1000.0 and idx < len(_DECIMAL_SUFFIXES) - 1:
        v /= 1000.0
        idx += 1
    prefix = _DECIMAL_SUFFIXES[idx]
    if idx == 0:
        return f"{v:.{precision}f} {suffix}"
    return f"{v:.{precision}f}{prefix} {suffix}"
