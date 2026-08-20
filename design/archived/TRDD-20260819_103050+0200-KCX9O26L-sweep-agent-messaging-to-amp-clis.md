---
trdd-id: KCX9O26L
title: Sweep bare-name agent-messaging invocations to the frozen amp-* CLIs
column: complete
created: 2026-08-19T10:30:50+0200
updated: 2026-08-20T08:29:45+0200
current-owner: ampa-main-session
task-type: docs
approval-tier: 0
relevant-rules: [1]
external-refs: [ai-maestro 8feccdd9, ai-maestro a24f8726, ai-maestro-orchestrator-agent d5d1588]
---

Hub-dispatched sweep (ai-maestro-fd, 2026-08-19), approved as planned.

## Defect

20 files reference `agent-messaging`. The skill IS real — it ships with
ai-maestro-plugin (verified at
`~/.claude/plugins/cache/ai-maestro-plugins/ai-maestro-plugin/3.1.26/skills/agent-messaging`)
— so this is NOT a phantom-reference sweep and nothing may be deleted on string
presence. The defect is narrower: plugin skills resolve NAMESPACED
(`ai-maestro-plugin:agent-messaging`), so a teaching that tells the agent to
invoke it by BARE NAME as the send mechanism fails at runtime.

Classified by whether the text INVOKES it as the mechanism:

- INVOCATION-shaped (14 sites, the defect):
  - `skills/ampa-orchestrator-communication/SKILL.md` :22,27,32,38,40,48,58,86
  - `skills/ampa-handoff-management/SKILL.md` :53,63,70,72,90
  - `agents/ai-maestro-programmer-agent-main-agent.md` :40,153,162,217,283,288
- PROSE/INFRA reference (6 files, correct as-is): the 3 `docs/` files and the
  op-* references that merely mention messaging in narrative.

## Fix

Per the spec's companion-surfaces NOTE ("teach the CLIs — the .sh form is
canonical — never a bare-name `agent-messaging` skill invocation"):

1. Convert the 14 invocation teachings to the frozen CLIs: `amp-send.sh` for
   sending, `amp-status.sh` for the connectivity probe, `amp-inbox.sh` for
   reading replies, `amp-init.sh` / `amp-identity.sh` for identity.
2. Namespace genuine knowledge pointers to `ai-maestro-plugin:agent-messaging`.
3. No bulk string deletion; prose mentions stay.

## Acceptance

- No file instructs reading or invoking `agent-messaging` by bare name as the
  send/status mechanism.
- Every remaining `agent-messaging` mention is either namespaced or plain prose.
- `uv run pytest tests/ -q` green.

## Scope correction (2026-08-20, at execution)

The original classification undercounted: the op-* reference files were listed
as "prose, correct as-is", but ~90 of their lines are INVOCATION-shaped
("Check your inbox using the `agent-messaging` skill", "Send X using the
`agent-messaging` skill:"). The acceptance criteria govern over the site
count, so all were converted: 14 original sites (5 files) + 15 reference/doc
files. Every replacement idiom was verified against the installed CLIs'
real flag surfaces (`amp-send.sh --reply-to` confirmed via --help; an invented
`amp-inbox.sh --sent` was caught and corrected to an exit-status check before
commit).

## Acceptance evidence (2026-08-20)

- `grep -rn 'agent-messaging' skills agents commands docs README.md CLAUDE.md hooks scripts | grep -v 'ai-maestro-plugin:agent-messaging'` → empty.
- Remaining mentions are all namespaced (9 across 4 files).
- `uv run --with pytest pytest tests/ -q` → 122 passed. (Bare `uv run pytest`
  falls back to a PATH pytest outside the venv and fails on `import yaml` —
  pre-existing env shape, pytest is not a project dep; `--with pytest` is the
  correct invocation, matching how publish.py runs ruff.)

## Approval log

- 2026-08-20T08:29:45+0200 — COMPLETED by ampa-main-session (Tier 0, docs). Hub directive 2026-08-20 (ai-maestro-e7) re-confirmed the sweep; native cross-session `SendMessage` prose audited in the same pass: 0 instructing hits (all mentions are deliberate non-adoption prose, kept).
