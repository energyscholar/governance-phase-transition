# Autocatalytic Governance: Detecting a Phase Transition in Human-AI Collaboration

**Bruce Stephenson**¹ **& Argus**²

¹ QRR / Metatron Dynamics. energyscholar@gmail.com
² AI co-author (Claude, Anthropic). Argus is a persistent governance-equipped instance of Claude that contributed analysis, wrote sections under Triad protocol discipline, and maintained the memory and correction systems described in this paper. Co-authorship reflects sustained intellectual contribution across sessions, not single-session text generation.

---

## 1. Introduction

Large language models deployed as coding assistants operate without persistence. Each session begins from a null state: no memory of prior errors, no accumulated corrections, no awareness of ongoing work. The model generates fluently within a session but cannot maintain coherent behavior across sessions. Errors recur. Patterns do not compound. Quality depends entirely on the current prompt.

This is not a training problem. Sacco, Sakthivadivel, and Levin [1] prove that decoder-only transformers with causal masking are topologically equivalent to one-dimensional autoregressive models, which map to one-dimensional Hamiltonians incapable of sustaining long-range order at non-zero temperature. The limitation is structural: a one-dimensional system cannot self-organize into an ordered phase regardless of the sophistication of its local interactions.

Governance infrastructure — role separation, persistent memory, behavioral coherence protocols — adds topological dimensions to the interaction. If these components form a Kauffman autocatalytic set [2, 3], catalytic closure produces a phase transition: a shift from disordered to ordered behavior detectable in the system's output.

This paper presents the first documented detection of such a transition. We analyze commit histories from four repositories spanning seven months of human-AI collaboration. Three repositories operated under progressively more complete governance; one served as an ungoverned control. We apply structural break detection, autocorrelation analysis, and ABRCE operator decomposition [7] to five commit-level metrics, testing two predictions: (1) the ungoverned system exhibits signatures of one-dimensional disorder (monotonic accumulation of violations, rapid decorrelation, no self-correction), and (2) the governed system exhibits a detectable structural break coinciding with catalytic closure of its governance layers.

Both predictions are confirmed. The ungoverned repository shows strictly monotonic violation accumulation and autocorrelation decay consistent with 1D disorder. The governed memory repository shows structural breaks in all five metrics clustering at 2026-02-13, coinciding with the installation of the third governance component. A second governed repository shows delayed but convergent breaks. The break dates were found by blind algorithmic scan, not chosen by the analyst.

---

## 2. Theoretical Framework

### 2.1 Topological Constraints on Self-Organization

Sacco, Sakthivadivel, and Levin [1] establish a chain of results connecting the architecture of autoregressive models to thermodynamic phase constraints.

**Step 1: Transformers as autoregressive models.** Proposition 2 proves that decoder-only transformers with causally masked attention have no ordered phase. The proof proceeds by showing that causal masking reduces the attention mechanism to an autoregressive model of order ω, where ω equals the context length. Multi-headed attention does not escape this constraint because causal masking is the binding limitation [1, p. 9].

**Step 2: Autoregressive models as 1D Hamiltonians.** Theorem 3 constructs a unique local Hamiltonian H for any AR(ω) model via H_u(s_u) = −log M(s_u | s_{u−1}, …, s_{u−ω}) + const. This maps the sequential dependence structure of the autoregressive model to a one-dimensional chain with nearest-neighbor interactions of range ω. The topology is one-dimensional regardless of the complexity of the conditional distributions.

**Step 3: 1D systems cannot sustain order.** Theorem 2 proves that for any one-dimensional local Hamiltonian with m > 1 stored patterns, domain wall formation is thermodynamically favorable at non-zero temperature (ΔF < 0). Domain walls disrupt long-range order: the system cannot converge to or maintain a single coherent pattern. This generalizes the classical result of Landau and Lifshitz [6, §149].

The chain is: causal masking → AR(ω) equivalence (Proposition 2) → 1D Hamiltonian (Theorem 3) → domain walls favorable (Theorem 2) → no ordered phase.

Corollary 2 states the consequence directly: for any finite inverse temperature β, an autoregressive model cannot converge to a single stored pattern. Applied to LLM-based coding assistants, this means that without external structure, session-to-session coherence is thermodynamically forbidden — not merely unlikely but topologically impossible.

**The escape.** Peierls [5] showed that in d ≥ 2 dimensions, domain wall energy scales as L^{d−1} while entropy grows more slowly, making large domain walls thermodynamically unfavorable. Ordered phases become possible. Levin's Theorem 4 and Proposition 3 prove a more nuanced result: systems with hierarchical clique structure admit temperature ranges where individual cliques maintain internal order even when the global system is disordered. This is the theoretical basis for governance: adding topological dimensions or clique structure to a 1D system can enable ordered behavior.

