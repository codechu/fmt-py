"""Private helpers shared across codechu_fmt modules.

Not part of the public API — do not import from outside this package.
"""

from __future__ import annotations

__all__ = ["_isinf", "_isnan", "_scale_to_unit"]


def _isnan(x: float) -> bool:
    """Return ``True`` if ``x`` is NaN. Avoids importing ``math``."""
    return x != x  # noqa: PLR0124 — NaN guard idiom


def _isinf(x: float) -> bool:
    """Return ``True`` if ``x`` is +inf or -inf. Avoids importing ``math``."""
    return x == float("inf") or x == float("-inf")


def _scale_to_unit(
    value: float,
    units: tuple[str, ...],
    base: float,
) -> tuple[float, int]:
    """Scale ``value`` down by ``base`` until it fits in ``units``.

    Returns ``(scaled_value, unit_index)``. The caller picks the unit
    string from ``units[unit_index]`` and formats as it likes — this
    keeps the helper free of any presentation concerns (precision,
    separators, suffixes).
    """
    v = float(value)
    idx = 0
    last = len(units) - 1
    while v >= base and idx < last:
        v /= base
        idx += 1
    return v, idx
