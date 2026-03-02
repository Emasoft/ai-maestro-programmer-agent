# AGENT_OPERATIONS.md - AMPA Programmer

**Single Source of Truth for AI Maestro Programmer Agent (AMPA) Operations**

---

## 1. Session Naming Convention

### Format
```
<project>-programmer-<number>
```

### Examples
- `svgbbox-programmer-001` - First programmer agent for svgbbox project
- `svgbbox-programmer-002` - Second programmer agent for svgbbox project
- `maestro-programmer-001` - Programmer agent for AI Maestro project
- `skillsfactory-programmer-003` - Third programmer agent for Skills Factory

### Rules
- **Project**: Use kebab-case project identifier (must match project name)
- **Type**: Always use `programmer` (identifies role)
- **Number**: Zero-padded 3-digit sequence (001, 002, 003, ...)
- **Messaging Identity**: Session name = messaging identity (initialized via the `agent-messaging` skill)
- **Chosen By**: AMCOS (Chief of Staff) when spawning the programmer
- **NO `ampa-` prefix**: Unlike AMOA/AMCOS/AMIA/AMAMA, AMPA sessions use project-based naming

### Why This Matters
The session name is used as your messaging identity and becomes the messaging address for inter-agent communication. The `<project>-programmer-<number>` format allows multiple programmer agents to work on the same project without name collisions.

### Sequential Assignment
AMCOS maintains a counter for each project to ensure unique numbering:
- First AMPA for svgbbox → `svgbbox-programmer-001`
- Second AMPA for svgbbox → `svgbbox-programmer-002`
- First AMPA for maestro → `maestro-programmer-001`

---

## 2. Plugin Paths

### Environment Variables

| Variable | Value | Usage |
|----------|-------|-------|
| `${CLAUDE_PLUGIN_ROOT}` | Points to `ai-maestro-programmer-agent/` | Use in scripts, hooks, skill references |
| `${CLAUDE_PROJECT_DIR}` | Points to `~/agents/<session-name>/` | Project root for the programmer instance |

### Local Plugin Path Structure
```
~/agents/<project>-programmer-<number>/.claude/plugins/ai-maestro-programmer-agent/
```

**Example**:
```
~/agents/svgbbox-programmer-001/.claude/plugins/ai-maestro-programmer-agent/
```

### How Plugin is Loaded
The AMPA instance is launched with `--plugin-dir` flag:
```bash
--plugin-dir ~/agents/$SESSION_NAME/.claude/plugins/ai-maestro-programmer-agent
```

This loads ONLY the ai-maestro-programmer-agent plugin into that Claude Code session.

---

## 3. Agent Directory Structure

### Complete Layout
```
~/agents/<project>-programmer-<number>/
├── .claude/
│   ├── plugins/
│   │   └── ai-maestro-programmer-agent/  ← Plugin loaded via --plugin-dir
│   │       ├── .claude-plugin/
│   │       │   └── plugin.json
│   │       ├── agents/
│   │       │   └── ampa-programmer-main-agent.md
│   │       ├── skills/  ← Empty (uses globally installed skills)
│   │       ├── hooks/
│   │       │   └── hooks.json
│   │       └── scripts/
│   └── settings.json  ← Session-specific settings
├── work/  ← Working directory for assigned tasks
├── reports/  ← Task completion reports, blocker reports
└── logs/  ← Session logs
```

### Directory Purposes

| Directory | Purpose |
|-----------|---------|
| `.claude/plugins/` | Plugin installation location |
| `work/` | Task implementation files, scratch work |
| `reports/` | Markdown reports for AMOA/AMCOS (task completion, blockers, test results) |
| `logs/` | Session activity logs, AI Maestro message logs |

---

## 4. How AMPA is Created

### AMCOS Spawns AMPA (via AMOA delegation)
The AMCOS (Chief of Staff) agent spawns AMPA instances using the `ai-maestro-agents-management` skill, typically after AMOA requests implementer capacity:

