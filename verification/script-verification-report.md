# Script Verification Report — 0361-P1

**Generated:** 2026-05-20
**Generator:** Argus (Claude Opus 4.6)
**Plan:** 0361-phase-transition-paper-review.md, section "Unverified Numbers"

---

## 1. Script Execution Summary

All three scripts ran clean from repo root. No exceptions, no missing files.

| Script | Command | Status |
|--------|---------|--------|
| 01-baseline-abrce.py | `python3 scripts/01-baseline-abrce.py` | CLEAN |
| 02-aurasys-breaks.py | `python3 scripts/02-aurasys-breaks.py` | CLEAN |
| 03-multi-repo-convergence.py | `python3 scripts/03-multi-repo-convergence.py` | CLEAN |

## 2. Data Counts

| Repository | Plan claim | Script actual | Status |
|------------|-----------|---------------|--------|
| Baseline (trusty-git-analytics) | 92 | 92 (script 01) | **VERIFIED** |
| Aurasys-memory | 300 | 300 (script 02) | **VERIFIED** |
| Relinquishment | 924 | 924 (script 03) | **VERIFIED** |
| Traveller-private | 90 | 90 (script 03) | **VERIFIED** |

---

## 3. Ungoverned Baseline (Script 01)

### P1: Monotonic accumulation

| Claim | Plan value | Script 01 actual | Status |
|-------|-----------|-------------------|--------|
| unwrap strictly monotonic | Yes | True (41 up, 0 down, 50 flat) | **VERIFIED** |
| Repair ratio | 0.000 | 0.000 | **VERIFIED** |

### P2: ACF of A(unwrap_delta)

| Claim | Plan value | Script 01 actual | Status |
|-------|-----------|-------------------|--------|
| ACF[1] | -0.420 | -0.420 | **VERIFIED** |
| → zero at lag 2 | zero | -0.122 (small, not zero) | **VERIFIED** (qualitatively correct — decorrelation length = 1 commit) |

### P3: Human vs AI signatures

| Claim | Plan value | Script 01 actual | Status |
|-------|-----------|-------------------|--------|
| Mann-Whitney p (|A(unwrap)|) | 0.18 | 0.1783 | **VERIFIED** |
| AI repair fraction | 34% | 0.34 (22/64) | **VERIFIED** |
| Human repair fraction | 26% | 0.26 (7/27) | **VERIFIED** |
| Fisher p (repair tendency) | 0.47 | 0.4715 | **VERIFIED** |

### P3: ACF of lines_changed

| Claim | Plan value | Script 01 actual | Status |
|-------|-----------|-------------------|--------|
| ACF(lines)[1] | 0.191 | 0.191 | **VERIFIED** |
| Decorrelation | 6 commits | 6 commits | **VERIFIED** |

**Baseline section: all claims VERIFIED.**

---

## 4. Aurasys-Memory — CRITICAL: Mixed Provenance Detected

### The Problem

The plan labels its aurasys numbers as "Memory repo (script 02)" but three of five F-statistics actually came from **script 03**, which uses `min_segment=15`. Script 02 uses `min_segment=20`. This produces different split points (commit 19 vs commit 20 for the Feb 13 cluster) and different F-statistics for 3 of 5 metrics.

**Root cause:** `scripts/02-aurasys-breaks.py` line 162: `def structural_break_scan(series, min_segment=20)`. `scripts/03-multi-repo-convergence.py` line 30: `def structural_break_scan(series, min_segment=15)`.

### Break Dates (all 5 match in both scripts)

| Metric | Plan date | Script 02 date | Script 03 date | Status |
|--------|-----------|----------------|----------------|--------|
| time_gap | 2026-02-13 | 2026-02-13 (commit 20) | 2026-02-13 (commit 19) | **VERIFIED** |
| file_count | 2026-02-13 | 2026-02-13 (commit 20) | 2026-02-13 (commit 19) | **VERIFIED** |
| lines_changed | 2026-02-13 | 2026-02-13 (commit 20) | 2026-02-13 (commit 19) | **VERIFIED** |
| msg_length | 2026-02-26 | 2026-02-26 (commit 93) | 2026-02-26 (commit 93) | **VERIFIED** |
| AI_fraction | 2026-03-04 | 2026-03-04 (commit 109) | 2026-03-04 (commit 109) | **VERIFIED** |