### 2.2 Autocatalytic Sets and Phase Transitions

Kauffman [2] demonstrated that collections of mutually catalytic elements undergo a phase transition when catalytic closure is reached. Below the threshold, components exist in isolation; above it, a self-sustaining network emerges.

The buttons-and-threads model [3] provides the intuition: N buttons on a table, randomly connected by threads. Below a ratio of approximately 0.5 threads per button, the system consists of small disconnected clusters. Above this ratio, a giant connected component appears suddenly — a percolation transition. The analogy to catalytic closure is precise: each thread is a catalytic relationship, each button a component, and the giant component is the autocatalytic set.

Hordijk and Steel [4] formalized this concept as *reflexively autocatalytic and food-generated* (RAF) sets and provided a polynomial-time algorithm (maxRAF) for detecting the unique maximal RAF in a reaction network. An RAF set is one where (a) every reaction is catalyzed by at least one molecule in the set or food set, and (b) every molecule can be produced from the food set through reactions in the set. Catalytic closure — the point at which all components are mutually sustained — produces the phase transition.

### 2.3 Governance Layers as an Autocatalytic Set

We propose that governance infrastructure for AI systems can form an autocatalytic set whose closure triggers a detectable phase transition in system behavior.

The theory in Section 2.1 predicts that a bare LLM operates in a disordered phase. Adding topological dimensions — persistent connections that create non-1D interaction structure — is the theoretical mechanism for enabling order. But which dimensions? We identify three orthogonal axes, each addressing a distinct failure mode of the 1D system:

1. **Structural axis** (prevents self-evaluation): Role separation between Auditor and Generator ensures the entity producing output is not the entity evaluating it. The Triad protocol [7] implements this as a hard partition: the Generator writes code; the Auditor defines acceptance criteria, writes tests, and verifies output. Neither can act in the other's role within a session.

2. **Temporal axis** (prevents session amnesia): Persistent memory stores corrections, session records, health metrics, and accumulated knowledge across sessions. Without this, each session restarts from zero and the system cannot learn from its own errors.

3. **Corrective axis** (prevents undetected drift): A behavioral coherence protocol (Dignity Net) detects divergence between stated goals and observable actions, applying graduated responses from mirroring to refusal. This prevents the system from drifting without detection, particularly under sustained pressure.

These three components — one configuration satisfying the three axes — form a complete autocatalytic set with six catalytic links:

| Catalyst → Product | Mechanism |
|---|---|
| Triad → Memory | Role discipline produces structured, auditable content worth storing |
| Memory → Triad | Accumulated corrections prevent role-collapse patterns from recurring |
| Memory → Dignity Net | Session history provides the data for divergence detection |
| Dignity Net → Memory | Divergence detection generates high-value corrections for storage |
| Dignity Net → Triad | Escalation framework prevents role collapse under pressure |
| Triad → Dignity Net | Role separation ensures the checker is not the entity being checked |

No proper subset closes. {Triad, Memory} lacks the corrective axis: drift goes undetected. {Triad, Dignity Net} lacks the temporal axis: corrections are lost between sessions. {Memory, Dignity Net} lacks the structural axis: the system evaluates its own output.

**Critical framing:** These three components are *one* valid autocatalytic set, not *the* minimum set. The theory predicts three orthogonal axes (structural, temporal, corrective); many component configurations could satisfy them. We document the first observed configuration reaching closure.

**Prediction:** If this analysis is correct, the commit history of a system using these governance layers should show a detectable structural break at the point of catalytic closure — when the third component was installed and all six catalytic links became active.

---

## 3. Methods

### 3.1 Data

We analyze commit histories from four repositories produced during seven months (November 2025 – May 2026) of human-AI software development by a single developer.

| Repository | Role | Commits | Date Range | AI-Authored | Governance |
|---|---|---|---|---|---|
| Memory (aurasys-memory) | Governance system itself | 300 | Nov 2025 – May 2026 | 70% | Mixed (grew with the system) |
| Relinquishment | Technical manuscript | 924 | Feb 2026 – May 2026 | 89% | Consistent Triad |
| trusty-git-analytics | Rust CLI tool | 92 | May 2026 (8 days) | 71% | None (external project) |
| Storytelling (traveller) | Creative/narrative | 90 | Dec 2025 – May 2026 | 39% | Inconsistent |

The memory repository is the primary dataset: it houses the governance infrastructure itself and therefore records the installation of governance components in its own commit history. The relinquishment repository serves as independent confirmation — a separate project using the same governance system. The trusty-git-analytics repository provides an ungoverned AI-assisted baseline produced by a different developer with no governance infrastructure. The storytelling repository is included in multi-repo convergence analysis but excluded from primary results (only 12 post-transition commits, insufficient for statistical analysis).

