"""Locale-aware percent formatter."""

from __future__ import annotations

from ._helpers import _isinf, _isnan

__all__ = ["format_percent"]

# Locale presentation rules.
#   "decimal": decimal separator
#   "template": how the percent token slots in around the number;
#               ``{n}`` is the formatted number.
_LOCALES = {
    "en": {"decimal": ".", "template": "{n}%"},
    "tr": {"decimal": ",", "template": "%{n}"},
}


def format_percent(ratio: float, *, precision: int = 1, locale: str = "en") -> str:
    """Render a 0-1 ratio as a percent string.

    ``0.42`` → ``"42.0%"`` (en) / ``"%42,0"`` (tr).
    Values above 1.0 are not clamped — ``1.5`` → ``"150.0%"``.

    The ``locale`` argument controls the decimal separator and the
    side the ``%`` token sits on. Recognised values: ``"en"`` (dot
    decimal, trailing ``%``) and ``"tr"`` (comma decimal, leading
    ``%``). Any other value falls back to ``"en"``.

    NaN renders as ``"NaN%"``; +/-Inf renders as ``"Inf%"`` /
    ``"-Inf%"``. Negative inputs render with a leading ``-``
    (e.g. ``-5.0%``).
    """
    if _isnan(ratio):
        rules = _LOCALES.get(locale, _LOCALES["en"])
        return rules["template"].format(n="NaN")

    rules = _LOCALES.get(locale, _LOCALES["en"])

    sign = ""
    if ratio < 0:
        sign = "-"
        ratio = -ratio

    if _isinf(ratio):
        return rules["template"].format(n=f"{sign}Inf")

    value = ratio * 100.0
    formatted = f"{value:.{precision}f}"
    if rules["decimal"] != ".":
        formatted = formatted.replace(".", rules["decimal"])
    return rules["template"].format(n=f"{sign}{formatted}")
