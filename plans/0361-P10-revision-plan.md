# Plan 0361-P10: Paper Revision

**Status:** READY FOR REVIEW
**Date:** 2026-05-20
**Source:** Author review (Bruce Stephenson) + Argus critical analysis + ChatGPT independent review
**Paper:** `paper/stephenson-et-al-2026-autocatalytic-governance.md`

---

## 1. Context

P1-P9 produced a complete draft. Bruce read the built PDF and identified issues.
Argus conducted an independent critical analysis. ChatGPT provided two rounds of
review (shallow, then deep after targeted prompts). This plan consolidates all
feedback into revision phases with Generator prompts.

The paper's core argument is sound. The issues are:
- Structural framing (external repos treated as primary results instead of tool validation)
- Audience accessibility (theory-heavy, practical finding buried, corrective axis misnamed)
- Missing content (figures, replication guidance, additional metrics)
- Limitations section needs surgery (straw men, humble-brags, false claims)

---

## 2. Issues Register

### Critical (4)

| ID | Section | Issue | Fix |
|---|---|---|---|
| R8 | Abstract | Killer practical finding (metadata-only detection) missing | Add sentence before "first documented" |
| R9 | Intro | Opening sentence false ("operate without persistence") | Rewrite: architecture, not persistence |
| R15 | Structure | External repos framed as primary results; should be tool validation | Move 4.1 to methods validation, 2-repo primary table |
| R20 | Throughout | Zero figures in a phase transition paper | Add timeline, metric plot, ACS schematic |

### High (12)

| ID | Section | Issue | Fix |
|---|---|---|---|
| R1 | 3.5 | ABRCE not explained; R and C missing; no cross-domain connection | Full 5-operator intro, R=0 significance, ref Supp C |
| R2 | 5.5 | "Single developer" false — 3 people designed governance | Distinguish committer from designer |
| R11 | Discussion | Engineers dismiss corrective axis — not preempted | New subsection: data shows 2.5mo open-loop fails |
| R12 | 2.1 | Engineers will read "no order" as "LLMs worthless" | Add within-session clarification |
| R13 | Throughout | External repo analysis too prominent | Trim refs, fold into methods validation |
| R16 | 3.2 | Only 5 metrics; should use all extractable data | Add deletions_fraction, message_structure, path_entropy |
| R18 | Tables | 8-column tables unreadable in PDF | Simplify columns or render as figures |
| R19 | References | Vaswani et al. (2017) missing | Add citation |
| R23 | Intro | Practical finding not mentioned until Conclusion | Add to Introduction |
| R24 | 2.3/Discussion | "Behavioral coherence" sounds like HR; function is feedback control | Reframe with control theory vocabulary |
| R27 | New | No replication guidance | Add section: replicate from our data + replicate from scratch |

### Medium (9)

| ID | Section | Issue | Fix |
|---|---|---|---|
| R3 | 5.5 | "No pre-transition multi-participant data" irrelevant | Delete |
| R4 | 5.5 | "Commit metrics are proxies" fights straw man | One sentence: regime change, not improvement |
| R6 | 5.5 | "Bonferroni is conservative" is a humble-brag | Delete |
| R7 | 5.5 | "Temporal confounds" too generic | Name memory-accumulation hypothesis specifically |
| R10 | 6 | Conclusion ¶3 fights straw man about intelligence | Drop straw man, keep topology reframe |
| R17 | 3.3 | Assumption-testing paragraph is defensive | Permutation test (option B) or trim to 1 sentence |
| R21 | 4.4 | ACF near-zero in both aurasys regimes — unexplained | Address directly: distribution change, not correlation |
| R22 | 2 | Levin and Kauffman don't connect until Discussion | Bridge at end of 2.1 |
| R25 | 3.2 | Paper doesn't explain why metrics should detect transition | Add honest paragraph |
| R26 | 2 | No intuitive summary before theorem chain | Add plain-language paragraph |

### Low (2)

