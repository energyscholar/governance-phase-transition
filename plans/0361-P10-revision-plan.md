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
| R19 | References | Vaswani et al. (2017) missing | Add citation |
| R28 | Tables | Tables cramped, unclear in PDF (supersedes R18) | Split into 2 tables (one per repo), 6 cols: metric, break, F, p-perm, Bonf, BH |
| R29 | New figure | No visual representation of topology argument | 1D chain vs 3D orthogonal K₃ — side-by-side topology comparison figure |
| R30 | Appendix | No guidance for AI-assisted reading of the paper | Appendix: 3 sequential LLM prompts for deep paper analysis (prep → theory → review) |
| R23 | Intro | Practical finding not mentioned until Conclusion | Add to Introduction |
| R24 | 2.3/Discussion | "Behavioral coherence" sounds like HR; function is feedback control | Reframe with control theory vocabulary |
| R27 | New | No replication guidance | Add section: replicate from our data + replicate from scratch |
| R31 | Data | Raw data not packaged for public access | Zip all data/, README with schema, paper links to repo URL. Private repo data = extracted metrics |

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

### P10-3a: Structural Reorganization (skeleton change)

**⚠ ANNEALING NOTE:** The original P10-3 was a single 86% confidence phase with hidden dependencies between 6 sub-tasks spanning Sections 3, 4, and Supplementary. Three failure modes: (1) section renumbering breaks cross-references, (2) ABRCE rewrite is an intellectual task that doesn't benefit from being bundled with mechanical edits, (3) table construction depends on P10-1 data but structure depends on nothing. Split into P10-3a/3b/3c to isolate these failure modes. Each sub-phase prompt needs fresh annealing at runtime — the paper's text will have changed from P10-2 by the time 3a runs.

**Depends on:** P10-2 (theory text should be settled before structural moves)
**Items:** R13, R14, R15
**Scope:** Mechanical restructuring only. No intellectual content changes.

**Changes:**
1. Section 3.1: Restructure to 2 primary repos (aurasys + relinquishment). Replace the 4-repo table with a 2-row table. Add methods-validation paragraph: "We validated the detection tools on 8 ungoverned open-source repos [list in Supplementary G]. All 8 showed 1D disorder signatures, confirming the tools detect the predicted pattern." (R15, R13)
2. Consistent repo naming throughout (R14): pick one convention (descriptive + real name)
3. Section 4.1: Move entire ungoverned baseline analysis to new Supplementary G: "Tool Validation on Ungoverned Repositories"
4. Renumber: current 4.2→4.1, 4.3→4.2, 4.4→4.3
5. Update ALL cross-references (Discussion, Limitations, Conclusion) that reference "the ungoverned baseline" or "Section 4.1"

**Acceptance:** 2-repo primary structure. Section 4 renumbered. All cross-references updated. No broken references. No content changes to ABRCE, metrics list, or tables (those are 3b/3c).

---

### P10-3b: ABRCE Rewrite (Section 3.5)

**Depends on:** P10-3a (needs stable section numbering)
**Items:** R1
**Scope:** Rewrite one section. Intellectual task requiring deep domain understanding.

**Changes:**
1. Replace current Section 3.5 with full 5-operator introduction:
   - A (Abstraction): NodeField→EdgeField. Pairwise differences.
   - B (Binding): EdgeField→EdgeField. Local symmetric accumulation.
   - R (Circulation): EdgeField × ℝ → EdgeField. **CRITICAL:** R is trivially zero on 1D data. This is the ABRCE-level statement of the Levin result — no circulation means no feedback loops, no non-trivial topology. R≠0 requires at least 2D.
   - C (Coherence): EdgeField→EdgeField. Bounded output in (-1, 1).
   - E (Composite): E(x) = C(R(B(A(x)),ρ)). On 1D, R=0, so E collapses to C(B(A(x))).
2. Add cross-domain statement: operators are domain-neutral by construction — same math describes lattice gradients, time-series first differences, signal processing filter cascades, graph neural network message-passing. Reference Supplementary C.

**Acceptance:** All 5 operators defined with representation types. R=0 significance explicitly connected to Levin. Cross-domain dictionary referenced. No other sections modified.

---

### P10-3c: Metrics, Tables, and ACF (Sections 3.2, 4.x)

