"""codechu-fmt — stdlib-only human-readable formatters.

Re-exports:

- :func:`format_bitrate` — bits/sec → ``"1.5 Mbps"`` (SI, 1000-base)
- :func:`format_compact` — large numbers → ``"15.2K"`` / ``"1.5M"``
- :func:`format_duration` — seconds → ``"1m 30s"`` / ``"1h 15m"``
- :func:`format_percent`  — 0-1 ratio → ``"42.0%"`` (locale-aware)
- :func:`format_rate`     — per-second rate (items / bytes / ops)
- :func:`format_size`     — bytes → ``"1.5 MiB"`` / ``"1.6 MB"``
"""

from __future__ import annotations

from .bitrate import format_bitrate
from .compact import format_compact
from .duration import format_duration
from .percent import format_percent
from .rate import format_rate
from .size import format_size

__version__ = "0.4.0"

__all__ = [
    "__version__",
    "format_bitrate",
    "format_compact",
    "format_duration",
    "format_percent",
    "format_rate",
    "format_size",
]
