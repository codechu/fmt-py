"""Bits-per-second bitrate formatter."""

from __future__ import annotations

from ._helpers import _isinf, _isnan, _scale_to_unit

__all__ = ["format_bitrate"]

# SI (1000-based) bit-rate ladder — networking convention.
_BPS_UNITS = ("bps", "Kbps", "Mbps", "Gbps", "Tbps", "Pbps")


def format_bitrate(bps: float, *, precision: int = 1) -> str:
    """Human-readable bitrate.

    Converts bits-per-second to ``bps`` / ``Kbps`` / ``Mbps`` /
    ``Gbps`` / ``Tbps`` / ``Pbps`` using the 1000-based SI ladder
    networking conventions expect — *not* IEC 1024.

    Examples::

        format_bitrate(500)            → "500 bps"
        format_bitrate(1_500_000)      → "1.5 Mbps"
        format_bitrate(2_500_000_000)  → "2.5 Gbps"

    NaN renders as ``"NaN bps"``; +/-Inf renders as ``"Inf bps"`` /
    ``"-Inf bps"``. Negative inputs render with a leading ``-``
    (e.g. ``-1.5 Mbps``).
    """
    if _isnan(bps):
        return "NaN bps"

    sign = ""
    if bps < 0:
        sign = "-"
        bps = -bps

    if _isinf(bps):
        return f"{sign}Inf bps"

    v, idx = _scale_to_unit(bps, _BPS_UNITS, 1000.0)

    if idx == 0:
        return f"{sign}{int(v)} {_BPS_UNITS[idx]}"
    return f"{sign}{v:.{precision}f} {_BPS_UNITS[idx]}"
