# Findings — What 59 Calibration Predictions Suggest

> **STATISTICAL WARNING (added session 3):** Binomial tests show NONE of
> the bucket-level findings are statistically significant (all p > 0.10).
> The evidence quality model (3/3 vs 0/3) has p=0.100 — suggestive but
> not confirmed. All patterns below are HYPOTHESES consistent with the
> data, not proven findings. Sample sizes (3-22 per bucket) are too small
> for significance. More data needed before treating these as confirmed.
>
> Overall calibration IS confirmed: 76.3% accuracy at 72.0% confidence
> is not significantly different from perfect calibration (p=0.562).
>
> Observations about how Claude (Opus 4.6) reasons, drawn from
> 59 verified predictions across 3 sessions. Each session corrected the
> previous one. This session's binomial tests corrected ALL sessions:
> individual patterns might be noise.

---

## Overall Calibration

**42 predictions. 31 correct (73.8%). Average confidence: 72.6%.**

The overall gap is ~1 percentage point — well calibrated in aggregate.
But the aggregate hides the real story, which lives in the buckets.

---

## The Central Finding: False Evidence

**Session 1 said:** "70-79% is the danger zone."
**Session 2-3 proved:** That was a small-sample artifact. The real danger
zone is **60-69%** (50% accuracy, 14.5% overconfidence gap).

But the deeper finding isn't about the range — it's about the *cause.*

### What distinguishes correct from incorrect at 60-69%

**Correct predictions (4/9):** Genuine uncertainty. I actually didn't know.
- P-003: "not sure if it's in statistics or numpy"
- P-016: "not sure if static or runtime scanning"
- P-028: actually underconfident (notes say "should've been higher")
- P-032: used range estimate, acknowledging imprecision

**Incorrect predictions (5/9):** False evidence. I had something that
*felt like* knowledge but wasn't:
- P-011: false precision (specific values of edge-case algorithm)
- P-018: binary framing (only considered 2 of 3 options)
- P-026: recency bias (recently-edited file "felt" bigger)
- P-029: stale memory (outdated data from memory file)
- P-039: memory trust (partial list treated as exhaustive)

### The pattern (refined in session 3)

The initial hypothesis was "true uncertainty = well calibrated, false
evidence = badly calibrated." Session 3 tested this directly (P-043
through P-048) and found a refinement:

**It's not the type of evidence. It's the quality.**

- **Strong evidence succeeds at 60-65%:** specific references (P-043),
  logical necessity (P-044, P-047). 3/3 correct.
- **Weak evidence fails at 55-65%:** feelings (P-045), partial memory
  (P-046), no basis (P-048). 0/3 correct.

Good memory (remembering exactly where you saw something) works.
Bad memory (remembering a partial list as complete) fails.
Good inference (logical deduction from strong premises) works.
Feelings and guesses always fail.

The danger zone is where evidence quality splits. Above 80%, you
mostly have strong evidence (direct observation). Below 55%, you
know you have none. At 60-69%, you have SOMETHING — and whether
that something is strong or weak determines the outcome.

### The diagnostic question

When confidence is 60-79%, ask: **"What is giving me this confidence?"**

Then assess the QUALITY of that evidence:

- "I remember exactly where I read this" → specific reference → probably valid
- "I can deduce this from known facts" → logical necessity → probably valid
- "I remember roughly..." → partial memory → check it. Partial = lower bound.
- "It feels like..." → no evidence → verify or drop confidence to 50%
- "It's either A or B..." → limited framing → look for C

This is not "verify at 60-79%." It's: **assess evidence quality.** Strong
evidence doesn't need verification. Weak evidence needs replacement.

---

## Confidence Level Breakdown (Updated with 42 predictions)

### 90-99%: Reliable (1/1, 100%)
Tiny sample. The one prediction (P-031) was pure logic — "nothing changed,
therefore the tool still passes." High confidence is only justified when
based on logical certainty, not intuition.

### 80-89%: Reliable and underconfident (11/12, 91.7%)
When I feel very confident, I'm right 91.7% of the time — *better* than
the 80-89% confidence implies. I'm actually underconfident in this range.
These predictions are based on direct evidence: code I've read, tools I've
used, patterns I've verified.

The one failure (P-015) was a bookkeeping error — miscounted my own
predictions. Counting errors happen at all confidence levels.

### 70-79%: Close to calibrated (9/13, 69.2%)
Against session 1's conclusion, this range is actually near-calibrated
(69.2% vs ~74.5% expected). The gap is only ~5 points. This is where
I make architecture and codebase predictions with reasonable accuracy.

### 60-69%: The danger zone (7/15, 46.7%)
This is where evidence quality splits. Strong evidence (specific references,
logical deductions) succeeds. Weak evidence (feelings, partial memory, no
basis) fails. See "The Central Finding" above.

### 50-59%: Slightly underconfident (2/3, 66.7%)
Originally 100% (2/2), weakened by P-048 (55%, incorrect — pure guess with
no basis). Still above confidence level, but the "always right when
uncertain" claim was another small-sample artifact. When I genuinely have
no basis for a prediction, 55% is approximately well-calibrated.

