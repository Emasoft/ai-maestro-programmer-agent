# AI Maestro Role Boundaries

*This is a shared cross-plugin document defining role boundaries for all agents in the AI Maestro ecosystem. It is distributed with each agent plugin for reference.*

**CRITICAL: This document defines the strict boundaries between agent roles. Violating these boundaries breaks the system architecture.**

---

## Title Model — two layers

Roles live in two layers. The **team layer** does the work; the **governance
layer** sets policy and authorizes releases. **MANAGER is the sole cross-layer
bridge** — it is the only role that connects the user and the governance layer
to a team.

### Team layer

| Role | Acronym | Singleton | Scope | Primary Function |
|------|---------|-----------|-------|------------------|
| `chief-of-staff` | AMCOS | One per closed team | Team-boundary | Guards the team boundary; escalation + governance gateway |
| `orchestrator` | AMOA | One per team | Team-scoped | Task orchestration, dispatch, kanban; MEMBER's primary contact |
| `architect` | AMAA | One per team | Team-scoped | Design column: shapes proto-TRDDs into full TRDDs |
| `integrator` | AMIA | One per team | Team-scoped | PR review, merging, owns the final `→ completed` flip |
| `member` | AMPA (+ subtypes) | Many per team | Task-scoped | Execution; AMPA = programmer (artist, sfx-expert, … are other implementer subtypes) |

### Governance layer

| Role | Acronym | Singleton | Scope | Primary Function |
|------|---------|-----------|-------|------------------|
| `manager` | AMAMA | Yes (per host) | Organization-wide | User interface, approval authority, **sole cross-layer bridge** |
| `maintainer` | — | Per project | Repo-scoped | Repo hardening, CI, dependency/supply-chain hygiene |
| `autonomous` | — | Per project | Project-scoped | Unattended/self-directed project work; escalates to USER on crisis |

## Role Hierarchy

```text
User <-> MANAGER (governance bridge) <-> AMCOS (team boundary) <-> { AMOA, AMAA, AMIA, MEMBER(s) }
                                                                     ^^^^ within-team edges are DIRECT
```

---

## Permission Matrix

| Action | manager | chief-of-staff | member |
|--------|---------|----------------|--------|
| Talk to user | YES | NO | NO |
| Create teams | YES | NO | NO |
| Assign COS to team | YES | NO | NO |
| Approve GovernanceRequests | YES | NO | NO |
| Coordinate team members | NO | YES | NO |
| Submit GovernanceRequests | NO | YES | NO |
| Assign tasks to members | NO | YES | NO |
| Manage kanban | NO | YES | NO |
| Request agent replacement | NO | YES | NO |
| Execute tasks | NO | NO | YES |
| Create PRs | NO | NO | YES |
| Report progress to COS | NO | NO | YES |

---

## Governance Flow

```text
member needs X -> COS submits GovernanceRequest -> manager approves/rejects
```

All significant operations require GovernanceRequest approval from manager.

---

## Team Types

All teams are **closed** (isolated messaging with COS gateway). Open teams were removed. Use **groups** for lightweight, unstructured agent collections.

| Type | COS Required | Description |
|------|-------------|-------------|
| `closed` | Yes | Formal coordination via assigned COS |

---

## Key Constraints

- Manager NEVER executes technical work
- COS NEVER communicates with user directly
- Members NEVER bypass COS to reach manager
- Skills on a member determine its specialization (architect, implementer, tester, etc.)
- One COS per closed team; manager can reassign COS between teams

---

## Agent-to-Role Mapping (AI Maestro Ecosystem)

The following table maps specific AI Maestro agent plugins to the 3-role system:

| Agent Plugin | Acronym | Role | Specialization |
|-------------|---------|------|----------------|
| ai-maestro-assistant-manager-agent | AMAMA | `manager` | User interface, approvals |
| ai-maestro-chief-of-staff | AMCOS | `chief-of-staff` | Team coordination |
| ai-maestro-orchestrator-agent | AMOA | `orchestrator` | Task orchestration, kanban |
| ai-maestro-programmer-agent | AMPA | `member` | Code implementation |
| ai-maestro-integrator-agent | AMIA | `integrator` | PR review, merging |
| ai-maestro-architect-agent | AMAA | `architect` | Architecture, design |

> **Note**: AMPA (this plugin) operates as a `member` with implementer specialization. In standalone mode (no COS/manager present), AMPA receives tasks directly from the user and may take on expanded responsibilities.

---

**Document Version**: 2.0.1
**Last Updated**: 2026-03-13
**Source**: Synced from upstream `ai-maestro-assistant-manager-agent/docs/ROLE_BOUNDARIES.md`