**Depends on:** P10-3a (needs stable structure) + P10-1 (needs 8-metric data)
**Items:** R16-text, R25, R28, R21
**Scope:** Data presentation. Reads P10-1 verification report, builds tables and prose.

**Changes:**
1. Section 3.2: List all 8 metrics with brief descriptions. Add: "We report all 8 rather than selecting those that produce significant breaks — the theory predicts a regime change, and metrics that do not break are informative null results." Add honest paragraph (R25) about why metrics detect transition.
2. Tables: Build 2 clean tables (R28), one per repo. Each: 6 columns (Metric | Break Date | F | p (perm) | Bonf | BH) × 8 rows. Pre/post means and Cohen's d in prose after each table. Use data from `verification/P10-1-eight-metrics.md`.
3. Address ACF non-result (R21): distribution change, not correlation change. The structural breaks detect a shift in commit-size distribution (bulk dumps→focused commits), not sequential dependence.

**Acceptance:** All 8 metrics listed in 3.2. Two tables (one per repo), 6 columns each. ACF addressed. All numbers sourced from P10-1 verification report.

---

### P10-4: Abstract, Introduction, Discussion, Conclusion, Replication

**Depends on:** P10-3b, P10-3c (all structural and data work settled)
**Items:** R2, R3, R4, R6, R7, R8, R9, R10, R11, R23, R27, R30

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
8. **Appendix: AI-Assisted Reading Prompts** (R30): Three sequential prompts for getting an LLM to deeply analyze this paper. The Sacco & Levin team (our primary audience for outreach) makes minimal use of AI — they won't know that dropping a paper into ChatGPT gives a shallow skim, but three careful preparation prompts produce genuine analysis. Include:
   - **Prompt 1 (Levin preparation):** "Read Sacco, Sakthivadivel & Levin 2026. Summarize: (a) the theorem chain from causal masking to no-ordered-phase, (b) how topology determines whether self-organization is possible, (c) what Proposition 2 says about decoder-only transformers specifically."
   - **Prompt 2 (Kauffman preparation):** "Read Kauffman 1986 on autocatalytic sets and Hordijk & Steel 2004 on RAF formalism. Summarize: (a) what catalytic closure means, (b) how a system transitions from subcritical to supercritical, (c) the formal conditions for a set to be reflexively autocatalytic and food-generated."
   - **Prompt 3 (deep review):** "Now read this paper. For each major claim, trace the argument chain back to the theoretical foundations you just studied. Identify: (a) where the authors' mapping from theory to application is rigorous, (b) where it requires assumptions not proven, (c) what would falsify the central claim."

**Acceptance:** Abstract has practical finding. Opening sentence fixed. Limitations trimmed from 6 to 3. Corrective axis subsection present. Replication guidance present. Vaswani cited. AI reading prompts in appendix.

---

### P10-5: Figures

**Depends on:** P10-1 (data), P10-4 (final paper structure)
**Items:** R20, R29

**Design rationale:** Three figures, three jobs. Each answers one question the reader asks at a specific point in the paper. No figure is decorative — each replaces prose.

**Figure 1: "Why does topology matter?"** (Section 2, after intuitive summary)
- **Purpose:** Make the theoretical argument visible before a single theorem. An engineer who reads only this figure should understand: 1D chain = unstable (domain walls break order), K₃ governance = stable (mutual reinforcement maintains order). The figure IS the abstract in visual form.
- **Left panel — 1D chain:** Reader should SEE instability. Nodes on a line. Domain walls as visible breaks where order collapses. Chain should look fragile. Key annotation: domain walls cost O(1) energy, gain O(log N) entropy — disorder always wins. This is Levin Theorem 2 in one picture.
- **Right panel — 3D orthogonal K₃:** Reader should SEE stability. Three bounded axes (Structural, Temporal, Corrective) from a common origin in isometric projection. K₃ complete graph connects endpoints — six directed catalytic links with brief labels. Food set enters from below. Structure should look robust.
- **Rendering:** Isometric-style 2D drawing (manual coordinate placement with matplotlib patches/arrows), NOT mplot3d. If isometric is too cluttered, fall back to equilateral triangle with axis labels. Visual clarity trumps dimensional accuracy.

