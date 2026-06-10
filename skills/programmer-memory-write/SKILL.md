---
name: programmer-memory-write
description:
  Capture a durable fact as a symptom-indexed markdown memory note. Use after
  solving a non-trivial bug (bug-autopsy gotcha), learning a project
  constraint, or when the user says "remember this", "save a memory",
  "capture this gotcha", "note that for next time". Writes a schema-valid
  note plus the MEMORY.md index line. Trigger with /programmer-memory-write.
license: MIT
compatibility: Works without memgrep (duplicate-check degrades to grep).
metadata:
  author: AI Maestro
  version: 1.0.26
  workflow-instruction: "support — bug-autopsy + durable-fact capture"
  procedure: "proc-memory-write"
---

# Programmer memory-write

## Overview

Capture one durable fact as a memory note so a future session — which will
have the SYMPTOM, not the answer — can recall it. The load-bearing decision is
the `description`: it MUST carry the words the problem will present with (the
user's words, the error, the symptom), because recall ranks on `description`
(+ `title` + `tags`). Put the symptom in `description`; put the answer in the
body.

Only capture what is NON-OBVIOUS and reusable: gotchas, constraints not in
the code, confirmed preferences, hard-won debugging facts. Do NOT capture
what the repo already records (code structure, git history, CLAUDE.md) or
what only matters to the current conversation.

**Bug Autopsy wiring**: after fixing a non-trivial bug, the WHY of the bug is
exactly the kind of fact this skill captures — write it with the error text /
symptom in the description so the next session finds the guardrail from the
failure, not from the fix's jargon.

## Prerequisites

- A durable, reusable fact worth capturing (one fact per note).
- Write access to the project memory dir (created if missing).

## Instructions

1. Resolve the memory dir (same as recall):

   ```bash
   MEMDIR="$HOME/.claude/projects/$(pwd | sed 's#/#-#g')/memory"
   [ -d "$MEMDIR" ] || MEMDIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)/memory"
   mkdir -p "$MEMDIR"
   ```

2. Choose `type` ∈ `user | feedback | project | reference` and a kebab slug
   (prefix the slug with the type, e.g. `feedback_…`, `reference_…`).

3. Check for an existing note that already covers this (update it rather than
   duplicate):

   ```bash
   if command -v memgrep >/dev/null 2>&1; then
     memgrep recall "<symptom>" "$MEMDIR"
   else
     grep -rliE "<symptom>" "$MEMDIR" 2>/dev/null
   fi
   ```

4. Write `"$MEMDIR/<type>_<slug>.md"` with the Write tool (NOT echo), schema:

   ```yaml
   ---
   name: <type>_<slug>
   description: "<the SYMPTOM in the user's / the error's words — the words a future session will search with, NOT the answer's jargon>"
   metadata:
     node_type: memory
     type: <user|feedback|project|reference>
   ---
   <the one fact. For feedback/project, follow with **Why:** and **How to apply:** lines.
   Link related notes with [[their-name]].>
   ```

5. Append a one-line pointer to `"$MEMDIR/MEMORY.md"` (create if missing).
   Each index line is a markdown-link bullet: a dash, the note title in
   square brackets, the note filename (`TYPE_SLUG.md`) in round parentheses
   placed immediately after the closing bracket (together they form a
   standard markdown link), then an em-dash and a one-line hook.

6. Sanity-check: would a future session, having only the SYMPTOM, find this
   note by searching `description`? If the description reads like the
   *answer*, rewrite it to read like the *question*.

## Correcting a memory — the 2-step non-destructive protocol

When a new discovery CONTRADICTS an existing memory, change it
non-destructively, in exactly two steps:

1. **Clean the fact in place.** Replace the wrong statement in the body with
   the correct one, so the page's record of the FACTS is always clean and
   true — no "we used to think X" clutter inline. The body is the current
   truth.
2. **Demote the error to a lesson — the WHY is the point.** Record the error
   that caused the false memory as a numbered footnote in a `## Notes and
   lessons learned` section at the BOTTOM of the page, and connect the
   corrected fact to it with a standard-markdown footnote `[^N]`. The
   load-bearing content is *why* the previous statement was wrong — the root
   cause, not merely "this was wrong". A lesson without a WHY cannot stop the
   next repeat.

This mirrors the Bug Autopsy directive (every fixed bug becomes a guardrail):
the *fact* is corrected, the *error* is never deleted — it is demoted to a
linked lesson so future readers don't repeat it.

Lesson format — standard markdown footnotes with per-element dates in a
leading `[…]` prefix (**OCD** = Original Creation Date, **LMD** = Last
Modified Date; these, not the file mtime, are the authoritative age):

```markdown
The widget retries 3× then fails.[^3] Tune via the `max_retries` config key.

## Notes and lessons learned
[^3]: [ocd:2026-06-09 lmd:2026-06-09] earlier this page said "retries 5×" —
  wrong, the cap is 3. The error: the constant was read off the guessed
  variable name `max_attempts` instead of the actual key `max_retries`.
  Lesson: verify a constant against the SOURCE, not a guessed name.
```

## Output

One note file + one MEMORY.md index line. Report the note path and the
one-line description; do NOT echo the whole note back into the conversation.

## Error Handling

| Condition                       | Action                                              |
| ------------------------------- | --------------------------------------------------- |
| Memory dir not writable         | Report the path + error; do not silently skip       |
| Existing note covers the fact   | Update that note (correction protocol) — no duplicate |
| Description reads like the answer | Rewrite it to read like the question before saving |

## Examples

<example>
After fixing a flaky pipe-truncation bug:
  description: "command output looks truncated / wrong line count when piping through tee | head"
  body: explains the SIGPIPE-kills-tee mechanism + the capture-to-file-first fix.
</example>

<example>
User: remember that this project pins ruff line-length to 320
  → type: project; description carries "lint fails on long lines / what
    line-length does this project use"; body records the 320 pin + where.
</example>

## Scope

ONLY authors/updates memory notes + the MEMORY.md index. Does NOT recall
(use `/programmer-memory-recall`). One fact per note. Symptom-indexed
description is mandatory — it is what makes the note recallable.

## Resources

- [rules/memory-protocol.md](../../rules/memory-protocol.md) — the protocol
  (the law, schema, lessons-learned conventions, dual-test method).
- The harness `# Memory` directive — the authoring source-of-truth this
  skill follows.
- **`programmer-memory-recall`** — the RECALL side (find a note before you
  duplicate or correct it).

## Related

- **ampa-task-execution** — Step 7 (report completion) is a natural moment
  to capture any bug-autopsy gotcha the task surfaced.
- **ampa-handoff-management** — handoffs carry session state; memories carry
  durable facts. Write both when pausing non-trivial work.
