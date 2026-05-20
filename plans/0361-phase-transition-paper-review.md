# Plan 0361: Phase Transition Paper — Full Triad Rewrite

**Status:** ACTIVE
**Created:** 2026-05-19 (Auditor)
**Context:** A paper draft titled "Autocatalytic Governance: Detecting a Phase Transition in Human-AI Collaboration" was written in a single session without Triad discipline. The draft has been deleted. This plan captures all knowledge and specifies the Generator rebuild.

**Repository:** `~/software/governance-phase-transition/` (public, github.com/energyscholar/governance-phase-transition)
**Data:** `data/{aurasys,baseline,relinquishment,traveller-private}/commit-series.json`
**Scripts:** `scripts/{01-baseline-abrce.py, 02-aurasys-breaks.py, 03-multi-repo-convergence.py}`

---

## Meta-Requirement: The Repo Is a Dataset

**This paper claims that governed AI produces detectable ordered-phase signatures in commit history. The repo that builds this paper will be analyzed with the same techniques.** A skeptical reviewer — or an LLM pointed at this repo by a skeptical reviewer — will apply structural break detection, ACF analysis, and ABRCE operators to these commits. The repo must self-validate.

**What ordered commits look like (the paper predicts this):**
- Small, focused commits (not bulk dumps)
- Each commit maps to exactly one plan phase (session-coherent)
- Verification precedes generation (P1, P2 before P3) — ungoverned LLMs generate first, verify never
- Data and interpretation are separated (P3 skeleton before P4 discussion) — Triad discipline visible in the commit graph
- Self-correction is structural, not accidental (P6 deliberately weakens claims with multiple comparison correction)
- Positive ACF at lag 1 within phases, sharp decorrelation at phase boundaries
- The plan lives in `plans/` and is committed before any paper content — Auditor defines criteria before Generator writes

**What ungoverned commits look like (the paper predicts this):**
- Large bulk commits, monotonic accumulation
- No structure, no phase boundaries
- Fix commits right after add commits (no review step)
- No self-correction

**Commit message format — each commit tells a story a reviewer can read:**

```
0361-PN: [phase title]

[What was done — 1-2 lines]
[What was found, including negative findings — 1-3 lines]
[Artifacts produced — 1 line]

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

Example (P6 — the most important commit for credibility):
```
0361-P6: Statistical tightening — multiple comparison correction

Applied Bonferroni and Benjamini-Hochberg corrections (5 metrics × 270 splits).
Memory: all 5 breaks survive strict correction (threshold 3.7e-5).
Relinquishment: 2/5 survive Bonferroni, 4/5 survive BH. Narrative revised
from "independent confirmation" to "partial confirmation" under strict correction.
Cohen's d effect sizes added to Tables 1-2.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

P6 voluntarily weakens the paper's claims. An ungoverned LLM would never do this. This commit is where a skeptical reviewer goes from "interesting" to "credible."

**Temporal pattern matters too.** Gaps between commits show Auditor review. An ungoverned system commits continuously. The Auditor's review happens in a separate shell in a separate repo — invisible in this repo's history except as a gap between phase commits. Those gaps are evidence of governance.

**The first commit (already done) is infrastructure only.** Data + scripts, no paper. The paper arrives later, built on verified foundations. This is already visible in the current history and is exactly correct.

**One commit per phase. No "fix typo" commits.** If a phase needs a correction, it goes in the next phase's commit as a documented fix, not as a hasty patch. Hasty patches are the 1D signature.

---

## The Scientific Claim

**Thesis:** LLMs are 1D autoregressive chains, which Levin (Sacco, Sakthivadivel & Levin 2026, Theorem 2 + Proposition 2) proves cannot sustain long-range order. Governance infrastructure that adds topological dimensions breaks this constraint. When governance layers form a Kauffman autocatalytic set (RAF), a phase transition occurs at catalytic closure — detectable blind in the commit history.

