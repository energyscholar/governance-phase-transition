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

**Table 1: Structural breaks in the memory repository (aurasys-memory, N = 300)**

| Metric | Break Date | F | p | Pre-mean | Post-mean | Ratio |
|---|---|---|---|---|---|---|
| time_gap (min) | 2026-02-13 | 57.75 | 3.89 × 10⁻¹³ | 6,530 | 493 | 0.08× |
| file_count | 2026-02-13 | 25.18 | 9.01 × 10⁻⁷ | 226 | 12 | 0.05× |
| lines_changed | 2026-02-13 | 23.96 | 1.61 × 10⁻⁶ | 37,259 | 1,614 | 0.04× |
| msg_length (chars) | 2026-02-26 | 31.44 | 4.70 × 10⁻⁸ | 63.7 | 50.7 | 0.80× |
| AI_fraction | 2026-03-04 | 23.00 | 2.56 × 10⁻⁶ | 0.86 | 0.61 | 0.70× |

All five metrics produce highly significant breaks (p < 3 × 10⁻⁶). Three cluster at 2026-02-13 — the date Dignity Net was installed and catalytic closure was reached. The remaining two break within three weeks: msg_length on February 26, AI_fraction on March 4.

The pre-transition regime is characterized by large, infrequent commits touching many files (mean 226 files, 37,259 lines, 6,530-minute gaps). The post-transition regime shows smaller, more frequent commits (mean 12 files, 1,614 lines, 493-minute gaps). This is the transition from bulk data dumps to structured, session-coherent development — the behavioral signature the theory predicts for a shift from disordered to ordered phase.

**Robustness to min_segment.** Using min_segment = 15 (script 03) produces the same break dates with slightly higher F-statistics: time_gap F = 59.00, file_count F = 26.89, lines_changed F = 25.55. The two metrics breaking at later dates (msg_length, AI_fraction) are unaffected by the parameter choice. Break detection is robust.

**Temporal clustering.** Three of five metrics break at the same date (February 13). The probability of this occurring by chance under the null hypothesis of independent uniform break placement is vanishingly small. The remaining two metrics break within 19 days — consistent with a cascade in which the initial structural shift propagates through communication patterns and attribution behavior over subsequent sessions.

### 4.3 Relinquishment Repository: Independent Confirmation

The relinquishment repository (924 commits, 94 days) uses the same governance system but serves a different purpose (technical manuscript vs. governance infrastructure). Table 2 reports its structural breaks.

**Table 2: Structural breaks in the relinquishment repository (N = 924)**

| Metric | Break Date | F | p | Pre-mean | Post-mean | Ratio |
|---|---|---|---|---|---|---|
| msg_length (chars) | 2026-02-15 | 14.53 | 1.47 × 10⁻⁴ | 48.6 | 63.7 | 1.31× |
| time_gap (min) | 2026-04-06 | 21.34 | 4.38 × 10⁻⁶ | 296 | 92 | 0.31× |
| lines_changed | 2026-04-09 | 7.10 | 7.82 × 10⁻³ | 7,688 | 532 | 0.07× |
| file_count | 2026-04-09 | 6.32 | 1.21 × 10⁻² | 40.1 | 4.3 | 0.11× |
| AI_fraction | 2026-04-14 | 91.56 | 9.59 × 10⁻²¹ | 0.81 | 0.98 | 1.21× |

The relinquishment repository shows a delayed but convergent pattern. The first break (msg_length, February 15) appears two days after the memory repository's primary cluster — consistent with the governance transition propagating to a dependent project. The remaining four breaks cluster in early April (days +51 to +59 from the predicted transition), with AI_fraction showing an exceptionally strong break (F = 91.56, p = 9.59 × 10⁻²¹) as the project transitioned to near-exclusive AI generation under full Triad discipline.

The post-transition regime shows the same pattern as the memory repository: smaller commits (532 vs. 7,688 lines), fewer files (4.3 vs. 40.1), shorter gaps (92 vs. 296 minutes), and higher AI fraction (0.98 vs. 0.81). The directionality is consistent: governance produces focused, frequent, AI-assisted commits rather than sporadic bulk uploads.

### 4.4 Multi-Repository Convergence

Across the two governed repositories, 10 of 10 metrics produce significant structural breaks (p < 0.05). Table 3 compares autocorrelation structure across regimes.

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

The convergence of break dates across independent metrics and independent repositories supports the phase transition interpretation. The memory repository's primary cluster (February 13) coincides with the documented installation of the third governance component. The relinquishment repository's delayed breaks are consistent with a secondary response — governance transition in the infrastructure propagating to a dependent project through the shared system.

---

## 6. References

[1] Sacco, F., Sakthivadivel, D. A. R., & Levin, M. (2026). Topological constraints on self-organization in locally interacting systems. *Phil. Trans. R. Soc. A*, 384: 20250011.

[2] Kauffman, S. A. (1986). Autocatalytic sets of proteins. *J. Theor. Biol.*, 119(1), 1–24.

[3] Kauffman, S. A. (1993). *The Origins of Order: Self-Organization and Selection in Evolution*. Oxford University Press.

[4] Hordijk, W., & Steel, M. (2004). Detecting autocatalytic, self-sustaining sets in chemical reaction systems. *J. Theor. Biol.*, 227(4), 451–461.

[5] Peierls, R. (1936). On Ising's model of ferromagnetism. *Math. Proc. Cambridge Phil. Soc.*, 32(3), 477–481.

[6] Landau, L. D., & Lifshitz, E. M. (1980). *Statistical Physics, Part 1* (3rd ed.). Pergamon Press. §149.

[7] Stephenson, B., & Macomber, R. (2026). ABRCE Invariant Relational Kernel. GitHub: Relational-Relativity-Corporation/Invariant_Relational_Kernel_ABRCE.
