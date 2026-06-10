# Markdown memory — the PROGRAMMER's recall + write protocol

The harness `# Memory` directive (injected each session) tells you how to
**WRITE** memories. This rule is the missing half for the PROGRAMMER (AMPA)
role: how to **RECALL** them, the **discipline** that makes recall work, and
the **tool** (`memgrep`) that powers it. Together they are "the memory
system": authoring (directive + `programmer-memory-write` skill) + recall
(this rule + `programmer-memory-recall` skill) + the search tool (memgrep) +
the note corpus.

This recalls **curated, symptom-indexed markdown notes** in the project's
`memory/` dir — NOT conversation/transcript history. Transcript search and
note recall are different systems.

## The one law that makes memory work: index by the QUESTION, not the answer

A memory is found from the SYMPTOM, not the solution. When you write a note,
its `description:` (and `title`/`tags`) MUST carry the words a future session
will have when the problem RECURS — the user's words, the error text, the
symptom — NOT the jargon of the fix.

- WRONG `description`: "OAuth creds live in the macOS keychain services".
  (Findable only if you already know the answer is "keychain".)
- RIGHT `description`: "rotator failed, had to log in manually — where are the
  creds / why did the swap fail" + the keychain fact in the BODY.

Two-hop recall: a symptom query lands you on the note; the note's BODY gives
the answer. The `description` is the load-bearing surface — `memgrep recall`
ranks on `description + title + tags` ONLY (the `metadata.type` taxonomy does
NOT affect ranking). Put symptom vocabulary in `description`; put the answer
in the body.

## Recall BEFORE acting (the protocol)

Before debugging a recurring problem, making a design decision, or starting a
task that smells familiar, RECALL first — "have we hit this before?". Cheap,
and it's the whole point of having a memory.

```bash
# memdir is the harness per-project memory dir:
MEMDIR="$HOME/.claude/projects/<project-slug>/memory"   # slug = project path, dashed
SYMPTOM="the user's words / the error / the symptom"     # NOT the answer's jargon

if command -v memgrep >/dev/null 2>&1; then
  memgrep recall "$SYMPTOM" "$MEMDIR"      # notes ranked best-first as: path — description
else
  grep -rliE "$SYMPTOM" "$MEMDIR"          # fallback: plain grep, degrade-not-break
fi
```

Read the top 1-3 notes the recall returns; the answer is in their bodies. If
recall returns nothing, the memory doesn't exist yet — solve the problem,
then capture it (per the `# Memory` directive and the
`programmer-memory-write` skill).

## PROGRAMMER workflow wiring (when AMPA recalls and writes)

- **Recall before debugging.** On receiving a bug, a failing test, or a
  recurring error, run `programmer-memory-recall` with the SYMPTOM before
  re-deriving the diagnosis — a past session may have written the answer.
- **Recall before design decisions.** Before choosing an approach for an
  assigned task, recall the task's domain words — prior constraints and
  user preferences may already be recorded.
- **Write after a non-trivial fix (Bug Autopsy).** Per the Bug Autopsy
  discipline, after fixing a non-trivial bug capture WHY it happened as a
  memory note (`programmer-memory-write`) with the SYMPTOM in the
  description, so the next session finds the guardrail from the error text.
- **Write confirmed constraints and preferences.** A project constraint not
  derivable from the code, or a user preference confirmed in conversation,
  is a memory — not a conversation footnote.

## memgrep — the recall engine

`memgrep` is `rg` for markdown (gitignore-aware tree walk, markdown-AST-aware
filters, and the memory subcommands `recall`/`find`/`index`). It lives in the
`ai-maestro-janitor` repo (`tools/memgrep/`).

- **Availability:** memgrep is a Rust binary. If `command -v memgrep` is
  empty, install it once from a checkout of `ai-maestro-janitor`:
  `cargo install --path <ai-maestro-janitor>/tools/memgrep` (puts it on
  `~/.cargo/bin`); prebuilt per-platform release binaries are tracked
  upstream. Until then, the plain-`grep` fallback above works on note
  frontmatter + bodies — **recall degrades, never breaks**. Every consumer of
  this protocol (skills, hooks, tests) MUST gate on `command -v memgrep` and
  fall back to `grep -rliE`.
- **recall** `memgrep recall "SYMPTOM" <memdir>` — symptom-ranked notes,
  precision-first (surface matches suppress body-only matches unless nothing
  matched the surface), printed `path — description`, best first. Useful
  flags: `--sort score|ocd|lmd`, `--order asc|desc`, `--since`/`--until`
  (date window), `--top N`, `--no-notes`/`--full-notes`.
- **find** `memgrep find "<query>" <memdir>` — note-level keyword search with
  a `+`/`-`/wildcard/phrase DSL (`+TERM` mandatory, `-TERM` exclude, bare
  `TERM` ranks, `"quoted phrase"` verbatim); `--only-notes` searches the
  resolved lessons.

## Read-the-notes rule — a memory's lessons are part of the memory

When you read ANY memory, also read **all the lessons attached to it** —
every `[^N]` footnote reference and the `## Notes and lessons learned`
entries they point to. The lessons are *why* the facts are the way they are
and *what errors not to repeat*. memgrep auto-appends each returned note's
resolved lessons on `recall`/`find` (suppress with `--no-notes`), so one call
yields the facts AND every linked WHY.

## The note format (recall-relevant fields)

The `# Memory` harness directive is the authoring source-of-truth. On disk:

```yaml
---
name: <kebab-slug>                 # == filename stem
description: "<symptom surface — the load-bearing recall field>"
metadata:
  node_type: memory
  type: user | feedback | project | reference
---
<body: the one fact; for feedback/project add **Why:** and **How to apply:**>
```

`MEMORY.md` is the human index (`- [Title](file.md) — hook`, one line per
note) loaded each session. Recall does not need the index — it scans the
notes directly.

## Lessons-learned conventions (footnotes + per-element dates)

Memory pages grow a bottom `## Notes and lessons learned` section, written as
**standard markdown footnotes**: reference a lesson as `[^N]` in the body,
define it as `[^N]: <the WHY>` at the bottom. A lesson is a first-class
memory element with two intrinsic dates in a leading `[ocd:… lmd:…]` prefix
(Original Creation Date / Last Modified Date) — these, not the file mtime,
are the authoritative age. Correcting a wrong memory is a 2-step
non-destructive protocol (clean the fact in place; demote the error to a
dated lesson with the WHY) — see the `programmer-memory-write` skill.

## Evaluating / improving the system: the dual-test method

When designing or testing memory recall, run BOTH tests and judge BOTH
dimensions in each:

- **Test A — cold-recall:** simulate a session with NO prior recollection;
  build the query ONLY from the symptom/user's words, never the answer's
  jargon. Tests "is the right note findable from the symptom?".
- **Test B — write-then-recall:** author a note, then retrieve it. Tests the
  round-trip.

In each, evaluate (1) YOUR search strategy AND (2) the system's retrieval,
and improve both. **Contamination warning:** after you WRITE a note you are
biased toward its wording — your own cold-recall is no longer cold. Do
cold-recall from a clean framing, or have the symptom come from the user
verbatim.

## Why this rule exists

Without a recall rule + skills, a fresh PROGRAMMER session is blind to the
note corpus even when the answer was written down last week — every session
re-derives the same architecture facts, gotchas, and prior decisions. This
rule makes "recall before acting" and "index by symptom" a standing
discipline for AMPA, with a tool command that degrades to grep when the
binary isn't present.
