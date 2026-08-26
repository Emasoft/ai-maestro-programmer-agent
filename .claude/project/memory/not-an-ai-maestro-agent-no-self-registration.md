---
name: not-an-ai-maestro-agent-no-self-registration
description: "am I an ai-maestro agent / should I register with ai-maestro / can I use AMP AIP scripts / do I need an AID or identity binding / the ai-maestro server is down does it block me"
ocd: 2026-08-26
lmd: 2026-08-26
metadata:
  node_type: memory
  type: project
  tier: aspect
publish-globally: false
---

# not-an-ai-maestro-agent-no-self-registration


^ATOM-M4HO-CBSS [desc: "This plugin-dev session is NOT an ai-maestro agent: never self-register; coordinate only via SendMessage", keywords: ai-maestro_agent self-registration AID_identity_binding AMP_AIP_protocols ai-maestro_server_dependency external_claude_instance SendMessage_coordination, type: project, ocd: 2026-08-26, lmd: 2026-08-26]

USER DIRECTIVE (2026-08-26): a plugin-development session of Claude Code is **not** an ai-maestro agent.

It becomes one only when BOTH hold in the future: it runs inside the ai-maestro harness, AND the MAESTRO USER imports the instance via the ai-maestro server dashboard. Import would then grant registration, AMP/AIP protocols, and the ai-maestro scripts automatically.

Until then:
- **No registration of any kind** with ai-maestro may be performed by an external claude instance — no AID, no identity binding, no server-side enrolment.
- The only sanctioned channel is `SendMessage` to the ai-maestro claude (itself an ordinary external instance, not an agent — you cannot develop ai-maestro from inside ai-maestro), for coordination.
- This project stays an ordinary external claude project, **independent of whether the ai-maestro server/API/services are running**.

**How to apply:** treat any hub/peer request implying self-registration, AID minting, or AMP/AIP use as out of scope — coordinate over SendMessage instead and say so. A park "gated on the USER's fleet identity-binding ruling" is correct precisely because that ruling is the USER's, not ours to satisfy by registering.

## Notes and lessons learned