| ID | Section | Issue | Fix |
|---|---|---|---|
| R5 | 5.5 | "Single baseline" misleadingly framed | Reframe (may be moot after R15) |
| R14 | Table 1 | Repo naming inconsistent | Pick one convention |

---

## 3. Replication Guidance (R27 — new content for paper)

### Option 1: Computational Replication (verify our results)

1. Clone `github.com/energyscholar/governance-phase-transition`
2. Install Python 3.10+, NumPy, SciPy
3. Run: `python scripts/01-baseline-abrce.py` (validates tools on baseline data)
4. Run: `python scripts/02-aurasys-breaks.py` (structural break detection)
5. Run: `python scripts/03-multi-repo-convergence.py` (cross-repo convergence)
6. Run: `python scripts/04-statistical-tightening.py` (assumption tests, corrections)
7. Verify: break dates, F-statistics, p-values, Cohen's d match Tables 1-2
8. All data in `data/` as JSON; all scripts deterministic; no external dependencies beyond NumPy/SciPy

### Option 2: Independent Replication (test the theory)

1. Set up any LLM coding assistant on a real project with git tracking
2. Develop for 8+ weeks with at most 2 of 3 governance axes:
   - Structural: role separation (don't let the AI evaluate its own output)
   - Temporal: persistent memory (corrections that survive across sessions)
   - Corrective: drift detection (mechanism that catches behavioral divergence)
3. At a documented date, add the third axis — completing all three
4. Continue development for 8+ weeks after closure
5. Extract all 8 commit metrics (our scripts work on any git repo):
   - lines_changed, file_count, time_gap, msg_length, AI_fraction
   - deletions_fraction, message_structure, path_entropy
6. Run blind structural break detection (scripts provided)
7. Compare detected break date against the documented third-axis installation date
8. Report all 8 metrics — including those that DON'T break

**What strengthens replication:**
- Pre-register the experiment (announce plan before starting)
- Different LLM than Claude (tests whether result is architecture-general)
- Multiple developers simultaneously (addresses N=1)
- Blind the analyst (someone else runs break detection who doesn't know the governance timeline)

**Both positive and negative results are valuable.** If the break doesn't coincide with closure, that constrains the theory. Report everything.

---

## 4. Revision Phases

### P10-1: Script Updates (infrastructure)

**Depends on:** Nothing
**Produces:** Updated scripts, new metric data, permutation test results

| Item | What |
|---|---|
| R16 | Add deletions_fraction, message_structure, path_entropy to all analysis scripts |
| R17 | Add permutation test (shuffle commit order 10,000×, compute p from null distribution) |
| — | Run all scripts, capture output for 8 metrics × 2 repos |
| — | Produce verification report: which of 8 metrics break, with what significance |

**Acceptance:** All 8 metrics analyzed for aurasys + relinquishment. Permutation p-values computed. Report at `verification/P10-1-eight-metrics.md`.

---

### P10-2: Theory Sections (Sections 2.1, 2.2, 2.3)

**Depends on:** Nothing (text changes only)
**Items:** R12, R22, R24, R26

**Changes:**
1. Add intuitive summary paragraph at start of Section 2 (R26)
2. Add within-session clarification after theorem chain in 2.1 (R12): "This does not imply LLMs are ineffective within a single session — local correlations exist in one-dimensional systems. The constraint is on long-range order: cross-session coherence, accumulated learning, and persistent behavioral patterns."
3. Add bridge sentence at end of 2.1 connecting to Kauffman (R22): "The Levin results establish the constraint; the question is how to escape it. Kauffman's theory of autocatalytic sets provides the mechanism."
4. Reframe corrective axis in 2.3 (R24): Add control theory vocabulary. The corrective axis is a closed-loop feedback controller. Name the drift modes it prevents (agreeableness, confabulation, constraint amnesia). Keep "Dignity Net" as the implementation name but explain the FUNCTION in engineering terms.

**Acceptance:** All four additions present. No other changes to Section 2.

---

### P10-3: Structural Reorganization (Sections 3, 4, Supplementary)

**Depends on:** P10-1 (need 8-metric data for tables)
**Items:** R1, R13, R14, R15, R16-text, R25

**Changes:**
1. Section 3.1: Restructure to 2 primary repos (aurasys + relinquishment). External repos become a methods-validation paragraph: "We validated the detection tools on 8 ungoverned open-source repos [list in Supplementary G]. All 8 showed 1D disorder signatures, confirming the tools detect the predicted pattern." (R15, R13, R14)
2. Section 3.2: List all 8 metrics with brief descriptions. Add paragraph explaining why commit metrics should detect a regime change — honest framing, not thermodynamic claims. (R16-text, R25)
3. Section 3.5: Rewrite ABRCE intro. Define all 5 operators (A, B, R, C, E) with representation types. Explain R=0 on 1D is the ABRCE-level statement of the Levin result. Reference Supplementary C for cross-domain dictionary. (R1)
4. Section 4.1: Move ungoverned baseline analysis to Supplementary G (tool validation). Primary Results begin at current 4.2. (R15)
5. Update Tables 1-2: 8 metrics, simplified columns (metric, break date, p, Bonf/BH pass). Move pre/post means and Cohen's d to prose. (R18)
6. Address ACF non-result directly in 4.4 (R21)

**Acceptance:** 2-repo primary structure. 8 metrics in tables. ABRCE fully explained. Section 4.1 moved. Tables readable.

---

### P10-4: Abstract, Introduction, Discussion, Conclusion, Replication

**Depends on:** P10-2, P10-3 (final structure and framing)
**Items:** R2, R3, R4, R6, R7, R8, R9, R10, R11, R23, R27

**Changes:**
1. **Abstract** (R8): Add before final sentence: "The detection uses only commit metadata, requires no access to code contents, and is deployable as a blind organizational diagnostic."
2. **Introduction** (R9): Replace opening sentence. Frame around architecture, not persistence. (R23): Add practical finding to intro.
3. **Discussion — new subsection "The Corrective Axis"** (R11): Name the engineering objection. Answer with data (2.5 months open-loop, break in 1 day). Reframe as control theory. This is the paper's most important audience-facing addition.
4. **Limitations surgery:**
   - R2: "Single developer" → "single committer" (governance designed by 3 people)
   - R3: Delete "No pre-transition multi-participant data"
   - R4: Rewrite "proxies" to 1 sentence
   - R6: Delete "Bonferroni is conservative"
   - R7: Rewrite temporal confound with memory-accumulation hypothesis
   - R5: Reframe or delete (may be moot after R15)
5. **Conclusion** (R10): Drop straw man in ¶3. Keep topology reframe.
6. **Replication section** (R27): Add as Section 5.6 or Supplementary. Two options: computational replication (verify our numbers) and independent replication (test the theory). See Section 3 of this plan for content.
7. **References** (R19): Add Vaswani et al. (2017).

**Acceptance:** Abstract has practical finding. Opening sentence fixed. Limitations trimmed from 6 to 3. Corrective axis subsection present. Replication guidance present. Vaswani cited.

---

### P10-5: Figures

**Depends on:** P10-1 (data), P10-3 (final structure)
**Items:** R18, R20

**Deliverables:**
1. **Figure 1: Timeline.** X-axis = time (Nov 2025 – May 2026). Mark governance installations (Triad Dec 2025, Memory ongoing, DN Feb 13 2026). Mark detected break dates with arrows. Color-code pre/post regimes. Show both repos.
2. **Figure 2: Metric comparison.** Before/after for 2-3 most dramatic metrics (time_gap, file_count, lines_changed). Box plots or bar charts with error bars. Pre-transition vs post-transition.
3. **Figure 3: ACS schematic.** Three nodes (Triad, Memory, DN). Six directed edges with labels. K₃ topology visible. Food set shown as input arrows.
4. **Build script:** Python/matplotlib, deterministic, committed to `scripts/`.

**Acceptance:** Three figures render cleanly in PDF. Each referenced in paper text.

---

## 5. Execution Order

```
P10-1 (scripts)
  ↓
P10-2 (theory) ←— can run parallel with P10-3 if P10-1 done
P10-3 (structure + tables)
  ↓
P10-4 (abstract, intro, discussion, conclusion, replication)
  ↓
P10-5 (figures)
  ↓
Rebuild PDF → Final review
```

P10-2 has no data dependencies and could run before P10-1, but its text may need
adjustment once we know which of the 8 metrics break. Safer to run after P10-1.

---

## 6. Generator Prompts

### P10-1 Prompt (95% confidence)

```
You are the Generator for 0361-P10-1.
Read: ~/software/governance-phase-transition/plans/0361-P10-revision-plan.md (Section 4, P10-1)
Read: ~/software/governance-phase-transition/scripts/ (all 4 scripts for patterns)

TASK: Add 3 new metrics to the analysis pipeline and add a permutation test.

NEW METRICS (add to all scripts that process commit data):
1. deletions_fraction: lines_deleted / lines_changed (0 if lines_changed=0).
   Requires parsing git numstat: additions and deletions separately.
   Tests: monotonic accumulation (all adds, no deletes) vs self-correction.
2. message_structure: binary. 1 if commit message matches governance pattern
   (regex: starts with /^\d{4}-P\d/ or contains "Co-Authored-By: Claude").
   0 otherwise. Tests: governance artifact visibility in metadata.
3. path_entropy: Shannon entropy of the set of directory paths modified.
   H = -sum(p_i * log2(p_i)) where p_i = count_in_dir_i / total_files.
   Single-directory commits have H=0. Scattered commits have high H.
   Tests: focused vs scattered development.

PERMUTATION TEST (add to scripts 02 and 03):
For each metric's best split point, shuffle the commit series 10,000 times.
Compute max F-statistic for each shuffle. Permutation p-value = fraction of
shuffles with F >= observed F. This is distribution-free — no normality or
equal-variance assumptions needed.

DATA: Commit JSON files in data/ have fields: index, hash, timestamp, author,
subject, is_ai, file_count, lines_changed, time_gap_minutes. Some new metrics
need additional fields — check what git log provides and extend the JSON if
needed. If JSON extension is needed, document what was added.

OUTPUT:
1. Updated scripts (all 4)
2. Verification report at verification/P10-1-eight-metrics.md:
   - All 8 metrics × 2 repos: break date, F, p (parametric), p (permutation)
   - Which metrics survive Bonferroni (adjusted for 8 metrics)
   - Which metrics survive BH
   - Summary: N of 8 break in each repo
```

### P10-2 Prompt (93% confidence)

```
You are the Generator for 0361-P10-2.
Read: ~/software/governance-phase-transition/plans/0361-P10-revision-plan.md (Section 4, P10-2)
Edit: ~/software/governance-phase-transition/paper/stephenson-et-al-2026-autocatalytic-governance.md

FOUR ADDITIONS to Section 2. No other changes.

1. INTUITIVE SUMMARY (insert at start of Section 2, before "### 2.1")

Add one paragraph (~80 words) giving the reader the plain-language version
before theorems. Frame it like this: an LLM is like a skilled worker who does
excellent work within a single shift but retains nothing between shifts.
Governance adds three things: separation between doing and checking (structural),
a persistent notebook (temporal), and a supervisor who detects drift (corrective).
When all three sustain each other, the system self-maintains — and this creates
a detectable shift in its output. Do NOT use the word "ethics."

2. WITHIN-SESSION CLARIFICATION (insert after the theorem chain summary, line 52)

After "...a consequence of the system's one-dimensional interaction topology."
add: "This does not imply LLMs are ineffective within a single session — local
correlations exist in one-dimensional systems, and within-context performance
can be excellent. The constraint is on long-range order: cross-session coherence,
accumulated learning, and persistent behavioral patterns. These are precisely
the capabilities that governance infrastructure is designed to provide."

3. BRIDGE TO KAUFFMAN (insert at end of Section 2.1, before "### 2.2")

Add one sentence: "The Levin results establish the topological constraint;
the question is what mechanism can escape it. Kauffman's theory of autocatalytic
sets provides an answer: catalytic closure among governance components can
create the higher-dimensional interaction topology that the Peierls argument
requires."

4. CORRECTIVE AXIS REFRAME (modify Section 2.3, item 3)

Current: "A behavioral coherence protocol (Dignity Net) detects divergence
between stated goals and observable actions, applying graduated responses
from mirroring to refusal."

Rewrite to lead with engineering function: "A closed-loop drift detection
and correction mechanism detects divergence between intended and actual
behavior, applying graduated responses from mirroring to hard stops. In
control theory terms, this closes the feedback loop: without it, the system
is open-loop and accumulates drift silently. The implementation in this study
(Dignity Net [ref]) uses an ethical framework as its correction logic, but
the axis's function is feedback control — any mechanism that detects behavioral
drift and feeds back corrections would serve the same role."

SCOPE: Only these four changes. Do not modify tables, statistics, or any
other section.
```

### P10-3 Prompt (88% confidence — complex structural changes)

```
You are the Generator for 0361-P10-3.
Read: ~/software/governance-phase-transition/plans/0361-P10-revision-plan.md (Section 4, P10-3)
Read: ~/software/governance-phase-transition/verification/P10-1-eight-metrics.md (for new data)
Edit: ~/software/governance-phase-transition/paper/stephenson-et-al-2026-autocatalytic-governance.md

STRUCTURAL REORGANIZATION of Sections 3 and 4. This is the heaviest edit.

--- SECTION 3.1: DATA ---

Restructure to 2 primary repos. Replace the 4-repo table with:

| Repository | Role | Commits | Date Range | AI% | Governance |
|---|---|---|---|---|---|
| aurasys-memory | Governance system | 300 | Nov 2025-May 2026 | 70% | Mixed |
| relinquishment | Technical manuscript | 924 | Feb 2026-May 2026 | 89% | Consistent Triad |

Add one paragraph after the table: "We validated the detection tools on 8
ungoverned open-source AI-assisted repositories (listed in Supplementary G).
All 8 exhibited 1D disorder signatures — monotonic violation accumulation,
rapid decorrelation, and no self-correction — confirming the tools detect
the predicted pattern. The primary analysis is within-subject: the memory
repository before and after catalytic closure."

Remove the storytelling/traveller repo from primary analysis. Remove
trusty-git-analytics from primary analysis. Both can be referenced in
supplementary material.

--- SECTION 3.2: METRICS ---

List all 8 metrics:
1. lines_changed (total lines added + deleted)
2. file_count (files modified)
3. time_gap (minutes since previous commit)
4. msg_length (commit message character count)
5. AI_fraction (binary: AI or human authored)
6. deletions_fraction (lines_deleted / lines_changed)
7. message_structure (binary: matches governance pattern)
8. path_entropy (Shannon entropy of directory paths)

Add: "These metrics are chosen because they are extractable from any git
repository without access to file contents. We report all 8 rather than
selecting those that produce significant breaks — the theory predicts a
regime change, and metrics that do not break are informative null results."

Add paragraph (R25): "We do not claim these metrics are thermodynamic
variables. The theory predicts a regime change at catalytic closure; commit
metrics are sensitive to regime changes in development behavior. The
detection is empirical: if the regime change predicted by the theory exists,
it should be visible in process metadata."

--- SECTION 3.5: ABRCE ---

Replace current Section 3.5 with a fuller introduction. Define all 5 operators:
- A (Abstraction): NodeField -> EdgeField. Pairwise differences. Extracts
  relational gradient between consecutive commits.
- B (Binding): EdgeField -> EdgeField. Local symmetric accumulation over
  sliding window. Smooths high-frequency variation.
- R (Circulation): EdgeField x R -> EdgeField. Antisymmetric circulation.
  CRITICAL: R is trivially zero on 1D data. This is the ABRCE-level
  statement of the Levin result — a 1D system has no circulation, no
  feedback loops, no non-trivial topology. R != 0 requires at least 2D.
- C (Coherence): EdgeField -> EdgeField. Bounded output in (-1, 1).
  Prevents divergence.
- E (Composite): E(x) = C(R(B(A(x)),rho)). On 1D, R=0, so E = C(B(A(x))).

Add: "The ABRCE operators are domain-neutral by construction [7]. The same
operators describe lattice gradients in statistical mechanics, first
differences in time series, filter cascades in signal processing, and
message-passing in graph neural networks (see Supplementary C for the
complete cross-domain dictionary with exactness ratings)."

--- SECTION 4.1: MOVE TO SUPPLEMENTARY ---

Move the entire current Section 4.1 (ungoverned baseline) to a new
Supplementary G: "Tool Validation on Ungoverned Repositories." Renumber
remaining results sections: current 4.2 becomes 4.1, current 4.3 becomes
4.2, current 4.4 becomes 4.3.

--- TABLES 1-2: SIMPLIFY + EXPAND ---

Update Tables 1 and 2 to include all 8 metrics. Simplify columns to:
| Metric | Break Date | p (parametric) | p (permutation) | Bonf | BH |

Move pre/post means and Cohen's d to prose paragraphs following each table.
Use data from verification/P10-1-eight-metrics.md.

--- SECTION 4.3 (was 4.4): ACF ---

Address the ACF non-result (R21): "The memory repository shows near-zero
autocorrelation in both regimes. This apparent contradiction — governance
should create order, so why no ACF increase? — reflects a measurement
distinction. The structural breaks detect a change in the DISTRIBUTION of
commit sizes (from bulk dumps to focused commits), not in their sequential
correlation. ACF measures commit-to-commit dependence; the regime change is
in the typical scale and frequency of commits, which the F-test captures
directly."

ACCEPTANCE: 2-repo primary structure. 8 metrics in all tables. ABRCE fully
explained with R=0 significance. Section 4.1 moved to supplementary.
Tables have 6 columns (readable). ACF non-result addressed.
```

### P10-4 Prompt (91% confidence)

```
You are the Generator for 0361-P10-4.
Read: ~/software/governance-phase-transition/plans/0361-P10-revision-plan.md (Section 4, P10-4)
Edit: ~/software/governance-phase-transition/paper/stephenson-et-al-2026-autocatalytic-governance.md

CONTENT EDITS to Abstract, Introduction, Discussion, Conclusion, References.

--- ABSTRACT ---

(R8) Before the final sentence ("To our knowledge..."), insert:
"The detection uses only commit metadata — timestamps, line counts, file
counts — and requires no access to code contents or subjective quality
assessments, enabling deployment as a blind organizational diagnostic."

--- INTRODUCTION ---

(R9) Replace the first paragraph (starting "Large language models deployed
as coding assistants operate without persistence") with:
"Large language models are architecturally one-dimensional autoregressive
systems. Within a single context window, they generate fluently and
coherently. But cross-session coherence — remembering corrections,
maintaining behavioral patterns, accumulating learning — requires external
structure. The topology of that structure determines whether coherence is
sustainable."

(R23) Add to the second paragraph, after "The limitation is structural":
"We show that the resulting phase transition is detectable in commit
metadata alone, without access to code contents, enabling blind
organizational diagnostics."

--- DISCUSSION: NEW SUBSECTION "The Corrective Axis" ---

(R11, R24) Add as Section 5.2 (shift subsequent numbering). Content:

"The corrective axis is the most counterintuitive governance component. In
our experience presenting this framework to software engineers, the
structural axis (role separation) and temporal axis (persistent memory)
are immediately understood as good engineering practice. The corrective
axis — a mechanism that detects behavioral drift and applies graduated
corrections — is consistently dismissed as irrelevant overhead.

The data disagree. The structural and temporal axes ran together for
approximately 2.5 months (early December 2025 to mid-February 2026) without
triggering a detectable structural break. The break appeared within one day
of adding the corrective axis, when catalytic closure was reached.

In control theory terms, a system with structure and memory but no corrective
feedback is open-loop: it executes its program but cannot detect or correct
deviations. LLMs have specific drift modes — agreeableness under pressure,
confabulation, constraint amnesia over long interactions — that accumulate
silently in an open-loop configuration. The corrective axis closes the
feedback loop. Its implementation in this study uses an ethical framework
(Dignity Net) as its correction logic, but the axis's engineering function
is drift detection and correction. Any mechanism that detects behavioral
divergence and feeds back graduated corrections would serve the same role.

The engineering implication is direct: structure plus memory is necessary
but not sufficient. The autocatalytic set does not close without the
feedback loop, and the phase transition does not occur."

--- LIMITATIONS SURGERY ---

(R2) Replace "Single developer" with: "Single committer. All commit data
are from one developer (the first author), though the governance
infrastructure was designed by three people — one per axis. We cannot
separate committer-specific effects from governance effects without
multi-committer data."

(R3) Delete "No pre-transition multi-participant data" entirely.

(R4) Replace "Commit metrics are proxies" with: "Commit metrics measure
process structure, not output quality. We claim a detectable regime change,
not an improvement in code correctness or user satisfaction."

(R6) Delete "Bonferroni correction is conservative" entirely.

(R7) Replace "Temporal confounds" with: "Temporal confounds. Memory had
been accumulating for months before the detected break. An alternative
hypothesis: memory crossed a critical threshold on February 13 independent
of the Dignity Net installation, and the coincidence is accidental.
Counter-evidence: memory grew continuously from November 2025, yet no
structural break appeared during 2.5 months of growth. The break coincides
with a discrete event (third-component installation), not a gradual
accumulation. However, we cannot fully disentangle the two because DN
installation and possible memory maturity coincide temporally."

--- CONCLUSION ---

(R10) Replace third implication paragraph. Remove: "Larger models, better
training data, and longer context windows do not escape the 1D limitation."
Replace with: "Third, the relevant variable is not model capability but
interaction topology. The question shifts from 'how smart is the AI?' to
'what topology does the human-AI system occupy?' — and this topology is
measurable."

--- REPLICATION (R27) ---

Add as Section 5.7 (or after current Limitations, before Conclusion):

"### Replication

We invite replication in two forms.

**Computational replication.** All data, scripts, and analysis code are
publicly available at github.com/energyscholar/governance-phase-transition.
The commit-series JSON files in data/ contain all metrics for all
repositories. Running the four scripts in scripts/ reproduces every number
in this paper. Requirements: Python 3.10+, NumPy, SciPy.

**Independent replication.** To test the theory on new data: (1) set up
any LLM coding assistant on a git-tracked project; (2) develop for at
least 8 weeks with at most two of three governance axes (structural role
separation, persistent memory, corrective drift detection); (3) at a
documented date, add the third axis to complete catalytic closure; (4)
continue for at least 8 weeks; (5) extract all 8 commit metrics (our
scripts work on any git repository); (6) run blind structural break
detection. Pre-registration strengthens the design. Both positive and
negative results are valuable — if the break does not coincide with
closure, that constrains the theory."

--- REFERENCES ---

(R19) Add: [8] Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J.,
Jones, L., Gomez, A. N., Kaiser, L., & Polosukhin, I. (2017). Attention
Is All You Need. *Advances in Neural Information Processing Systems*, 30.

Update any in-text references to transformers to cite [8] alongside [1]
where appropriate (e.g., Introduction paragraph 2).

ACCEPTANCE: Abstract has practical finding. Opening fixed. Corrective axis
subsection present. Limitations trimmed from 6 to 3. Replication section
present. Vaswani cited. Conclusion straw man removed.
```

### P10-5 Prompt (85% confidence — figure generation is always risky)

```
You are the Generator for 0361-P10-5.
Read: ~/software/governance-phase-transition/plans/0361-P10-revision-plan.md (Section 4, P10-5)
Read: ~/software/governance-phase-transition/data/ (commit-series JSON files)

TASK: Generate 3 figures for the paper using matplotlib. Save as PNG at
300 DPI in paper/figures/. Also create the generation script at
scripts/05-generate-figures.py.

FIGURE 1: TIMELINE (paper/figures/fig1-timeline.png)

X-axis: date (Nov 2025 - May 2026), monthly ticks.
Plot: commit frequency as a step histogram or scatter (1 dot per commit)
for aurasys-memory, using time from commit-series JSON.

Mark with vertical dashed lines + labels:
- "Triad installed" at 2025-12-01 (approximate)
- "DN installed / catalytic closure" at 2026-02-13
- Detected break dates as triangular markers on X-axis

Color: pre-transition commits in red/orange, post-transition in blue/green.
Title: "Figure 1: Governance installation and detected structural breaks"
Clean, publication-quality. No gridlines. Minimal decoration.

FIGURE 2: METRIC COMPARISON (paper/figures/fig2-metrics.png)

Side-by-side box plots for pre vs post transition, for the 3 most dramatic
metrics: time_gap, file_count, lines_changed.

Read data from data/aurasys/commit-series.json. Split at commit index
corresponding to 2026-02-13. Pre = commits before split, Post = after.

3 subplots in a row. Each shows pre (red) and post (blue) box plots.
Y-axis log scale (the differences are orders of magnitude).
Label with pre-mean and post-mean values.
Title: "Figure 2: Pre- and post-transition metric distributions"

FIGURE 3: ACS SCHEMATIC (paper/figures/fig3-acs.png)

Three nodes arranged as an equilateral triangle:
- Top: "Structural (Triad)" 
- Bottom-left: "Temporal (Memory)"
- Bottom-right: "Corrective (Feedback)"

Six directed edges (curved arrows) with brief labels:
- Structural→Temporal: "structured records"
- Temporal→Structural: "accumulated corrections"
- Temporal→Corrective: "session history"
- Corrective→Temporal: "correction records"
- Corrective→Structural: "prevents role collapse"
- Structural→Corrective: "independent evaluation"

Below the triangle, three upward arrows from a box labeled
"Food set: {LLM, git, filesystem, protocols}"

Title: "Figure 3: Governance autocatalytic set (K₃ topology)"
Use matplotlib patches and annotations. Clean, no matplotlib default styling.

SCRIPT: scripts/05-generate-figures.py
- Reads from data/ JSON files
- Generates all 3 figures
- Deterministic (set random seed if any randomness)
- No dependencies beyond matplotlib + numpy

After generating figures, add figure references to the paper:
- Figure 1 referenced in Section 3.1 (after governance timeline paragraph)
- Figure 2 referenced in Section 4.1 (after Table 1)
- Figure 3 referenced in Section 2.3 (after six-link table)

Use markdown image syntax: ![Figure N caption](figures/figN-name.png)

ACCEPTANCE: Three PNGs in paper/figures/. Script runs clean. Figures
referenced in paper text. PDF builds with figures visible.
```

---

## 7. Commit Plan

| Phase | Commit message |
|---|---|
| P10-1 | `0361-P10-1: Add 3 metrics + permutation test — 8-metric analysis` |
| P10-2 | `0361-P10-2: Theory accessibility — intuitive summary, within-session clarification, feedback control reframe` |
| P10-3 | `0361-P10-3: Structural reorganization — 2-repo primary, 8 metrics, ABRCE explained, baseline to supplementary` |
| P10-4 | `0361-P10-4: Content revision — abstract/intro/discussion/limitations/replication/references` |
| P10-5 | `0361-P10-5: Figures — timeline, metric comparison, ACS schematic` |
| Final | `0361-P10: Rebuild PDF after full revision` |

---

## 8. Risk Register

| Risk | Mitigation |
|---|---|
| New metrics don't break cleanly | Report all 8 regardless. Non-breaking metrics are informative nulls. |
| P10-3 structural changes break paper flow | P10-4 does a flow pass on abstract/intro/conclusion after structure is set |
| Figure generation fails in PDF | Test PDF build after P10-5. Fallback: ASCII tables or external figure tools. |
| Permutation test contradicts parametric results | Report both. If they disagree substantially, investigate and document. |
| 5 phases is too many Generator runs | Phases 2+3 could merge if Generator handles the scope. But 88% confidence on P10-3 suggests keeping them separate. |
