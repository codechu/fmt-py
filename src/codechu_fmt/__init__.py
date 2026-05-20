"""codechu-fmt — stdlib-only human-readable formatters.

Re-exports:

- :func:`format_duration` — seconds → ``"1m 30s"`` / ``"1h 15m"``
- :func:`format_rate`     — per-second rate (items / bytes / ops)
- :func:`format_size`     — bytes → ``"1.5 MiB"`` / ``"1.6 MB"``
"""

from __future__ import annotations

from .duration import format_duration
from .rate import format_rate
from .size import format_size

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "format_duration",
    "format_rate",
    "format_size",
]
