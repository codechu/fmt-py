"""Compact short-form large-number formatter (K/M/B/T)."""

from __future__ import annotations

from ._helpers import _isinf, _isnan, _scale_to_unit

__all__ = ["format_compact"]

# English engineering convention — K/M/B/T, 1000-based.
# Note: "B" (billion) here is *not* bytes; this is a numeric magnitude
# label, used in dashboards and consumer-facing summaries.
_COMPACT_UNITS = ("", "K", "M", "B", "T")


def format_compact(n: float, *, precision: int = 1) -> str:
    """Compact large-number string in the English engineering style.

    Examples::

        format_compact(999)            → "999"
        format_compact(15_234)         → "15.2K"
        format_compact(1_500_000)      → "1.5M"
        format_compact(2_500_000_000)  → "2.5B"
        format_compact(3.4e12)         → "3.4T"

    NaN renders as ``"NaN"``; +/-Inf renders as ``"Inf"`` / ``"-Inf"``.
    Negative inputs render with a leading ``-`` (e.g. ``-15.2K``).
    """
    if _isnan(n):
        return "NaN"

    sign = ""
    if n < 0:
        sign = "-"
        n = -n

    if _isinf(n):
        return f"{sign}Inf"

    v, idx = _scale_to_unit(n, _COMPACT_UNITS, 1000.0)
    suffix = _COMPACT_UNITS[idx]

    if idx == 0:
        return f"{sign}{int(v)}"
    return f"{sign}{v:.{precision}f}{suffix}"
