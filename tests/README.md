# Tests — codechu-fmt

Run the suite from the repo root:

```bash
pytest -q
```

With coverage:

```bash
pytest --cov=codechu_fmt --cov-report=term-missing
```

## Coverage gate

The coverage floor is **90 %**. PRs that drop below it are rejected;
add tests with your change.

## Conventions

- Edge cases are mandatory: `0`, sub-second / sub-byte, very large
  values (years, TiB), NaN, negative input.
- Output strings are part of the public contract — assert them
  exactly. If you intentionally change a string, that's a
  breaking change and lands in a major version bump.
