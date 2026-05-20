"""Human-readable byte size formatter."""

from __future__ import annotations

from ._helpers import _isnan, _scale_to_unit

__all__ = ["format_size"]

_BINARY_UNITS = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB")
_DECIMAL_UNITS = ("B", "kB", "MB", "GB", "TB", "PB", "EB")


def format_size(num_bytes: float, *, binary: bool = True, precision: int = 1) -> str:
    """Human-readable byte size.

    ``binary=True`` (default): IEC ``1.5 MiB`` (1024-based).
    ``binary=False``:          SI  ``1.6 MB``  (1000-based).

    Negative values and NaN render as ``"?"``.
    """
    if _isnan(num_bytes) or num_bytes < 0:
        return "?"

    base = 1024.0 if binary else 1000.0
    units = _BINARY_UNITS if binary else _DECIMAL_UNITS

    v, idx = _scale_to_unit(num_bytes, units, base)

    if idx == 0:
        return f"{int(v)} {units[idx]}"
    return f"{v:.{precision}f} {units[idx]}"
