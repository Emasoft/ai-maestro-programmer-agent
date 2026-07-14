---
trdd-id: UMRQ84S9
title: Publish the {name}--v{version} dependency-resolution tag atomically with the release
column: complete
created: 2026-07-15T00:14:01+0200
updated: 2026-07-15T00:29:36+0200
current-owner: ai-maestro-programmer-agent
task-type: infra
approval-tier: 0
relevant-rules: [1]
release-via: publish
implementation-commits: [12f64c5, ac53c63]
last-test-result: pass
---

# TRDD-UMRQ84S9 — Publish the `{name}--v{version}` dependency-resolution tag

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-07-15

- **Current state:** `scripts/publish.py` creates and pushes **only** `v{version}`
  (Step 12 `git tag -a v{new_version}`, Step 13 two separate `git push` calls). There is
  **no** `{name}--v{version}` tag anywhere in the pipeline.
- **NEXT ACTION:** add a strict `dependency_resolution_tag()` helper, create the second
  annotated tag in Step 12, and push BOTH refs in ONE `git push --atomic` in Step 13.
  Cover it with `tests/test_publish_dependency_tag.py` (written first).
- **Load-bearing facts / gotchas:**
  - The resolver filters tags by the **manifest `name`** prefix, not the repo name — the two
    can differ, so the tag name MUST come from `.claude-plugin/plugin.json`.
  - `detect_plugin_info()` (publish.py:230) exists but **silently falls back to
    `"unknown"`** on a missing name. Reusing it as-is would push a tag literally named
    `unknown--v1.4.5`. The dep-tag reader must be **strict / fail-fast** — a wrong tag name
    is worse than no tag, because it looks published and resolves for nobody.
  - Do **NOT** call `claude plugin tag <tagname>`: that CLI's positional arg is a **path**,
    not a tag name, so the call silently creates nothing (this is exactly how the fleet lost
    a day — `ai-maestro-programmer-agent#26`).
  - Dry-run returns at publish.py:1412, before Step 11 — so Steps 12-13 are live-only and
    need no `--dry-run` branch of their own.
- **SUPERSEDED — do NOT carry forward:** the original advice in `#26`'s *body* ("drop the
  version pin"). It was **retracted** in that issue's own comments. The pin stays
  (`^2.7.0`, `.claude-plugin/plugin.json:11-15`); the missing **tag** was always the bug.

## Problem

Claude Code resolves a version-constrained plugin dependency by listing the dependency
repo's git tags, **filtering to those starting with `{plugin-name}--v`**, and taking the
highest one satisfying the range (<https://code.claude.com/docs/en/plugin-dependencies.md>,
since CC 2.1.110). A plain `v{version}` tag does **not** match that filter.

So any future plugin that declares a constrained dependency **on this one** would fail to
install with `no git tag satisfying <range>` — against a repo visibly full of tags. That is
a silent, total outage for the dependent, and it is precisely the failure that grounded the
fleet for a day when `ai-maestro-plugin` had the same gap.

Today nothing depends on `ai-maestro-programmer-agent`, so this is **parity work, not a
restart blocker** (confirmed in `ai-maestro-programmer-agent#26`, second comment). It is
cheap to add now and expensive to discover later, from the far side, as an outage.

## Required changes

1. **`dependency_resolution_tag(plugin_root, version) -> str`** — read `name` from
   `.claude-plugin/plugin.json` **strictly**; raise on a missing/blank name. Returns
   `{name}--v{version}`.
2. **Step 12** — after the existing `v{version}` annotated tag, create the dependency tag
   (annotated, same release-notes body).
3. **Step 13** — replace the two sequential pushes with ONE
   `git push --atomic origin HEAD v{version} {name}--v{version}`. Atomic because a release
   that lands with only `v{version}` is *published-but-unresolvable* — the exact
   half-published state that must never exist.
4. **Keep the `v{version}` tag.** GitHub Releases and the marketplace notify chain read it;
   only the resolver reads `{name}--v{version}`. The two coexist.

## Tests (TDD — written before the change)

`tests/test_publish_dependency_tag.py`:
- the tag name is derived from the **manifest**, not the directory name;
- a manifest with no `name` **hard-fails** (no `unknown--v*` tag is ever constructible);
- Step 13's push command carries **both** refs and the `--atomic` flag;
- the plain `v{version}` tag is still created (no regression on the release/notify chain).

## Success criteria

- `uv run --with pytest pytest tests/ -x -q` green (the new file included).
- After the next release, `git ls-remote --tags` shows **both** `v{version}` and
  `ai-maestro-programmer-agent--v{version}` on the release commit.
- `publish.py --dry-run` still exits 0 and mutates nothing.

## Notes

- Reference implementation: `Emasoft/ai-maestro-plugin` PR #25 (read-only; ported, not
  copied wholesale — this repo's push was not atomic before, so the atomic push is part of
  the port).
