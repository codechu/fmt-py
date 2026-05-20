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

Stdlib-only human-readable formatters — durations, rates, and byte
sizes — extracted from the [Disk Cleaner](https://github.com/codechu/disk-cleaner)
toolchain. No external dependencies. Python 3.10+.

## Install

```bash
pip install codechu-fmt
```

## API

```python
from codechu_fmt import (
    format_bitrate, format_compact, format_duration,
    format_percent, format_rate, format_size,
)

format_duration(90)                       # → '1m 30s'
format_duration(90, compact=True)         # → '1m30s'
format_duration(0.5, compact=True)        # → '500ms'
format_duration(0.0005)                   # → '500µs'
format_duration(0.0000001)                # → '100ns'

format_rate(123.4)                        # → '123.4/s'
format_rate(1.5 * 1024**2, unit="bytes")  # → '1.5 MB/s'
format_rate(1500, unit="ops")             # → '1.5k ops/s'

format_size(1536)                         # → '1.5 KiB'   (binary, IEC)
format_size(1500, binary=False)           # → '1.5 kB'    (decimal, SI)
format_size(-1024)                        # → '-1.0 KiB'  (deltas welcome)

format_bitrate(1_500_000)                 # → '1.5 Mbps'  (SI, 1000-base)
format_bitrate(2_500_000_000)             # → '2.5 Gbps'

format_percent(0.42)                      # → '42.0%'
format_percent(0.42, locale="tr")         # → '%42,0'

format_compact(15_234)                    # → '15.2K'
format_compact(2_500_000_000)             # → '2.5B'
```

### `format_duration(seconds, *, compact=False)`

Default form renders a human-friendly two-unit duration:
`0.5s`, `45.3s`, `1m 30s`, `1h 15m`, `1d 5h`, `2y 30d`.

`compact=True` packs the same information into a tighter form suited
for status lines: `500ms`, `45s`, `1m30s`, `1h15m`.

Negative values and NaN render as `"?"`.

### `format_rate(units_per_sec, *, unit="items", precision=1)`

- `unit="items"` (default) → `123.4/s`
- `unit="bytes"`            → IEC byte-rate, e.g. `1.5 MB/s`
- `unit="ops"`              → decimal-scaled, e.g. `2.5M ops/s`
- any other label           → `42.0 req/s`-style suffix

### `format_size(num_bytes, *, binary=True, precision=1)`

- `binary=True` (default) → IEC powers of 1024: `KiB`, `MiB`, `GiB`, …
- `binary=False`           → SI powers of 1000: `kB`, `MB`, `GB`, …

### `format_bitrate(bps, *, precision=1)`

SI (1000-based) bitrate ladder for networking: `bps`, `Kbps`, `Mbps`,
`Gbps`, `Tbps`, `Pbps`. Input is bits per second.

### `format_percent(ratio, *, precision=1, locale="en")`

0-1 ratio → percent string. `locale="en"` → `"42.0%"`; `locale="tr"`
→ `"%42,0"` (comma decimal, leading `%`). Other locales fall back
to `"en"`.

### `format_compact(n, *, precision=1)`

Large numbers → short SI-prefix string using K/M/B/T (English
engineering convention). `15_234` → `"15.2K"`, `2.5e9` → `"2.5B"`.

## Negative & non-finite handling

All formatters share the same conventions:

| Function          | NaN          | +Inf / -Inf            | Negative          |
| ----------------- | ------------ | ---------------------- | ----------------- |
| `format_size`     | `"?"`        | scales to top unit     | `-` prefix        |
| `format_rate`     | `"?"`        | scales to top unit     | `-` prefix        |
| `format_duration` | `"?"`        | scales to years branch | `-` prefix        |
| `format_bitrate`  | `"NaN bps"`  | `"Inf bps"` / `"-Inf bps"` | `-` prefix    |
| `format_percent`  | `"NaN%"` / `"%NaN"` | `"Inf%"` / `"-Inf%"` | `-` prefix |
| `format_compact`  | `"NaN"`      | `"Inf"` / `"-Inf"`     | `-` prefix        |

## Design

- **Pure stdlib.** Zero third-party dependencies. The whole library is
  three small modules.
- **Predictable strings.** Output is stable across platforms and
  locales — no thousand separators, no locale formatting.
- **Defensive.** Negative, NaN, and Inf inputs never raise. NaN
  renders as `"?"` for the original three formatters and as
  `"NaN…"` for the v0.3 additions; negatives carry a leading `-`
  so deltas read naturally. Useful when the source is a noisy
  counter.

## Tests

```bash
pip install -e ".[dev]"
pytest -q
```

Coverage gate: ≥90 %.

## Documentation

- [API reference](docs/API.md) — every public symbol, signatures, edge cases
- [Migration guide](docs/MIGRATION.md) — v0.1 → v0.2 (drop-in replacement)
- [Recipes](docs/RECIPES.md) — idiomatic patterns for CLIs, logs, progress bars

## Codechu family

Companion libraries from the Codechu Python ecosystem:

| Library | Purpose |
|---------|---------|
| [codechu-meter](https://pypi.org/project/codechu-meter/) | Timing primitives — Stopwatch, ETA, percentile, histogram |
| [codechu-spark](https://pypi.org/project/codechu-spark/) | Unicode sparklines, mini bar charts, heatmaps |
| [codechu-cli](https://pypi.org/project/codechu-cli/) | CLI primitives — colors, progress, spinners, prompts, table |
| [codechu-events](https://pypi.org/project/codechu-events/) | Thread-safe multi-channel pub/sub bus with replay |
| [codechu-xdg](https://pypi.org/project/codechu-xdg/) | XDG Base Directory helpers, vendor-namespaced |
| [codechu-treeviz](https://pypi.org/project/codechu-treeviz/) | Tree visualization — treemap, sunburst, icicle, flame |
| [codechu-fs](https://pypi.org/project/codechu-fs/) | Filesystem primitives — atomic write, XDG trash, safe walk |
| [codechu-term](https://pypi.org/project/codechu-term/) | Terminal capability detection, alt buffer, raw mode |
| [codechu-color](https://pypi.org/project/codechu-color/) | Color palettes, WCAG contrast, color-blind variants |
| [codechu-treedata](https://pypi.org/project/codechu-treedata/) | N-ary tree data structures and algorithms |
| [codechu-log](https://pypi.org/project/codechu-log/) | Structured logging — context, JSON, rotation, redaction |
| [codechu-i18n](https://pypi.org/project/codechu-i18n/) | Internationalization — locale, plural rules, RTL |
| [codechu-ipc](https://pypi.org/project/codechu-ipc/) | Local IPC — Unix socket, FIFO, JSON-line protocol |
| [codechu-config](https://pypi.org/project/codechu-config/) | Schema-driven config — atomic save, migrations |

## Credits

- Inspired by [humanize](https://github.com/python-humanize/humanize) for the conceptual goal of human-readable values
- IEC binary prefix convention follows IEEE 1541-2002

## License

MIT — see [LICENSE](LICENSE).