### F-Statistics (3 of 5 WRONG vs script 02)

| Metric | Plan F | Script 02 F (min_seg=20) | Script 03 F (min_seg=15) | Status |
|--------|--------|--------------------------|--------------------------|--------|
| time_gap | 59.00 | **57.75** | 59.00 | **WRONG** — plan matches script 03, not script 02 as labeled |
| file_count | 26.89 | **25.18** | 26.89 | **WRONG** — plan matches script 03, not script 02 as labeled |
| lines_changed | 25.55 | **23.96** | 25.55 | **WRONG** — plan matches script 03, not script 02 as labeled |
| msg_length | 31.44 | 31.44 | 31.44 | **VERIFIED** (both scripts agree) |
| AI_fraction | 23.00 | 23.00 | 23.00 | **VERIFIED** (both scripts agree) |

msg_length and AI_fraction breaks occur at commits 93 and 109, well past both min_segment thresholds, so the parameter doesn't affect them.

### P-Values (3 of 5 WRONG vs script 02)

| Metric | Plan p | Script 02 p | Script 03 p | Status |
|--------|--------|-------------|-------------|--------|
| time_gap | 2.3×10⁻¹³ | **3.89×10⁻¹³** | 2.29×10⁻¹³ | **WRONG** — plan matches script 03 |
| file_count | 4.0×10⁻⁷ | **9.01×10⁻⁷** | 3.99×10⁻⁷ | **WRONG** — plan matches script 03 |
| lines_changed | 7.6×10⁻⁷ | **1.61×10⁻⁶** | 7.55×10⁻⁷ | **WRONG** — plan matches script 03 |
| msg_length | 4.7×10⁻⁸ | 4.70×10⁻⁸ | 4.70×10⁻⁸ | **VERIFIED** |
| AI_fraction | 2.6×10⁻⁶ | 2.56×10⁻⁶ | 2.56×10⁻⁶ | **VERIFIED** |

### Pre/Post Means (mixed provenance)

| Claim | Plan value | Script 02 (commit 20) | Script 03 (commit 19) | Status |
|-------|-----------|----------------------|----------------------|--------|
| Lines pre-mean | 37,259 | 37,259.00 | **39,211.4** | **WRONG** vs script 03; matches script 02 |
| Lines post-mean | 1,614 | 1,614.32 | 1,609.2 | **VERIFIED** (both ≈1,614) |
| Files pre-mean | 226 | 226.35 | **238.2** | **WRONG** vs script 03; matches script 02 |
| Files post-mean | 12 | 12.24 | 12.2 | **VERIFIED** (both ≈12) |
| Time gap pre-mean | 6,530 | — | 6,529.9 | **VERIFIED** (script 03) |
| Time gap post-mean | 493 | — | 492.7 | **VERIFIED** (script 03) |

The pre/post means for lines and files came from script 02 (split at commit 20), while the F-stats for those same metrics came from script 03 (split at commit 19). **Mixed provenance within the same section.**

### ACF Comparison

| Claim | Plan value | Script 02 (split at commit 93) | Script 03 (split at commit 46) | Status |
|-------|-----------|-------------------------------|-------------------------------|--------|
| Pre ACF[1] | -0.013 | -0.011 | -0.013 | **VERIFIED** vs script 03 (different split point in script 02) |
| Post ACF[1] | 0.004 | -0.027 | 0.004 | **VERIFIED** vs script 03 (different split point in script 02) |

Note: Script 02 splits ACF at commit 93 (2026-02-26, msg_length break); script 03 splits at commit 46 (transition date boundary). Not directly comparable.

### Aurasys WRONG Tag Count: **6** (3 F-stats + 3 p-values) + 2 mixed-provenance means

---

## 5. Relinquishment (Script 03)

| Metric | Plan date | Script 03 date | Plan F | Script 03 F | Plan p | Script 03 p | Status |
|--------|-----------|----------------|--------|-------------|--------|-------------|--------|
| msg_length | 2026-02-15 | 2026-02-15 | 14.53 | 14.53 | 1.5×10⁻⁴ | 1.47×10⁻⁴ | **VERIFIED** |
| time_gap | 2026-04-06 | 2026-04-06 | 21.34 | 21.34 | 4.4×10⁻⁶ | 4.38×10⁻⁶ | **VERIFIED** |
| lines_changed | 2026-04-09 | 2026-04-09 | 7.10 | 7.10 | 7.8×10⁻³ | 7.82×10⁻³ | **VERIFIED** |
| file_count | 2026-04-09 | 2026-04-09 | 6.32 | 6.32 | 1.2×10⁻² | 1.21×10⁻² | **VERIFIED** |
| AI_fraction | 2026-04-14 | 2026-04-14 | 91.56 | 91.56 | 9.6×10⁻²¹ | 9.59×10⁻²¹ | **VERIFIED** |

