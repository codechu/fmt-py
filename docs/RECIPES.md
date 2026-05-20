# Recipes

Short, idiomatic patterns for using `codechu-fmt` in real code. Each
recipe is a self-contained snippet — copy, paste, adapt.

## 1. Format a size for display in a CLI tool

You have a byte count from `os.path.getsize` or `shutil.disk_usage`
and want to print it next to a filename.

```python
import os
from codechu_fmt import format_size

for name in os.listdir("."):
    if os.path.isfile(name):
        print(f"{format_size(os.path.getsize(name)):>10}  {name}")
```

Output:

```
   1.2 KiB  README.md
  45.0 MiB  data.parquet
       0 B  empty.log
```

Right-align the size column with `:>10` so the unit suffix lines up.
Use `binary=False` if your tool's audience expects disk-vendor MB
(1000-based) rather than IEC MiB.

## 2. Format a duration for logs (compact vs default)

Logs benefit from compact strings; status panels read better with the
spaced form.

```python
import time
import logging
from codechu_fmt import format_duration

t0 = time.monotonic()
do_work()
elapsed = time.monotonic() - t0

# Log line — compact
logging.info("work done in %s", format_duration(elapsed, compact=True))
# → 'work done in 1m30s'

# Status panel — default
print(f"Elapsed: {format_duration(elapsed)}")
# → 'Elapsed: 1m 30s'
```

The compact form is also right for fixed-width status bars where every
column counts. The default form scans more naturally in human-read
output.

## 3. Format a rate for a progress-bar caption

A progress bar typically shows both throughput and ETA. Pair
[`format_rate`](API.md#format_rate) with [`format_duration`](API.md#format_duration).

```python
from codechu_fmt import format_rate, format_duration

def caption(bytes_done: int, bytes_total: int, elapsed_s: float) -> str:
    rate = bytes_done / elapsed_s if elapsed_s > 0 else 0.0
    remaining = bytes_total - bytes_done
    eta = remaining / rate if rate > 0 else float("nan")
    return f"{format_rate(rate, unit='bytes')}  ETA {format_duration(eta, compact=True)}"

print(caption(1.5 * 1024**3, 4 * 1024**3, 12.0))
# → '128.0 MB/s  ETA 19s'
```

Note that `format_duration(float('nan'))` renders as `"?"`, so a
stalled bar (rate = 0) shows `ETA ?` instead of crashing.

## 4. Render a noisy counter safely

When the source of your number is a counter that might wrap to
negative or produce NaN (e.g. a moving-average rate that hasn't
warmed up yet), use the formatters without a guard — they already
handle it.

```python
from codechu_fmt import format_rate

samples = [12.3, float("nan"), -1.0, 0.0, 99.0]
for s in samples:
    print(format_rate(s))
# 12.3/s
# ?
# ?
# 0.0/s
# 99.0/s
```

This is the intended trade-off: the formatter is the last line of
defence for display code, not a place where noisy upstream data
should bubble up as exceptions.

## 5. Decimal sizes for disk-vendor parity

Disk manufacturers and most cloud dashboards use SI (1000-based)
units. Match their numbers when reporting capacity.

```python
from codechu_fmt import format_size

capacity = 500 * 1000**3  # "500 GB" disk
print(format_size(capacity))                # → '465.7 GiB'  (IEC math)
print(format_size(capacity, binary=False))  # → '500.0 GB'   (matches the label)
```

Switch on `binary` based on context: filesystem reports → IEC,
hardware capacity → SI.

## 6. Build a custom-unit rate

Anything other than `items`, `bytes`, `ops` is treated as a literal
label suffix.

```python
from codechu_fmt import format_rate

format_rate(7.2, unit="frames")    # → '7.2 frames/s'
format_rate(1500, unit="req")      # → '1500.0 req/s'  (no decimal scaling)
format_rate(0.4, unit="msg")       # → '0.4 msg/s'
```

Custom labels do **not** get decimal scaling — `1500` stays as
`1500.0`, not `1.5k`. If you want `1.5k req/s`, scale the value
yourself or use `unit="ops"` and rewrite the suffix.

## See also

- [API reference](API.md) — full signatures and edge-case tables
- [Migration guide](MIGRATION.md) — v0.1 → v0.2 changes
