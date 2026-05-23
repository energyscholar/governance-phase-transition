# P10-1 Verification Report: Eight-Metric Analysis with Permutation Tests

**Generator:** Argus (Claude Opus 4.6)
**Date:** 2026-05-20
**Script:** `scripts/05-eight-metric-analysis.py`
**Parameters:** min_segment=20, alpha=0.05, n_perms=10,000, seed=42

---

## 1. Metrics Analyzed

Five original metrics (from P4) plus three new:

| # | Metric | Definition | Available |
|---|---|---|---|
| 1 | lines_changed | lines_added + lines_deleted | Both repos |
| 2 | file_count | files modified per commit | Both repos |
| 3 | time_gap | minutes since previous commit | Both repos |
| 4 | msg_length | character count of commit subject | Both repos |
| 5 | AI_fraction | 1 if AI-authored, 0 if human | Both repos |
| 6 | deletions_fraction | lines_deleted / lines_changed | Both repos |
| 7 | message_structure | 1 if subject contains ":" before char 50, else 0 | Both repos |
| 8 | path_entropy | Shannon entropy of top-level directory distribution per commit | Aurasys only |

**path_entropy unavailable for relinquishment:** The relinquishment commit-series JSON does not include per-commit file paths. The metric is computable from any git repo (see replication guidance) but was not extracted during initial data collection.

---

## 2. Aurasys-Memory (N = 300, 8 metrics)

**Bonferroni threshold:** 0.05 / (8 × 260) = 2.40 × 10⁻⁵

| Metric | Break Date | F | p (param) | p (perm) | Cohen's d | Bonf | BH | BH-perm |
|---|---|---|---|---|---|---|---|---|
| time_gap | 2026-02-13 | 57.75 | 3.89 × 10⁻¹³ | < 0.0001 | +1.76 | PASS | PASS | PASS |
| message_structure | 2026-02-14 | 57.98 | 3.52 × 10⁻¹³ | < 0.0001 | −1.23 | PASS | PASS | PASS |
| file_count | 2026-02-13 | 25.18 | 9.01 × 10⁻⁷ | 0.0005 | +1.16 | PASS | PASS | PASS |
| lines_changed | 2026-02-13 | 23.96 | 1.61 × 10⁻⁶ | 0.0008 | +1.13 | PASS | PASS | PASS |
| msg_length | 2026-02-26 | 31.44 | 4.70 × 10⁻⁸ | < 0.0001 | +0.70 | PASS | PASS | PASS |
| AI_fraction | 2026-03-04 | 23.00 | 2.56 × 10⁻⁶ | 0.0001 | +0.58 | PASS | PASS | PASS |
| path_entropy | 2026-03-07 | 10.55 | 1.29 × 10⁻³ | 0.0338 | −0.39 | FAIL | PASS | PASS |
| deletions_fraction | 2026-02-28 | 9.65 | 2.07 × 10⁻³ | 0.0452 | −0.38 | FAIL | PASS | PASS |

**Pre/post means for new metrics:**

| Metric | Pre-mean | Post-mean | Interpretation |
|---|---|---|---|
| deletions_fraction | 0.09 | 0.17 | Post-transition commits delete more (refactoring, not just adding) |
| message_structure | 0.53 | 0.92 | Post-transition commits nearly all use structured "prefix: description" format |
| path_entropy | 0.17 | 0.37 | Post-transition commits touch more diverse directory structures |

**Summary — aurasys:**
- Bonferroni (parametric): **6/8** (original 5 + message_structure)
- BH (parametric): **8/8**
- Permutation p < 0.05: **8/8**
- BH (permutation): **8/8**
- Parametric vs permutation agreement: **8/8** (no disagreements)

