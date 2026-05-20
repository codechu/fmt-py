# API Reference — codechu-fmt 0.3.0

Complete reference for every public symbol re-exported from the
`codechu_fmt` package.

The package exposes six pure functions plus a version string:

| Symbol                                    | Kind     | Module                  |
| ----------------------------------------- | -------- | ----------------------- |
| [`__version__`](#__version__)             | `str`    | `codechu_fmt`           |
| [`format_bitrate`](#format_bitrate)       | function | `codechu_fmt.bitrate`   |
| [`format_compact`](#format_compact)       | function | `codechu_fmt.compact`   |
| [`format_duration`](#format_duration)     | function | `codechu_fmt.duration`  |
| [`format_percent`](#format_percent)       | function | `codechu_fmt.percent`   |
| [`format_rate`](#format_rate)             | function | `codechu_fmt.rate`      |
| [`format_size`](#format_size)             | function | `codechu_fmt.size`      |

Submodules (`codechu_fmt.bitrate`, `codechu_fmt.compact`,
`codechu_fmt.duration`, `codechu_fmt.percent`, `codechu_fmt.rate`,
`codechu_fmt.size`) exist but contain nothing beyond the function
re-exported into the top-level namespace. The `codechu_fmt._helpers`
module is private and not part of the public API.

All functions are pure, side-effect-free, thread-safe, and depend only
on the Python standard library.

---

## `__version__`

```python
__version__: str = "0.3.0"
```

Semantic-version string of the installed package, set at import time
in `codechu_fmt/__init__.py`. Use it for compatibility checks or for
rendering in `--version` output of downstream CLIs.

```python
from codechu_fmt import __version__
print(__version__)  # → '0.3.0'
```

---

## `format_bitrate`

```python
def format_bitrate(bps: float, *, precision: int = 1) -> str: ...
```

Render a bits-per-second value with the 1000-based SI ladder used by
networking gear — `bps`, `Kbps`, `Mbps`, `Gbps`, `Tbps`, `Pbps`. The
input is in *bits*, not bytes; convert with `bytes * 8` first if your
source counts bytes.

### Parameters

| Name        | Type    | Default | Description                                                                                                |
| ----------- | ------- | ------- | ---------------------------------------------------------------------------------------------------------- |
| `bps`       | `float` | —       | Bits-per-second. NaN renders as `"NaN bps"`; Inf renders as `"Inf bps"` / `"-Inf bps"`.                    |
| `precision` | `int`   | `1`     | Decimal places for the scaled value. Ignored for the integer floor (`"500 bps"`).                          |

### Returns

| Type  | Meaning                                                                              |
| ----- | ------------------------------------------------------------------------------------ |
| `str` | Formatted bitrate with a space between number and unit (`"1.5 Mbps"`). Always ASCII. |

### Negative input

| Input                  | Output         |
| ---------------------- | -------------- |
| `format_bitrate(-1.5e6)` | `"-1.5 Mbps"` |
| `format_bitrate(-500)`   | `"-500 bps"`  |

### Examples

```python
from codechu_fmt import format_bitrate

format_bitrate(500)              # → '500 bps'
format_bitrate(1500)             # → '1.5 Kbps'
format_bitrate(1_500_000)        # → '1.5 Mbps'
format_bitrate(2_500_000_000)    # → '2.5 Gbps'
format_bitrate(3e12)             # → '3.0 Tbps'

format_bitrate(1_234_567, precision=2)  # → '1.23 Mbps'

format_bitrate(float('nan'))     # → 'NaN bps'
format_bitrate(float('inf'))     # → 'Inf bps'
format_bitrate(-1.5e6)           # → '-1.5 Mbps'
```

### See also

- [`format_rate`](#format_rate) with `unit="bytes"` — bytes-per-second variant
- [`format_size`](#format_size) — bytes (not bits) ladder

---

## `format_compact`

```python
def format_compact(n: float, *, precision: int = 1) -> str: ...
```

Compact short-form representation of a number using the English
engineering convention `K` / `M` / `B` / `T` (1000-based). For
dashboards, counters, and consumer-facing summaries where space is
tight.

Note: the `"B"` here means *billion*, not bytes. If you want bytes,
use [`format_size`](#format_size) instead.

### Parameters

| Name        | Type    | Default | Description                                                                              |
| ----------- | ------- | ------- | ---------------------------------------------------------------------------------------- |
| `n`         | `float` | —       | Number to compact. NaN renders as `"NaN"`; Inf renders as `"Inf"` / `"-Inf"`.            |
| `precision` | `int`   | `1`     | Decimal places for the scaled value. Ignored for sub-thousand integer floor (`"999"`).    |

### Returns

| Type  | Meaning                                                                  |
| ----- | ------------------------------------------------------------------------ |
| `str` | Compact string. No space between number and suffix (`"15.2K"`). ASCII.   |

### Negative input

| Input                       | Output     |
| --------------------------- | ---------- |
| `format_compact(-15_234)`   | `"-15.2K"` |
| `format_compact(-999)`      | `"-999"`   |

### Examples

```python
from codechu_fmt import format_compact

format_compact(999)            # → '999'
format_compact(15_234)         # → '15.2K'
format_compact(1_500_000)      # → '1.5M'
format_compact(2_500_000_000)  # → '2.5B'
format_compact(3.4e12)         # → '3.4T'

format_compact(15_234, precision=0)  # → '15K'
format_compact(15_234, precision=3)  # → '15.234K'

format_compact(float('nan'))   # → 'NaN'
format_compact(float('inf'))   # → 'Inf'
format_compact(-2.5e9)         # → '-2.5B'
```

The ladder tops out at `T`. Values past `1e15` stay in `T` and grow
without further scaling — guard upstream if you need pet/exa scale.

### See also

- [`format_size`](#format_size) — same idea for bytes with proper unit
- [`format_bitrate`](#format_bitrate) — same idea for bits/sec

---

## `format_duration`

```python
def format_duration(seconds: float, *, compact: bool = False) -> str: ...
```

Render a number of seconds as a two-unit, human-readable duration.
Use it for log lines, status bars, ETA strings — anywhere you want
`"1m 30s"` instead of `90`. Sub-millisecond values render with `µs`
(microseconds) or `ns` (nanoseconds) in both forms. The function
never raises on numerical inputs.

### Parameters

| Name      | Type    | Default | Description                                                                                       |
| --------- | ------- | ------- | ------------------------------------------------------------------------------------------------- |
| `seconds` | `float` | —       | Duration in seconds. NaN renders as `"?"`.                                                        |
| `compact` | `bool`  | `False` | If `True`, omit the space between units (`"1m30s"`) and render sub-second values ≥ 1ms as ms (`"500ms"`). Sub-ms granularity (`µs`/`ns`) is the same in both forms. |

### Returns

| Type  | Meaning                                                                                                    |
| ----- | ---------------------------------------------------------------------------------------------------------- |
| `str` | Formatted duration. See examples for shape. ASCII except `µ` (U+00B5) on the sub-millisecond branch.        |

### Negative input

| Input                            | Output      |
| -------------------------------- | ----------- |
| `format_duration(-1)`            | `"-1.0s"`   |
| `format_duration(-90)`           | `"-1m 30s"` |
| `format_duration(-90, compact=True)` | `"-1m30s"` |

### Raises

| Exception | Condition                                                                                  |
| --------- | ------------------------------------------------------------------------------------------ |
| —         | Numerical inputs never raise. Passing a non-numeric type propagates the underlying `TypeError` from arithmetic / comparison operations. |

### Examples

```python
from codechu_fmt import format_duration

# Sub-millisecond — same granularity in both forms
format_duration(0.0000001)              # → '100ns'
format_duration(0.0005)                 # → '500µs'
format_duration(0.0005, compact=True)   # → '500µs'

# Default form — space between units, decimal sub-seconds
format_duration(0.5)        # → '0.5s'
format_duration(45)         # → '45.0s'
format_duration(90)         # → '1m 30s'
format_duration(3700)       # → '1h 1m'
format_duration(86400)      # → '1d 0h'
format_duration(86400 * 400)  # → '1y 35d'

# Compact form — no spaces; ms for sub-second, µs/ns for sub-ms
format_duration(0.5, compact=True)    # → '500ms'
format_duration(45, compact=True)     # → '45s'
format_duration(90, compact=True)     # → '1m30s'
format_duration(3700, compact=True)   # → '1h1m'
format_duration(3600, compact=True)   # → '1h'

# Edge cases
format_duration(0)                # → '0.0s'
format_duration(float('nan'))     # → '?'
format_duration(-1)               # → '-1.0s'
```

Boundary behaviour: thresholds use `<` against the next unit boundary
(1e-6 s, 1e-3 s, 1 s, 60 s, 3600 s, 86400 s, 365 d). Years are computed
as `days // 365` with no leap-year correction — appropriate for status
display, not calendar arithmetic.

### See also

- [`format_rate`](#format_rate) — same value domain inverted (per-second)
- [`format_size`](#format_size) — sibling formatter for bytes

---

## `format_percent`

```python
def format_percent(ratio: float, *, precision: int = 1, locale: str = "en") -> str: ...
```

Render a 0-1 ratio as a percent string. The `locale` argument selects
the decimal separator and the side of the number that carries the `%`
sign — needed for i18n UIs.

### Parameters

| Name        | Type    | Default | Description                                                                                              |
| ----------- | ------- | ------- | -------------------------------------------------------------------------------------------------------- |
| `ratio`     | `float` | —       | Ratio. `0.42` renders as `"42.0%"`; values above 1 are not clamped.                                      |
| `precision` | `int`   | `1`     | Decimal places for the percent value.                                                                    |
| `locale`    | `str`   | `"en"`  | Recognised: `"en"` (dot decimal, trailing `%`), `"tr"` (comma decimal, leading `%`). Others fall back to `"en"`. |

### Returns

| Type  | Meaning                                                                |
| ----- | ---------------------------------------------------------------------- |
| `str` | Formatted percent. ASCII except the `%` glyph and locale decimal mark. |

### Negative input

| Input                                  | Output     |
| -------------------------------------- | ---------- |
| `format_percent(-0.05)`                | `"-5.0%"`  |
| `format_percent(-0.05, locale="tr")`   | `"%-5,0"`  |

### Examples

```python
from codechu_fmt import format_percent

format_percent(0.42)                   # → '42.0%'
format_percent(0.42, locale="tr")      # → '%42,0'
format_percent(1.0)                    # → '100.0%'
format_percent(1.5)                    # → '150.0%'   (no clamping)
format_percent(-0.05)                  # → '-5.0%'

format_percent(0.4267, precision=0)    # → '43%'
format_percent(0.42678, precision=3)   # → '42.678%'
format_percent(0.4267, precision=2, locale="tr")  # → '%42,67'

# Unknown locale → en fallback
format_percent(0.42, locale="de")      # → '42.0%'

format_percent(float('nan'))           # → 'NaN%'
format_percent(float('inf'))           # → 'Inf%'
```

### See also

- [`format_compact`](#format_compact) — companion for magnitude counters

---

## `format_rate`

```python
def format_rate(
    units_per_sec: float,
    *,
    unit: str = "items",
    precision: int = 1,
) -> str: ...
```

Render a per-second rate. Use it for throughput readouts in CLI
progress bars, telemetry, log lines. The function dispatches on the
`unit` keyword to four behaviours: a bare `"/s"` (items), an IEC-scaled
byte-rate with legacy `KB/MB/GB` labels (bytes), a decimal-prefixed
ops-per-second (ops), and a generic `"<label>/s"` for any other
string. NaN renders as `"?"`.

### Parameters

| Name            | Type    | Default   | Description                                                                                                                |
| --------------- | ------- | --------- | -------------------------------------------------------------------------------------------------------------------------- |
| `units_per_sec` | `float` | —         | Rate. NaN renders as `"?"`.                                                                                                |
| `unit`          | `str`   | `"items"` | Dispatch key. Recognised: `"items"`, `"bytes"`, `"ops"`. Any other string becomes a generic suffix (e.g. `"req"` → `"req/s"`). |
| `precision`     | `int`   | `1`       | Number of digits after the decimal point in the scaled value. Ignored for the integer `"0 B/s"` floor of the bytes path.   |

### Returns

| Type  | Meaning                                                                                                                                 |
| ----- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `str` | Formatted rate. Items form has no space (`"123.4/s"`); bytes, ops, and custom labels render with a space before the unit (`"1.5 MB/s"`). |

### Negative input

| Input                                 | Output         |
| ------------------------------------- | -------------- |
| `format_rate(-5)`                     | `"-5.0/s"`     |
| `format_rate(-1024, unit="bytes")`    | `"-1.0 KB/s"`  |
| `format_rate(-1500, unit="ops")`      | `"-1.5k ops/s"` |
| `format_rate(-42, unit="req")`        | `"-42.0 req/s"` |

### Examples

```python
from codechu_fmt import format_rate

# items (default) — no space, plain '/s'
format_rate(0)         # → '0.0/s'
format_rate(123.4)     # → '123.4/s'
format_rate(1500, precision=0)  # → '1500/s'

# bytes — IEC math (1024-based) with legacy SI-style labels
format_rate(0, unit="bytes")              # → '0 B/s'
format_rate(512, unit="bytes")            # → '512 B/s'
format_rate(1.5 * 1024**2, unit="bytes")  # → '1.5 MB/s'
format_rate(2 * 1024**3, unit="bytes")    # → '2.0 GB/s'

# ops — decimal prefixes (1000-based): '', k, M, G, T, P
format_rate(1500, unit="ops")             # → '1.5k ops/s'
format_rate(2.5e6, unit="ops")            # → '2.5M ops/s'
format_rate(42, unit="ops")               # → '42.0 ops/s'

# custom label — generic "<value> <label>/s"
format_rate(42, unit="req")               # → '42.0 req/s'

# Edge cases
format_rate(float('nan'))                 # → '?'
format_rate(-1, unit="bytes")             # → '-1 B/s'
```

Notes on the bytes path: the label set is the legacy
`B/s, KB/s, MB/s, GB/s, …` (binary-scaled but SI-style suffix), kept
this way because downstream progress bars and tests depend on it. If
you want strict IEC suffixes (`KiB/s`), format the size with
[`format_size`](#format_size) and append `"/s"` yourself. For bits/sec
(networking), use [`format_bitrate`](#format_bitrate).

### See also

- [`format_size`](#format_size) — same scaling logic, different label set
- [`format_bitrate`](#format_bitrate) — bits-per-second variant
- [`format_duration`](#format_duration) — the time-side companion

---

## `format_size`

```python
def format_size(num_bytes: float, *, binary: bool = True, precision: int = 1) -> str: ...
```

Render a byte count as a human-readable string. Use it for file-size
displays, disk-usage tables, network transfer totals. Defaults to IEC
binary units (`KiB`, `MiB`, …, 1024-based); pass `binary=False` for
SI decimal units (`kB`, `MB`, …, 1000-based). The sub-base branch
(values under one unit) renders as an integer with no decimal point.
NaN renders as `"?"`.

### Parameters

| Name        | Type    | Default | Description                                                                                                                  |
| ----------- | ------- | ------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `num_bytes` | `float` | —       | Byte count. NaN renders as `"?"`.                                                                                            |
| `binary`    | `bool`  | `True`  | If `True`, use 1024-based IEC units (`B`, `KiB`, `MiB`, `GiB`, `TiB`, `PiB`, `EiB`). If `False`, use 1000-based SI (`B`, `kB`, `MB`, `GB`, `TB`, `PB`, `EB`). |
| `precision` | `int`   | `1`     | Decimal places for the scaled value. Ignored for the bytes floor (integer `"512 B"`).                                        |

### Returns

| Type  | Meaning                                                                                                          |
| ----- | ---------------------------------------------------------------------------------------------------------------- |
| `str` | Formatted size with a space between the number and the unit (`"1.5 MiB"`). Always ASCII; no locale formatting.   |

### Negative input

| Input                              | Output       |
| ---------------------------------- | ------------ |
| `format_size(-1)`                  | `"-1 B"`     |
| `format_size(-1024)`               | `"-1.0 KiB"` |
| `format_size(-1_500_000, binary=False)` | `"-1.5 MB"` |

### Examples

```python
from codechu_fmt import format_size

# Binary (IEC, default) — 1024-based
format_size(0)                  # → '0 B'
format_size(512)                # → '512 B'
format_size(1024)               # → '1.0 KiB'
format_size(1536)               # → '1.5 KiB'
format_size(1024**3)            # → '1.0 GiB'
format_size(1024**6, precision=2)  # → '1.00 PiB'

# Decimal (SI) — 1000-based
format_size(1500, binary=False)  # → '1.5 kB'
format_size(1_000_000, binary=False)  # → '1.0 MB'

# Negative — useful for size deltas
format_size(-1024)              # → '-1.0 KiB'

# Edge cases
format_size(float('nan'))       # → '?'
format_size(float('inf'))       # scales to the top unit ('EiB'); guard upstream
```

The unit ladder is bounded. For binary, the largest label is `EiB`
(2^60); for decimal, `EB` (10^18). Values exceeding the top unit
stay in that unit and grow without further scaling.

### See also

- [`format_rate`](#format_rate) with `unit="bytes"` — the per-second variant
- [`format_bitrate`](#format_bitrate) — bits, not bytes
- [`format_duration`](#format_duration) — sibling formatter for time
