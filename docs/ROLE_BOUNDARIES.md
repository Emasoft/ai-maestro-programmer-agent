# AI Maestro Role Boundaries

*This is a shared cross-plugin document defining role boundaries for all agents in the AI Maestro ecosystem. It is distributed with each agent plugin for reference.*

**CRITICAL: This document defines the strict boundaries between agent roles. Violating these boundaries breaks the system architecture.**

---

## 3-Role System

| Role | Singleton | Scope | Primary Function |
|------|-----------|-------|------------------|
| `manager` | Yes (per host) | Organization-wide | User interface, approval authority |
| `chief-of-staff` | One per closed team | Team-scoped | Agent coordination within team |
| `member` | Many per team | Task-scoped | Execution; skills determine specialization |

## Role Hierarchy

```text
User <-> manager <-> chief-of-staff <-> member(s)
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