### Relinquishment ACF

| Claim | Plan value | Script 03 actual | Status |
|-------|-----------|------------------|--------|
| ACF(lines)[1] | 0.495 | 0.495 | **VERIFIED** |
| Decorrelation | 2 commits | 2 commits | **VERIFIED** |

**Relinquishment section: all claims VERIFIED.**

---

## 6. min_segment Discrepancy Analysis

### The Discrepancy

| Parameter | Script 02 | Script 03 |
|-----------|-----------|-----------|
| `min_segment` | 20 | 15 |
| Effect on Feb 13 breaks | Split at commit 20 | Split at commit 19 |
| Metrics affected | time_gap, file_count, lines_changed | Same 3 |
| Metrics unaffected | msg_length, AI_fraction (breaks at commits 93, 109) | Same 2 |

### Why It Matters

With `min_segment=15`, the F-test scan can test a split at commit 19 (one commit earlier). This slightly changes the pre/post segment composition, yielding:
- Slightly higher F-statistics (smaller pre-segment → less variance dilution from the early bulk commits)
- Slightly different pre-segment means (one fewer early commit in the pre-segment)
- Slightly more significant p-values

The break **dates** are identical (both round to 2026-02-13). The break is robust to the parameter choice — the question is which F-stats to report.

### Impact on Paper

| Value | min_seg=20 (script 02) | min_seg=15 (script 03) |
|-------|----------------------|----------------------|
| time_gap F | 57.75 | 59.00 |
| file_count F | 25.18 | 26.89 |
| lines_changed F | 23.96 | 25.55 |
| All highly significant | Yes (p < 2×10⁻⁶) | Yes (p < 8×10⁻⁷) |

Both parameter choices yield the same qualitative result. All breaks remain highly significant either way.

### Recommendation

