---
name: publish-dependency-resolution-tag
description: "a plugin that declares a version-constrained dependency on THIS one fails to install with 'no git tag satisfying <range>' against a repo full of tags — why, and the {name}--v{version} tag that fixes it"
ocd: 2026-07-15
lmd: 2026-07-15
metadata:
  node_type: memory
  type: project
  tier: component
  functionality: architecture
publish-globally: false
---
Claude Code (≥ 2.1.110) resolves a **version-constrained plugin dependency** by listing the
dependency repo's git tags, **filtering to those whose name starts with `{plugin-name}--v`**
(the name comes from the dependency's manifest, not its repo/dir name), and taking the
highest one satisfying the declared range
(<https://code.claude.com/docs/en/plugin-dependencies.md>). A plain `v{version}` tag does
**not** match that filter.

So a repo that tags releases only `v{version}` is **unresolvable** as a constrained
dependency: every dependent fails to install with `no git tag satisfying <range>` — against
a repo visibly full of tags. It looks like an upstream CC bug; it is a **spec requirement the
publisher never met**. This exact gap on `ai-maestro-plugin` grounded the AI-Maestro fleet
for a day (`ai-maestro-programmer-agent#26`).

**The fix (shipped v1.4.5, `TRDD-UMRQ84S9`, commit `12f64c5`):** `scripts/publish.py`
Step 12 creates the dependency tag **alongside** `v{version}` (both annotated, same
release-notes body) and Step 13 pushes all three refs in **one** transaction:
`git push --atomic origin HEAD v{version} {name}--v{version}`.

Load-bearing facts (each cost thought to get right):
- **The tag name is read STRICTLY from `.claude-plugin/plugin.json`** by
  `dependency_resolution_tag()`, which **raises** on a missing/blank name. It deliberately
  does NOT reuse `detect_plugin_info()`, whose `"unknown"` fallback would push a tag named
  `unknown--v1.4.5` — published, resolvable by nobody. A missing tag fails loudly; a
  wrongly-named one fails silently.
- **Both tags coexist by design.** GitHub Releases + the marketplace notify chain read
  `v{version}`; only the CC resolver reads `{name}--v{version}`.
- **The dep tag triggers NO workflow.** `release.yml` fires on `v*.*.*` and `validate.yml`
  has no tag trigger at all, so `ai-maestro-programmer-agent--v1.4.5` (starts with `a`)
  matches neither — exactly one Release run fires, for `v{version}`. Verified on the v1.4.5
  push: both tags on origin pointing at the same release commit, all three CI runs green.
- **Never `claude plugin tag <name>`** — that CLI's positional arg is a **path**, not a tag
  name, so the call silently creates nothing (the trap that cost the fleet the day).
  `tests/test_publish_dependency_tag.py` pins it shut.
- **The version pin stays.** `#26`'s original "drop the pin" advice was **retracted** in its
  own comments; the pin (`^2.7.0`) protects this plugin from a breaking core release, and the
  missing **tag** — not the pin — was always the bug.

## See also
- [[publish-changelog-generation]] — the other publish.py Step-10/12 gotcha (git-cliff).
- [[publish-ci-vs-dryrun]] — why a local-green publish gate is not the same as CI-green.

## Notes and lessons learned
[^1]: [ocd:2026-07-15 lmd:2026-07-15] The symptom (`no git tag satisfying <range>` on a repo
  full of tags) screams "upstream resolver bug" and the first fleet-wide diagnosis said
  exactly that, prescribing "drop the version pin". Both were wrong. Lesson: when a resolver
  reports "no matching X" against a store that visibly HAS X, suspect a **naming/filter**
  mismatch (the resolver is looking for a differently-shaped name) before an upstream bug —
  and read the tool's own spec for the exact name shape it filters on.