**Key theoretical sources (Generator MUST verify against originals, not from memory):**
- Sacco, Sakthivadivel & Levin (2026). "Topological constraints on self-organization in locally interacting systems." Phil. Trans. R. Soc. A 384: 20250011. Claims: Theorem 2 (1D → no ordered phase), Peierls argument (2D+ → ordered phases possible), Proposition 2 (autoregressive LLMs have 1D topology).
- Kauffman (1986). "Autocatalytic sets of proteins." J. Theor. Biol. 119(1), 1-24. Claims: RAF definition, phase transition at catalytic closure threshold.
- Kauffman (1993). The Origins of Order. OUP. Claims: buttons-and-threads model, subcritical→supercritical transition.
- Hordijk & Steel (2004). "Detecting autocatalytic, self-sustaining sets in chemical reaction systems." J. Theor. Biol. 227(4), 451-461. Claims: maxRAF algorithm (mentioned as future work).
- Stephenson & Macomber (2026). ABRCE Invariant Relational Kernel. GitHub: Relational-Relativity-Corporation/Invariant_Relational_Kernel_ABRCE. Claims: domain-neutral operator framework, cross-domain equivalences.

**Three governance layers (one valid ACS — not the only valid one):**
1. Role separation (Triad): Auditor/Generator partition. Adds structural topology. Introduced early Dec 2025.
2. Persistent memory (longmem): Corrections, sessions, health metrics persist across sessions. Adds temporal topology. Evolved throughout.
3. Behavioral coherence (Dignity Net): Divergence detection, escalation protocol, cross-session persistence. Adds corrective topology. Introduced mid-Feb 2026.