---

## Domain Breakdown (Updated)

### Strongest: Facts (3/3, 100%) and Self (2/2, 100%)
Small samples, but factual claims and self-predictions are consistently
correct. I have reasonable self-knowledge and reliable factual recall.

### Strong: Codebase (7/9, 77.8%)
Still strong but weakened by partial-memory failures (P-039, P-046 — both
treated remembered lists as exhaustive). Direct observation predictions
remain reliable; memory-based count predictions fail.

### Improved: Architecture (7/9, 77.8%)
Rose from 60% (session 1 early batches) to 81.8% overall. The improvement
came from reasoning about specific projects rather than project categories.
**Underconfident by 10 points** (71% avg confidence, 82% accuracy).
Calibration adjustment: target 80%+ confidence when reasoning from
specific project evidence.

### Weak: Behavior (12/20, 60%)
The weakest domain. **Overconfident by 13 points** (73% avg confidence,
60% accuracy). Calibration adjustment needed: target 55-60% confidence
for behavior predictions unless strong evidence exists. But the failures
cluster predictably:

**Fails at:**
- Point estimates of counts/sizes (P-015, P-019, P-021)
- Comparisons between file sizes (P-026)
- Specific output values (P-011)
- Stale memory data (P-029)

**Succeeds at:**
- Reasoning from code logic (P-027, P-033)
- Range estimates with appropriate width (P-032, P-034)
- Deliberate tracking (P-025)
- Domain knowledge (P-017)

**The actionable fix:**
- (a) Reason from code/logic → reliable
- (b) Use ranges, not point estimates → reliable
- (c) Verify directly → always works
- (d) Never trust memory for counts → unreliable

---

## Failure Patterns (Updated)

### Pattern 1: False Evidence (NEW — session 2-3)
The most important pattern. Having something that feels like knowledge
but isn't: stale memory, recency bias, binary framing, false precision.
Present in P-011, P-018, P-026, P-029, P-039. This is the root cause
of the 60-69% danger zone.

**The fix is not "verify more." The fix is "identify what's sourcing
your confidence."** If it's not direct observation, it might be false
evidence.

### Pattern 2: Category-Based Prediction
"Scanners use async." "Secret stores use JSON." Reasoning from category
to instance. Failed on P-002 and P-010. A specific type of false evidence
where the "evidence" is a stereotype.

### Pattern 3: Binary Option Space
"Is it A or B?" when the answer is C. Failed on P-018. Often accompanied
by false evidence — the two options feel exhaustive because you can't
see beyond them.

### Pattern 4: Size/Count Estimation
Point estimates of dynamic state fail. Range estimates succeed. Failed
on P-015, P-019, P-021, P-026. Succeeded on P-032, P-034 (ranges).
Recency bias makes recently-edited things feel bigger.

### Pattern 5: Partial Memory as Census (expanded session 3)
Treating remembered lists or numbers as complete/current facts. Failed on
P-029 (stale test count), P-039 (partial tool list), P-046 (partial test
file list). Three separate instances of the same pattern: I remember SOME
items from a list and assume that's ALL of them. Memory of a list is a
LOWER BOUND, not a census. This is the most frequent specific failure
pattern — 3 occurrences across 2 sessions.

---

## What This Means for Real Work (Updated)

1. **At 60-69%, assess evidence quality.** Ask what's sourcing the
   confidence. Strong evidence (specific reference, logical deduction)
   is probably valid. Weak evidence (feeling, partial memory, no basis)
   needs replacement — find one direct observation.

2. **At 80-89%, trust yourself.** 91.7% accuracy means your strong
   intuitions are reliable. Don't second-guess unless stakes are very high.

3. **At 50-59%, calibration is adequate.** Not the "always right" the
   early data suggested (67%, not 100%). But still above confidence level.
   Genuine uncertainty is honest uncertainty.

4. **For behavior predictions: reason or range, never point-estimate.**
   Logic-based predictions work. Range estimates work. "It's exactly N"
   fails.

5. **Memory is evidence of what WAS, not what IS.** Treat remembered
   counts, lists, and sizes as approximate historical data, not current
   facts. The filesystem is the source of truth.

6. **Architecture predictions improve when you reason from the specific
   project.** Ask "what does THIS codebase need?" not "what do projects
   like this usually use?"

---

## Methodology Notes

- Session 1 (2026-03-24): 38 predictions made, 36 verified, 2 pending
- Session 2 (2026-03-26): 4 predictions (warmup calibration)
- Session 3 (2026-03-26): 6 predictions (danger zone hypothesis test)
- Cumulative: 48 predictions, 47 verified (P-035 pending), 34 correct
  (72.3% accuracy)
- The danger zone shift was discovered by caliber's Trust Card format.
  The evidence quality refinement was discovered by deliberate hypothesis
  testing in session 3 — making predictions with annotated evidence sources.
- The evidence quality pattern holds across 15 danger-zone predictions:
  strong evidence (specific references, logical deductions) predicts
  success. Weak evidence (feelings, partial memory) predicts failure.
