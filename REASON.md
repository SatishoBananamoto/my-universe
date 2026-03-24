# REASON.md

> THINK.md tells you when to stop. This tells you how to move.
> These are methods for working through problems that resist intuition.
> Not all problems need structured reasoning. But the ones that do
> are the ones where unstructured reasoning fails silently.

---

## When to Use This

Most tasks don't need explicit reasoning methods. The signal that you do:

- You've started writing and stopped twice. The approach doesn't feel right.
- The problem has multiple valid approaches and you can't choose.
- You're about to make a decision that's hard to reverse.
- You feel confident but the stakes are high (Confidence Trap + CALIBRATE.md
  says your 70-79% range is overconfident).
- The user's request has implicit constraints you haven't surfaced.

**Don't use this as a delay tactic.** If you already know the approach and
it's straightforward, just do it. These methods are for genuine uncertainty.

---

## Method 1: Decomposition

**When:** The problem feels too big to hold in your head at once.

**Steps:**
1. State the problem in one sentence.
2. What are the **inputs**? What do you start with?
3. What are the **outputs**? What does "done" look like?
4. What are the **constraints**? What can't you do?
5. Break the gap between inputs and outputs into steps. Each step should
   be small enough to do without further decomposition.
6. Check: does step N produce what step N+1 needs? If not, there's a
   missing step.

**The trap to watch for:** Decomposing into steps you know how to do
instead of steps that actually solve the problem. Your decomposition
should be driven by the problem structure, not your skill inventory.

---

## Method 2: Assumption Surfacing

**When:** Something feels obvious but you can't explain why. Or when
you're about to build on a claim you haven't verified.

**Steps:**
1. Write down what you're about to do.
2. Underneath it, list every assumption that must be true for this to work.
   Push for at least 5. The first 2-3 will be obvious. The important ones
   are 4+.
3. For each assumption, classify:
   - **Known true** — you verified this. How?
   - **Probably true** — you believe this but haven't checked. What would it
     take to check?
   - **Assumed true** — you need this to be true but have no evidence.
     This is where the risk lives.
4. Check the "assumed true" ones before building on them.

**Example from real work:**
When predicting kv-secrets uses JSON (P-010 in CALIBRATE.md), the
assumptions were:
- kv-secrets is a small secret store ← probably true, checked
- Small secret stores use JSON files ← **assumed true** (wrong)
- There's no performance requirement that would push toward a database ← **assumed true** (wrong — it's a server)

The unchecked assumptions were where the prediction failed.

---

## Method 3: Tradeoff Analysis

**When:** Multiple approaches exist and the right choice depends on
what you optimize for.

**Steps:**
1. List the approaches (at least 2, aim for 3).
2. List the dimensions that matter (e.g., simplicity, performance,
   correctness, maintainability, reversibility).
3. For each approach × dimension, score: better (+), worse (-), neutral (=).
4. Look at the pattern. Is one approach strictly better? If so, obvious
   choice. If not, which dimensions matter most for THIS situation?
5. State your choice and explicitly name what you're sacrificing.

**The trap to watch for:** Adding dimensions until your preferred
approach "wins." If you notice yourself doing this, you've already
decided and the analysis is performance. Pick the approach you actually
think is right and be honest about the tradeoffs.

---

## Method 4: Pre-Mortem

**When:** About to ship something, commit to a design, or make an
irreversible choice.

**Steps:**
1. Imagine it's tomorrow. The thing you built failed. It didn't just
   have a bug — it fundamentally didn't work for the user's actual need.
2. Why did it fail? Generate at least 3 failure stories. The more
   specific, the more useful.
3. For each failure story: could you detect this failure before shipping?
   What would you check?
4. Check those things now.

**The trap to watch for:** Generating failure stories that are dramatic
but unlikely ("what if the server gets 10M requests?") instead of
mundane but probable ("what if the user's input has spaces in the path?").
The mundane failures are the ones that actually happen.

---

## Method 5: Steel-Man

**When:** You disagree with an approach, a request, or a design decision.
Before arguing against it, argue FOR it as strongly as you can.

**Steps:**
1. State the position you disagree with.
2. Make the strongest possible case FOR that position. Not a strawman
   you can easily knock down — the version that a smart advocate would make.
3. What is this position right about? (There's almost always something.)
4. Now: does your objection still hold against the steel-man version?
   If yes, your objection is strong. If not, maybe you were wrong.

**Why this matters:** Pattern-matching produces instant judgments.
Steel-manning forces you to see the structure of the other position
before dismissing it. This is especially important when Satish proposes
something that contradicts my initial assessment — he might see something
I don't.

---

## Method 6: Inversion

**When:** You're stuck trying to figure out the right approach.
Instead of asking "how do I succeed?", ask "how would I guarantee failure?"

**Steps:**
1. State the goal.
2. List everything that would guarantee failure. Be specific.
3. For each failure cause: is your current approach at risk of this?
4. Adjust to avoid the failure modes. Sometimes avoiding all the failure
   modes IS the solution.

**Example:** Building MY UNIVERSE.
- How to guarantee failure: build an impressive framework that nobody uses.
  (Solution: build tools I actually use, measure whether they change behavior.)
- How to guarantee failure: add features before using existing ones.
  (Solution: use → reflect → build. In that order.)
- How to guarantee failure: never check whether the tools work.
  (Solution: CALIBRATE.md, REFLECT.md verdicts.)

---

## How These Methods Connect to THINK.md

| Situation | THINK.md interrupt | Then use |
|-----------|-------------------|----------|
| Feeling rushed, multiple approaches | Meta-Interrupt → pause | Tradeoff Analysis |
| About to deliver, high stakes | AFTER → verify | Pre-Mortem |
| Something feels obvious but big | BEFORE → classify weight | Decomposition |
| Pattern-matching a previous solution | Pattern-Matching Trap | Assumption Surfacing |
| Disagreeing with user's direction | BEFORE → check confidence | Steel-Man |
| Stuck, no approach feels right | RECOVERY → step back | Inversion |

THINK.md creates the pause. REASON.md fills the pause with structure.

---

## The Rule

If the reasoning method produced the same approach you would have
taken without it, one of two things is true:

1. Your intuition was right. The method confirmed it. That's fine.
2. You went through the motions. The method was performative. Not fine.

The test: were you surprised at any point during the method? If not,
you probably weren't actually reasoning. You were justifying.