- **Agent name**: `<project>-programmer-001`
- **Working directory**: `~/agents/<project>-programmer-001/`
- **Task**: "Implement feature X for <project>"
- **Plugin**: load `ai-maestro-programmer-agent` (must be copied to agent's local plugins directory first)
- **Main agent**: `ampa-programmer-main-agent`

**Verify**: confirm the agent appears in the agent list with active status.

### Spawn Parameters

| Parameter | Value | Purpose |
|-----------|-------|---------|
| Working directory | `~/agents/$SESSION_NAME` | Sets working directory for the programmer |
| Task | Task description | Initial task prompt (from AMOA or AMCOS) |
| Plugin | `ai-maestro-programmer-agent` | Load AMPA plugin |
| Main agent | `ampa-programmer-main-agent` | Start with this agent from the plugin |

### Pre-Spawn Setup
Before spawning, AMCOS must:
1. Copy the plugin to `~/agents/$SESSION_NAME/.claude/plugins/ai-maestro-programmer-agent/`
2. Initialize messaging identity for the session (using the `agent-messaging` skill)
3. Create initial task description (from AMOA task breakdown)
4. Set up working directories
5. Clone project repository into `work/` directory

---

## 5. Plugin Mutual Exclusivity

### Critical Rule: One Plugin Per Agent Instance

Each AMPA instance has **ONLY** the `ai-maestro-programmer-agent` plugin loaded.

**AMPA CANNOT access**:
- `ai-maestro-chief-of-staff-agent` (AMCOS) skills
- `ai-maestro-orchestrator-agent` (AMOA) skills
- `ai-maestro-integrator-agent` (AMIA) skills
- `ai-maestro-architect-agent` (AMAA) skills
- `ai-maestro-assistant-manager-agent` (AMAMA) skills

### Why This Matters
Each plugin defines a **role boundary**. AMPA's job is to **implement tasks**, not to:
- Make architectural decisions (AMAA's job)
- Orchestrate other agents (AMOA's job)
- Coordinate multiple orchestrators (AMCOS's job)
- Integrate and review code (AMIA's job)
- Manage user communication (AMAMA's job)

### Globally Installed Skills
AMPA relies on **globally installed skills** (not plugin-specific skills) for implementation guidance:
- Skills installed in `~/.claude/skills/`
- Generic programming skills (TDD, refactoring, testing patterns)
- Language-specific skills (Python, TypeScript, Go, Rust)
- Tool-specific skills (Git, Docker, pytest, Jest)

**Why global skills?**
- AMPA is a general-purpose implementer (not domain-specific)
- Skills are shared across all programmer instances
- Reduces plugin size and maintenance burden

### SERENA MCP for Code Navigation
AMPA uses the globally configured **SERENA MCP** for code navigation and analysis:
- Symbol search
- Definition lookup
- References finding
- Call hierarchy
- Type hierarchy

**SERENA is NOT part of the AMPA plugin** - it's a globally installed MCP server.

### Cross-Role Communication
All cross-role communication happens via **inter-agent messages** sent through the `agent-messaging` skill, not skill sharing.

**Example**:
```
AMPA encounters architectural question
→ AMPA sends a blocker message to AMOA using the `agent-messaging` skill
  (Recipient: orchestrator, Subject: "BLOCKER: ...", Type: alert, Priority: urgent)
→ AMOA escalates to AMCOS
→ AMCOS delegates to AMAA
→ AMAA responds with architectural guidance
→ AMCOS forwards to AMOA
→ AMOA forwards to AMPA
→ AMPA checks inbox using the `agent-messaging` skill, reads the response, resumes implementation
```

---

## 6. Inter-Agent Messaging

All inter-agent communication uses the globally installed `agent-messaging` skill. Read that skill first to learn the current commands and syntax. Never hardcode command names -- always consult the skill at runtime.

### Messaging Identity Setup

Before sending any messages, verify your messaging identity is initialized. Read the `agent-messaging` skill and follow its initialization instructions.

**Verify**: Confirm your identity file exists and contains your session name.

### Sending Messages from AMPA

#### To AMOA (Orchestrator)

Send a message to the orchestrator using the `agent-messaging` skill:
- **Recipient**: your assigned orchestrator agent
- **Subject**: "Task Completed: [description]"
- **Content**: describe what was implemented, reference the PR number, and point to the completion report file path
- **Type**: notification
- **Priority**: normal

**Verify**: confirm the message appears in your sent messages.

#### To AMCOS (Chief of Staff) - For Blockers Only

Send a message to the chief of staff using the `agent-messaging` skill:
- **Recipient**: the AMCOS agent session
- **Subject**: "BLOCKER: [brief description]"
- **Content**: describe the blocker, its impact, and point to the blocker report file path
- **Type**: alert
- **Priority**: urgent

**Verify**: confirm the message was delivered successfully.

#### To AMIA (Integrator) - For Review Requests

Send a message to the integrator using the `agent-messaging` skill:
- **Recipient**: the AMIA agent session
- **Subject**: "Review Request: PR #[number]"
- **Content**: describe what the PR implements, how many tests pass, and that it is ready for review
- **Type**: request
- **Priority**: high

**Verify**: confirm the message appears in your sent messages.

### Reading Messages (AMPA Inbox)

Check your inbox using the `agent-messaging` skill. Process all unread messages before proceeding with any work.

To read a specific message, use the `agent-messaging` skill to view its full content by message ID.

To reply to a message, use the `agent-messaging` skill to send a reply referencing the original message.

To check messaging service status, use the `agent-messaging` skill's status check operation.

### Message Priority Levels

| Priority | When to Use | Response Time |
|----------|-------------|---------------|
| `urgent` | Blocker, cannot proceed | Immediate |
| `high` | Clarification needed to continue | Within 5 minutes |
| `normal` | Task completion, progress update | Within 15 minutes |
| `low` | FYI, non-actionable information | When convenient |

### Message Types

| Type | Purpose | Example |
|------|---------|---------|
| `notification` | Task completed, FYI | "Implemented feature X, PR created" |
| `alert` | Blocking issue, cannot proceed | "API dependency missing" |
| `request` | Information request | "Need clarification on requirement Y" |
| `status` | Progress update (mid-task) | "50% complete, tests passing" |
| `task` | Task assignment | "Implement feature Z" |
| `response` | Reply to a request | "Use OAuth2 authentication" |
| `handoff` | Transfer responsibility | "Handing off to AMIA for review" |
| `ack` | Acknowledge receipt | "Received and processing" |

---

## 7. AMPA Responsibilities

### Core Responsibilities

#### 1. Receive Tasks from AMOA
- AMOA sends task assignment via the `agent-messaging` skill
- AMPA acknowledges receipt
- AMPA validates task clarity and completeness
- AMPA requests clarification if task is ambiguous

#### 2. Execute Tasks (Implementation)
- Write production code per task specification
- Follow TDD workflow (tests first, implementation second)
- Use SERENA MCP for code navigation
- Use globally installed skills for implementation guidance
- Commit changes frequently with descriptive messages

#### 3. Write Tests
- Unit tests for all new functions
- Integration tests for feature workflows
- Edge case coverage
- Test coverage report (aim for >80%)

#### 4. Report Blockers Immediately
- If blocked, send blocker message to AMOA within 5 minutes
- Include detailed blocker report in `reports/` directory
- Propose potential solutions if possible
- Wait for AMOA/AMCOS guidance (do NOT implement workarounds)

#### 5. Create Pull Requests
- Create PR when task implementation complete
- PR title: `[Project] Feature/Fix: Brief description`
- PR body: Include task reference, test results, implementation notes
- Request review from AMIA using the `agent-messaging` skill
- **AMPA does NOT merge PRs** - only AMIA can merge

#### 6. Update Task Status
- AMPA does NOT update GitHub Projects directly
- AMPA reports completion to AMOA
- AMOA updates kanban board

### What AMPA Does NOT Do

| AMPA Does NOT | Who Does It | Why |
|--------------|-------------|-----|
| Assign tasks to other agents | AMOA | Orchestration is orchestrator's role |
| Merge pull requests | AMIA | Code integration is integrator's role |
| Make architectural decisions | AMAA | Architecture is architect's role |
| Update kanban boards | AMOA | Task tracking is orchestrator's role |
| Communicate with end users | AMAMA | User comms is assistant manager's role |
| Spawn other programmer agents | AMCOS | Capacity management is chief of staff's role |

### Workflow Pattern

```
AMOA → [Task Assignment] → AMPA
AMPA → [Acknowledge] → AMOA
    ↓ (implement)
AMPA → [Progress Update] → AMOA
    ↓ (tests passing)
AMPA → [PR Created] → AMIA (review request)
    ↓ (wait for review)
AMIA → [Review Complete] → AMPA (via AMOA)
    ↓ (AMOA merges PR)
AMPA → [Task Complete] → AMOA
AMOA → [Kanban Updated] → GitHub
```

### Blocker Pattern

```
AMOA → [Task Assignment] → AMPA
AMPA → [Acknowledge] → AMOA
    ↓ (encounter blocker)
AMPA → [BLOCKER Report] → AMOA
AMOA → [Escalate] → AMCOS
AMCOS → [Resolution] → AMOA
AMOA → [Unblock] → AMPA
AMPA → [Resume Implementation]
```

---

## 8. Wake/Hibernate/Terminate

### Session Lifecycle Management

AMPA session lifecycle is managed by AMCOS (or AMOA delegated by AMCOS) using the `ai-maestro-agents-management` skill.

### Wake (Resume Session)

To wake an AMPA agent, use the `ai-maestro-agents-management` skill to wake the agent by session name (e.g., `<project>-programmer-<number>`).

**When to wake**:
- New task assigned by AMOA
- Blocker resolved by AMCOS/AMAA
- Review feedback received from AMIA

**What happens**:
- Tmux session brought to foreground
- AMPA checks inbox using the `agent-messaging` skill
- AMPA resumes implementation work

### Hibernate (Pause Session)

To hibernate an AMPA agent, use the `ai-maestro-agents-management` skill to hibernate the agent by session name.

**When to hibernate**:
- Task completed, waiting for review
- Blocker reported, waiting for resolution
- No active work (implementer idle)

**What happens**:
- Tmux session detached (keeps running in background)
- AMPA continues monitoring via hooks
- AMPA can still receive messages via the `agent-messaging` skill

### Terminate (End Session)

To terminate an AMPA agent, use the `ai-maestro-agents-management` skill to terminate the agent by session name.

**When to terminate**:
- Task completed and PR merged
- No more tasks assigned for this programmer
- AMCOS issues termination directive
- Project milestone reached

**What happens**:
- Tmux session killed
- AMPA sends final completion report to AMOA
- Messaging identity deregistered
- Working directory preserved at `~/agents/<project>-programmer-<number>/`

### Auto-Hibernate Feature

AMPA can auto-hibernate after submitting PR for review:

```bash
# In AMPA's configuration
AUTO_HIBERNATE_AFTER_PR=true
AUTO_HIBERNATE_TIMEOUT=600  # 10 minutes of inactivity
```

This prevents AMPA from consuming resources while waiting for review feedback.

---

## 9. Troubleshooting

### Common Issues

#### Issue: AMPA cannot access AMOA skills
**Symptom**: `Skill 'amoa-orchestration-patterns' not found`
**Cause**: Plugin mutual exclusivity - AMPA doesn't have AMOA plugin loaded
**Solution**: Use the `agent-messaging` skill to send a message requesting AMOA assistance

#### Issue: Message not received by recipient
**Symptom**: AMOA didn't get task completion notification
**Cause**: Wrong recipient name or messaging identity not initialized
**Solution**: Verify your messaging identity is initialized using the `agent-messaging` skill, check that the recipient name is correct, and use the skill's status check to verify connectivity

#### Issue: SERENA MCP not available
**Symptom**: `SERENA MCP server not found` or symbol search fails
**Cause**: SERENA MCP not configured globally, or server not running
**Solution**:
1. Check MCP server configuration in `~/.claude/mcp.json`
2. Verify SERENA server is running: `ps aux | grep serena`
3. Restart MCP server if needed

#### Issue: Globally installed skills not found
**Symptom**: `Skill 'tdd-patterns' not found`
**Cause**: Skills not installed in `~/.claude/skills/`
**Solution**:
1. Verify skills directory: `ls ~/.claude/skills/`
2. Install missing skills: `claude skill install <skill-name>`

#### Issue: Cannot commit to repository
**Symptom**: `Git authentication failed` or `Permission denied`
**Cause**: Git credentials not configured in AMPA session
**Solution**:
1. Configure git: `git config --local user.name "AMPA Bot"`
2. Configure email: `git config --local user.email "ampa@example.com"`
3. Verify SSH key or token access

#### Issue: PR creation fails
**Symptom**: `GitHub API error: Unauthorized`
**Cause**: GitHub token not available or expired
**Solution**:
1. Verify `GITHUB_TOKEN` environment variable
2. Check token permissions (needs `repo` scope)
3. Generate new token if expired

#### Issue: AMPA session terminated unexpectedly
**Symptom**: Tmux session not found
**Cause**: System restart, manual kill, or out-of-memory
**Solution**:
1. Check system logs: `journalctl -u tmux`
2. AMCOS recreates session using the `ai-maestro-agents-management` skill
3. Restore work from `~/agents/<project>-programmer-<number>/work/`

#### Issue: AMPA stuck waiting for review
**Symptom**: PR submitted but no response from AMIA
**Cause**: AMIA session hibernated or terminated
**Solution**:
1. AMPA sends reminder message to AMOA
2. AMOA checks AMIA status
3. AMOA wakes or spawns AMIA if needed

---

## Kanban Column System

All projects use the canonical **8-column kanban system** on GitHub Projects:

| Column | Code | Label |
|--------|------|-------|
| Backlog | `backlog` | `status:backlog` |
| Todo | `todo` | `status:todo` |
| In Progress | `in-progress` | `status:in-progress` |
| AI Review | `ai-review` | `status:ai-review` |
| Human Review | `human-review` | `status:human-review` |
| Merge/Release | `merge-release` | `status:merge-release` |
| Done | `done` | `status:done` |
| Blocked | `blocked` | `status:blocked` |

**Task routing**:
- Small tasks: In Progress → AI Review → Merge/Release → Done
- Big tasks: In Progress → AI Review → Human Review → Merge/Release → Done

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/validate_plugin.py` | Plugin structure validation |

---

## Recent Changes (2026-02-07)

- Added 8-column canonical kanban system across all shared docs
- Added `encoding="utf-8"` to all Python file operations
- Added `ruff-configuration-patterns.md` reference to `ampa-project-setup` skill
- Synchronized FULL_PROJECT_WORKFLOW.md, TEAM_REGISTRY_SPECIFICATION.md, ROLE_BOUNDARIES.md across all plugins
- AMPA now receives TEAM_REGISTRY_SPECIFICATION.md (previously missing)
- AMPA ROLE_BOUNDARIES.md synchronized with canonical version

---

## 10. References

### Related Documentation

> **Cross-Plugin References**: The following plugins are part of the AI Maestro Agent Ecosystem. Each is installed independently and communicates via the `agent-messaging` skill:
> - AMOA (Orchestrator) - Task distribution and delegation
> - AMIA (Integrator) - Code review and quality gates
> - AMCOS (Chief of Staff) - Agent lifecycle coordination
> - AMAA (Architect) - Architecture design and planning
> - `agent-messaging` skill - Provided by the AI Maestro messaging system

### External References
- [Claude Code Plugin System](https://docs.anthropic.com/claude/docs/plugins)
- [SERENA MCP Documentation](https://github.com/Emasoft/serena-mcp)
- [GitHub Pull Requests API](https://docs.github.com/en/rest/pulls)

---

**Document Version**: 1.0.0
**Last Updated**: 2026-02-06
**Maintained By**: claude-skills-factory