**Figure 2: "When did the transition happen?"** (Section 4, after repo description)
- **Purpose:** Show temporal coincidence — something changed at exactly the moment the third axis was installed. This is the empirical core.
- **Content:** X = date (Nov 2025 – May 2026). Y = time_gap (minutes since previous commit — the most dramatic metric, 6,328→486). One dot per commit. Color: pre-transition red, post-transition blue. Vertical dashed lines at governance installations (Triad, DN/closure). Detected break date as distinct marker. The visual cliff at the break date tells the story.
- **Why time_gap:** Largest effect size, most intuitive interpretation (long gaps = bursty, short = disciplined). Reader sees the regime change without understanding statistics.

**Figure 3: "How big is the effect?"** (Section 4, after tables)
- **Purpose:** Show this isn't a subtle statistical artifact — it's an order-of-magnitude shift across multiple independent metrics. Tables give numbers; this figure gives visceral impact.
- **Content:** 3 subplots, one per metric (time_gap, lines_changed, file_count). Pre (red) vs post (blue) box plots. Log scale if needed. Pre/post mean values labeled. Reader sees massive effect sizes across multiple dimensions.
- **Why these 3:** Most intuitive (engineers understand gap, size, file count), most dramatic (order-of-magnitude shifts). Other metrics in prose.

**Build script:** `scripts/05-generate-figures.py`. matplotlib + numpy only. Deterministic. 300 DPI PNG to `paper/figures/`. No matplotlib defaults (remove unnecessary spines, ticks, gridlines). Publication-quality.

**Acceptance:** Three PNGs render in PDF. Each at correct paper location. Fig 1 conveys 1D→K₃ without theorems. Fig 2 shows temporal coincidence. Fig 3 shows effect magnitude.

---

## 5. Execution Order

```
P10-1 (scripts — get the data first)
  ↓
P10-2 (theory — text only, no data dependency, but run after P10-1
        so metric language is informed by results)
  ↓
P10-3a (structural reorg — skeleton change, moves sections, renumbers)
  ↓
P10-3b (ABRCE rewrite — intellectual task, needs stable section numbers)
P10-3c (metrics/tables/ACF — needs P10-3a structure + P10-1 data)
  ↓ (both must complete before P10-4)
P10-4 (abstract, intro, discussion, conclusion, replication, appendix)
  ↓
P10-5 (figures — needs P10-1 data + final paper structure)
  ↓
Rebuild PDF → Final review
```

**Dependency notes:**
- P10-1, P10-2, P10-3a have no mutual dependencies but are ordered for safety
- P10-3b and P10-3c are independent of each other (different sections), both need P10-3a
- P10-3c also needs P10-1 data — verified met since P10-1 runs first
- P10-4 needs ALL prior phases settled — it writes the framing around everything
- P10-5 needs data (P10-1) and final structure (P10-4 done)
- **Each P10-3x prompt needs fresh annealing at runtime** — paper text will have shifted

---

## 6. Generator Prompts

All detail lives in this plan file (Section 4). Prompts just point the Generator here.

### P10-1 (95%)
```
You are the Generator for 0361-P10-1.
Read: ~/software/governance-phase-transition/plans/0361-P10-revision-plan.md § P10-1
Read: ~/software/governance-phase-transition/scripts/ (all scripts for patterns)
Execute P10-1: add 3 new metrics + permutation test to the analysis pipeline.
Report at verification/P10-1-eight-metrics.md. All 8 metrics × 2 repos.
```

### P10-2 (93%)
```
You are the Generator for 0361-P10-2.
Read: ~/software/governance-phase-transition/plans/0361-P10-revision-plan.md § P10-2
Edit: ~/software/governance-phase-transition/paper/stephenson-et-al-2026-autocatalytic-governance.md
Execute P10-2: four additions to Section 2 (intuitive summary, within-session
clarification, Levin→Kauffman bridge, corrective axis reframe). No other changes.
```

### P10-3a (91%) ⚠ anneal at runtime — re-read paper first
```
You are the Generator for 0361-P10-3a.
Read: ~/software/governance-phase-transition/plans/0361-P10-revision-plan.md § P10-3a
Edit: ~/software/governance-phase-transition/paper/stephenson-et-al-2026-autocatalytic-governance.md
Execute P10-3a: structural reorganization. 2-repo primary table, move Section 4.1
to Supplementary G, renumber 4.x, update all cross-references. Structure only —
do not touch ABRCE, metrics list, tables, or ACF.
```

