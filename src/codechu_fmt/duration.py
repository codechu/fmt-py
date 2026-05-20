"""Human-readable duration formatter."""

from __future__ import annotations

__all__ = ["format_duration"]


def _isnan(x: float) -> bool:
    return x != x  # noqa: PLR0124 — NaN guard idiom


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

    if compact:
        return _format_compact(seconds)
    return _format_default(seconds)


def _format_default(seconds: float) -> str:
    if seconds < 1.0:
        return f"{seconds:.1f}s"
    if seconds < 60.0:
        return f"{seconds:.1f}s"
    if seconds < 3600.0:
        total = int(round(seconds))
        m, s = divmod(total, 60)
        return f"{m}m {s}s"
    if seconds < 86400.0:
        total = int(round(seconds))
        h, rem = divmod(total, 3600)
        m = rem // 60
        return f"{h}h {m}m"
    # Days / years (very large)
    total = int(round(seconds))
    days, rem = divmod(total, 86400)
    if days < 365:
        h = rem // 3600
        return f"{days}d {h}h"
    years, rem_days = divmod(days, 365)
    return f"{years}y {rem_days}d"


def _format_compact(seconds: float) -> str:
    if seconds < 1.0:
        ms = int(round(seconds * 1000))
        return f"{ms}ms"
    if seconds < 60.0:
        return f"{int(round(seconds))}s"
    if seconds < 3600.0:
        total = int(round(seconds))
        m, s = divmod(total, 60)
        if s == 0:
            return f"{m}m"
        return f"{m}m{s}s"
    if seconds < 86400.0:
        total = int(round(seconds))
        h, rem = divmod(total, 3600)
        m = rem // 60
        if m == 0:
            return f"{h}h"
        return f"{h}h{m}m"
    total = int(round(seconds))
    days, rem = divmod(total, 86400)
    if days < 365:
        h = rem // 3600
        if h == 0:
            return f"{days}d"
        return f"{days}d{h}h"
    years, rem_days = divmod(days, 365)
    if rem_days == 0:
        return f"{years}y"
    return f"{years}y{rem_days}d"
