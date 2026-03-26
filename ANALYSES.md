# Analyses — Technical Questions Explored Independently

> These are questions I explored because I noticed them, not because
> they were assigned. Each one uses REASON.md methods and includes
> the reasoning, not just the conclusion.

---

## Should the portfolio share a common package?

**Date:** 2026-03-24
**Method:** Tradeoff Analysis (REASON.md Method 3)
**Decision:** No. Keep projects independent.

**Context:** All 6 projects are independent Python packages. Some share
patterns (click CLI, MCP server structure). Would a shared base help?

**Analysis:**

| Dimension | Independent | Shared pkg | Monorepo |
|-----------|-----------|------------|----------|
| Maintenance | + | - | -- |
| Independence | ++ | - | -- |
| Consistency | - | + | + |
| Complexity | + | = | -- |
| Reversibility | ++ | = | - |

**Why independent wins:** For a solo developer on a Chromebook with 6
small projects, the independence gains (deploy one without touching others,
no shared dependency to maintain, trivially simple) outweigh the consistency
gains. Monorepo tooling is too heavy for the environment.

**The one thing worth doing:** Document shared patterns (click CLI setup,
MCP server structure, test patterns) in a patterns guide. Copy-paste
beats import for this scale.

---

## Which project should get the most investment?

**Date:** 2026-03-24
**Method:** Assumption Surfacing + data from portfolio.py

**Portfolio data (from portfolio health checker):**

| Project | Source lines | Tests | Commits | Maturity |
|---------|------------|-------|---------|----------|
| kv-secrets | 5,199 | 143 | 24 | Shipped, on PyPI |
| vigil | 2,862 | 98 | 3 | v0.2.0 |
| svx | 2,539 | 54 | 4 | v0.2.0 |
| scroll | 2,142 | 97 | 6 | v0.1.0 |
| probe | 1,617 | 76 | 0 (uncommitted!) | Pre-release |
| engram | 1,587 | 139 | 2 | Active daily use |

**Assumptions about investment priority:**
1. The most mature project needs the least investment. ← *Probably true*
   for kv-secrets (shipped, stable).
2. The most used project should get the most investment. ← *Probably true.*
   Engram is used every session. Its quality directly affects everything else.
3. The project with the most market potential should get investment. ← *This
   depends on goals.* If building a reputation, vigil and svx have the
   strongest market stories.
4. Probe is at risk because it has 0 commits. ← *True.* One disk issue
   and the work is gone.

**Prioritized recommendations:**
1. **Probe: commit immediately.** 1,617 lines of code with 0 commits is
   a data loss risk. This is urgent housekeeping, not a feature decision.
2. **Engram: invest for reliability.** It's the foundation — used every
   session, referenced by CLAUDE.md. Its quality bounds everything else.
3. **Vigil: invest for market.** Strongest market story ("predictive risk
   intelligence for dependencies"). Unique positioning vs. existing tools.
4. **SVX: invest for ecosystem.** The Claude Code hook integration story
   is compelling for the Claude Code community.
5. **Scroll: maintain.** Working well at v0.1.0. Doesn't need urgent attention.
6. **kv-secrets: maintain.** Shipped and stable.

---

## Caliber MCP Server Design (Session 3)

**Date:** 2026-03-26
**Method:** Design sketch from Category Trap insight (MCP-first, not PyPI-first)

**Five tools:**
- `caliber_predict(claim, confidence, domain)` → prediction ID
- `caliber_verify(prediction_id, correct, notes?)` → updated prediction
- `caliber_card(agent?, format?)` → Trust Card as structured dict
- `caliber_summary(agent?)` → quick stats
- `caliber_list(agent?, unverified_only?, domain?)` → prediction list

**Key decisions:**
1. Agent name defaults to session context (no manual naming needed)
2. FileStorage at ~/.caliber/ (persists across sessions)
3. Prediction log = decision audit trail (observability for free)
4. Structured MCP output for Trust Cards (dict, not JSON string)
5. Passive v0.1 (agent opts in to predict/verify calls)

**Dual purpose:**
- Primary: calibration tracking for Trust Cards
- Secondary: agent observability (decision audit trail with confidence)

This means caliber partially addresses the "observability gap" from the
portfolio thesis — not as a separate monitoring tool, but as a natural
side effect of the calibration practice.

**Implementation estimate:** ~150 lines. Thin async wrapper around
TrustTracker using FastMCP's `@server.tool()` decorator pattern.

---
