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
from codechu_fmt import format_duration, format_rate, format_size

format_duration(90)                       # → '1m 30s'
format_duration(90, compact=True)         # → '1m30s'
format_duration(0.5, compact=True)        # → '500ms'

format_rate(123.4)                        # → '123.4/s'
format_rate(1.5 * 1024**2, unit="bytes")  # → '1.5 MB/s'
format_rate(1500, unit="ops")             # → '1.5k ops/s'

format_size(1536)                         # → '1.5 KiB'   (binary, IEC)
format_size(1500, binary=False)           # → '1.5 kB'    (decimal, SI)
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

## Design

- **Pure stdlib.** Zero third-party dependencies. The whole library is
  three small modules.
- **Predictable strings.** Output is stable across platforms and
  locales — no thousand separators, no locale formatting.
- **Defensive.** Negative inputs and NaN never raise; they render as
  `"?"`. Useful when the source is a noisy counter.

## Tests

```bash
pip install -e ".[dev]"
pytest -q
```

Coverage gate: ≥90 %.

## License

MIT — see [LICENSE](LICENSE).
