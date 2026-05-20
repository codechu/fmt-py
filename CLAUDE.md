# CLAUDE.md — codechu-fmt

Bootstrap per `codechu-org/ai/AGENTS.md` §0 before any work. Prefer
the local clone at `$org_home/codechu-org/ai/AGENTS.md` (if
`~/.config/codechu/config.toml` has `org_home` set); otherwise
WebFetch the public raw URL
<https://raw.githubusercontent.com/codechu/codechu-org/main/ai/AGENTS.md>.
This file lists only product-local overrides.

## Product-local notes

- Pure stdlib formatter library. **No** external runtime dependencies.
- Public API: `format_duration`, `format_rate`, `format_size` (and
  nothing else — module internals are not API).
- Output strings are part of the public contract. Changing a format
  string (e.g. `'1m 30s'` → `'1min 30sec'`) is a breaking change.
- Negative values and NaN must always render as `"?"` — never raise.
- Coverage target: ≥90 %.

## Discipline reminders (org rules apply)

- Conventional Commits, no AI signature.
- No `--no-verify`, no force push, no unapproved publish.
- See `codechu-org/ai/AGENTS.md` for the full list.
