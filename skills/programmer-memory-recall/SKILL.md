---
name: programmer-memory-recall
description:
  Recall durable project memories from a SYMPTOM before debugging, designing,
  or acting on a recurring problem. Searches the project's markdown memory
  notes with memgrep (plain-grep fallback when absent). Use when you think
  "have we hit this before?", or the user says "recall memories about X",
  "did we already solve this", "check what we learned about Y". Trigger with
  /programmer-memory-recall.
license: MIT
compatibility: Works without memgrep (grep fallback). memgrep optional.
metadata:
  author: AI Maestro
  version: 1.0.26
  workflow-instruction: "support — recall before debugging/designing"
  procedure: "proc-memory-recall"
---

# Programmer memory-recall

## Overview

Recall is the FIRST step before debugging a recurring problem, making a design
decision, or starting a task that smells familiar — "have we hit this
before?". It searches the project's curated markdown memory notes (the
`memory/` dir the harness maintains) and returns the notes whose
`description`/`title`/`tags` best match your SYMPTOM. The answer is in the
matched note's body.

This is distinct from conversation/transcript search: it recalls *curated,
symptom-indexed notes*, not raw chat history.

**The one law**: query with the SYMPTOM — the user's words, the error text,
the problem — NOT the answer's jargon. A note is findable from the symptom
because its author put symptom vocabulary in `description`. (Query "keychain"
and you only find the note once you already know the answer; query "rotator
failed, had to log in" and you find it from the problem.)

## Prerequisites

- A project memory dir (the harness per-project notes dir, or a project-local
  `memory/` folder). If neither exists there is nothing to recall yet.
- `memgrep` on PATH is OPTIONAL — without it the skill degrades to plain
  `grep` and still works.

## Instructions

1. Resolve the project memory dir (the harness per-project notes dir):

   ```bash
   MEMDIR="$HOME/.claude/projects/$(pwd | sed 's#/#-#g')/memory"
   # If that path doesn't exist, fall back to a project-local memory/ dir:
   [ -d "$MEMDIR" ] || MEMDIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)/memory"
   ```

2. Build a SYMPTOM query from the user's words / the error / the problem
   (never the answer's jargon), then recall — memgrep if present, plain grep
   otherwise:

   ```bash
   SYMPTOM="the symptom in the user's / the error's words"
   if command -v memgrep >/dev/null 2>&1; then
     memgrep recall "$SYMPTOM" "$MEMDIR"        # notes ranked best-first: path — description
   else
     grep -rliE "$SYMPTOM" "$MEMDIR" 2>/dev/null # fallback: degrade, never break
   fi
   ```

   If `memgrep` is not installed, it can be installed once from a checkout of
   the `ai-maestro-janitor` repo:
   `cargo install --path <ai-maestro-janitor>/tools/memgrep` — until then the
   grep fallback works on note frontmatter + bodies.

3. Read the top 1-3 notes the recall returns; the fact you need is in their
   bodies. Read each note WHOLE — including its `[^N]` lessons (memgrep
   appends them by default; `--no-notes` suppresses, `--full-notes` keeps the
   lessons' `[ocd:… lmd:…]` metadata prefixes).

4. If recall returns nothing, the memory doesn't exist yet — solve the
   problem, then capture it with `/programmer-memory-write`.

Useful memgrep refinements (verify with `memgrep recall --help`):
`--sort score|ocd|lmd`, `--order asc|desc`, `--since`/`--until` (date
window), `--top N`; `memgrep find "+TERM -TERM" "$MEMDIR"` for keyword
search, `--only-notes` to search only the lessons.

## Output

A short ranked list of `path — description` lines (memgrep) or matching
paths (grep fallback), best first. Read the top few; do NOT dump full note
bodies into the conversation — open the one you need.

## Error Handling

| Condition                  | Action                                                       |
| -------------------------- | ------------------------------------------------------------ |
| Memory dir missing         | Nothing to recall — proceed; consider writing notes later    |
| memgrep absent             | Use the grep fallback (built into step 2) — never block      |
| No notes match the symptom | Memory doesn't exist yet — solve, then write it              |
| grep exits non-zero        | Exit 1 = no match (normal); >1 = report the error, continue  |

## Examples

<example>
User: this publish failed again with a stale lockfile — didn't we fix this?
→ recall "publish failed stale lockfile" → surfaces the uv.lock staging note;
  read it whole (fact + lessons) before re-deriving the diagnosis.
</example>

<example>
User: recall what we learned about the flaky pipeline last week
→ memgrep recall "flaky pipeline" "$MEMDIR" --since 2026-06-01 --sort lmd
  → recent notes, newest-modified first, lessons appended.
</example>

## Scope

ONLY searches + surfaces existing memory notes (read-only). Does NOT write
notes (use `/programmer-memory-write`). Degrades to plain grep when memgrep
is absent; never blocks on a missing binary.

## Resources

- [rules/memory-protocol.md](../../rules/memory-protocol.md) — the recall
  protocol (the law, the schema, the read-the-notes rule, the dual-test
  method).
- **`programmer-memory-write`** — the WRITE side (authoring + the correction
  protocol).

## Related

- **ampa-task-execution** — recall before Step 4 (implement) when the task
  smells familiar; recall the error text before debugging a failing test.
- **ampa-handoff-management** — handoffs transfer session state; memories
  transfer durable facts. Different lifetimes, complementary.