### P10-3b (87%)
```
You are the Generator for 0361-P10-3b.
Read: ~/software/governance-phase-transition/plans/0361-P10-revision-plan.md § P10-3b
Edit: ~/software/governance-phase-transition/paper/stephenson-et-al-2026-autocatalytic-governance.md
Execute P10-3b: rewrite Section 3.5 (ABRCE Operators). Define all 5 operators
with representation types. R=0 on 1D is the ABRCE-level Levin result — make this
the key paragraph. Add cross-domain dictionary reference. Section 3.5 only.
```

### P10-3c (92%)
```
You are the Generator for 0361-P10-3c.
Read: ~/software/governance-phase-transition/plans/0361-P10-revision-plan.md § P10-3c
Read: ~/software/governance-phase-transition/verification/P10-1-eight-metrics.md
Edit: ~/software/governance-phase-transition/paper/stephenson-et-al-2026-autocatalytic-governance.md
Execute P10-3c: list 8 metrics in §3.2, build 2 tables (per-repo, 6 cols),
address ACF non-result. All numbers from P10-1 verification report only.
```

### P10-4 (91%)
```
You are the Generator for 0361-P10-4.
Read: ~/software/governance-phase-transition/plans/0361-P10-revision-plan.md § P10-4
Edit: ~/software/governance-phase-transition/paper/stephenson-et-al-2026-autocatalytic-governance.md
Execute P10-4: abstract fix, opening sentence, corrective axis subsection,
limitations surgery (6→3), replication section, Vaswani citation, AI reading
prompts appendix. Plan has exact replacement text for each item.
```

### P10-5 (85%)
```
You are the Generator for 0361-P10-5.
Read: ~/software/governance-phase-transition/plans/0361-P10-revision-plan.md § P10-5
Read: ~/software/governance-phase-transition/data/ (commit-series JSON files)
Execute P10-5: generate 3 figures (topology comparison, timeline, metric
distributions). Script at scripts/05-generate-figures.py. matplotlib+numpy only.
300 DPI PNG to paper/figures/. Add figure refs to paper. Design specs in plan.
```

---

## 7. Commit Plan

| Phase | Commit message |
|---|---|
| P10-1 | `0361-P10-1: Add 3 metrics + permutation test — 8-metric analysis` |
| P10-2 | `0361-P10-2: Theory accessibility — intuitive summary, within-session clarification, feedback control reframe` |
| P10-3a | `0361-P10-3a: Structural reorganization — 2-repo primary, baseline to supplementary, section renumbering` |
| P10-3b | `0361-P10-3b: ABRCE rewrite — all 5 operators, R=0 significance, cross-domain dictionary` |
| P10-3c | `0361-P10-3c: Metrics and tables — 8 metrics listed, 2 tables (per-repo), ACF addressed` |
| P10-4 | `0361-P10-4: Content revision — abstract/intro/discussion/limitations/replication/appendix` |
| P10-5 | `0361-P10-5: Figures — topology comparison, timeline, metric distributions` |
| Final | `0361-P10: Rebuild PDF after full revision` |

---

## 8. Risk Register

| Risk | Mitigation |
|---|---|
| New metrics don't break cleanly | Report all 8 regardless. Non-breaking metrics are informative nulls. |
| P10-3a renumbering breaks cross-references | Grep for old section numbers + "ungoverned baseline" after P10-3a. Fix before P10-3b/3c. |
| P10-3b ABRCE rewrite misses R=0 significance | Acceptance criterion: R=0 explicitly linked to Levin Thm 2. Auditor verifies. |
| P10-3c tables use wrong data | Acceptance: all numbers sourced from P10-1 verification report. No invented values. |
| P10-3x prompts stale after earlier phases | **Each P10-3x prompt needs fresh annealing at runtime.** Paper text shifts with each phase. |
| Figure generation fails in PDF | Test PDF build after P10-5. Fallback: ASCII tables or external figure tools. |
| Topology figure (Fig 1) too cluttered | Fallback: equilateral triangle instead of isometric 3D. K₃ topology is identical either way. |
| Permutation test contradicts parametric results | Report both. If they disagree substantially, investigate and document. |
| 7 phases is many Generator runs | Each is focused and high-confidence (87-95%). Split reduces risk vs monolithic P10-3 (was 86%). |
