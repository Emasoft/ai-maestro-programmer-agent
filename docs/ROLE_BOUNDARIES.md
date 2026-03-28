# AI Maestro Role Boundaries

*This is a shared cross-plugin document defining role boundaries for all agents in the AI Maestro ecosystem. It is distributed with each agent plugin for reference.*

**CRITICAL: This document defines the strict boundaries between agent roles. Violating these boundaries breaks the system architecture.**

---

## 4-Title Governance System

| Title | Singleton | Scope | Primary Function |
|-------|-----------|-------|------------------|
| `MANAGER` | Yes (per host) | Organization-wide | User interface, approval authority |
| `CHIEF-OF-STAFF` | One per team | Team-scoped | Agent coordination within team |
| `ORCHESTRATOR` | One per team | Team-scoped | Primary kanban manager, task distribution, direct MANAGER communication |
| `MEMBER` | Many per team | Task-scoped | Execution; skills determine specialization |

## Title Hierarchy

```
User <-> MANAGER <-> CHIEF-OF-STAFF <-> ORCHESTRATOR <-> MEMBER(s)
```

> **Note**: ORCHESTRATOR can message MANAGER directly (no COS relay needed).

---

## Permission Matrix

| Action | MANAGER | CHIEF-OF-STAFF | ORCHESTRATOR | MEMBER |
|--------|---------|----------------|--------------|--------|
| Talk to user | YES | NO | NO | NO |
| Create teams | YES | NO | NO | NO |
| Assign COS to team | YES | NO | NO | NO |
| Approve GovernanceRequests | YES | NO | NO | NO |
| Coordinate team members | NO | YES | YES | NO |
| Submit GovernanceRequests | NO | YES | NO | NO |
| Assign tasks to members | NO | NO | YES | NO |
| Manage kanban (primary) | NO | NO | YES | NO |
| Manage kanban (secondary) | YES | YES | — | NO |
| Request agent replacement | NO | YES | NO | NO |
| Execute tasks | NO | NO | NO | YES |
| Create PRs | NO | NO | NO | YES |
| Report progress to Orchestrator | NO | NO | — | YES |

---

## Governance Flow

```
MEMBER needs X -> ORCHESTRATOR escalates to COS -> COS submits GovernanceRequest -> MANAGER approves/rejects
```

All significant operations require GovernanceRequest approval from MANAGER.

---

## Team Structure

All teams are **closed** — there are no "open" teams. Every team requires a CHIEF-OF-STAFF. Each agent belongs to **at most one team** at a time.

---

## Key Constraints

- MANAGER NEVER executes technical work
- CHIEF-OF-STAFF NEVER communicates with user directly
- MEMBERS NEVER bypass ORCHESTRATOR/COS to reach MANAGER
- ORCHESTRATOR is the primary kanban manager; COS and MANAGER are secondary
- Skills on a MEMBER determine its specialization (architect, implementer, tester, etc.)
- One COS per team; MANAGER can reassign COS between teams
- Each agent belongs to at most one team

---

## Agent-to-Title Mapping (AI Maestro Ecosystem)

The following table maps specific AI Maestro agent plugins to the 4-title governance system:

| Agent Plugin | Acronym | Title | Specialization |
|-------------|---------|-------|----------------|
| ai-maestro-assistant-manager-agent | AMAMA | `MANAGER` | User interface, approvals |
| ai-maestro-chief-of-staff | AMCOS | `CHIEF-OF-STAFF` | Team coordination |
| ai-maestro-orchestrator-agent | AMOA | `ORCHESTRATOR` | Task orchestration, kanban (primary manager) |
| ai-maestro-programmer-agent | AMPA | `MEMBER` | Code implementation |
| ai-maestro-integrator-agent | AMIA | `MEMBER` | PR review, merging |
| ai-maestro-architect-agent | AMAA | `MEMBER` | Architecture, design |

> **Note**: AMPA (this plugin) operates as a `MEMBER` with implementer specialization. In standalone mode (no ORCHESTRATOR/MANAGER present), AMPA receives tasks directly from the user and may take on expanded responsibilities.

---

**Document Version**: 3.0.0
**Last Updated**: 2026-03-28
**Source**: Synced from upstream `ai-maestro-assistant-manager-agent/docs/ROLE_BOUNDARIES.md`
