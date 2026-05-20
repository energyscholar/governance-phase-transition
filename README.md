# Autocatalytic Governance: Detecting a Phase Transition in Human-AI Collaboration

Stephenson & Argus, 2026.

## Summary

We report the first empirical detection of a phase transition in human-AI collaboration. Using blind structural break detection on 1,015 commits across three repositories, we detect a sharp transition coinciding with the activation of a three-component autocatalytic governance set. The result is predicted by the conjunction of Levin's topological theorems (1D systems cannot sustain order) and Kauffman's RAF theory (phase transitions at catalytic closure).

## This Repo Is a Dataset

This paper claims governed AI produces ordered-phase signatures in commit history. This repo is built under the same governance system, and its commit history is intended to be analyzed with the same techniques. See [METHODOLOGY.md](METHODOLOGY.md) for details and an invitation to test this claim.

## Repository Structure

```
METHODOLOGY.md      Why this repo's commit history is itself testable evidence
paper/              The manuscript
data/               Commit series data (JSON) for each repository
  aurasys/          Governance system (300 commits, Nov 2025 - May 2026)
  baseline/         Ungoverned external project (92 commits, May 2026)
  traveller-private/ Creative project (90 commits, Dec 2025 - May 2026)
  relinquishment/   Technical manuscript project (924 commits, Feb - May 2026)
scripts/            Analysis scripts (Python)
  01-baseline-abrce.py       ABRCE operators on ungoverned baseline
  02-aurasys-breaks.py       Phase transition detection in governance repo
  03-multi-repo-convergence.py  Cross-repository break convergence
supplementary/      Developer attestation, screening report
```

## Requirements

- Python 3.10+
- NumPy, SciPy

## License

CC BY 4.0
