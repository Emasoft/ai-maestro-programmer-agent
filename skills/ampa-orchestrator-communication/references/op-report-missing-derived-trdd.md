---
name: op-report-missing-derived-trdd
description: Report a missing derived TRDD (NPT/EHT) to the sender and author it — the MEMBER missing-derived duty
parent-skill: ampa-orchestrator-communication
---

# Report a missing derived TRDD (NPT/EHT) — report-to-sender + author template

> **Token rule**: Write all command output to a report file. Return only a 2-3
> line summary + file path to the caller.

A MEMBER that receives an assigned TRDD and judges a required **derived** TRDD —
a Necessary Prerequisite Task (NPT) or an Effects-Handling Task (EHT) — to be
**missing** MUST NOT silently execute the parent and leave the gap. Landing the
change while an EHT is absent leaves the wound open. This op is the two-part duty:
**report it to the sender**, and **author the missing derived TRDD** yourself.
(AI-Maestro ruling Emasoft/ai-maestro#61, Q1.)

## When to Use

- You are the assignee of a TRDD in `dev`, and while answering the comprehension
  handshake (loop a) or during implementation (loop b) you find a prerequisite or
  a consequence that has no TRDD behind it.
- The parent TRDD's `npt:` / `eht:` lists omit a task the work actually needs.

## Part 1 — Report to the sender (ORCHESTRATOR, direct edge)

Send ORCH a `MISSING-DERIVED` note (R6 v3: ORCH ↔ MEMBER is a direct edge):

```text
Subject: MISSING-DERIVED — TRDD-<parent-id8> needs a <NPT|EHT>
Body:
  Parent: TRDD-<parent-id8> (<title>)
  Missing: <one line — what prerequisite/consequence has no TRDD>
  Why it blocks/harms: <the concrete gap if left unhandled>
  My action: authoring it as <self-mandate | proposal> (see Part 2), id TRDD-<new-id8>.
```

Reporting is informational — it does not wait for approval when Part 2 is a
self-mandate. It DOES wait when Part 2 is a proposal past your authority.

## Part 2 — Author the missing derived TRDD

Decide the path by the derived task's objective floor:

- **Inside your slice (floor = `none`)** → author it directly via `ama-trdd-write`
  as a **self-mandate** into `design/tasks/`:

  ```yaml
  column: planned
  min-approval-requirement: none
  mandate: true
  mandated-by: self
  ```

  It is born approved. Link it to the parent (`blocked-by:` / the parent's
  `npt:`/`eht:` via `ama-trdd-update`).

- **Past your authority** (GOLDEN PRRD, `.github/`, cross-repo source, a release) →
  author it in `design/proposals/` with `min-approval-requirement:` set to the
  required approver (`chief-of-staff` / `manager` / `user`) and route it via your
  COS. Do NOT self-approve it.

## Output

- One `MISSING-DERIVED` AMP note to ORCH.
- One new derived TRDD (self-mandate in `design/tasks/`, or proposal in
  `design/proposals/`), linked to the parent.
- A 2-3 line summary + the new TRDD id back to the caller.

## Error Handling

- Uncertain whether the derived task is inside your slice → treat it as past your
  authority and route the proposal (conservative: better a needless COS round-trip
  than a self-approved out-of-scope task).
- The parent TRDD is terminal/frozen → do NOT edit it; author the derived TRDD
  standalone and cite the parent in its body.
