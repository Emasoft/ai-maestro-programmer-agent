---
name: op-comprehension-handshake
description: Answer the task-comprehension handshake (all 5 points) before any coding starts
parent-skill: ampa-orchestrator-communication
---

# Task-Comprehension Handshake — answer template

> **Token rule**: Write all command output to a report file. Return only a 2-3
> line summary + file path to the caller.

The task-comprehension handshake is the first dialog loop (loop (a)) of the
corrected workflow model. AMOA asks its question set with the assignment; the
assigned MEMBER must answer **ALL FIVE points** before coding starts. A bare
"Task received" ACK is forbidden — it confirms delivery, not understanding,
and misunderstandings caught here cost a message; caught after implementation
they cost the whole implementation (R6 v3 / #17 M7a).

## When to Use

- Immediately after validating a task assignment
  (`op-receive-task-assignment`, Step 1.5) — BEFORE any code is written.
- Whenever AMOA re-issues or substantially revises an assignment mid-flight
  (re-answer the handshake for the revised scope).

## Procedure

1. **Read the full assignment** (and its TRDD if referenced) before answering.
2. **Compose the five answers** (template below). Be concrete — paths, not
   "the relevant files"; named risks, not "some risks".
3. **Send to AMOA** via the `agent-messaging` skill and **WAIT** for
   confirmation. Do not start coding while waiting.
4. **On confirmation** — begin work (`op-parse-task-requirements` onward).
5. **On correction** — AMOA fixes your restatement / answers the ambiguity;
   re-confirm the corrected understanding, then begin.
6. **If an ambiguity is a design flaw** — AMOA routes it to AMAA (design
   revision or new TRDDs). Wait for the revised assignment; never improvise
   around a design flaw.

## Answer template (MEMBER → AMOA)

- **Recipient**: your assigned orchestrator agent (AMOA)
- **Subject**: `HANDSHAKE: <TASK_ID> — comprehension answer`
- **Type**: status
- **Priority**: normal
- **Content**:

```text
1) RESTATE — <the task in your own words: what changes, where, and why —
   not a copy of the assignment text>
2) FILES/DOMAINS — <the paths, modules, configs, schemas you will touch>
3) AMBIGUITIES — <each underspecified point as a concrete question;
   or "none identified">
4) RISKS — <what could go wrong: regressions, API drift, data migration,
   coupling to in-flight work>
5) NPT/EHT — NPT: <prerequisite tasks that must complete first, or "none">;
   EHT: <effect-handling tasks the change implies: update callers, docs,
   downstream consumers, re-test suites>

Awaiting your confirmation before starting work.
```

## Reply semantics (AMOA → MEMBER)

| Reply | Meaning | Your next action |
| ----- | ------- | ---------------- |
| **CONFIRMED** | Understanding matches the intent | Begin work |
| **CORRECTED: \<fix\>** | Restatement or scope was off | Acknowledge the corrected understanding, then begin |
| **ANSWERS: \<…\>** | Your ambiguity questions answered | Fold the answers in, re-confirm, begin |
| **BACK-TO-ARCH: \<reason\>** | An ambiguity exposed a design flaw | Wait — AMAA revises the design / authors new TRDDs; re-handshake on the revised assignment |

## Example

- **Subject**: `HANDSHAKE: TRDD-9a8aba94 — comprehension answer`
- **Content**: "1) RESTATE: add retry-with-backoff and an idempotency key to
  the order pipeline's `process()` so transient gateway failures no longer
  drop orders. 2) FILES: src/orders/pipeline.py, src/orders/idempotency.py
  (new), tests/orders/. 3) AMBIGUITIES: max retry count — 3 or configurable?
  4) RISKS: changes `process()`'s public signature; downstream `BatchRunner`
  calls it positionally. 5) NPT: none; EHT: update BatchRunner call sites +
  docs/orders.md + extend the e2e order suite. Awaiting your confirmation
  before starting work."

**Verify**: confirm the handshake answer appears in your sent messages; do not
write code until AMOA replies.

## Error Handling

| Error | Cause | Resolution |
| ----- | ----- | ---------- |
| No AMOA reply within the team's handshake timeout | AMOA busy / offline | Re-send once; if still none, report the blocker to AMCOS — do **not** start coding unconfirmed |
| Assignment too vague to restate | Underspecified task | Make point 3 the headline: list the questions; AMOA must resolve them before confirmation |
| You already started coding before the handshake | Gate skipped | Stop, send the handshake now, reconcile any divergence AMOA flags before continuing |
