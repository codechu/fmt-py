```text
   ┌──────────────────────────────────────────────────┐
   │  c o d e c h u — f m t                           │
   │  0.001s   1.5KB   42m07s   3.14MB/s   1h23m      │
   │  ·······raw numbers in, human strings out······· │
   └──────────────────────────────────────────────────┘
```

[![PyPI](https://img.shields.io/pypi/v/codechu-fmt.svg)](https://pypi.org/project/codechu-fmt/)
[![Python](https://img.shields.io/pypi/pyversions/codechu-fmt.svg)](https://pypi.org/project/codechu-fmt/)
[![CI](https://github.com/codechu/fmt-py/actions/workflows/ci.yml/badge.svg)](https://github.com/codechu/fmt-py/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> *Precision formatters for durations, rates and byte sizes.*

# codechu-fmt

Stdlib-only human-readable formatters: durations, rates, byte
sizes, bitrates, percent, large-number compact. Consistent NaN /
negative handling across the family, locale support where it
matters.

| Call | Output |
|------|--------|
| `format_duration(90)` | `1m 30s` |
| `format_duration(0.0005)` | `500µs` |
| `format_size(1536)` | `1.5 KiB` |
| `format_size(-1024)` | `-1.0 KiB` |
| `format_rate(1.5e6, unit="bytes")` | `1.5 MB/s` |
| `format_bitrate(2.5e9)` | `2.5 Gbps` |
| `format_percent(0.42, locale="tr")` | `%42,0` |
| `format_compact(2_500_000_000)` | `2.5B` |

## Install

```bash
pip install codechu-fmt
```

Python 3.10+. Zero third-party dependencies.

## Quick example

```python
from codechu_fmt import format_duration, format_size, format_rate

print(format_duration(elapsed_secs))             # '1m 30s'
print(format_size(file.stat().st_size))          # '1.5 MiB'
print(format_rate(bytes_read / elapsed_secs,
                  unit="bytes"))                 # '3.2 MB/s'
```

## What you get

- **`format_duration`** — two-unit human durations
  (`0.5s` / `45.3s` / `1m 30s` / `1h 15m` / …). `compact=True` for
  tight status lines, `integer_seconds=True` for progress bars.
- **`format_rate`** — items/bytes/ops/custom-label per-second
  formatter with `precision="auto"` (magnitude-adaptive decimals).
- **`format_size`** — IEC (`KiB`) or SI (`kB`) byte sizes. Negative
  values render with a leading `-` so size *deltas* read cleanly.
- **`format_bitrate`** — SI (1000-based) bitrate ladder for
  networking (`bps` → `Kbps` → `Mbps` → `Gbps` …).
- **`format_percent`** — 0–1 ratio → percent string, with `"en"` /
  `"tr"` locale variants.
- **`format_compact`** — large numbers → `K`/`M`/`B`/`T` short
  form for dashboards and counters.

NaN renders as `"?"` consistently. Negative inputs keep their
sign for size/rate/duration *deltas*.

## Read more

- [API reference](docs/API.md) — every formatter with signatures,
  edge cases, and rounding rules.
- [Recipes](docs/RECIPES.md) — idiomatic patterns for log lines,
  progress bars, status fields.
- [Migration guide](docs/MIGRATION.md) — between major versions.
- [Changelog](CHANGELOG.md)

## Family

| Library | Purpose |
|---------|---------|
| [codechu-meter](https://pypi.org/project/codechu-meter/) | Timing — stopwatch, ETA, rate, histogram |
| [codechu-spark](https://pypi.org/project/codechu-spark/) | Unicode sparklines, mini bar charts, heatmaps |
| [codechu-cli](https://pypi.org/project/codechu-cli/) | CLI primitives — colors, progress, prompts |
| [codechu-color](https://pypi.org/project/codechu-color/) | Color palettes, WCAG contrast |
| [codechu-i18n](https://pypi.org/project/codechu-i18n/) | Internationalization — locale, plural rules, RTL |

Full ecosystem: [github.com/codechu](https://github.com/codechu).

## Credits

- IEC byte units per
  [IEC 80000-13](https://en.wikipedia.org/wiki/Binary_prefix).
- SI bitrate conventions per
  [Wikipedia: Data-rate units](https://en.wikipedia.org/wiki/Data-rate_units).

## License

MIT — see [LICENSE](LICENSE).

Part of [Codechu](https://github.com/codechu).
