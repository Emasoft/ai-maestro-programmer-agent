---
trdd-id: IUJ75HDL
title: Realign AMPA to Claude Code v2.1.224 and AI Maestro CORE v3.0.5
column: published
created: 2026-08-08T10:24:12+0200
updated: 2026-08-08T10:32:00+0200
current-owner: ai-maestro-programmer-agent
task-type: bugfix
scope: project
project-id: ai-maestro-programmer-agent
min-approval-requirement: none
mandate: true
mandated-by: self
relevant-rules: [1]
delivery: direct
release-via: publish
impacts: [plugin-manifest, skills, agent-definition, docs, tests]
test-requirements: [pytest, ruff, cpv-strict]
npt: []
eht: []
implementation-commits: [1f67a5e, ac0809c, da26fd3]
released-as: v2.0.0
---

# Realign AMPA to Claude Code v2.1.224 and AI Maestro CORE v3.0.5

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-08-08

- **Six skills**: `context: fork`, `agent:`, `disable-model-invocation:` REMOVED. DONE.
- **`plugin.json`**: dependency `ai-maestro-plugin` `^2.7.0` → `^3.0.5`. DONE.
- **Agent body**: nesting facts corrected; single-layer fan-out policy added. DONE.
- **README**: compatibility re-anchored to v2.1.224; two false nesting claims removed;
  new v2.1.184–v2.1.224 table added. DONE.
- **Tests**: 4 platform-contract guards added to `tests/test_primary_skills.py`. 107 pass.
- **SHIPPED**: `v2.0.0`, remote `main` at `da26fd3`, GitHub release live. MAJOR because the
  CORE dependency floor moved to 3.x — a consumer on CORE 2.x can no longer satisfy it.
- **NEXT ACTION**: none for this card. Open follow-up, tracked separately: the ai-maestro
  session was asked for `design/specs/role-plugins-spec.md` (branch `governance-rules`); if it
  constrains role-plugin frontmatter/manifest, a follow-up TRDD may be needed.
- **Gate note (load-bearing)**: `publish.py` rewrites `.githooks/pre-push` from
  `PRE_PUSH_HOOK_TEMPLATE` at step 0.5, BEFORE the validate gate. A fix applied only to the
  generated file is silently reverted on the next publish. Always fix both; they are asserted
  byte-identical.
- **SUPERSEDED — do NOT carry forward**: the "add `background: false` to the six skills"
  fix. It is wrong here; see "Why not `background: false`" below. Several fleet peers
  requested exactly that — the request is understandable but the premise does not hold
  for an AMP-coupled skill.

## Why

AMPA was authored against Claude Code v2.1.183 and CORE `^2.7.0`. Claude Code is now
v2.1.224 and CORE is v3.0.5. Three defects resulted, none of which produced an error,
a warning, or a failing test:

1. **v2.1.218 flipped `context: fork` skills to background by default.** All six
   `ampa-*` skills declared `context: fork` and none declared `background:`. From
   v2.1.218 they returned an agent handle instead of their result: the invoking agent
   received **nothing** in the turn that asked for it.
2. **`disable-model-invocation: true` excludes a skill from subagent preload.** All six
   set it, while the agent's `skills:` field listed all six — so the preload was inert
   and the role agent booted without its own operating procedures in context.
3. **The CORE dependency `^2.7.0` cannot resolve to the shipped CORE (3.0.5).** A caret
   range on 2.x never matches 3.x.

## Why not `background: false` (the fix that was asked for, and rejected)

Pinning `background: false` restores in-turn delivery but leaves a deeper defect intact.
Verified by reading the skill bodies, not by grep:

- `ampa-task-execution:37` — step 1 is "Read the AI Maestro message"; `:57-60` requires
  pausing on an inbound AMP message and resuming.
- `ampa-prrd-trdd-kanban:58-61` — a prerequisite is "A TRDD assigned to **this session**
  … received via an AMP notification **directly from your ORCHESTRATOR**".
- `ampa-orchestrator-communication` — the whole skill is AMP send/receive.
- `ampa-github-operations:50` — step 8 is "Notify AMOA".

And this repo's own agent definition states: *"Any subagents you spawn via the Agent tool
CANNOT send AMP messages at all. They have no AMP identity."*

So a forked copy — foreground **or** background — can never complete any of these
procedures. Separately, `agent:` named this same agent, making every invocation a
self-recursive fork counting against the depth cap. The correct fix is to remove
`context: fork` and `agent:` so the procedures run inline.

Net effect on the fleet's "unpinned fork skills" metric is the same or better: with zero
`context: fork` there is nothing left to pin.

## Evidence for the CORE bump

The CHANGELOG upstream ships only its newest section, so release notes are the available
evidence:

- All 10 `ama-*` skills AMPA references still exist in CORE v3.0.5 (`skills/` listing +
  CORE README table) — no renames.
- CORE v3.0.0 release notes contain **no** BREAKING section; the major bump is fixes and
  documentation.

## Claims checked and REFUSED (do not re-encode)

Two claims arrived from a peer session with a citation. Both failed first-hand
verification, and the peer subsequently confirmed both corrections:

- **`R42.8`** — cited as a USER grant. `Emasoft/ai-maestro#125` is **OPEN** and titled
  "R42 amendment **request**". A pending request, not ratified governance. The cited
  source is the document that disproves the claim.
- **`ama-unblock`** — cited as a new CORE skill. Not present in CORE v3.0.5; it exists
  only in an unpushed local tree.

Lesson recorded: a citation is a claim *about a document*; passing one on without opening
it converts one agent's error into everyone's.

## Native cross-session messaging — considered, not adopted

Claude Code v2.1.224 extended `SendMessage` to reach sessions on other machines and added
`ListAgents`. AMPA does **not** adopt it for role-to-role traffic. It is not unsafe —
relayed messages have carried no user authority since v2.1.166 and are classifier-evaluated
before dispatch since v2.1.222 — but it carries no AI Maestro AID, so a message has no
verifiable author, no R6 routing, and no audit entry. Choosing the fleet's transport is
governance (Tier 2/3), not a role plugin's decision. AMP remains the governed channel.

## Acceptance criteria

- [x] No `ampa-*` skill declares `context:`, `agent:`, or `disable-model-invocation:`.
- [x] The agent's `skills:` preload resolves to six skills that exist and are preloadable.
- [x] `plugin.json` depends on `ai-maestro-plugin ^3.0.5`; no `2.7` string survives.
- [x] No document claims a 5-level nesting depth.
- [x] README states verification through v2.1.224 and marks the two breaking changes.
- [x] Regression guards fail if `context: fork`, an inert preload, or a `:` in a name returns.
- [x] `pytest tests/ -q` green (107 passed).
- [x] `ruff check .` green.
- [x] `publish.py` gate green (CRITICAL=0 MAJOR=0 MINOR=0 NIT=0); tagged `v2.0.0` +
      `ai-maestro-programmer-agent--v2.0.0`, pushed atomically, GitHub release created.
- [x] Remote re-measure: zero `context: fork` on the published branch.

## Approval log

- 2026-08-08T10:24:12+0200 — Tier-0 self-mandate (in-scope repair of this plugin's own
  defects). USER authorized implement + push + publish in-session.
- 2026-08-08T10:31:00+0200 — PUBLISHED as v2.0.0 (`da26fd3`). Gate green on the second
  attempt; the first was blocked by two shellcheck MINORs in `.githooks/pre-push`, fixed in
  both the generated file and its generating template (`ac0809c`).