**Key finding:** message_structure breaks at **Feb 14** — one day after the Feb 13 cluster. This is the strongest new metric (F = 57.98, Cohen's d = −1.23). The shift from 53% to 92% structured commit messages coincides precisely with catalytic closure. Four metrics now cluster within 2 days of Feb 13 (time_gap, file_count, lines_changed at Feb 13; message_structure at Feb 14).

---

## 3. Relinquishment (N = 924, 7 metrics)

**Bonferroni threshold:** 0.05 / (7 × 884) = 8.08 × 10⁻⁶

| Metric | Break Date | F | p (param) | p (perm) | Cohen's d | Bonf | BH | BH-perm |
|---|---|---|---|---|---|---|---|---|
| AI_fraction | 2026-04-14 | 91.56 | 9.59 × 10⁻²¹ | < 0.0001 | −0.63 | PASS | PASS | PASS |
| deletions_fraction | 2026-03-18 | 45.40 | 2.83 × 10⁻¹¹ | < 0.0001 | −0.57 | PASS | PASS | PASS |
| time_gap | 2026-04-06 | 21.34 | 4.38 × 10⁻⁶ | 0.0186 | +0.34 | PASS | PASS | PASS |
| message_structure | 2026-04-13 | 14.00 | 1.94 × 10⁻⁴ | 0.0107 | −0.25 | FAIL | PASS | PASS |
| msg_length | 2026-02-16 | 11.51 | 7.21 × 10⁻⁴ | 0.0270 | −0.77 | FAIL | PASS | PASS |
| lines_changed | 2026-04-09 | 7.10 | 7.82 × 10⁻³ | 0.2578 | +0.19 | FAIL | PASS | FAIL |
| file_count | 2026-04-09 | 6.32 | 1.21 × 10⁻² | 0.2953 | +0.18 | FAIL | PASS | FAIL |

**Pre/post means for new metrics:**

| Metric | Pre-mean | Post-mean | Interpretation |
|---|---|---|---|
| deletions_fraction | 0.24 | 0.37 | Same direction as aurasys — more refactoring post-transition |
| message_structure | 0.75 | 0.85 | Modest increase; higher baseline (Triad was already active) |

**Summary — relinquishment:**
- Bonferroni (parametric): **3/7** (original 2 + deletions_fraction)
- BH (parametric): **7/7**
- Permutation p < 0.05: **5/7**
- BH (permutation): **5/7**
- Parametric vs permutation agreement: **5/7** (2 disagreements)

**Key finding — deletions_fraction:** Bonferroni PASS with F = 45.40, p < 10⁻¹¹, p_perm < 0.0001. Breaks at Mar 18. This is the **third Bonferroni survivor** for relinquishment (was 2/5 in P4, now 3/7). The direction is consistent with aurasys: governed development deletes more code (refactoring, cleanup) rather than only adding.

**Key finding — permutation disagreements:** lines_changed (p_perm = 0.258) and file_count (p_perm = 0.295) are parametrically significant (p < 0.013) but fail the permutation test. The permutation test accounts for the scan across 884 split points, which the parametric p-value does not. These two metrics showed small effect sizes (Cohen's d: 0.18–0.19) and were already Bonferroni failures. The permutation test confirms they are not robustly significant in relinquishment.

---

## 4. Parametric vs Permutation Comparison

| Repo | Metric | p (param) | p (perm) | Agree? |
|---|---|---|---|---|
| aurasys | lines_changed | 1.61 × 10⁻⁶ | 0.0008 | YES |
| aurasys | file_count | 9.01 × 10⁻⁷ | 0.0005 | YES |
| aurasys | time_gap | 3.89 × 10⁻¹³ | < 0.0001 | YES |
| aurasys | msg_length | 4.70 × 10⁻⁸ | < 0.0001 | YES |
| aurasys | AI_fraction | 2.56 × 10⁻⁶ | 0.0001 | YES |
| aurasys | deletions_fraction | 2.07 × 10⁻³ | 0.0452 | YES |
| aurasys | message_structure | 3.52 × 10⁻¹³ | < 0.0001 | YES |
| aurasys | path_entropy | 1.29 × 10⁻³ | 0.0338 | YES |
| relinquishment | lines_changed | 7.82 × 10⁻³ | 0.2578 | **DISAGREE** |
| relinquishment | file_count | 1.21 × 10⁻² | 0.2953 | **DISAGREE** |
| relinquishment | time_gap | 4.38 × 10⁻⁶ | 0.0186 | YES |
| relinquishment | msg_length | 7.21 × 10⁻⁴ | 0.0270 | YES |
| relinquishment | AI_fraction | 9.59 × 10⁻²¹ | < 0.0001 | YES |
| relinquishment | deletions_fraction | 2.83 × 10⁻¹¹ | < 0.0001 | YES |
| relinquishment | message_structure | 1.94 × 10⁻⁴ | 0.0107 | YES |

**13/15 agree** at α = 0.05. The 2 disagreements are both in relinquishment, both with small effect sizes (d < 0.2), both already Bonferroni failures. The permutation test is more conservative for weak effects in large datasets because it properly accounts for the search across all split points.

---

## 5. Impact on Paper Claims

### Original 5 metrics (P4 results unchanged)

The new Bonferroni threshold shifts slightly because we now correct for 8 (not 5) metrics:
- Aurasys: 2.40 × 10⁻⁵ (was 3.85 × 10⁻⁵) — all 5 originals still PASS
- Relinquishment: 8.08 × 10⁻⁶ (was 1.13 × 10⁻⁵) — time_gap and AI_fraction still PASS

The original 5 metrics are robust to the expanded correction.

### New metrics strengthen the case

1. **message_structure** (aurasys): F = 57.98, Bonferroni PASS, breaks at Feb 14. This is the second-highest F-statistic of any metric in either repo (after AI_fraction in relinquishment at F = 91.56). The one-day lag after the Feb 13 cluster is consistent with a cascading behavioral shift — commit message conventions changed within one session of catalytic closure.

2. **deletions_fraction** (both repos): Consistent direction (more deletions post-transition). Bonferroni PASS in relinquishment (F = 45.40). Interpretation: governed development produces refactoring commits (deleting and replacing code) rather than only accumulating new code. This is the behavioral opposite of the monotonic accumulation observed in the ungoverned baseline.

3. **path_entropy** (aurasys only): Borderline (Bonferroni FAIL, permutation p = 0.034). Modest effect (d = −0.39). Post-transition commits touch more diverse directories, consistent with structured cross-cutting work rather than single-directory bulk dumps.

### Updated tallies

| Correction | Aurasys (8 metrics) | Relinquishment (7 metrics) | Total |
|---|---|---|---|
| Bonferroni (parametric) | 6/8 | 3/7 | 9/15 |
| BH (parametric) | 8/8 | 7/7 | 15/15 |
| Permutation p < 0.05 | 8/8 | 5/7 | 13/15 |
| BH (permutation) | 8/8 | 5/7 | 13/15 |

---

## 6. Data Availability Note

**path_entropy for relinquishment:** The commit-series JSON for relinquishment does not include per-commit file paths. Path entropy is computable from any git repository using `git log --name-only` and is included in the replication scripts. Future data extraction should include file paths for all repos. This is a data collection limitation, not a methodological one.

---

## 7. Reproducibility

```bash
cd ~/software/governance-phase-transition
python3 scripts/05-eight-metric-analysis.py
```

All results are deterministic (fixed seed=42). Requires Python 3.10+, NumPy, SciPy.