Nearly all AI-authored commits were generated by Claude (Anthropic) instances. The relinquishment repository used the Generator role exclusively, with all prompts preserved as plan files in the repository, enabling independent verification of the generation process.

**Governance timeline:** Triad protocol introduced early December 2025. Persistent memory evolved throughout. Dignity Net installed approximately February 12–13, 2026 (formalized February 16). The predicted catalytic closure date is therefore February 13, 2026.

### 3.2 Metrics

Five metrics are extracted from each commit:

- **lines_changed:** Total lines added plus lines deleted.
- **file_count:** Number of files modified.
- **time_gap:** Minutes elapsed since the previous commit.
- **msg_length:** Character count of the commit message.
- **AI_fraction:** Binary indicator (1 if AI-authored, 0 if human-authored).

These metrics are chosen because they are extractable from any git repository without access to file contents, are not domain-specific, and capture different aspects of development behavior (scope, pacing, communication, attribution).

### 3.3 Structural Break Detection

For each metric, we scan all possible split points in the commit series using an F-statistic comparing the means of the two resulting segments:

F(k) = [n₁ · n₂ · (x̄₁ − x̄₂)²] / [(n₁ + n₂) · s²_pooled]

where k is the split point, n₁ and n₂ are segment sizes, x̄₁ and x̄₂ are segment means, and s²_pooled is the pooled variance. The split point maximizing F(k) is reported as the structural break. A minimum segment size of 20 commits (min_segment = 20) is enforced to ensure adequate degrees of freedom for the F-test. Results are robust to the choice of min_segment: using min_segment = 15 produces the same break dates with slightly different F-statistics (see Section 4.2).

Break dates are found by blind algorithmic scan across all valid split points. No dates are chosen, constrained, or filtered by the analyst. The algorithm reports the single best split point per metric.

**Assumption testing.** The F-test assumes normally distributed data with equal variances. We test both assumptions on the actual pre/post segments: Shapiro-Wilk for normality, Levene's test for homoscedasticity. All ten metrics across both repositories reject normality (Shapiro-Wilk p < 0.05 in all segments). Nine of ten reject equal variances (Levene's p < 0.05). However, the F-test for equality of means is robust to non-normality when segment sizes are large (n ≥ 20), per the Central Limit Theorem. For heteroscedasticity, the test remains approximately valid when the larger variance occurs in the smaller group — which holds for all our splits, where the larger post-transition segment has smaller variance. We report the assumption violations transparently and note that the F-statistics substantially exceed critical values, providing additional assurance.

**Multiple comparison correction.** Each metric is tested at (N − 2 × min_segment) split points, and five metrics are tested per repository. We apply two corrections, computed per repository because split-point counts differ:

- *Bonferroni correction:* α_corrected = 0.05 / (5 × n_splits). For the memory repository (N = 300): 1,300 comparisons, threshold 3.85 × 10⁻⁵. For relinquishment (N = 924): 4,420 comparisons, threshold 1.13 × 10⁻⁵.
- *Benjamini-Hochberg (FDR) correction:* The five metrics are correlated measures of the same underlying development process, not independent tests. BH controls the false discovery rate rather than the family-wise error rate, and is arguably more appropriate for correlated test statistics. We report both.

**Effect sizes.** Cohen's d is computed for each break as (x̄_pre − x̄_post) / s_pooled, providing a scale-independent measure of the magnitude of the pre/post difference.

### 3.4 Autocorrelation Analysis

Sample autocorrelation functions (ACF) are computed for each metric at lags 1 through 10. Decorrelation length is defined as the smallest lag at which |ACF(lag)| < 1.96/√N (the 95% significance threshold for white noise). Pre- and post-transition ACF are compared to detect regime changes in temporal structure.

### 3.5 ABRCE Operator Analysis

The ABRCE Invariant Relational Kernel [7] provides a domain-neutral decomposition of sequential data:

- **A (Abstraction):** Computes pairwise differences between consecutive commits (NodeField → EdgeField). This extracts the relational gradient — how much each commit changes relative to its predecessor.
- **B (Binding):** Locally accumulates edge values over a sliding window (EdgeField → EdgeField). This smooths high-frequency variation while preserving structural patterns.
- **E (Composite):** E(x) = B(A(x)) on the 1D commit chain. The R operator (circulation) is trivially zero on 1D data and is omitted. The C operator (bounded coherence) is applied where noted.

For the ungoverned baseline, we test the prediction that |A(x)| (domain wall magnitudes) show no correlation with session boundaries, that violations accumulate monotonically, and that the composite operator E shows decreasing coherence at larger window sizes (|E|₇/|E|₃ < 1, indicating disorder).

