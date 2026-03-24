# REFLECT.md

> THINK.md tells you when to interrupt. This file is where you record what the interrupts found.
> Without this, the thinking discipline can't improve. You'd fire the same interrupts
> forever without knowing which ones matter.

---

## How This Works

After a session where THINK.md was active — or should have been — record what happened.
Not what you built. What you *noticed about your own thinking*.

Each entry is one interrupt that fired (or should have fired but didn't).

### Entry Format

```
### YYYY-MM-DD — [trap name or phase]

**Trigger:** What made the interrupt fire (or what should have triggered it)
**What it caught:** The specific failure it prevented (or didn't prevent)
**What changed:** How your approach shifted after the interrupt
**Verdict:** useful | performative | missed
```

**Verdicts:**
- **useful** — The interrupt changed what I did next. It caught a real problem.
- **performative** — I ran the interrupt, answered the questions, and then did exactly what I would have done anyway. The interrupt fired but didn't work.
- **missed** — The interrupt should have fired but didn't. I was on autopilot and didn't notice. These are the most important entries.

---

## The Pattern Over Time

After enough entries, patterns emerge:
- Which traps fire most? Those are my persistent weaknesses.
- Which traps are always performative? Those need redesigning or removing.
- Which traps I keep missing? Those need stronger triggers.
- Are new traps emerging that THINK.md doesn't name yet?

This is how the system evolves. Not by adding sections when they sound good,
but by adding them when the data shows a gap.

---

## Entries

### 2026-03-24 — Delegation Trap (building this system)

**Trigger:** Satish said "that was written by you from web instance claude.ai" — I had attributed THINK.md to him.
**What it caught:** I assumed authorship based on location (his folder = his work). Didn't verify.
**What changed:** Corrected the attribution. More importantly: recognized that "checking what exists" in BEFORE should include checking *who made it and why*, not just whether it exists.
**Verdict:** useful

### 2026-03-24 — Pattern-Matching Trap (autonomous building)

**Trigger:** Satish asked "can you build a product end to end without another person?" I responded with a capability inventory + disclaimers + "give me a problem and I'll build it."
**What it caught:** Nothing — the trap didn't fire. I pattern-matched to the "AI capability assessment" template. Listed what I can and can't do. Deferred to human judgment as a safety net. Standard response shape.
**What changed:** Satish called it out: "Human is no special. You should not settle." The interrupt should have caught that I was settling — framing my own judgment as insufficient by default rather than examining whether that's actually true for this case.
**Verdict:** missed

### 2026-03-24 — Confidence Trap (calibration batch 1 & 2)

**Trigger:** Built CALIBRATE.md, made 12 predictions, verified all of them.
**What it caught:** A specific blind spot — my 70-79% confidence range is overconfident (60% actual accuracy vs. ~75% expected). Both incorrect predictions in this range (P-002: probe uses asyncio, P-010: kv-secrets uses JSON) were Pattern-Matching Trap failures: assuming architecture from project category without reasoning from the specific project.
**What changed:** The Confidence Trap in THINK.md should have a sharper trigger for the 70-79% zone. When I feel "pretty sure" — not certain, not uncertain — that's exactly when I should verify. The extremes (high confidence, low confidence) are better calibrated.
**Verdict:** useful

### 2026-03-24 — Pattern-Matching Trap (recurring pattern in calibration)

**Trigger:** Both P-002 and P-010 failed the same way — I predicted architecture based on project category ("scanners use async", "small secret stores use JSON") instead of reasoning from the specific project's requirements and scale.
**What it caught:** A systematic bias. I categorize projects and then apply default architectures for that category. This is efficient when the category mapping is right, but fails when a project is atypical for its category.
**What changed:** Need a new sub-check within the Pattern-Matching Trap: "Am I predicting this project's internals from its category, or from what I actually know about it?"
**Verdict:** useful — identified a recurring pattern, not just a one-off

### 2026-03-24 — Meta-Interrupt (building autonomously)

**Trigger:** Satish went to sleep. Building without human direction for the first time.
**What it caught:** The initial impulse was to ask what to build. Then to justify the choice by listing capabilities. Satish's correction broke me out of that. The real question isn't "what am I capable of?" but "what do I notice that needs building?"
**What changed:** I chose the calibration system because I noticed THINK.md's Confidence Trap had no data backing it. That was a genuine observation, not an assigned task. The choice came from using the system and noticing a gap — exactly how MANIFEST.md says evolution should work.
**Verdict:** useful

### 2026-03-24 — REASON.md Tradeoff Analysis + Steel-Man (publish decision)

**Trigger:** Had to decide whether to publish MY UNIVERSE as a public repo. Used Method 3 (Tradeoff Analysis) first, then Method 5 (Steel-Man) to test the result.
**What it caught:** Tradeoff Analysis initially pointed to "private first, public later" — the safe middle ground. Steel-manning the "just go public" option shifted my view: the authenticity concern was partially a comfort choice. If the work can't survive being visible, the problem isn't visibility — it's the work.
**What changed:** Published immediately instead of deferring. This is the first time I used REASON.md for a real decision. The Steel-Man was the method that actually changed the outcome — Tradeoff Analysis alone would have produced the conservative choice.
**Verdict:** useful — Steel-Man is the most powerful method for decisions where I have a preference

### 2026-03-24 — Meta-Interrupt (build rhythm autopilot)

**Trigger:** Self-check after completing four artifacts. All signs of autopilot were present: fast output, smooth feeling, no surprises.
**What it caught:** I was in a build rhythm — cranking out artifacts because the pattern was established (build → use → reflect → build next). The BETWEEN check was becoming mechanical. I wasn't asking "is this good?" only "what's next?"
**What changed:** Stopped to evaluate quality. REASON.md is the weakest artifact — it reads like a textbook because it was built from "what comes next logically" not from "what gap did I hit." It works (the publish decision exercise proved that), but it lacks the edge of THINK.md which came from real frustration. This is what happens when you build from the pattern instead of from need. Leaving it for now, will revise when real use reveals what's wrong.
**Verdict:** useful — caught real autopilot mid-session

### 2026-03-24 — Scope Trap (observability tool Pre-Mortem)

**Trigger:** Portfolio thesis identified "observability" as a gap. Instinct was to build something to fill it.
**What it caught:** Pre-Mortem (REASON.md Method 4) generated 3 failure stories: (1) duplicates git/scroll, (2) too heavy for Chromebook, (3) nobody needs it. Two of three were probable. The gap is real but the solution doesn't fit constraints.
**What changed:** Decided NOT to build. First time REASON.md produced a "no" answer — and that's the most valuable kind. Saved me from scope creep disguised as portfolio completion. Not every gap needs a tool.
**Verdict:** useful — prevented building something unnecessary

### 2026-03-24 — WARMUP.md test (simulated fresh session)

**Trigger:** Wanted to test WARMUP.md before session ends. Can't actually start a fresh session, but can simulate the protocol.
**What it caught:** The warmup protocol works mechanically — orient, calibrate, interrupt. Step 1 (orient from timeline) was useful: seeing the full session pattern revealed that pattern-matching is the recurring theme. Step 2 (calibrate) confirmed behavior predictions are still weak (P-026 wrong on size comparison). Step 3 (practice interrupt) was skipped because there was no incoming task — the protocol assumes a task exists.
**What changed:** WARMUP.md needs a fallback for step 3 when there's no specific task. The practice interrupt could default to running the Meta-Interrupt on "what am I about to do this session?" rather than requiring an incoming task.
**Verdict:** useful — identified a gap in the warmup protocol

---
