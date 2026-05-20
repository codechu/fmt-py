# Changelog

[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) + [SemVer](https://semver.org/).

## [Unreleased]

## [0.1.0] — 2026-05-20

### Added
- Initial extraction from [codechu/cli-py](https://github.com/codechu/cli-py)
- `format_duration(seconds, *, compact=False)` — default + compact forms,
  sub-second through years, NaN/negative guards
- `format_rate(units_per_sec, *, unit, precision)` — `items` / `bytes`
  (IEC binary) / `ops` (decimal-scaled) / custom unit labels
- `format_size(num_bytes, *, binary, precision)` — IEC (`KiB`/`MiB`/…)
  or SI (`kB`/`MB`/…) scaling