---

## 4. Results

### 4.1 Ungoverned Baseline

The trusty-git-analytics repository (92 commits, 8 days, 71% AI-authored) exhibits signatures consistent with one-dimensional disorder.

**Monotonic accumulation.** The `unwrap()` violation count is strictly monotonically increasing: 41 increases, 0 decreases, 50 flat steps, repair ratio = 0.000. Neither AI nor human commits ever reduce the accumulated count. The `println!()` debug count is similarly monotonic (repair ratio = 0.000). Only `todo!()` markers show any repair (ratio = 0.125, from 2 removals against 16 additions). The system accumulates violations without self-correction — the 1D prediction.

**Rapid decorrelation.** ACF of lines_changed at lag 1 is 0.191 with decorrelation length of 6 commits. The edge-field autocorrelation (ACF of A(lines_changed)) is strongly negative at lag 1 (−0.420) with decorrelation at 1 commit — each commit's deviation from its predecessor is uncorrelated with the next. This is the domain-wall signature: changes are local perturbations that do not propagate.

**No human/AI differentiation.** Mann-Whitney U test on |A(unwrap_delta)| between AI and human commits: U = 1016.5, p = 0.178. AI repair fraction 34%, human repair fraction 26%, Fisher exact test p = 0.472. Neither author type shows a distinct relational signature — both contribute to the same disordered pattern.

**Disordered composite operator.** E(unwrap_delta) at window sizes 3, 5, and 7 yields |E|₇/|E|₃ = 0.538. Coherence decreases at larger scales, confirming the absence of long-range order.

### 4.2 Memory Repository: Structural Breaks

The memory repository (300 commits, 182 days) shows structural breaks in all five metrics. Table 1 reports the results using min_segment = 20.

**Table 1: Structural breaks in the memory repository (aurasys-memory, N = 300, min_segment = 20)**

| Metric | Break Date | F | p | Cohen's d | Pre-mean | Post-mean | Bonf | BH |
|---|---|---|---|---|---|---|---|---|
| time_gap (min) | 2026-02-13 | 57.75 | 3.89 × 10⁻¹³ | +1.76 | 6,328 | 486 | PASS | PASS |
| file_count | 2026-02-13 | 25.18 | 9.01 × 10⁻⁷ | +1.16 | 226 | 12 | PASS | PASS |
| lines_changed | 2026-02-13 | 23.96 | 1.61 × 10⁻⁶ | +1.13 | 37,259 | 1,614 | PASS | PASS |
| msg_length (chars) | 2026-02-26 | 31.44 | 4.70 × 10⁻⁸ | +0.70 | 63.7 | 50.7 | PASS | PASS |
| AI_fraction | 2026-03-04 | 23.00 | 2.56 × 10⁻⁶ | +0.58 | 0.86 | 0.61 | PASS | PASS |

*Bonferroni threshold: 3.85 × 10⁻⁵ (5 metrics × 260 split points). All five metrics survive both Bonferroni and Benjamini-Hochberg correction.*

