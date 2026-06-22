---
trdd-id: ab0d98b0-0a00-4233-934c-daf072218587
title: docs and meta accuracy — README facts, agent skill declaration, tests/README
column: complete
created: 2026-06-22T02:40:15+0200
updated: 2026-06-22T03:07:24+0200
current-owner: ampa
assignee: ampa
priority: 4
severity: MEDIUM
effort: S
labels: [docs, readme, agent, accuracy]
task-type: docs
parent-trdd: null
relevant-rules: []
release-via: publish
delivery: direct-push
target-branch: main
test-requirements: [unit]
review-requirements: []
impacts: []
attempts: 1
last-test-result: pass
implementation-commits: [e31a1c6]
---

# TRDD-ab0d98b0 — docs / meta accuracy

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-06-22

**Origin:** the `go-on-yourself` pass. Factual inaccuracies + missing contributor
doc found by the docs-meta audit
(`reports/ampa-audit/20260622_023429+0200-docs-meta.md`). Doc-only; touches
`README.md`, the agent `.md` + `.agent.toml`, and adds `tests/README.md`.

**Current state:** PLANNED. NEXT ACTION: apply the README fixes, make the
kanban-skill decision, add tests/README.md, verify the test suite still passes.

### README factual fixes
- **H3:** `README.md:79` "5 project utility scripts" → **"4"** (only 4 exist; the
  table itself lists 4).
- **M3:** `README.md:90` relabel `test_order_pipeline.py` from the opaque
  "OrderPipeline validation test suite" → **"Tests `publish.py` release-step ordering"**.
- **M4:** `README.md:104-112` the Workflow header says "Steps 14,15,17-19,21-23" but
  the body lists only 14,15,17,19,21,22 (Steps 18 & 23 missing). Reconcile header↔body
  (cross-check `docs/FULL_PROJECT_WORKFLOW.md` for canonical numbers; prefer correcting
  the header to match the real steps, or add the missing entries if they are real).
- **L1:** normalize the Opus generation refs (`README.md:347` "Opus 4.7" vs `:382`
  "Opus 4.8") — the plugin pins no model; make the references consistent.
- **L2:** `README.md:120-122` the "Installation (Production)" fenced block is a bare
  comment stub — either show the real `claude plugin install … --scope local` command
  or fold the restart note into prose and drop the empty fence.

### The kanban-skill agent-declaration decision (M2 + L3)
- **Fact:** `README.md` lists **6** skills (all 6 dirs ship a `SKILL.md`), but the
  agent frontmatter (`agents/ai-maestro-programmer-agent-main-agent.md:6-12`) and
  `ai-maestro-programmer-agent.agent.toml` `[skills]` declare only **5** —
  `ampa-prrd-trdd-kanban` is undeclared on the agent.
- **Decision rule:** the PROGRAMMER agent performs TRDD authoring + kanban column
  transitions as core workflow (e.g. the #7 frozen-CLI kanban work), so the kanban
  skill IS core → **declare it on the agent**: add `ampa-prrd-trdd-kanban` to the
  agent frontmatter `skills:` and to `agent.toml` `[skills]` (secondary). Keep
  README's 6. If on reading the agent it is clearly meant to be model-discovered
  only, instead add a one-line README note — but default to declaring it.
- **L3:** ensure `agent.toml` `[mcp].recommended` and README agree on
  `llm-externalizer` status (README treats it OPTIONAL); make the three meta
  surfaces consistent (don't remove a working recommendation — just align wording).

### Missing contributor doc (M1)
- Add **`tests/README.md`** documenting how to run the suite locally — the exact
  gate `publish.py` runs (`uv run --with pytest pytest tests/ -x -q --tb=short`),
  what each test file guards, and that a non-zero exit means a skill/persona drifted
  from its contract. (Draft content in the audit report §M1.) After TRDD-e4e12416
  lands, also mention `tests/test_smart_exec.py`.

## Acceptance criteria
- Every README claim matches the real tree (script count, labels, workflow steps,
  Opus refs, install command). `tests/README.md` exists and is accurate.
- The 6th skill is consistently represented across README + agent `.md` + `agent.toml`.
- `uv run --with pytest pytest tests/ -x -q` still passes (the primary-skills test
  that counts skills/agent declarations must stay green — update the test if the
  agent skill-count assertion legitimately changes, never weaken it).

## Durable artifacts to read before acting
- `reports/ampa-audit/20260622_023429+0200-docs-meta.md` (all findings + the tests/README draft)

## Approval log
- 2026-06-22T02:40:15+0200 — Authored under `go-on-yourself`. Tier-0 / planned.
