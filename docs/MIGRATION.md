# Migration Guide — v0.1 → v0.2

`codechu-fmt` 0.2.0 is a **drop-in replacement** for 0.1.0. The public
API is unchanged: same module path, same function names, same
signatures, same return strings (byte-identical output across the test
suite). The only required action is a version bump.

## Recommended action

Update your dependency constraint:

```toml
# pyproject.toml
dependencies = [
    "codechu-fmt>=0.2.0",
]
```

or

```bash
pip install --upgrade codechu-fmt
```

No source-code changes are required in callers.

## What changed internally

The 0.2.0 release is a refactor with no behavioural delta. Summary:

| Area                     | 0.1.0                                                                | 0.2.0                                                                                  |
| ------------------------ | -------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| NaN guard                | Inline `x != x` duplicated in each module                            | Centralised in private `codechu_fmt._helpers._isnan`                                   |
| Scaling logic            | `format_size` and `format_rate(unit='bytes')` each had their own loop | Shared `codechu_fmt._helpers._scale_to_unit` helper                                    |
| `format_rate` bytes path | Computed via `_iec_to_legacy_bps` string rewrite of the size output  | Computed directly from the shared scaler with the legacy label tuple                   |
| `format_duration`        | Two near-duplicate functions `_format_default` / `_format_compact`   | Single `_format` parameterised on a separator constant                                 |
| Version                  | `0.1.0`                                                              | `0.2.0` (aligned with sibling Codechu libraries)                                       |

## Deprecations

None. No symbol was removed, renamed, or marked deprecated.

## New public symbols

None. The `__all__` of `codechu_fmt` is unchanged:

```python
__all__ = [
    "__version__",
    "format_duration",
    "format_rate",
    "format_size",
]
```

## Private-API note

`codechu_fmt._helpers` is new in 0.2.0 and is **private** by
convention (leading underscore on the module name). Do not import
`_isnan` or `_scale_to_unit` from outside the package — they are not
covered by the SemVer compatibility promise and may change shape in
any future release.

If you previously reached into `codechu_fmt.size._iec_to_legacy_bps`
or similar private helpers (none were documented, but the names were
visible), those identifiers no longer exist. Switch to the public
[`format_rate`](API.md#format_rate) / [`format_size`](API.md#format_size)
functions.

## Test-suite expectations

Existing tests written against 0.1.0 continue to pass against 0.2.0
without modification. Output strings are byte-identical for every
input in the regression set.

## Forward compatibility

The 0.2 line is expected to remain API-stable. Any future
behavioural change will land behind a new keyword argument with a
back-compatible default, or in a major-version bump.