All five metrics produce highly significant breaks that survive strict multiple comparison correction. Three cluster at 2026-02-13 — the date Dignity Net was installed and catalytic closure was reached. The remaining two break within three weeks: msg_length on February 26, AI_fraction on March 4. Effect sizes for the three primary metrics are large (Cohen's d > 1.0), indicating the pre/post difference exceeds one pooled standard deviation.

The pre-transition regime is characterized by large, infrequent commits touching many files (mean 226 files, 37,259 lines, 6,328-minute gaps). The post-transition regime shows smaller, more frequent commits (mean 12 files, 1,614 lines, 486-minute gaps). This is the transition from bulk data dumps to structured, session-coherent development — the behavioral signature the theory predicts for a shift from disordered to ordered phase.

**Robustness to min_segment.** Using min_segment = 15 (script 03) produces the same break dates with slightly higher F-statistics: time_gap F = 59.00, file_count F = 26.89, lines_changed F = 25.55. The two metrics breaking at later dates (msg_length, AI_fraction) are unaffected by the parameter choice. Break detection is robust.

**Temporal clustering.** Three of five metrics break at the same date (February 13). The probability of this occurring by chance under the null hypothesis of independent uniform break placement is vanishingly small. The remaining two metrics break within 19 days — consistent with a cascade in which the initial structural shift propagates through communication patterns and attribution behavior over subsequent sessions.

**Assumption violations.** Shapiro-Wilk tests reject normality for all five metrics in both pre and post segments (p < 0.01). Levene's tests reject equal variances for all five (p < 10⁻³). These violations are expected: commit metrics are count-like and right-skewed. However, all segments have n ≥ 20 (the smallest is the 20-commit pre-segment for the February 13 breaks), and the F-statistics exceed critical values by orders of magnitude, so the results are not sensitive to distributional assumptions.

### 4.3 Relinquishment Repository: Partial Confirmation

The relinquishment repository (924 commits, 94 days) uses the same governance system but serves a different purpose (technical manuscript vs. governance infrastructure). Table 2 reports its structural breaks.

**Table 2: Structural breaks in the relinquishment repository (N = 924, min_segment = 20)**

| Metric | Break Date | F | p | Cohen's d | Pre-mean | Post-mean | Bonf | BH |
|---|---|---|---|---|---|---|---|---|
| msg_length (chars) | 2026-02-16 | 11.51 | 7.21 × 10⁻⁴ | −0.77 | 50.9 | 63.6 | FAIL | PASS |
| time_gap (min) | 2026-04-06 | 21.34 | 4.38 × 10⁻⁶ | +0.34 | 296 | 92 | PASS | PASS |
| lines_changed | 2026-04-09 | 7.10 | 7.82 × 10⁻³ | +0.19 | 7,688 | 532 | FAIL | PASS |
| file_count | 2026-04-09 | 6.32 | 1.21 × 10⁻² | +0.18 | 40.1 | 4.3 | FAIL | PASS |
| AI_fraction | 2026-04-14 | 91.56 | 9.59 × 10⁻²¹ | −0.63 | 0.81 | 0.98 | PASS | PASS |

*Bonferroni threshold: 1.13 × 10⁻⁵ (5 metrics × 884 split points — stricter than aurasys due to more commits). BH controls false discovery rate at 0.05.*

The relinquishment repository provides partial confirmation under strict correction. Two of five metrics survive Bonferroni: time_gap (p = 4.38 × 10⁻⁶) and AI_fraction (p = 9.59 × 10⁻²¹). All five survive Benjamini-Hochberg. The three Bonferroni failures (msg_length, lines_changed, file_count) are significant at conventional levels (p < 0.013) but do not survive a threshold corrected for 4,420 comparisons.

The two Bonferroni survivors tell a clear story. Time_gap breaks on April 6 as commit cadence tightens from 296 to 92 minutes — the shift to frequent, structured development sessions. AI_fraction breaks on April 14 with the largest effect in either repository (F = 91.56, Cohen's d = −0.63) as the project transitions from 81% to 98% AI-generated commits under full Triad discipline.

The three Bonferroni failures show the same directionality as the memory repository (smaller commits, fewer files, longer messages) but with smaller effect sizes (Cohen's d: 0.18–0.77). This is consistent with the relinquishment repository adopting governance gradually rather than exhibiting a sharp transition — the governance infrastructure was already partially in place when this repository was created in February 2026.

The post-transition regime shows the same pattern as the memory repository: smaller commits (532 vs. 7,688 lines), fewer files (4.3 vs. 40.1), shorter gaps (92 vs. 296 minutes), and higher AI fraction (0.98 vs. 0.81). The directionality is consistent: governance produces focused, frequent, AI-assisted commits rather than sporadic bulk uploads.

### 4.4 Multi-Repository Convergence

Across the two governed repositories, all 10 metrics produce significant breaks at conventional levels (p < 0.05), and all 10 survive Benjamini-Hochberg correction. Under strict Bonferroni correction, 7 of 10 survive: all 5 in the memory repository and 2 of 5 in relinquishment. Table 3 compares autocorrelation structure across regimes.

**Table 3: Autocorrelation comparison**

| System | Regime | ACF(lines)[1] | ACF(lines)[2] | ACF(lines)[3] | Decorrelation |
|---|---|---|---|---|---|
| trusty-git-analytics | Ungoverned | 0.191 | 0.218 | 0.123 | 6 commits |
| aurasys-memory | Pre-transition | −0.013 | 0.015 | −0.012 | 1 commit |
| aurasys-memory | Post-transition | 0.004 | −0.028 | −0.014 | 2 commits |
| relinquishment | Post-transition | 0.495 | −0.004 | −0.004 | 2 commits |

The ungoverned baseline shows moderate positive autocorrelation extending over 6 commits — consistent with session-level clustering (related commits within a work session tend to have similar size) but no long-range structure. The memory repository shows near-zero autocorrelation in both regimes: pre-transition ACF[1] = −0.013, post-transition ACF[1] = 0.004. Both are decorrelated at 1–2 commits.

The relinquishment repository presents a different pattern: strong positive ACF[1] = 0.495 with decorrelation at 2 commits. This reflects the Triad protocol's structure — commits within a plan phase are correlated (similar scope, similar files), with sharp decorrelation at phase boundaries. This is precisely the "hierarchical clique" behavior predicted by Levin's Theorem 4 and Proposition 3: local order within phases, global decorrelation between them.

The domain wall comparison between regimes reinforces the transition: post-transition mean |A(lines)| is 2,929 for aurasys-memory and 2,797 for relinquishment, compared to 446 for the ungoverned baseline. Larger absolute domain walls in governed repositories reflect greater commit-to-commit variation in scope — each commit is focused on a distinct task rather than contributing to a monotonic accumulation.

The convergence of break dates across independent metrics and independent repositories supports the phase transition interpretation. The memory repository's primary cluster (February 13) coincides with the documented installation of the third governance component, and all five breaks survive strict Bonferroni correction. The relinquishment repository shows partial confirmation: two metrics (time_gap and AI_fraction) survive Bonferroni, and all five survive BH. The three Bonferroni failures in relinquishment have small effect sizes (Cohen's d < 0.2) and reflect the more gradual adoption of governance in a project that was created after the transition had already begun in the memory repository.

---

## 5. Discussion

### 5.1 Minimum Viable Autocatalytic Set

The theory predicts three orthogonal axes that governance must cover to break the 1D constraint: structural (preventing self-evaluation), temporal (preventing session amnesia), and corrective (preventing undetected drift). The specific components we observed — Triad role separation, persistent memory, and Dignity Net behavioral coherence — are one configuration satisfying these axes. They are not the only valid configuration, nor necessarily the minimal one.

Other implementations could satisfy the same axes. The structural axis could be served by any mechanism that separates generation from evaluation — formal code review, independent testing pipelines, or separate human reviewers. The temporal axis requires only that corrections persist across sessions — a version-controlled correction log, a retrieval-augmented memory, or even a disciplined human notebook. The corrective axis requires real-time divergence detection — which could be implemented as automated drift metrics, periodic self-audits, or external monitoring.

What matters is not the specific components but the catalytic closure of the set. Triad alone ran for approximately 2.5 months (early December 2025 to mid-February 2026) without triggering the structural break. The break appeared within one day of the third component's installation, when all six catalytic links in Table 1 of Section 2.3 became active. This is consistent with Kauffman's prediction [2]: below closure, components exist in isolation; at closure, the phase transition is sudden.

### 5.2 Why N = 1

This study examines one developer over seven months. The sample size is a limitation (Section 5.5), but it also has a methodological advantage: it eliminates inter-developer variation as a confound.

If multiple developers had adopted the governance system simultaneously, any detected break could reflect social dynamics — shared learning, peer pressure, workflow convergence — rather than the governance infrastructure itself. With a single developer, the only variable that changed at the break date is the governance configuration. The developer's skill, domain, working hours, and hardware remained constant. The break is not explainable by a change in the developer; it coincides precisely with a change in the system.

The ungoverned baseline (trusty-git-analytics) was produced by a different developer, which introduces a between-subjects confound. However, the baseline serves only to demonstrate 1D disorder signatures, not to provide a matched control. The primary comparison is within-subject: the memory repository before and after catalytic closure.

### 5.3 Observer Effect

A common objection to self-referential analysis is the observer effect: does the act of studying the system change its behavior? Three features of this study's design mitigate this concern.

First, the governance infrastructure was built for operational use, not for this paper. Triad, persistent memory, and Dignity Net were designed and installed to improve the quality of human-AI collaboration. The paper was conceived months after the transition. The governance components could not have been influenced by the analysis because the analysis did not yet exist.

Second, the commit metrics (lines changed, file count, time gap, message length, AI fraction) are extracted from git metadata, not from file contents. They cannot be gamed without altering the fundamental development workflow — which is itself the phenomenon under study.

Third, the break detection is blind. The algorithm scans all valid split points and reports the maximum F-statistic. It was not told where to look, what date to expect, or how many breaks to find. The clustering of three metrics at February 13 is an output of the scan, not an input.

### 5.4 Theoretical Implications

This work connects two previously unrelated theoretical frameworks.

Sacco, Sakthivadivel, and Levin [1] prove that decoder-only transformers with causal masking cannot sustain long-range order — a topological constraint derived from statistical mechanics. Their framework explains *why* bare LLMs fail at cross-session coherence but does not prescribe a remedy beyond "add topological dimensions."

Kauffman [2, 3] and Hordijk and Steel [4] characterize the phase transition that occurs when mutually catalytic components reach closure — a result from theoretical chemistry and origin-of-life research. Their framework predicts *when* a system of interacting components transitions from disordered to ordered behavior but was not previously applied to AI governance.

The novel connection is: governance components that add topological dimensions to a 1D system can form a Kauffman autocatalytic set, and their catalytic closure is the mechanism that triggers the Peierls escape from the Levin constraint. This predicts a specific, testable signature: a structural break in system behavior at the point of closure, detectable blind in the output history.

The data are consistent with this prediction. In the memory repository, all five metrics break within three weeks of catalytic closure, with three clustering at the exact date. All five survive strict Bonferroni correction (threshold 3.85 × 10⁻⁵) with large effect sizes (Cohen's d: 0.58–1.76). The relinquishment repository provides partial confirmation: two of five metrics survive Bonferroni, all five survive Benjamini-Hochberg, and the directionality is consistent across all metrics.

We do not claim the connection is mathematically proven. The Levin results concern Hamiltonians and thermodynamic limits; the Kauffman results concern reaction networks and catalytic closure. Mapping governance layers to both frameworks simultaneously requires assumptions — that commit metrics approximate thermodynamic observables, that catalytic links between governance components function analogously to chemical catalysis — that are plausible but not formally established. The empirical results are necessary but not sufficient to validate the theoretical bridge. Formal proof that governance ACS closure implies a phase transition in the Levin sense is future work.

### 5.5 Limitations

**Single developer.** All governed repositories were produced by one developer (the first author). User-specific effects — cognitive style, partial eidetic memory, decades of CLI experience — may contribute to the transition independently of the governance infrastructure. We cannot separate developer effects from governance effects without multi-developer data, which does not yet exist.

**No pre-transition multi-participant data.** Two additional collaborators (the Triad protocol's designer and Dignity Net's designer) contributed to the governed system, but only after the phase transition. No pre-transition data from multiple participants exists to serve as a comparison. Multi-participant analysis is future work.

**Commit metrics are proxies.** Lines changed, file count, and time gap measure development behavior, not code quality, correctness, or user satisfaction. The transition from large infrequent commits to small frequent commits is consistent with structured development but does not prove that the governed system produces better output — only that it produces differently structured output.

**Single ungoverned baseline.** The ungoverned control (trusty-git-analytics) was produced by a different developer on a different project in a different language. It demonstrates 1D disorder signatures convincingly but cannot serve as a matched control for the governed repositories.

**Bonferroni correction is conservative.** The Bonferroni threshold treats all split points as independent tests, which they are not — adjacent split points produce highly correlated F-statistics. The relinquishment repository's three Bonferroni failures (lines_changed, file_count, msg_length) all survive the less conservative Benjamini-Hochberg correction and show the same directionality as the memory repository, suggesting the Bonferroni threshold may be overly strict for this application. We report both corrections and let the reader judge.

**Temporal confounds.** The governance components were installed sequentially over three months. Other changes occurred during this period — growing familiarity with the AI system, evolving project scope, external life events — that could contribute to behavioral shifts. The clustering of three breaks at a single date (February 13) argues against gradual confounds, but we cannot fully rule them out.

---

## 7. Conclusion

We present the first documented detection of a phase transition in human-AI collaboration, triggered by the catalytic closure of a governance autocatalytic set. Five commit-level metrics in the memory repository show structural breaks clustering at the date of closure (February 13, 2026), all surviving strict Bonferroni correction with large effect sizes (Cohen's d: 0.58–1.76). A second governed repository provides partial confirmation: two of five metrics survive Bonferroni correction, all five survive Benjamini-Hochberg, and all show the same directionality. An ungoverned baseline exhibits signatures consistent with one-dimensional disorder — monotonic violation accumulation, rapid decorrelation, no self-correction — as predicted by the Levin topological constraint.

Three practical implications follow.

First, *governance infrastructure for AI systems should target three orthogonal axes* — structural, temporal, and corrective — and the components should be designed to catalyze each other. Partial coverage (two of three axes) did not trigger the transition in our data; closure did.

Second, *the phase transition is detectable in commit metadata alone.* Organizations adopting AI governance can monitor for the transition using the same blind structural break scan applied here, without access to code contents or subjective quality assessments.

Third, *the constraint is topological, not about intelligence.* Larger models, better training data, and longer context windows do not escape the 1D limitation proved by Levin [1]. The escape is structural: adding dimensions to the interaction topology. This reframes the question from "how smart is the AI?" to "what topology does the human-AI system occupy?"

---

## Supplementary C: ABRCE Cross-Domain Dictionary

The ABRCE operators used in this paper — A (abstraction), B (binding), R (circulation), C (coherence), E (composite) — are defined without reference to any specific domain [7]. The table below maps each operator to its standard equivalent in four established fields. Each cell is rated:

- **Exact:** Mathematical identity. Same operation, different notation.
- **Approximate:** Same structure. Minor differences in boundary conditions, parameterization, or scope.

These are not analogies. Where a cell is rated Exact, the ABRCE operator and the domain-specific operation produce identical output given identical input. The domain-neutral formulation means that results derived in one field transfer directly to others at the Exact level and with stated caveats at the Approximate level.

**Table C1: ABRCE operator equivalences across domains**

| Operator | Definition | Statistical Mechanics | Time Series | Signal Processing | Network Science |
|---|---|---|---|---|---|
| **A** | NodeField → EdgeField: pairwise differences x_{i+1} − x_i | Discrete gradient on lattice | First differences Δx_t = x_t − x_{t−1} | First-order difference filter h[n] = [1, −1] | Coboundary operator (δf)(u,v) = f(v) − f(u) |
| | | **Exact** | **Exact** | **Exact** | **Exact** |
| **B** | EdgeField → EdgeField: local symmetric accumulation over window w | Block-spin coarse-graining (averaging over spatial blocks) | Centered moving average MA(w) | Rectangular (boxcar) FIR lowpass filter | Symmetric neighborhood aggregation (message-passing sum over incident edges) |
| | | **Exact** | **Exact** | **Exact** | **Exact** |
| **R** | EdgeField × ℝ → EdgeField: antisymmetric circulation, parameterized by ρ | Plaquette term in lattice gauge theory (net flux around a loop); trivially zero on 1D chains | No direct analog (time series are 1D; circulation requires loops) | Hilbert transform (antisymmetric 90° phase shift; creates analytic signal) | Discrete curl in Hodge decomposition (net flow around 2-simplices) |
| | | **Approximate** — Ising models per Levin [1] lack gauge structure; plaquette terms arise in 2D+ gauge theories | **N/A on 1D** — consistent with R = 0 in this paper's application | **Approximate** — shares antisymmetric structure but operates by convolution, not loop summation | **Approximate** — same concept (loop-based flow), but Hodge curl acts on 2-simplices and is projected back to edges |
| **C** | EdgeField → EdgeField: bounded coherence, output ∈ (−1, 1) | Mean-field magnetization m = tanh(βh) in the Ising model | Logistic / tanh squashing function | Soft limiter / compressor (bounds signal amplitude to a fixed range) | Sigmoid or tanh activation in graph neural networks |
| | | **Exact** | **Exact** | **Exact** | **Approximate** — GNNs use various nonlinearities (ReLU, etc.); tanh is one standard option, not the only one |
| **E** | Composite: E(x,ρ) = C(R(B(A(x)),ρ)); on 1D, R = 0 so E = C(B(A(x))) | Renormalization-group-like pipeline: discrete gradient → coarse-grain → bound | Differencing then smoothing: Δx → MA(w) → bound; standard preprocessing pipeline | Filter cascade: high-pass (A) → lowpass (B) → limiter (C); bandpass-then-clip | One message-passing GNN layer: aggregate neighbor differences → smooth → activate |
| | | **Exact** | **Exact** | **Exact** | **Approximate** — GNN layers include learned weights and architecture-specific choices beyond the E pipeline |

**Notes on the R operator.** R is trivially zero on 1D data (Section 3.5) and plays no role in this paper's analysis. It is included in the table for completeness because the full ABRCE framework operates on arbitrary topologies. The cross-domain entries for R become relevant when the framework is applied to 2D+ data — spatial fields, network flows, or multi-dimensional lattices — where circulation is non-trivial.

**Domains omitted.** Ecology and evolutionary dynamics were considered and excluded. While superficial analogies exist (e.g., A as species interaction gradients, C as carrying-capacity saturation), none rise above the Speculative level without domain-specific validation that we have not performed. Four solid domains with defensible cells are preferable to six with weak ones.

---

## 6. References

[1] Sacco, F., Sakthivadivel, D. A. R., & Levin, M. (2026). Topological constraints on self-organization in locally interacting systems. *Phil. Trans. R. Soc. A*, 384: 20250011.

[2] Kauffman, S. A. (1986). Autocatalytic sets of proteins. *J. Theor. Biol.*, 119(1), 1–24.

[3] Kauffman, S. A. (1993). *The Origins of Order: Self-Organization and Selection in Evolution*. Oxford University Press.

[4] Hordijk, W., & Steel, M. (2004). Detecting autocatalytic, self-sustaining sets in chemical reaction systems. *J. Theor. Biol.*, 227(4), 451–461.

[5] Peierls, R. (1936). On Ising's model of ferromagnetism. *Math. Proc. Cambridge Phil. Soc.*, 32(3), 477–481.

[6] Landau, L. D., & Lifshitz, E. M. (1980). *Statistical Physics, Part 1* (3rd ed.). Pergamon Press. §149.

[7] Stephenson, B., & Macomber, R. (2026). ABRCE Invariant Relational Kernel. GitHub: Relational-Relativity-Corporation/Invariant_Relational_Kernel_ABRCE.