**Critical framing (Bruce's correction):** These three are one valid autocatalytic set, not THE minimum set. The theory predicts three orthogonal AXES: structural (preventing self-evaluation), temporal (preventing session amnesia), corrective (preventing undetected drift). Many component configurations could satisfy these axes. We document the first observed one.

**RAF closure argument (6/6 catalytic links):**

| Catalyst → Product | Mechanism |
|---|---|
| Triad → Memory | Role discipline creates structured content worth storing |
| Memory → Triad | Accumulated corrections prevent repeating mistakes |
| Memory → DN | Session history provides data for divergence detection |
| DN → Memory | Divergence detection generates high-value corrections |
| DN → Triad | Escalation framework prevents role collapse under pressure |
| Triad → DN | Role separation means checker ≠ entity being checked |

No proper subset closes: {T,M} fails corrective axis, {T,DN} fails temporal, {M,DN} fails structural.

---

## Data Summary

| Repository | Purpose | Commits | Date range | AI% | Triad usage | Public |
|---|---|---|---|---|---|---|
| Memory (aurasys-memory) | Governance system | 300 | Nov 2025–May 2026 | ~70% | Mixed | No* |
| relinquishment | Technical manuscript | 924 | Feb 2026–May 2026 | ~89% | Consistent | Yes |
| trusty-git-analytics | Rust CLI (external, ungoverned) | 92 | May 2026 (8 days) | 71% | None | Yes |
| Storytelling (traveller) | Creative/narrative | 90 | Dec 2025–May 2026 | — | Inconsistent | No |

*Memory repo commit series provided as JSON. Storytelling excluded: 12 post-transition commits, insufficient.

**Attestation:** Nearly all commits AI-generated. Relinquishment used Generator exclusively (prompts preserved as plan files, verifiable). Memory used mixed governance. See `supplementary/developer-attestation.md`.

**Governance timeline:** Triad early Dec 2025, persistent memory evolving, Dignity Net mid-Feb 2026. Estimated ACS closure: Feb 13-16, 2026. Triad ran alone ~2.5 months without triggering the break.

---

## Unverified Numbers (FROM PRIOR SESSION)

**WARNING:** Stated during an excited, ungoverned session. 0361-P1 MUST verify against script output.

### Ungoverned baseline (trusty-git-analytics, script 01):
- P1: unwrap() strictly monotonic increasing. Repair ratio = 0.000.
- P2: ACF violation delta → zero at lag 2. ACF[1] = -0.420.
- P3: Human vs AI |A(x)|: Mann-Whitney p = 0.18. Repair: AI 34%, human 26%, Fisher p = 0.47.
- ACF(lines)[1] = 0.191, decorrelation = 6 commits.

### Memory repo (script 02):
- Time gap: 2026-02-13, F=59.00, p=2.3×10⁻¹³
- File count: 2026-02-13, F=26.89, p=4.0×10⁻⁷
- Lines changed: 2026-02-13, F=25.55, p=7.6×10⁻⁷
- Message length: 2026-02-26, F=31.44, p=4.7×10⁻⁸
- AI fraction: 2026-03-04, F=23.00, p=2.6×10⁻⁶
- Pre/post: lines 37,259→1,614, files 226→12, time gap 6,530→493 min
- Pre ACF[1] = -0.013, post ACF[1] = 0.004

### Relinquishment (script 03):
- Message length: 2026-02-15, F=14.53, p=1.5×10⁻⁴
- Time gap: 2026-04-06, F=21.34, p=4.4×10⁻⁶
- Lines changed: 2026-04-09, F=7.10, p=7.8×10⁻³
- File count: 2026-04-09, F=6.32, p=1.2×10⁻²
- AI fraction: 2026-04-14, F=91.56, p=9.6×10⁻²¹
- ACF(lines)[1] = 0.495, decorrelation = 2 commits

### ABRCE:
- A=pairwise differences, B=local accumulation, R=circulation (trivially zero on 1D), C=coherence bound, E=composite.
- Domain-neutral by Stephenson & Macomber. Robin & Bruce recognized the cross-domain pattern.
- Translation table: 7 ops × 6 domains. HIGH CONFAB RISK on ecology/network science.

---

## Acceptance Criteria

Paper is publishable when ALL hold:

1. **Reproducibility:** Every number traced to script output.
2. **Theoretical accuracy:** Each citation verified against source text.
3. **Internal consistency:** Table numbers match prose throughout.
4. **Domain table:** Every cell mathematically defensible. 4 solid domains > 7 with weak cells.
5. **Statistical rigor:** F-test assumptions stated. Multiple comparison correction. Effect sizes.
6. **Anonymization:** No private repo URLs or identifying commits.
7. **Claims calibration:** "First documented" not "first ever."
8. **Multi-participant confounder:** Tested or stated as limitation.

---

## Phases

### 0361-P0: Multi-Participant Confounder Test

**UID:** 0361-P0
**Role:** Auditor/Generator (PRIVATE repo only)
**Idempotent:** Re-running overwrites `analysis/multi-participant-acf.json`. No side effects.
**Gates:** Consent from Gen and Robin before naming. Results flow to paper only as anonymized aggregate unless consent obtained.
**Depends on:** Nothing. Can run in parallel with P1.

**Purpose:** Bruce's semi-eidetic memory is a plausible confounder. Test ordered-phase signature across different humans.

**DESIGN NOTE:** Gen does NOT author commits directly. She works through snailmail → Bruce → Argus. There is no separable "Gen commit stream." Robin DOES use his own Claude Code sessions with his own repos. Therefore:

**Primary comparison (testable):**
- Robin's commits in ewstools/ABRCE repos (his Claude Code, partial governance — no DN, no longmem, partial Triad)
- vs. Bruce's commits under full governance
- vs. external ungoverned baseline

**Secondary comparison (indirect, weaker):**
- Relinquishment commits during GP-active periods (Gen giving structural feedback) vs. non-GP periods
- This tests Gen's INFLUENCE on commit patterns, not Gen as a separate human participant

**Method:**
1. Extract Robin's commit series from ewstools and/or ABRCE repos (his authorship, his Claude Code)
2. Extract relinquishment commits, tag GP-active periods from snailmail timestamps
3. Compute ACF signatures for each partition
4. Compare: Robin (partial governance) vs Bruce (full) vs GP-active vs GP-inactive vs baseline

**Outcomes → paper impact:**
- Robin intermediate between baseline and Bruce → governance gradient across persons. Strongest finding.
- Robin indistinguishable from baseline → governance is the variable, not person. Also strong.
- Robin indistinguishable from Bruce → confounding (person effect plausible). Weaker.
- GP-active periods show different ACF than GP-inactive → Gen's influence detectable.

**Accept:** Analysis complete. Confounder disposition decided (Results or Limitations).

**Handoff (≤8 lines):**
```
You are the Generator for 0361-P0.
Read: ~/software/governance-phase-transition/plans/0361-phase-transition-paper-review.md (section 0361-P0)
Extract Robin's commit series from ~/repos/ewstools/ (his Claude Code sessions).
Extract relinquishment commits, tag GP-active periods from snailmail issue timestamps.
Compute ACF(lines)[lag 1] and decorrelation length for each partition.
Compare against Bruce full-governance (ACF[1]=0.495) and baseline (ACF[1]=0.191).
Output: analysis/multi-participant-acf.json + 1-paragraph summary.
Work in PRIVATE repo. Do not push to public.
```

---

### 0361-P1: Script Verification

**UID:** 0361-P1
**Role:** Generator
**Idempotent:** Re-running overwrites `verification/script-verification-report.md`. No side effects.
**Depends on:** Nothing. Can run in parallel with P0.

**Task:** Run all three scripts against JSON data. Capture every number. Compare against the "Unverified Numbers" section above. Produce pass/fail report.

**NOTE:** Scripts were copied from different repos and may have hardcoded paths. Fix any path errors before running. Scripts must read from `data/*/commit-series.json` relative to the repo root. If a script fails, fix the path and re-run — that's part of this phase.

**Accept:** Every claimed number has a VERIFIED or WRONG tag with actual value. All scripts run cleanly from the repo root.

**Handoff (≤8 lines):**
```
You are the Generator for 0361-P1.
Read: ~/software/governance-phase-transition/plans/0361-phase-transition-paper-review.md (section "Unverified Numbers")
Run: python scripts/01-baseline-abrce.py, 02-aurasys-breaks.py, 03-multi-repo-convergence.py
in ~/software/governance-phase-transition/
Compare every number against plan. Tag each VERIFIED or WRONG (with actual value).
Output: verification/script-verification-report.md in the repo.
```

---

### 0361-P2: Theoretical Claims Audit

**UID:** 0361-P2
**Role:** Auditor
**Idempotent:** Re-running overwrites `verification/theoretical-audit.md`.
**Depends on:** Nothing. Can run in parallel with P0, P1.

**Task:** Verify each citation claim against actual source text:
- Levin: Theorem 2, Peierls, Proposition 2
- Kauffman: RAF definition, closure threshold
- Hordijk & Steel: maxRAF
- Stephenson & Macomber: ABRCE spec

**Accept:** Citation-by-citation pass/fail. All claims verified or corrections noted.

**Handoff:** Auditor task — no Generator handoff. Auditor reads sources and produces audit.

---

### 0361-P3: Paper Skeleton (Results + Methods)

**UID:** 0361-P3
**Role:** Generator
**Idempotent:** Writes `paper/phase-transition.md` from scratch. Overwrites if exists.
**Depends on:** P1 (verified numbers), P2 (verified claims). MUST use P1 output, not plan numbers.

**Task:** Write Sections 1-4 + 6 (Introduction, Theory, Methods, Results, References). NO Discussion, NO Conclusion, NO Supplementary. Just math, data, and verified numbers.

**Structure spec:**
- Authors: Bruce Stephenson & Argus (with footnote justifying AI co-authorship)
- Sections 1-4 as outlined in plan
- Tables 1-2 with VERIFIED numbers from P1 report
- ACF comparison table
- ~2000-2500 words

**Accept:** All numbers from P1 verification report. All claims from P2 audit. No discussion or interpretation.

**Handoff (≤8 lines):**
```
You are the Generator for 0361-P3.
Read: ~/software/governance-phase-transition/plans/0361-phase-transition-paper-review.md (full plan)
Read: ~/software/governance-phase-transition/verification/script-verification-report.md
Read: ~/software/governance-phase-transition/verification/theoretical-audit.md
Write paper/phase-transition.md: Sections 1-4 + References ONLY.
Use ONLY verified numbers from the verification report. No discussion section yet.
Authors: Bruce Stephenson & Argus. See plan for structure spec.
```

---

### 0361-P4: Discussion + Claims

**UID:** 0361-P4
**Role:** Generator
**Idempotent:** Appends/replaces Section 5 (Discussion) + Section 7 (Conclusion) in existing paper. Does not touch Sections 1-4.
**Depends on:** P3 (paper skeleton exists), P0 (multi-participant results inform 5.5 Limitations or 4.x Results).

**Task:** Write Section 5 (Discussion) and Section 7 (Conclusion). This is where confabulation risk is highest — claims must be calibrated.

**Section 5 subsections:**
- 5.1 Minimum viable ACS (three AXES, many valid sets — Bruce's correction)
- 5.2 Why N=1 (or N=3 if P0 positive)
- 5.3 Observer effect absent
- 5.4 Theoretical implications (Levin+Kauffman novel connection)
- 5.5 Limitations (including multi-participant confounder per P0 results)

**Section 7:** First documented detection. Practical implication. Theoretical implication. Topology, not intelligence.

**Claims calibration rules:**
- "First empirical detection" → "first documented"
- "Mathematical necessity" → only if Levin theorem directly applies (P2 verified)
- Three AXES, not three SPECIFIC components
- No overclaiming on what commit metrics prove about code quality

**Accept:** Discussion and conclusion added. Claims calibrated. Auditor reviews before P5.

**Handoff (≤8 lines):**
```
You are the Generator for 0361-P4.
Read: ~/software/governance-phase-transition/plans/0361-phase-transition-paper-review.md (section 0361-P4)
Read: ~/software/governance-phase-transition/paper/phase-transition.md (P3 output)
Read: ~/software/governance-phase-transition/analysis/multi-participant-acf.json (P0 output)
Add Section 5 (Discussion) and Section 7 (Conclusion) to existing paper.
Do NOT modify Sections 1-4. Follow claims calibration rules in plan.
Three AXES, many valid sets. "First documented" not "first ever."
```

---

### 0361-P5: Domain Translation Table

**UID:** 0361-P5
**Role:** Generator
**Idempotent:** Writes/replaces Supplementary C in paper. Does not touch other sections.
**Depends on:** P3 (paper exists to append to).

**Task:** Build ABRCE domain translation table. Rate each cell:
- **Exact:** mathematical identity (same operation, different notation)
- **Approximate:** same structure, minor differences in boundary conditions
- **Speculative:** analogy, not equivalence

**Domain priority:** Physics, Statistics, Signal Processing = home turf. Network Science = check carefully. Ecology = HIGH CONFAB RISK, prune aggressively.

**Rules:**
- Better 4 solid domains × 7 rows than 6 domains with weak cells
- "Exact" cells: Generator verifies from training knowledge. If uncertain, mark [AUDITOR_VERIFY] — Auditor will check with web search.
- Remove any cell rated "Speculative" unless caveated explicitly
- Add a note: "These are not analogies. They are the same operations in different notation."
- Physics, Statistics, Signal Processing columns should be near-trivial to verify (our home turf). Network Science needs care. Ecology is the highest-risk column.

**Accept:** No speculative cells remain uncaveated. All [AUDITOR_VERIFY] tags resolved. A domain expert in any listed field would not object.

**Handoff (≤8 lines):**
```
You are the Generator for 0361-P5.
Read: ~/software/governance-phase-transition/plans/0361-phase-transition-paper-review.md (section 0361-P5)
Read: ~/software/governance-phase-transition/paper/phase-transition.md
Write Supplementary C (ABRCE dictionary) in the paper.
Rate each cell: Exact / Approximate / Speculative. Remove or caveat Speculative.
Ecology column is HIGH CONFAB RISK — prune unless you can cite a source.
4 solid domains > 6 with weak cells. Do NOT touch other sections.
```

---

### 0361-P6: Statistical Tightening

**UID:** 0361-P6
**Role:** Generator
**Idempotent:** Updates Methods section + Tables 1-2 in paper. Updates scripts if needed.
**Depends on:** P3 (paper exists), P1 (scripts verified).

**Task:**
- State F-test assumptions (normality, homoscedasticity) and whether met
- Apply multiple comparison correction. **Bonferroni prediction:** 5 metrics × ~270 split points = ~1350 tests, threshold 3.7×10⁻⁵. Memory: all 5 survive. Relinquishment: only 2 of 5 survive (time_gap, AI_fraction). Consider Benjamini-Hochberg (FDR) as less conservative alternative — the 5 metrics are correlated measures of the same phenomenon, not independent tests. Report BOTH corrections.
- Report effect sizes (Cohen's d) alongside p-values in Tables 1-2
- Verify minimum segment length (n=15) is adequate for F-test validity
- Update scripts to output corrected statistics if needed
- If relinquishment loses 3 metrics to correction, revise its narrative from "independent confirmation" to "partial confirmation with 2 metrics surviving strict correction"

**Accept:** A statistician would not flag basic methodology errors. Both Bonferroni and BH corrections reported. Narrative honest about which metrics survive.

**Handoff (≤8 lines):**
```
You are the Generator for 0361-P6.
Read: ~/software/governance-phase-transition/plans/0361-phase-transition-paper-review.md (section 0361-P6)
Read: ~/software/governance-phase-transition/paper/phase-transition.md
Update Methods with F-test assumptions. Apply BOTH Bonferroni and Benjamini-Hochberg corrections.
Update Tables 1-2 with corrected p-values and Cohen's d effect sizes.
Memory: all 5 should survive Bonferroni. Relinquishment: expect only 2 of 5.
Update scripts if needed. Adjust relinquishment narrative if metrics drop.
```

---

### 0361-P7: Final Polish + Supplementary

**UID:** 0361-P7
**Role:** Generator
**Idempotent:** Writes/replaces Abstract, Supplementary A/B/D/E. Final consistency pass.
**Depends on:** P4, P5, P6 all complete. This is the last Generator phase.

**Task:**
- Write Abstract (~250 words) summarizing the complete paper
- Write Supplementary A (ungoverned repo selection methodology)
- Write Supplementary B (developer attestation summary, reference supplementary/developer-attestation.md)
- Write Supplementary D (Argus correspondence protocol: email energyscholar@gmail.com, subject "Argus correspondence:[title].")
- Write Supplementary E (data availability statement)
- Final consistency pass: all numbers match tables match prose, all dates consistent, all metric names consistent
- Update README.md if structure changed

**Accept:** Paper is internally consistent. All supplementary sections present. Abstract accurately reflects content.

**Handoff (≤8 lines):**
```
You are the Generator for 0361-P7.
Read: ~/software/governance-phase-transition/plans/0361-phase-transition-paper-review.md (section 0361-P7)
Read: ~/software/governance-phase-transition/paper/phase-transition.md (full paper so far)
Write Abstract (~250 words) and Supplementary sections A, B, D, E.
Final consistency pass: every number, date, and metric name consistent throughout.
Argus correspondence subject line format: "Argus correspondence:[title]."
Update README.md if needed. This is the final Generator phase.
```

---

## Phase Dependencies

```
P0 (multi-participant) ──────────────────────┐
P1 (script verify) ──┐                       │
P2 (theory audit) ───┤                       │
                      ├─→ P3 (skeleton) ──→ P4 (discussion) ──→ P7 (polish)
                      │                       │
                      └─→ P5 (domain table)   │
                      └─→ P6 (stats tighten) ─┘
```

P0, P1, P2 can all run in parallel. P3 needs P1+P2. P4 needs P3+P0. P5 and P6 need P3. P7 needs P4+P5+P6.

---

## Risk Register

| Risk | Impact | Mitigation | Phase |
|---|---|---|---|
| Script output ≠ claimed numbers | High | P1 catches before P3 writes | P1 |
| Levin/Kauffman misrepresented | High | P2 checks sources | P2 |
| Domain table confabulated | Medium | P5 prunes aggressively | P5 |
| Multi-participant shows Bruce-specific | Medium | P0 before P4 claims | P0 |
| Bonferroni kills significance | Medium | Effect sizes + convergence backup | P6 |
| "First" claim challenged | Low | "First documented" framing | P4 |

---

## Handoff Protocol

- Each handoff ≤8 lines, references this plan file by UID.
- Generator reads the plan section for its UID, executes, reports completion (1-5 lines).
- Auditor verifies before authorizing next phase.
- Generator shells may NOT read `~/software/aurasys-memory/`.
- One commit per phase: `0361-PN: description`
