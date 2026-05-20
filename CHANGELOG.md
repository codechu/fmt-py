# Changelog

[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) + [SemVer](https://semver.org/).

## [Unreleased]

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
