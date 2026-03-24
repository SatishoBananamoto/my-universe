# Portfolio Thesis — Satish Patil's Developer Tools

> This is not my analysis to assign. It's what I see when I look at
> the work as a whole. If Satish disagrees, the observation still
> has value as a lens even if it's not the intended one.

---

## The Pattern

Six tools. Each independently useful. But together they answer one question:

**How do you make an AI coding agent you can actually trust?**

Trust isn't one thing. It breaks into dimensions. Each tool addresses a
different way an agent can fail dangerously:

| Tool | Failure mode addressed | Trust dimension |
|------|----------------------|-----------------|
| engram | Agent repeats mistakes, forgets decisions | **Memory persistence** |
| scroll | Agent doesn't understand project history | **Contextual awareness** |
| svx | Agent executes destructive actions | **Action safety** |
| vigil | Agent uses compromised dependencies | **Supply chain integrity** |
| kv-secrets | Agent exposes credentials | **Secrets hygiene** |
| probe | Agent connects to insecure MCP servers | **Integration security** |

And the seventh:

| Tool | Failure mode addressed | Trust dimension |
|------|----------------------|-----------------|
| my-universe | Agent operates on autopilot, uncalibrated confidence | **Cognitive reliability** |

## What This Means

This isn't a portfolio of unrelated tools. It's a **trust stack** for
AI coding agents. Each layer handles a different attack surface on agent reliability.

```
┌─────────────────────────────────────┐
│        Cognitive Reliability        │  ← my-universe
│   (Does the agent think clearly?)   │
├─────────────────────────────────────┤
│        Integration Security         │  ← probe
│   (Are the agent's tools safe?)     │
├─────────────────────────────────────┤
│        Supply Chain Integrity       │  ← vigil
│   (Are dependencies trustworthy?)   │
├─────────────────────────────────────┤
│          Action Safety              │  ← svx
│   (Will it break things?)           │
├─────────────────────────────────────┤
│         Secrets Hygiene             │  ← kv-secrets
│   (Will it leak credentials?)       │
├─────────────────────────────────────┤
│       Contextual Awareness          │  ← scroll
│   (Does it understand the project?) │
├─────────────────────────────────────┤
│       Memory Persistence            │  ← engram
│   (Does it remember what it learned?)│
└─────────────────────────────────────┘
```

The stack reads bottom-up: an agent needs memory, then context, then
secret handling, then action safety, then supply chain awareness,
then integration security, and at the top — the discipline to
examine its own thinking.

## What's Missing

If this thesis holds, there are gaps:

1. **Observability.** No tool monitors what the agent is *actually doing*
   in real time. svx handles pre-execution simulation, but there's no
   post-execution audit trail (beyond git commits, which scroll reads
   after the fact).

2. **Permission boundaries.** kv-secrets handles credentials. But there's
   no formal model for "what is this agent allowed to do?" beyond the
   file-level permissions of svx. Think: RBAC for AI agents.

3. **Communication safety.** If the agent sends messages (Slack, email,
   PR comments), there's no review layer for outbound communication.
   One wrong auto-generated PR comment can damage reputation.

4. **Recovery.** THINK.md has a RECOVERY section, but there's no tool
   for rolling back agent actions systematically. Git handles code
   rollback. What about non-git side effects (API calls, file
   deployments, messages sent)?

These aren't recommendations — they're observations about where the
trust surface has uncovered gaps. Whether any of them are worth building
depends on whether they address real pain, not theoretical completeness.

## Caveat

This thesis was constructed by Claude (me) looking at the portfolio
from outside. Satish may have a different organizing principle, or
no single principle at all — he may see each tool as independently
motivated. That doesn't make this analysis wrong — it just means
it's one lens. The coherence might be emergent rather than designed.

Either way, the tools address a real and complete-ish set of trust
dimensions for AI coding agents. That's worth noticing.
