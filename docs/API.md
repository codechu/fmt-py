# API Reference — codechu-fmt 0.2.0

Complete reference for every public symbol re-exported from the
`codechu_fmt` package.

The package exposes three pure functions plus a version string:

| Symbol                                    | Kind     | Module                  |
| ----------------------------------------- | -------- | ----------------------- |
| [`__version__`](#__version__)             | `str`    | `codechu_fmt`           |
| [`format_duration`](#format_duration)     | function | `codechu_fmt.duration`  |
| [`format_rate`](#format_rate)             | function | `codechu_fmt.rate`      |
| [`format_size`](#format_size)             | function | `codechu_fmt.size`      |

Submodules (`codechu_fmt.duration`, `codechu_fmt.rate`,
`codechu_fmt.size`) exist but contain nothing beyond the function
re-exported into the top-level namespace. The `codechu_fmt._helpers`
module is private and not part of the public API.

All functions are pure, side-effect-free, thread-safe, and depend only
on the Python standard library.

---

## `__version__`

```python
__version__: str = "0.2.0"
```

Semantic-version string of the installed package, set at import time
in `codechu_fmt/__init__.py`. Use it for compatibility checks or for
rendering in `--version` output of downstream CLIs.

```python
from codechu_fmt import __version__
print(__version__)  # → '0.2.0'
```

---

## `format_duration`

```python
def format_duration(seconds: float, *, compact: bool = False) -> str: ...
```

Render a non-negative number of seconds as a two-unit, human-readable
duration. Use it for log lines, status bars, ETA strings — anywhere
you want `"1m 30s"` instead of `90`. Sub-second values produce either
a decimal-seconds string (default form) or a millisecond integer
(compact form). The function never raises on numerical inputs; bad
values render as the literal string `"?"`.

### Parameters

| Name      | Type    | Default | Description                                                                                       |
| --------- | ------- | ------- | ------------------------------------------------------------------------------------------------- |
| `seconds` | `float` | —       | Non-negative duration in seconds. NaN and negative values render as `"?"`.                        |
| `compact` | `bool`  | `False` | If `True`, omit the space between units (`"1m30s"`) and render sub-second values as ms (`"500ms"`). |

### Returns

| Type  | Meaning                                                                                                    |
| ----- | ---------------------------------------------------------------------------------------------------------- |
| `str` | Formatted duration. See examples for shape. Always ASCII; no locale-specific separators or thousands marks. |

### Raises

| Exception | Condition                                                                                  |
| --------- | ------------------------------------------------------------------------------------------ |
| —         | Numerical inputs never raise. Passing a non-numeric type propagates the underlying `TypeError` from arithmetic / comparison operations. |

### Examples

```python
from codechu_fmt import format_duration

# Default form — space between units, decimal sub-seconds
format_duration(0.5)        # → '0.5s'
format_duration(45)         # → '45.0s'
format_duration(90)         # → '1m 30s'
format_duration(3700)       # → '1h 1m'
format_duration(86400)      # → '1d 0h'
format_duration(86400 * 400)  # → '1y 35d'

# Compact form — no spaces; ms for sub-second
format_duration(0.5, compact=True)    # → '500ms'
format_duration(45, compact=True)     # → '45s'
format_duration(90, compact=True)     # → '1m30s'
format_duration(3700, compact=True)   # → '1h1m'
format_duration(3600, compact=True)   # → '1h'

# Edge cases
format_duration(0)                # → '0.0s'
format_duration(float('nan'))     # → '?'
format_duration(-1)               # → '?'
format_duration(float('inf'))     # → '1y 0d' is not produced; inf is non-finite and
                                  #   compares as >= every bound, so it scales to the
                                  #   years branch — prefer guarding upstream.
```

Boundary behaviour: thresholds use `<` against the next unit boundary
(60 s, 3600 s, 86400 s, 365 d). Years are computed as `days // 365`
with no leap-year correction — appropriate for status display, not
calendar arithmetic.

### See also

- [`format_rate`](#format_rate) — same value domain inverted (per-second)
- [`format_size`](#format_size) — sibling formatter for bytes

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
string. Negative values and NaN render as `"?"`.

### Parameters

| Name            | Type    | Default   | Description                                                                                                                |
| --------------- | ------- | --------- | -------------------------------------------------------------------------------------------------------------------------- |
| `units_per_sec` | `float` | —         | Non-negative rate. NaN and negative values render as `"?"`.                                                                |
| `unit`          | `str`   | `"items"` | Dispatch key. Recognised: `"items"`, `"bytes"`, `"ops"`. Any other string becomes a generic suffix (e.g. `"req"` → `"req/s"`). |
| `precision`     | `int`   | `1`       | Number of digits after the decimal point in the scaled value. Ignored for the integer `"0 B/s"` floor of the bytes path.   |

### Returns

| Type  | Meaning                                                                                                                                 |
| ----- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `str` | Formatted rate. Items form has no space (`"123.4/s"`); bytes, ops, and custom labels render with a space before the unit (`"1.5 MB/s"`). |

### Raises

| Exception | Condition                                                                                                |
| --------- | -------------------------------------------------------------------------------------------------------- |
| —         | Numerical inputs never raise. Non-numeric `units_per_sec` propagates the underlying arithmetic exception. |

### Examples

```python
from codechu_fmt import format_rate

# items (default) — no space, plain '/s'
format_rate(0)         # → '0.0/s'
format_rate(123.4)     # → '123.4/s'
format_rate(1500, precision=0)  # → '1500/s'

# bytes — IEC math (1024-based) with legacy SI-style labels
format_rate(0, unit="bytes")              # → '0 B/s'
format_rate(512, unit="bytes")            # → '512.0 B/s' is NOT produced — the
                                          #   sub-base branch is integer-only:
                                          #   format_rate(512, unit='bytes') → '512 B/s'
format_rate(1.5 * 1024**2, unit="bytes")  # → '1.5 MB/s'
format_rate(2 * 1024**3, unit="bytes")    # → '2.0 GB/s'

# ops — decimal prefixes (1000-based): '', k, M, G, T, P
format_rate(1500, unit="ops")             # → '1.5k ops/s'
format_rate(2.5e6, unit="ops")            # → '2.5M ops/s'
format_rate(42, unit="ops")               # → '42.0 ops/s'

# custom label — generic "<value> <label>/s"
format_rate(42, unit="req")               # → '42.0 req/s'
format_rate(7, unit="frames")             # → '7.0 frames/s'

# Edge cases
format_rate(float('nan'))                 # → '?'
format_rate(-1, unit="bytes")             # → '?'
format_rate(0, unit="ops")                # → '0.0 ops/s'
```

Notes on the bytes path: the label set is the legacy
`B/s, KB/s, MB/s, GB/s, …` (binary-scaled but SI-style suffix), kept
this way because downstream progress bars and tests depend on it. If
you want strict IEC suffixes (`KiB/s`), format the size with
[`format_size`](#format_size) and append `"/s"` yourself.

### See also

- [`format_size`](#format_size) — same scaling logic, different label set
- [`format_duration`](#format_duration) — the time-side companion

---

## `format_size`

```python
def format_size(num_bytes: float, *, binary: bool = True, precision: int = 1) -> str: ...
```

Render a non-negative byte count as a human-readable string. Use it
for file-size displays, disk-usage tables, network transfer totals.
Defaults to IEC binary units (`KiB`, `MiB`, …, 1024-based); pass
`binary=False` for SI decimal units (`kB`, `MB`, …, 1000-based). The
sub-base branch (values under one unit) renders as an integer with
no decimal point. Negative values and NaN render as `"?"`.

### Parameters

| Name        | Type    | Default | Description                                                                                                                  |
| ----------- | ------- | ------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `num_bytes` | `float` | —       | Non-negative byte count. NaN and negative values render as `"?"`.                                                            |
| `binary`    | `bool`  | `True`  | If `True`, use 1024-based IEC units (`B`, `KiB`, `MiB`, `GiB`, `TiB`, `PiB`, `EiB`). If `False`, use 1000-based SI (`B`, `kB`, `MB`, `GB`, `TB`, `PB`, `EB`). |
| `precision` | `int`   | `1`     | Decimal places for the scaled value. Ignored for the bytes floor (integer `"512 B"`).                                        |

### Returns

| Type  | Meaning                                                                                                          |
| ----- | ---------------------------------------------------------------------------------------------------------------- |
| `str` | Formatted size with a space between the number and the unit (`"1.5 MiB"`). Always ASCII; no locale formatting.   |

### Raises

| Exception | Condition                                                                                                |
| --------- | -------------------------------------------------------------------------------------------------------- |
| —         | Numerical inputs never raise. Non-numeric `num_bytes` propagates the underlying arithmetic exception.    |

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

# Precision
format_size(1536, precision=0)  # → '2 KiB'   (banker's rounding via f-string)
format_size(1536, precision=3)  # → '1.500 KiB'

# Edge cases
format_size(float('nan'))       # → '?'
format_size(-1)                 # → '?'
format_size(float('inf'))       # scales to the top unit ('EiB'); guard upstream
```

The unit ladder is bounded. For binary, the largest label is `EiB`
(2^60); for decimal, `EB` (10^18). Values exceeding the top unit
stay in that unit and grow without further scaling.

### See also

- [`format_rate`](#format_rate) with `unit="bytes"` — the per-second variant
- [`format_duration`](#format_duration) — sibling formatter for time
