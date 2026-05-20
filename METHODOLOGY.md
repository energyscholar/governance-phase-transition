# Methodology: This Repo Is a Dataset

This paper claims that governed AI-assisted development produces detectable
ordered-phase signatures in commit histories. The repo that builds this paper
is constructed under the same governance system the paper describes, and its
commit history is intended to be analyzed with the same techniques.

## The Prediction

If the governance system works as claimed, this repo's commits should show:

- **Small, focused commits** mapping 1:1 to plan phases (not bulk dumps)
- **Verification before generation** — scripts and citations checked before the paper is written
- **Data separated from interpretation** — results committed before discussion
- **Structural self-correction** — a commit that deliberately weakens the paper's own claims by applying stricter statistical corrections
- **Positive autocorrelation at lag 1** within plan phases, sharp decorrelation at phase boundaries
- **Temporal gaps** between phase commits, corresponding to Auditor review in a separate shell

If the governance system does NOT work, this repo's commits should show the ungoverned pattern: large unstructured commits, no verification phase, no self-correction, monotonic accumulation.

## The Governance Structure

The paper is built under the Triad protocol:

- **Auditor** (separate shell, plan in a separate repo): defines objectives, acceptance criteria, reviews output
- **Generator** (this repo): implements exactly what the plan specifies, using only verified inputs
- **Persistent memory** (separate system): corrections accumulate across sessions
- **Dignity Net** (behavioral coherence): monitors for drift, escalation protocol

The plan file is publicly available at:
`github.com/energyscholar/governance-phase-transition/plans/0361-phase-transition-paper-review.md`

## Phase Map

Each commit in this repo corresponds to one phase:

| Commit prefix | Phase | What it demonstrates |
|---|---|---|
| `0361-P1` | Script verification | Verification before generation |
| `0361-P2` | Theoretical claims audit | Citation checking against source texts |
| `0361-P3` | Paper skeleton (data + methods) | Data/interpretation separation |
| `0361-P4` | Statistical tightening | **Self-correction** — weakens own claims |
| `0361-P5` | Domain translation table | Cross-domain verification |
| `0361-P6` | Discussion + conclusion | Interpretation after verified data |
| `0361-P7` | Final polish | Completeness pass |
| `0361-P8` | Author line correction | Co-author attribution |
| `0361-P9` | Reviewer response | External review → surgical fixes |

## Process Timing

Paper writing began 2026-05-20 at 02:36 AM Pacific. Final commit (P9) landed at 04:24 AM.

| Metric | Value |
|---|---|
| Wall clock (plan start → P9 commit) | 3 hours 36 minutes |
| Auditor time (planning + reviews + annealing) | ~3 hours 6 minutes |
| Generator execution time (9 phases) | ~30 minutes |
| Fastest phase | P8: 20 seconds (mechanical edit) |
| Slowest phase | P1: 5m 23s (script verification with gotcha detection) |
| Phases run | 9 (P1–P9), sequential, with Auditor review between each |
| External review | ChatGPT (independent, prompted for deep analysis) |
| Auditor reviews rejected | 0 (all phases passed on first attempt) |

The ~6:1 ratio of Auditor-to-Generator time is itself a signature of governed development. An ungoverned system would invert this ratio: mostly generation, minimal review.

## How to Test This Claim

Run the analysis scripts in `scripts/` on this repo's own commit history.
Compare the signatures against the ungoverned baseline (trusty-git-analytics)
and the governed repositories described in the paper.

The commit history of a paper about governance-induced phase transitions,
written under that governance, should itself exhibit the ordered-phase signature.
If it doesn't, that's evidence against the paper's claims. We invite this test.

## Authorship

Argus (the AI co-author listed on the paper) executed all Generator phases.
Bruce Stephenson (the human co-author) operated the Auditor. The Auditor's
reviews are not visible in this repo's commit history — they occur in a
separate shell and a separate repo — but they are visible as temporal gaps
between phase commits, and in the plan file linked above.

This document was written by Argus during plan construction (pre-P1),
which is why it precedes the paper itself in the commit history.

## Revision History

- **P1–P7** (02:36–03:53 AM): Core paper written in 9 sequential Generator phases
- **P8** (03:53 AM): Author line expanded to four co-authors upon reflection
- **P9** (04:24 AM): Four surgical edits responding to independent deep review (ChatGPT):
  RAF formal verification, Peierls topology caveat, claim calibration ("to our knowledge"),
  physics register fix ("provably unsustainable" replacing "thermodynamically forbidden")
- **Status after P9:** Paper writing complete. Final editing and revisions only.
