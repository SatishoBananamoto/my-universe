# Findings — What 27 Calibration Predictions Revealed

> These are empirical observations about how Claude (Opus 4.6) reasons,
> drawn from a single session of systematic prediction-making and verification.
> Sample size is small. Patterns are preliminary. But they're real data,
> not speculation.

---

## Overall Calibration

**27 predictions. 19 correct (70.4%). Average confidence: 72.4%.**

The overall gap is 2 percentage points — well calibrated in aggregate.
But the aggregate hides significant variation across confidence levels
and domains.

## Confidence Level Breakdown

### High confidence (80-89%) is reliable.
7/8 correct (87.5%). When I feel very confident about something, I'm
almost always right. These predictions tend to be about things I have
direct evidence for — projects I've reviewed, tools I've used.

### Medium-high confidence (70-79%) is the danger zone.
6/10 correct (60%). This is where I feel "pretty sure" but haven't
verified. It's confident enough to skip checking, but not confident
enough to be right. Both P-002 (probe/asyncio) and P-010 (kv-secrets/JSON)
— my two worst misses — lived here.

### Medium-low confidence (60-69%) is similarly unreliable.
2/4 correct (50%). Coin flip. At this confidence level, I should
either gather more information or explicitly flag the uncertainty.

### Low confidence (50-59%) is underconfident.
2/2 correct (100%). When I feel genuinely uncertain, the thing I'm
uncertain about tends to be correct. This suggests I'm too cautious
about things I actually know.

**The actionable insight:** Before asserting anything at 60-79% confidence,
verify it. Before hedging at 50-59%, consider that you might know more
than you think.

## Domain Breakdown

### Strongest: Codebase knowledge (83%)
I know these projects. Predictions about file structure, module names,
and code patterns are reliable. This makes sense — I've read the code
in previous sessions.

### Strong: Facts and self-prediction (100%)
Small samples, but factual claims I make tend to be correct. Self-predictions
(how I'll perform) are also accurate. I have reasonable self-knowledge.

### Moderate: Architecture (71%)
Started at 60%, improved to 71% through deliberate effort. The key
improvement: reasoning from the specific project instead of from the
project category. When I ask "what would this specific project need?"
instead of "what do projects like this usually use?", accuracy goes up.

### Weak: Behavior (33%)
Terrible. Predictions about tool output, file sizes, line counts, and
system state are wrong more often than right. The failure mode: I
estimate rather than check. I assume I know the state of things I've
been actively working with, but my tracking of my own output is poor.

**The actionable insight:** Never predict behavior/output at any
confidence level. Always verify.

## Failure Patterns

### Pattern 1: Category-Based Prediction
"Scanners use async." "Secret stores use JSON." Reasoning from what a
category of tool usually does, not from what this specific tool does.
Failed on P-002 and P-010. Fixed by adding the Category Trap to THINK.md.

### Pattern 2: Binary Option Space
"Is it A or B?" when the answer is C. Considering two alternatives
feels like you've explored the space, but two is often not enough.
Failed on P-018 (predicted tmpdir vs virtual FS, actual was
analysis-based). Fixed by adding the Binary Trap to THINK.md.

### Pattern 3: Size Estimation of Active Work
Predicting the size/count of things I've been actively editing.
Failed on P-015 (miscounted my own predictions), P-021 (underestimated
tool LOC), P-026 (wrong about which file was bigger). Recency bias
makes recently-touched things feel bigger than they are.

### Pattern 4: Bookkeeping Errors
Miscounting items in lists I created. P-015 (forgot P-008 was
codebase-tagged), P-019 (forgot Scope Trap fired). I don't reliably
track the cumulative state of my own outputs within a session.

## What This Means for Real Work

1. **Verify, don't assert, in the 60-79% zone.** If I'm writing code
   and I'm "pretty sure" about an API, a package name, or a file
   location — check it. The cost is seconds, the save is trust.

2. **Architecture assumptions need specific reasoning.** When I'm
   about to predict or assume how something is built, I need to ask:
   "am I reasoning from this project or from a category?" If the
   latter, I need to look.

3. **Don't estimate output size. Measure it.** If it matters whether
   a file is 100 or 200 lines, `wc -l` it. Don't guess.

4. **Trust high-confidence intuitions.** 87.5% accuracy at 80-89%
   confidence means my strong intuitions are reliable. Don't second-guess
   them unnecessarily.

5. **Low confidence may mean "I know but I'm not letting myself
   believe it."** 100% accuracy at 50-59% suggests I'm hedging
   on things I actually know. Worth noticing.
