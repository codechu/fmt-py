"""Human-readable duration formatter."""

from __future__ import annotations

from ._helpers import _isnan

__all__ = ["format_duration"]


# Separator styles for the two presentation modes. Each tuple is:
#   (between_units, sub_second_suffix_for_default)
# Default form uses a space between components ("1m 30s"); compact form
# is tight ("1m30s"). Sub-second handling differs structurally and is
# handled inline below.
_DEFAULT_SEP = " "
_COMPACT_SEP = ""


def format_duration(seconds: float, *, compact: bool = False) -> str:
    """Human-readable duration.

    Default form (``compact=False``)::

        0.5    → "0.5s"
        45     → "45.0s"
        90     → "1m 30s"
        3700   → "1h 1m"

    Compact form (``compact=True``)::

        0.5    → "500ms"
        45     → "45s"
        90     → "1m30s"
        3700   → "1h1m"

    Negative values and NaN render as ``"?"``.
    """
    if _isnan(seconds) or seconds < 0:
        return "?"
    return _format(seconds, compact=compact)


def _format(seconds: float, *, compact: bool) -> str:
    sep = _COMPACT_SEP if compact else _DEFAULT_SEP

    # Sub-second: the two forms diverge structurally (ms vs decimal s).
    if seconds < 1.0:
        if compact:
            ms = int(round(seconds * 1000))
            return f"{ms}ms"
        return f"{seconds:.1f}s"

    # 1s ≤ s < 60s
    if seconds < 60.0:
        if compact:
            return f"{int(round(seconds))}s"
        return f"{seconds:.1f}s"

    total = int(round(seconds))

    # 1m ≤ s < 1h
    if seconds < 3600.0:
        m, s = divmod(total, 60)
        if compact and s == 0:
            return f"{m}m"
        return f"{m}m{sep}{s}s"

    # 1h ≤ s < 1d
    if seconds < 86400.0:
        h, rem = divmod(total, 3600)
        m = rem // 60
        if compact and m == 0:
            return f"{h}h"
        return f"{h}h{sep}{m}m"

    # 1d ≤ s
    days, rem = divmod(total, 86400)
    if days < 365:
        h = rem // 3600
        if compact and h == 0:
            return f"{days}d"
        return f"{days}d{sep}{h}h"

    years, rem_days = divmod(days, 365)
    if compact and rem_days == 0:
        return f"{years}y"
    return f"{years}y{sep}{rem_days}d"
