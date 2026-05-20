# Changelog

[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) + [SemVer](https://semver.org/).

## [Unreleased]

## [0.3.0] — 2026-05-20

### Added
- `format_bitrate(bps, *, precision=1)` — SI 1000-based bits-per-second
  ladder (`bps`, `Kbps`, `Mbps`, `Gbps`, `Tbps`, `Pbps`) for networking
  UIs.
- `format_percent(ratio, *, precision=1, locale="en")` — 0-1 ratio →
  percent string, locale-aware. Supports `"en"` (dot decimal, trailing
  `%`) and `"tr"` (comma decimal, leading `%`). Unknown locales fall
  back to `"en"`.
- `format_compact(n, *, precision=1)` — large numbers → short SI-prefix
  form `K`/`M`/`B`/`T` (English engineering convention) for dashboards
  and counters.
- `format_duration` now renders sub-millisecond values with `µs`
  (microseconds) and `ns` (nanoseconds) in both default and compact
  forms.

### Changed
- **Breaking**: negative inputs now render with a leading `-` prefix
  across all formatters instead of `"?"`. `format_size(-1024)` →
  `"-1.0 KiB"`, `format_rate(-5)` → `"-5.0/s"`, `format_duration(-90)`
  → `"-1m 30s"`. Makes size/rate/duration *deltas* readable.
- NaN handling for the original three formatters (`format_size`,
  `format_rate`, `format_duration`) is unchanged — still `"?"`. New
  v0.3 formatters use `"NaN…"`-style strings; see the README parity
  table.

## [0.2.0] — 2026-05-20

### Changed
- Internal refactor only — public API unchanged.
- Consolidated duplicated `_isnan` NaN guard into a private
  `codechu_fmt._helpers` module.
- Replaced the fragile `_iec_to_legacy_bps` string rewrite in
  `format_rate(unit='bytes')` with a shared `_scale_to_unit` helper —
  size and rate now share scaling logic without coupling on the
  formatted string.
- Collapsed near-duplicate `_format_default` / `_format_compact` in
  `duration.py` into a single `_format` function parameterised on a
  separator. Output is byte-identical.
- Version aligned with sibling libs (no breaking changes).

## [0.1.0] — 2026-05-20

### Added
- Initial extraction from [codechu/cli-py](https://github.com/codechu/cli-py)
- `format_duration(seconds, *, compact=False)` — default + compact forms,
  sub-second through years, NaN/negative guards
- `format_rate(units_per_sec, *, unit, precision)` — `items` / `bytes`
  (IEC binary) / `ops` (decimal-scaled) / custom unit labels
- `format_size(num_bytes, *, binary, precision)` — IEC (`KiB`/`MiB`/…)
  or SI (`kB`/`MB`/…) scaling