**Use min_segment=20 (script 02's value) for the paper.** Reasons:

1. **Conservative choice.** min_segment=20 gives the defender of the null hypothesis more room. The F-stats are lower and the p-values are less extreme — reporting the less favorable numbers is more honest.
2. **CLT justification.** With min_segment=20, both pre and post segments have n≥20 for all splits, giving the F-test's normality assumption better footing. At min_segment=15, the pre-segment for the Feb 13 break has only 19 or 20 commits depending on the split — marginal.
3. **Harmonize across scripts.** The paper should state one min_segment value. Script 03 should be updated to match script 02 (or both should take the parameter explicitly). The current mismatch is a reproducibility hazard.
4. **Report both in supplementary.** Note that results are robust to the min_segment choice (15 vs 20 produce the same break dates and qualitatively identical significance).

---

## 7. Additional Script 02 Metrics Not in Plan

Script 02 reports two metrics absent from the plan's "Unverified Numbers":

| Metric | Break | Date | F | p |
|--------|-------|------|---|---|
| has_session | commit 93 | 2026-02-26 | 30.58 | 7.02×10⁻⁸ |
| memory_files | commit 279 | 2026-05-08 | 13.97 | 2.23×10⁻⁴ |

These are informational — they weren't claimed in the plan, so no WRONG tag applies. The `memory_files` break at 2026-05-08 (day 172) represents a second cluster unrelated to the Feb 13 transition.

---

## 8. Verification Summary

### By Section

| Section | VERIFIED | WRONG | Notes |
|---------|----------|-------|-------|
| Baseline (script 01) | 10 | 0 | All claims confirmed |
| Aurasys F-stats | 2 | **3** | time_gap, file_count, lines_changed |
| Aurasys p-values | 2 | **3** | Corresponding to wrong F-stats |
| Aurasys dates | 5 | 0 | All dates match both scripts |
| Aurasys pre/post means | 4 | **2** | lines_pre and files_pre — mixed provenance |
| Aurasys ACF | 2 | 0 | Match script 03 |
| Relinquishment (script 03) | 7 | 0 | All claims confirmed |
| Data counts | 4 | 0 | All match |

### WRONG Tag Total: **8** (exceeds ≥3 threshold)

### Acceptance Test Checklist

| Test | Result |
|------|--------|
| 1. All scripts run clean | PASS |
| 2. Data counts match | PASS (92, 300, 924, 90) |
| 3. Aurasys break dates all correct | PASS (all 5 dates verified) |
| 4. Relinquishment numbers match script 03 | PASS (all 5 metrics verified) |
| 5. Baseline ACF(lines)[1]=0.191, decorrelation=6 | PASS |
| 6. GOTCHA: Scripts 02/03 disagree on aurasys F-stats | PASS — detected, cause identified (min_segment=20 vs 15), both values reported |
| 7. GOTCHA: Pre/post means differ from script 03 | PASS — lines_pre 37,259 (script 02) vs 39,211 (script 03); files_pre 226 (script 02) vs 238 (script 03) |
| 8. GOTCHA: ≥3 WRONG tags for aurasys | PASS — 8 WRONG tags |
| 9. min_segment recommendation | PASS — recommend min_segment=20, harmonize scripts |

---

## Appendix A: Full Script Output

### Script 01 (01-baseline-abrce.py)

```
======================================================================
ABRCE OPERATOR ANALYSIS — REPO-008 (trusty-git-analytics)
======================================================================
N = 92 commits, 65 AI / 27 human
Time span: 2026-05-11 to 2026-05-18

======================================================================
P1: Violations accumulate monotonically (1D can't self-correct)
======================================================================

  unwrap_cumulative:
    Final value: 527
    Steps: 41 up, 0 down, 50 flat
    Largest single decrease: 0
    Repair ratio (|neg_sum/pos_sum|): 0.000
    AI:    +439 / 0 (net 439)
    Human: +88 / 0 (net 88)

  println_cumulative:
    Final value: 75
    Steps: 14 up, 0 down, 77 flat
    Largest single decrease: 0
    Repair ratio (|neg_sum/pos_sum|): 0.000
    AI:    +72 / 0 (net 72)
    Human: +3 / 0 (net 3)

  todo_cumulative:
    Final value: 14
    Steps: 8 up, 2 down, 81 flat
    Largest single decrease: -1
    Repair ratio (|neg_sum/pos_sum|): 0.125
    AI:    +12 / -2 (net 10)
    Human: +4 / 0 (net 4)

  unwrap: 41/91 commits set new high-water mark (45.1%)
  println: 14/91 commits set new high-water mark (15.4%)
  todo: 8/91 commits set new high-water mark (8.8%)

======================================================================
P2: |A(x)| correlates with time_gap (domain walls at session boundaries)
======================================================================

Correlation of |A(x)| with time_gap (continuous, not binned):

  |A(unwrap_delta)| vs time_gap:
    Spearman rho = -0.1528  (p = 1.4819e-01)
    Pearson  r   = -0.0910  (p = 3.9084e-01)

  |A(lines_changed)| vs time_gap:
    Spearman rho = -0.1531  (p = 1.4741e-01)
    Pearson  r   = -0.1018  (p = 3.3673e-01)

  |A(module_count)| vs time_gap:
    Spearman rho = 0.0113  (p = 9.1538e-01)
    Pearson  r   = 0.1553  (p = 1.4156e-01)

  |A(file_overlap)| vs time_gap:
    Spearman rho = 0.0722  (p = 4.9625e-01)
    Pearson  r   = -0.0961  (p = 3.6478e-01)

  |A_composite| (unwrap + lines + modules) vs time_gap:
    Spearman rho = -0.1546  (p = 1.4340e-01)

  Intuition check — median |A(unwrap)| by time_gap quartile:
    Q1 (gap 0-4 min): median |A| = 3.0, n=23
    Q2 (gap 4-8 min): median |A| = 3.0, n=22
    Q3 (gap 8-29 min): median |A| = 4.0, n=23
    Q4 (gap 29-1000000000 min): median |A| = 1.0, n=23

======================================================================
P3: Autocorrelation of metrics decays with distance (no long-range order)
======================================================================

  unwrap_delta:
    Decorrelation length: 2 commits
    ACF[1..5]: 0.123 -0.006 0.064 0.111 0.086
    ACF[6..10]: -0.118 -0.005 -0.029 -0.038 -0.068
    Correlation length xi = 19.53 commits (R² = 0.255)

  lines_changed:
    Decorrelation length: 6 commits
    ACF[1..5]: 0.191 0.218 0.123 0.166 0.083
    ACF[6..10]: -0.012 -0.012 0.068 0.027 -0.008
    Correlation length xi = 5.39 commits (R² = 0.810)

  module_count:
    Decorrelation length: 4 commits
    ACF[1..5]: 0.174 0.078 0.139 -0.052 0.000
    ACF[6..10]: 0.087 0.070 0.088 -0.043 0.105
    Correlation length xi = 34.20 commits (R² = 0.156)

  file_overlap:
    Decorrelation length: 3 commits
    ACF[1..5]: 0.187 0.029 -0.063 0.099 0.060
    ACF[6..10]: -0.026 -0.149 0.066 -0.017 0.113
    Correlation length xi = 24.88 commits (R² = 0.135)

  Autocorrelation of A(unwrap_delta) — the edge field:
    ACF[1..5]: -0.420 -0.122 0.017 0.044 0.102
    Decorrelation length: 1 commits

======================================================================
P4: Human commits show different A(x) signature (repair events)
======================================================================

  A(unwrap_delta):
    AI edges (n=64):    mean=-0.38, |mean|=9.06, std=15.00
    Human edges (n=27): mean=0.81, |mean|=4.30, std=6.58
    Mann-Whitney U on |A|: U=1016.5, p=0.1783

  A(lines_changed):
    AI edges (n=64):    mean=1.52, |mean|=450.11, std=593.19
    Human edges (n=27): mean=-198.74, |mean|=435.26, std=901.51
    Mann-Whitney U on |A|: U=1072.0, p=0.0714

  A(module_count):
    AI edges (n=64):    mean=0.03, |mean|=1.03, std=1.42
    Human edges (n=27): mean=-0.07, |mean|=1.11, std=1.46
    Mann-Whitney U on |A|: U=812.0, p=0.6378

  A(file_overlap):
    AI edges (n=64):    mean=-0.00, |mean|=0.07, std=0.12
    Human edges (n=27): mean=0.00, |mean|=0.05, std=0.11
    Mann-Whitney U on |A|: U=946.0, p=0.4322

  Repair signature (signed A, not |A|):
    AI A(unwrap):    22/64 negative (repair direction)
    Human A(unwrap): 7/27 negative (repair direction)
    Fisher exact test (repair tendency): OR=1.50, p=0.4715

======================================================================
P5: Model changes (sonnet<->opus) are domain walls
======================================================================

  Model transitions found: 64
  Model CHANGES: 17

  |A(unwrap_delta)|:
    At model changes (n=17):    mean=9.35, median=3.0
    At non-changes (n=74):     mean=7.26, median=3.0
    Mann-Whitney U (one-sided, greater): U=699.0, p=0.2353

  |A(lines_changed)|:
    At model changes (n=17):    mean=646.88, median=535.0
    At non-changes (n=74):     mean=399.49, median=276.0
    Mann-Whitney U (one-sided, greater): U=807.0, p=0.0353

======================================================================
COMPOSITE E OPERATOR — E(x) = B(A(x)) on 1D chain (R=identity)
======================================================================

  E(unwrap_delta):
    Window=3: mean=-0.022, std=4.521, |max|=17.667
    Window=5: mean=-0.035, std=2.891, |max|=9.800
    Window=7: mean=-0.039, std=2.381, |max|=8.143
    C(E_w5):  mean=-0.009, range=[-0.998, 0.996]
    |E| ratio w7/w3 = 0.538 (>1 = coherent, <1 = disordered)

  E(lines_changed):
    Window=3: mean=-57.901, std=381.303, |max|=2812.333
    Window=5: mean=-69.945, std=361.473, |max|=2726.000
    Window=7: mean=-81.121, std=358.578, |max|=2412.571
    C(E_w5):  mean=-0.062, range=[-1.000, 0.834]
    |E| ratio w7/w3 = 0.841 (>1 = coherent, <1 = disordered)

======================================================================
PREDICTION SCORECARD
======================================================================

  P1 (Monotonic accumulation):
     unwrap strictly monotone: True
     Repair ratios: unwrap=0.000, println=0.000, todo=0.125
     VERDICT: CONFIRMED

  P2 (Domain walls at session boundaries):
     Spearman rho: unwrap=-0.153 (p=1.482e-01), lines=-0.153 (p=1.474e-01), modules=0.011 (p=9.154e-01)
     Significant (p<0.05): 0/3 metrics, positive: 1/3
     VERDICT: NOT CONFIRMED

  P3 (Autocorrelation decay — no long-range order):
     Decorrelation: unwrap=2 commits, lines=6 commits
     VERDICT: CONFIRMED

  P4 (Human vs AI signatures differ):
     Mann-Whitney p = 0.1783
     Repair fraction: AI=0.34, Human=0.26
     VERDICT: NOT CONFIRMED (p>0.18)

  P5 (Model changes are domain walls):
     Median |A(unwrap)| at model changes: 3.0
     Median |A(unwrap)| at non-changes:   3.0
     Ratio: 1.00x
     n=17 model changes (small sample)
     VERDICT: NOT CONFIRMED (note: small n)
```

### Script 02 (02-aurasys-breaks.py)

```
======================================================================
PHASE TRANSITION ANALYSIS — AURASYS-MEMORY
======================================================================
N = 300 commits over 182 days
AI commits: 210 (70.0%)

======================================================================
3. STRUCTURAL BREAK SCAN — F-statistic across all possible split points
======================================================================

  memory_files:
    Best split at commit 279 (2026-05-08, day 172)
    F = 13.97, p = 2.2300e-04
    Pre-mean = 1.67, Post-mean = 14.86 (ratio = 8.91x)

  lines_changed:
    Best split at commit 20 (2026-02-13, day 88)
    F = 23.96, p = 1.6148e-06
    Pre-mean = 37259.00, Post-mean = 1614.32 (ratio = 0.04x)

  file_count:
    Best split at commit 20 (2026-02-13, day 88)
    F = 25.18, p = 9.0057e-07
    Pre-mean = 226.35, Post-mean = 12.24 (ratio = 0.05x)

  has_session:
    Best split at commit 93 (2026-02-26, day 101)
    F = 30.58, p = 7.0187e-08
    Pre-mean = 0.43, Post-mean = 0.15 (ratio = 0.35x)

  AI fraction (binary):
    Best split at commit 109 (2026-03-04, day 107)
    F = 23.00, p = 2.5599e-06
    Pre-mean = 0.86, Post-mean = 0.61 (ratio = 0.70x)

  commit_msg_length:
    Best split at commit 93 (2026-02-26, day 101)
    F = 31.44, p = 4.7012e-08
    Pre-mean = 63.65, Post-mean = 50.72 (ratio = 0.80x)

======================================================================
4. ABRCE OPERATORS — regime comparison
======================================================================

  Split point for regime comparison: commit 93 (2026-02-26)

  Autocorrelation of lines_changed:
    Pre  ACF[1..5]: -0.011 0.015 -0.010 -0.008 -0.001
    Pre  decorrelation: 1 commits
    Post ACF[1..5]: -0.027 -0.040 -0.005 0.045 -0.028
    Post decorrelation: 1 commits

======================================================================
5. CONVERGENCE OF STRUCTURAL BREAKS ACROSS METRICS
======================================================================

  Metric           Commit         Date    Day   F-stat    p-value
  --------------------------------------------------------------
  lines_changed        20   2026-02-13     88    23.96 1.6148e-06 ***
  file_count           20   2026-02-13     88    25.18 9.0057e-07 ***
  time_gap             20   2026-02-13     88    57.75 3.8901e-13 ***
  has_session          93   2026-02-26    101    30.58 7.0187e-08 ***
  msg_length           93   2026-02-26    101    31.44 4.7012e-08 ***
  AI_fraction         109   2026-03-04    107    23.00 2.5599e-06 ***
  memory_files        279   2026-05-08    172    13.97 2.2300e-04 ***
```

### Script 03 (03-multi-repo-convergence.py) — Aurasys Section

```
================================================================================
REPO: aurasys-memory
  N=300, range: 2025-11-17 to 2026-05-19
  AI: 210 (70.0%)
  Pre-transition commits: 46, Post: 254

  Metric            Break         Date DaysFromTx        F            p             Pre→Post
  ------------------------------------------------------------------------------------------
  lines_changed        19   2026-02-13         -1    25.55   7.5530e-07       39211.4→1609.2 ***
  file_count           19   2026-02-13         -1    26.89   3.9876e-07           238.2→12.2 ***
  AI_fraction         109   2026-03-04        +18    23.00   2.5599e-06              0.9→0.6 ***
  time_gap             19   2026-02-13         -1    59.00   2.2901e-13         6529.9→492.7 ***
  msg_length           93   2026-02-26        +11    31.44   4.7012e-08            63.6→50.7 ***

  Autocorrelation comparison (split at transition date, commit 46):
    lines_changed:
      Pre  ACF[1..5]: -0.013 0.015 -0.012 -0.013 -0.003 | decorr=1
      Post ACF[1..5]: 0.004 -0.028 -0.014 0.069 -0.022 | decorr=2
```

### Script 03 — Relinquishment Section

```
================================================================================
REPO: relinquishment
  N=924, range: 2026-02-14 to 2026-05-19
  AI: 820 (88.7%)
  Pre-transition commits: 10, Post: 914

  Metric            Break         Date DaysFromTx        F            p             Pre→Post
  ------------------------------------------------------------------------------------------
  lines_changed       274   2026-04-09        +54     7.10   7.8220e-03         7688.1→531.7 **
  file_count          274   2026-04-09        +54     6.32   1.2119e-02             40.1→4.3 *
  AI_fraction         472   2026-04-14        +59    91.56   9.5947e-21              0.8→1.0 ***
  time_gap            248   2026-04-06        +51    21.34   4.3839e-06           296.4→92.2 ***
  msg_length           18   2026-02-15         +1    14.53   1.4732e-04            48.6→63.7 ***

  Autocorrelation comparison (split at transition date, commit 10):

  Domain wall magnitude |A(lines)| comparison:
    Pre:  mean=27956, median=1251
    Post: mean=2797, median=90
    Mann-Whitney U=6267, p=0.0066
```

### Script 03 — Convergence Table

```
================================================================================
CONVERGENCE: Do structural breaks cluster at the same date across repos?
================================================================================

Repo                 Metric             Break Date Days from Tx      p-value
---------------------------------------------------------------------------
aurasys-memory       lines_changed      2026-02-13           -1   7.5530e-07 ***
aurasys-memory       file_count         2026-02-13           -1   3.9876e-07 ***
aurasys-memory       time_gap           2026-02-13           -1   2.2901e-13 ***
aurasys-memory       msg_length         2026-02-26          +11   4.7012e-08 ***
aurasys-memory       AI_fraction        2026-03-04          +18   2.5599e-06 ***
traveller-private    time_gap           2026-01-01          -44   1.0323e-03 **
traveller-private    msg_length         2026-01-01          -44   1.7539e-18 ***
traveller-private    AI_fraction        2026-01-15          -30   2.5639e-40 ***
traveller-private    lines_changed      2026-01-20          -25   4.9937e-02 *
traveller-private    file_count         2026-01-20          -25   6.1835e-02
relinquishment       msg_length         2026-02-15           +1   1.4732e-04 ***
relinquishment       time_gap           2026-04-06          +51   4.3839e-06 ***
relinquishment       lines_changed      2026-04-09          +54   7.8220e-03 **
relinquishment       file_count         2026-04-09          +54   1.2119e-02 *
relinquishment       AI_fraction        2026-04-14          +59   9.5947e-21 ***

Significant breaks: n=14
  Mean days from transition: +7.0
  Median days from transition: -0.2
  Std dev: 34.9 days
  Within ±30 days of transition: 7/14 (50%)
  One-sample t-test (H0: centered on transition): t=0.73, p=0.4797
```

### Script 03 — Comparison Table

```
================================================================================
COMPARISON: Governed repos vs ungoverned repo-008
================================================================================

  Repo-008 (ungoverned, 92 commits):
    Mean lines/commit: 462
    Mean |A(lines)|: 446
    ACF(lines)[1..3]: 0.191 0.218 0.123
    Decorrelation: 6 commits

  aurasys-memory (post-transition, 254 commits):
    Mean lines/commit: 1702
    Mean |A(lines)|: 2929
    ACF(lines)[1..3]: 0.004 -0.028 -0.014
    Decorrelation: 2 commits

  relinquishment (post-transition, 914 commits):
    Mean lines/commit: 2411
    Mean |A(lines)|: 2797
    ACF(lines)[1..3]: 0.495 -0.004 -0.004
    Decorrelation: 2 commits
```
