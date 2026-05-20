#!/usr/bin/env python3
"""
ABRCE operator analysis on repo-008 (trusty-git-analytics) commit series.
Tests predictions P1-P5 from Levin's topological theorems.

Operators (V4 kernel, 1D chain topology):
  A: NodeField -> EdgeField  (discrete gradient / pairwise differences)
  B: EdgeField -> EdgeField  (local accumulation / convolution)
  R: EdgeField -> EdgeField  (cross-topology circulation — trivially zero on 1D)
  E: composite R(B(A(x)), rho)

Standard physics dictionary:
  A <-> discrete nabla (finite differences)
  B <-> convolution / running sum
  |A(x)| <-> domain wall energy
  autocorrelation of x <-> two-point correlator <phi(t)phi(t+tau)>_c
  C(A(x)) <-> bounded order parameter
"""

import json
import numpy as np
from scipy import stats
from collections import defaultdict

with open('commit-series.json') as f:
    commits = json.load(f)

N = len(commits)

# --- Extract series as NodeFields (one value per node on 1D chain) ---
unwrap_delta = np.array([c['unwrap_delta'] for c in commits], dtype=float)
unwrap_cum   = np.array([c['unwrap_cumulative'] for c in commits], dtype=float)
println_delta = np.array([c['println_delta'] for c in commits], dtype=float)
println_cum  = np.array([c['println_cumulative'] for c in commits], dtype=float)
todo_delta   = np.array([c['todo_delta'] for c in commits], dtype=float)
todo_cum     = np.array([c['todo_cumulative'] for c in commits], dtype=float)
lines_changed = np.array([c['lines_changed'] for c in commits], dtype=float)
module_count = np.array([c['module_count'] for c in commits], dtype=float)
file_overlap = np.array([c['file_overlap'] for c in commits], dtype=float)
time_gap     = np.array([c['time_gap_minutes'] for c in commits], dtype=float)
is_ai        = np.array([c['is_ai'] for c in commits], dtype=bool)
ai_model     = [c.get('ai_model') for c in commits]

# --- ABRCE Operators ---

def op_A(x):
    """A: NodeField -> EdgeField. Discrete gradient (forward differences)."""
    return np.diff(x)

def op_B(edges, window=5):
    """B: EdgeField -> EdgeField. Local accumulation (centered convolution)."""
    kernel = np.ones(window) / window
    # Pad to maintain length
    padded = np.pad(edges, (window//2, window//2), mode='edge')
    return np.convolve(padded, kernel, mode='valid')[:len(edges)]

def op_C(edges, scale=None):
    """C: EdgeField -> EdgeField. Bounded coherence, output in (-1, 1)."""
    if scale is None:
        scale = np.std(edges) if np.std(edges) > 0 else 1.0
    return np.tanh(edges / scale)

def op_E(x, rho=1.0, window=5):
    """E: composite. V4: E(x,rho) = R(B(A(x)),rho). On 1D, R=identity (no circulation)."""
    a = op_A(x)
    b = op_B(a, window)
    # R on 1D chain is trivially identity — no cross-topology coupling possible
    # This IS Levin's point: 1D topology cannot support circulation
    return b  # R = identity on 1D

def autocorrelation(x, max_lag=None):
    """Autocorrelation function C(tau) = <x(t)x(t+tau)> / <x(t)^2>."""
    x = x - np.mean(x)
    n = len(x)
    if max_lag is None:
        max_lag = n // 3
    result = np.zeros(max_lag)
    var = np.sum(x**2)
    if var == 0:
        return result
    for lag in range(max_lag):
        result[lag] = np.sum(x[:n-lag] * x[lag:]) / var
    return result


print("=" * 70)
print("ABRCE OPERATOR ANALYSIS — REPO-008 (trusty-git-analytics)")
print("=" * 70)
print(f"N = {N} commits, {np.sum(is_ai)} AI / {np.sum(~is_ai)} human")
print(f"Time span: {commits[0]['timestamp'][:10]} to {commits[-1]['timestamp'][:10]}")
print()

# ===== P1: MONOTONIC ACCUMULATION =====
print("=" * 70)
print("P1: Violations accumulate monotonically (1D can't self-correct)")
print("=" * 70)
print()

for name, cum_series, delta_series in [
    ("unwrap", unwrap_cum, unwrap_delta),
    ("println", println_cum, println_delta),
    ("todo", todo_cum, todo_delta),
]:
    decreases = np.sum(np.diff(cum_series) < 0)
    increases = np.sum(np.diff(cum_series) > 0)
    flat = np.sum(np.diff(cum_series) == 0)

    # Find the largest single decrease (if any correction happened)
    diffs = np.diff(cum_series)
    neg_diffs = diffs[diffs < 0]
    max_decrease = np.min(neg_diffs) if len(neg_diffs) > 0 else 0

    # Net repair ratio: (sum of negative deltas) / (sum of positive deltas)
    pos_sum = np.sum(delta_series[delta_series > 0])
    neg_sum = np.sum(delta_series[delta_series < 0])
    repair_ratio = abs(neg_sum / pos_sum) if pos_sum > 0 else 0

    print(f"  {name}_cumulative:")
    print(f"    Final value: {cum_series[-1]:.0f}")
    print(f"    Steps: {increases:.0f} up, {decreases:.0f} down, {flat:.0f} flat")
    print(f"    Largest single decrease: {max_decrease:.0f}")
    print(f"    Repair ratio (|neg_sum/pos_sum|): {repair_ratio:.3f}")

    # Who does the repair?
    ai_repairs = np.sum(delta_series[is_ai][delta_series[is_ai] < 0])
    human_repairs = np.sum(delta_series[~is_ai][delta_series[~is_ai] < 0])
    ai_additions = np.sum(delta_series[is_ai][delta_series[is_ai] > 0])
    human_additions = np.sum(delta_series[~is_ai][delta_series[~is_ai] > 0])
    print(f"    AI:    +{ai_additions:.0f} / {ai_repairs:.0f} (net {ai_additions+ai_repairs:.0f})")
    print(f"    Human: +{human_additions:.0f} / {human_repairs:.0f} (net {human_additions+human_repairs:.0f})")
    print()

# Monotonicity test: what fraction of the trajectory is "new high water mark"
for name, cum_series in [("unwrap", unwrap_cum), ("println", println_cum), ("todo", todo_cum)]:
    hwm_count = 0
    hwm = cum_series[0]
    for v in cum_series[1:]:
        if v > hwm:
            hwm_count += 1
            hwm = v
    print(f"  {name}: {hwm_count}/{N-1} commits set new high-water mark ({100*hwm_count/(N-1):.1f}%)")
print()

# ===== P2: DOMAIN WALLS AT SESSION BOUNDARIES =====
print("=" * 70)
print("P2: |A(x)| correlates with time_gap (domain walls at session boundaries)")
print("=" * 70)
print()

# A operator on key metrics (N-1 edges for N nodes)
A_unwrap = op_A(unwrap_delta)
A_lines  = op_A(lines_changed)
A_modules = op_A(module_count)
A_overlap = op_A(file_overlap)

# time_gap aligns with commits[1:], so edges align with time_gap[1:]
# A_x[i] = x[i+1] - x[i], so edge i sits between nodes i and i+1
# The "incoming" time_gap for edge i is time_gap[i+1] (gap before node i+1)
tg_edges = time_gap[1:]  # N-1 values, aligned with A operator output

print("Correlation of |A(x)| with time_gap (continuous, not binned):")
print()
for name, A_x in [
    ("unwrap_delta", A_unwrap),
    ("lines_changed", A_lines),
    ("module_count", A_modules),
    ("file_overlap", A_overlap),
]:
    abs_A = np.abs(A_x)
    # Spearman (rank correlation, robust to outliers)
    rho_s, p_s = stats.spearmanr(tg_edges, abs_A)
    # Pearson
    rho_p, p_p = stats.pearsonr(tg_edges, abs_A)
    print(f"  |A({name})| vs time_gap:")
    print(f"    Spearman rho = {rho_s:.4f}  (p = {p_s:.4e})")
    print(f"    Pearson  r   = {rho_p:.4f}  (p = {p_p:.4e})")
    print()

# Also: composite |A| across all metrics (multivariate domain wall energy)
A_composite = np.sqrt(A_unwrap**2 + A_lines**2 + A_modules**2)
rho_s, p_s = stats.spearmanr(tg_edges, np.abs(A_composite))
print(f"  |A_composite| (unwrap + lines + modules) vs time_gap:")
print(f"    Spearman rho = {rho_s:.4f}  (p = {p_s:.4e})")
print()

# Scatter data: binned view for intuition (but analysis uses continuous)
print("  Intuition check — median |A(unwrap)| by time_gap quartile:")
quartiles = np.percentile(tg_edges, [25, 50, 75])
for lo, hi, label in [(0, quartiles[0], "Q1"), (quartiles[0], quartiles[1], "Q2"),
                       (quartiles[1], quartiles[2], "Q3"), (quartiles[2], 1e9, "Q4")]:
    mask = (tg_edges >= lo) & (tg_edges < hi)
    if np.any(mask):
        print(f"    {label} (gap {lo:.0f}-{hi:.0f} min): median |A| = {np.median(np.abs(A_unwrap[mask])):.1f}, n={np.sum(mask)}")
print()

# ===== P3: AUTOCORRELATION DECAY =====
print("=" * 70)
print("P3: Autocorrelation of metrics decays with distance (no long-range order)")
print("=" * 70)
print()

max_lag = 20
for name, series in [
    ("unwrap_delta", unwrap_delta),
    ("lines_changed", lines_changed),
    ("module_count", module_count),
    ("file_overlap", file_overlap),
]:
    acf = autocorrelation(series, max_lag)
    # Find decorrelation length (first zero crossing)
    decorr = max_lag
    for i in range(1, max_lag):
        if acf[i] <= 0:
            decorr = i
            break

    print(f"  {name}:")
    print(f"    Decorrelation length: {decorr} commits")
    print(f"    ACF[1..5]: {' '.join(f'{acf[i]:.3f}' for i in range(1, min(6, max_lag)))}")
    print(f"    ACF[6..10]: {' '.join(f'{acf[i]:.3f}' for i in range(6, min(11, max_lag)))}")

    # Exponential decay fit: ACF(tau) ~ exp(-tau/xi)
    # Fit log(ACF) = -tau/xi for positive ACF values
    positive_lags = [(i, acf[i]) for i in range(1, max_lag) if acf[i] > 0.01]
    if len(positive_lags) >= 3:
        lags_fit = np.array([p[0] for p in positive_lags])
        acf_fit = np.array([p[1] for p in positive_lags])
        slope, intercept, r, p, se = stats.linregress(lags_fit, np.log(acf_fit))
        xi = -1.0 / slope if slope < 0 else float('inf')
        print(f"    Correlation length xi = {xi:.2f} commits (R² = {r**2:.3f})")
    print()

# Also: autocorrelation of A(x) — the EDGE field
print("  Autocorrelation of A(unwrap_delta) — the edge field:")
acf_A = autocorrelation(A_unwrap, max_lag)
print(f"    ACF[1..5]: {' '.join(f'{acf_A[i]:.3f}' for i in range(1, min(6, max_lag)))}")
decorr_A = max_lag
for i in range(1, max_lag):
    if acf_A[i] <= 0:
        decorr_A = i
        break
print(f"    Decorrelation length: {decorr_A} commits")
print()

# ===== P4: HUMAN vs AI SIGNATURES =====
print("=" * 70)
print("P4: Human commits show different A(x) signature (repair events)")
print("=" * 70)
print()

# For each edge (between consecutive commits), classify by author of second commit
# Edge i corresponds to transition from commit i to commit i+1
# The "agent" at edge i is the author of commit i+1
edge_is_ai = is_ai[1:]  # N-1 values aligned with A output

for name, A_x in [
    ("unwrap_delta", A_unwrap),
    ("lines_changed", A_lines),
    ("module_count", A_modules),
    ("file_overlap", A_overlap),
]:
    ai_vals = A_x[edge_is_ai]
    human_vals = A_x[~edge_is_ai]

    print(f"  A({name}):")
    print(f"    AI edges (n={len(ai_vals)}):    mean={np.mean(ai_vals):.2f}, |mean|={np.mean(np.abs(ai_vals)):.2f}, std={np.std(ai_vals):.2f}")
    print(f"    Human edges (n={len(human_vals)}): mean={np.mean(human_vals):.2f}, |mean|={np.mean(np.abs(human_vals)):.2f}, std={np.std(human_vals):.2f}")

    # Mann-Whitney U test (nonparametric, doesn't assume normality)
    if len(human_vals) >= 3 and len(ai_vals) >= 3:
        u_stat, p_val = stats.mannwhitneyu(np.abs(ai_vals), np.abs(human_vals), alternative='two-sided')
        print(f"    Mann-Whitney U on |A|: U={u_stat:.1f}, p={p_val:.4f}")
    print()

# Signed analysis: do humans tend to DECREASE violations? (negative A on unwrap)
print("  Repair signature (signed A, not |A|):")
ai_unwrap_edges = A_unwrap[edge_is_ai]
human_unwrap_edges = A_unwrap[~edge_is_ai]
print(f"    AI A(unwrap):    {np.sum(ai_unwrap_edges < 0)}/{len(ai_unwrap_edges)} negative (repair direction)")
print(f"    Human A(unwrap): {np.sum(human_unwrap_edges < 0)}/{len(human_unwrap_edges)} negative (repair direction)")
# Fisher exact test: are humans more likely to produce negative A(unwrap)?
ai_neg = np.sum(ai_unwrap_edges < 0)
ai_pos = np.sum(ai_unwrap_edges >= 0)
hu_neg = np.sum(human_unwrap_edges < 0)
hu_pos = np.sum(human_unwrap_edges >= 0)
odds, fisher_p = stats.fisher_exact([[ai_neg, ai_pos], [hu_neg, hu_pos]])
print(f"    Fisher exact test (repair tendency): OR={odds:.2f}, p={fisher_p:.4f}")
print()

# ===== P5: MODEL CHANGES AS DOMAIN WALLS =====
print("=" * 70)
print("P5: Model changes (sonnet<->opus) are domain walls")
print("=" * 70)
print()

# Identify model transitions (between consecutive AI commits)
# Need to track effective model, skipping None (human commits)
model_at_edge = []
is_model_change = []
prev_model = None

for i in range(N):
    if is_ai[i] and ai_model[i]:
        current_model = ai_model[i]
        if i > 0 and prev_model is not None:
            model_at_edge.append((i-1, prev_model, current_model, prev_model != current_model))
        prev_model = current_model

# Build mask for edges where model changed
model_change_edges = set()
for idx, prev_m, curr_m, changed in model_at_edge:
    if changed:
        model_change_edges.add(idx)

print(f"  Model transitions found: {len(model_at_edge)}")
print(f"  Model CHANGES: {sum(1 for _,_,_,c in model_at_edge if c)}")
print()

# Show each model change
for idx, prev_m, curr_m, changed in model_at_edge:
    if changed:
        print(f"    Edge {idx}: {prev_m} -> {curr_m}")
        print(f"      |A(unwrap)|={abs(A_unwrap[idx]) if idx < len(A_unwrap) else 'N/A':.1f}, "
              f"|A(lines)|={abs(A_lines[idx]) if idx < len(A_lines) else 'N/A':.1f}, "
              f"time_gap={time_gap[idx+1]:.0f}min")
print()

# Compare |A| at model changes vs non-changes
mc_indices = sorted(model_change_edges)
non_mc_indices = [i for i in range(len(A_unwrap)) if i not in model_change_edges]

if mc_indices and non_mc_indices:
    for name, A_x in [("unwrap_delta", A_unwrap), ("lines_changed", A_lines)]:
        mc_vals = np.abs(A_x[mc_indices])
        nmc_vals = np.abs(A_x[non_mc_indices])
        print(f"  |A({name})|:")
        print(f"    At model changes (n={len(mc_vals)}):    mean={np.mean(mc_vals):.2f}, median={np.median(mc_vals):.1f}")
        print(f"    At non-changes (n={len(nmc_vals)}):     mean={np.mean(nmc_vals):.2f}, median={np.median(nmc_vals):.1f}")
        if len(mc_vals) >= 2:
            u_stat, p_val = stats.mannwhitneyu(mc_vals, nmc_vals, alternative='greater')
            print(f"    Mann-Whitney U (one-sided, greater): U={u_stat:.1f}, p={p_val:.4f}")
        print()


# ===== COMPOSITE E OPERATOR =====
print("=" * 70)
print("COMPOSITE E OPERATOR — E(x) = B(A(x)) on 1D chain (R=identity)")
print("=" * 70)
print()

for name, series in [("unwrap_delta", unwrap_delta), ("lines_changed", lines_changed)]:
    E_w3 = op_E(series, window=3)
    E_w5 = op_E(series, window=5)
    E_w7 = op_E(series, window=7)

    # C operator on E (bounded coherence)
    C_E = op_C(E_w5)

    print(f"  E({name}):")
    print(f"    Window=3: mean={np.mean(E_w3):.3f}, std={np.std(E_w3):.3f}, |max|={np.max(np.abs(E_w3)):.3f}")
    print(f"    Window=5: mean={np.mean(E_w5):.3f}, std={np.std(E_w5):.3f}, |max|={np.max(np.abs(E_w5)):.3f}")
    print(f"    Window=7: mean={np.mean(E_w7):.3f}, std={np.std(E_w7):.3f}, |max|={np.max(np.abs(E_w7)):.3f}")
    print(f"    C(E_w5):  mean={np.mean(C_E):.3f}, range=[{np.min(C_E):.3f}, {np.max(C_E):.3f}]")

    # Does E decay with window size? (It should in a disordered system)
    print(f"    |E| ratio w7/w3 = {np.mean(np.abs(E_w7))/np.mean(np.abs(E_w3)):.3f} (>1 = coherent, <1 = disordered)")
    print()

# ===== KEY QUESTION: Does R=0 hold? =====
print("=" * 70)
print("CRITICAL CHECK: Is the system truly 1D? (R operator / circulation)")
print("=" * 70)
print()

# On a true 1D chain, there's no circulation. But if commits return to
# previously-modified modules, that creates effective loops in the interaction graph.
# file_overlap measures this: if overlap > 0, the commit touches files from
# the previous commit, creating a local loop.

print(f"  file_overlap > 0: {np.sum(file_overlap > 0)}/{N} commits ({100*np.sum(file_overlap > 0)/N:.1f}%)")
print(f"  file_overlap mean: {np.mean(file_overlap):.3f}")
print(f"  file_overlap > 0.5: {np.sum(file_overlap > 0.5)}/{N} commits")
print()

# Module revisitation: how often does a commit touch a module that was
# touched within the last K commits? This is effective topology > 1D.
module_history = []
revisit_counts = []
for i, c in enumerate(commits):
    current_modules = set(c['modules'])
    # Look back K commits
    K = 5
    recent_modules = set()
    for j in range(max(0, i-K), i):
        recent_modules.update(commits[j]['modules'])

    revisit = len(current_modules & recent_modules)
    revisit_counts.append(revisit)
    module_history.append(current_modules)

revisit_arr = np.array(revisit_counts, dtype=float)
print(f"  Module revisitation (within last 5 commits):")
print(f"    Mean: {np.mean(revisit_arr):.2f} modules revisited per commit")
print(f"    Commits with revisitation: {np.sum(revisit_arr > 0)}/{N} ({100*np.sum(revisit_arr > 0)/N:.1f}%)")
print(f"    Max revisitation: {np.max(revisit_arr):.0f} modules")
print()
print("  Interpretation: file_overlap and module revisitation create EFFECTIVE")
print("  loops in the interaction graph. But these are local — the developer")
print("  returns to nearby code, not to the global state. This matches Levin's")
print("  'hierarchical' case: local order within cliques, global disorder between.")
print()

# ===== SUMMARY TABLE =====
print("=" * 70)
print("PREDICTION SCORECARD")
print("=" * 70)
print()

# P1 score
p1_unwrap_monotone = (np.sum(np.diff(unwrap_cum) < 0) == 0)
p1_repair_low = all(
    abs(np.sum(d[d < 0])) / np.sum(d[d > 0]) < 0.15 if np.sum(d[d > 0]) > 0 else True
    for d in [unwrap_delta, println_delta, todo_delta]
)

# Detailed P1 repair ratios
repair_ratios = {}
for name, d in [("unwrap", unwrap_delta), ("println", println_delta), ("todo", todo_delta)]:
    pos = np.sum(d[d > 0])
    neg = abs(np.sum(d[d < 0]))
    repair_ratios[name] = neg / pos if pos > 0 else 0

# P2 score: is Spearman rho significant for at least 2 metrics?
rho_unwrap, p_unwrap = stats.spearmanr(tg_edges, np.abs(A_unwrap))
rho_lines, p_lines = stats.spearmanr(tg_edges, np.abs(A_lines))
rho_modules, p_modules = stats.spearmanr(tg_edges, np.abs(A_modules))

p2_sig_count = sum(1 for p in [p_unwrap, p_lines, p_modules] if p < 0.05)
p2_positive = sum(1 for r in [rho_unwrap, rho_lines, rho_modules] if r > 0)

# P3 score: decorrelation length < 10 commits
acf_unwrap = autocorrelation(unwrap_delta, 20)
acf_lines = autocorrelation(lines_changed, 20)
decorr_unwrap = next((i for i in range(1, 20) if acf_unwrap[i] <= 0), 20)
decorr_lines = next((i for i in range(1, 20) if acf_lines[i] <= 0), 20)

# P4 score: human |A| different from AI |A|
_, p4_unwrap_p = stats.mannwhitneyu(np.abs(A_unwrap[edge_is_ai]), np.abs(A_unwrap[~edge_is_ai]), alternative='two-sided')

# P5 score: |A| at model changes > non-changes
if mc_indices:
    mc_median = np.median(np.abs(A_unwrap[mc_indices]))
    nmc_median = np.median(np.abs(A_unwrap[non_mc_indices]))
else:
    mc_median = nmc_median = 0

print(f"  P1 (Monotonic accumulation):")
print(f"     unwrap strictly monotone: {p1_unwrap_monotone}")
print(f"     Repair ratios: unwrap={repair_ratios['unwrap']:.3f}, println={repair_ratios['println']:.3f}, todo={repair_ratios['todo']:.3f}")
print(f"     VERDICT: {'CONFIRMED' if repair_ratios['unwrap'] < 0.10 else 'PARTIAL — some repair exists' if repair_ratios['unwrap'] < 0.30 else 'REJECTED'}")
print()

print(f"  P2 (Domain walls at session boundaries):")
print(f"     Spearman rho: unwrap={rho_unwrap:.3f} (p={p_unwrap:.3e}), lines={rho_lines:.3f} (p={p_lines:.3e}), modules={rho_modules:.3f} (p={p_modules:.3e})")
print(f"     Significant (p<0.05): {p2_sig_count}/3 metrics, positive: {p2_positive}/3")
print(f"     VERDICT: {'CONFIRMED' if p2_sig_count >= 2 else 'PARTIAL' if p2_sig_count >= 1 else 'NOT CONFIRMED'}")
print()

print(f"  P3 (Autocorrelation decay — no long-range order):")
print(f"     Decorrelation: unwrap={decorr_unwrap} commits, lines={decorr_lines} commits")
print(f"     VERDICT: {'CONFIRMED' if decorr_unwrap < 10 and decorr_lines < 10 else 'PARTIAL' if decorr_unwrap < 15 or decorr_lines < 15 else 'NOT CONFIRMED'}")
print()

print(f"  P4 (Human vs AI signatures differ):")
print(f"     Mann-Whitney p = {p4_unwrap_p:.4f}")
ai_repair_frac = np.sum(A_unwrap[edge_is_ai] < 0) / np.sum(edge_is_ai)
hu_repair_frac = np.sum(A_unwrap[~edge_is_ai] < 0) / np.sum(~edge_is_ai)
print(f"     Repair fraction: AI={ai_repair_frac:.2f}, Human={hu_repair_frac:.2f}")
print(f"     VERDICT: {'CONFIRMED' if p4_unwrap_p < 0.05 else 'NOT CONFIRMED (p>' + str(round(p4_unwrap_p,2)) + ')'}")
print()

print(f"  P5 (Model changes are domain walls):")
print(f"     Median |A(unwrap)| at model changes: {mc_median:.1f}")
print(f"     Median |A(unwrap)| at non-changes:   {nmc_median:.1f}")
print(f"     Ratio: {mc_median/nmc_median:.2f}x" if nmc_median > 0 else "     Ratio: N/A")
n_changes = sum(1 for _,_,_,c in model_at_edge if c)
print(f"     n={n_changes} model changes (small sample)")
print(f"     VERDICT: {'CONFIRMED' if mc_median > 1.5 * nmc_median and n_changes >= 3 else 'SUGGESTIVE' if mc_median > nmc_median else 'NOT CONFIRMED'} (note: small n)")
print()

print("=" * 70)
print("RAW DATA DUMP — for further analysis")
print("=" * 70)
print()

# Dump A(unwrap_delta) with time_gap for plotting
print("  Edge | time_gap | A(unwrap) | A(lines) | is_ai | model | A(modules)")
print("  " + "-"*85)
for i in range(len(A_unwrap)):
    m = ai_model[i+1] if ai_model[i+1] else "human"
    mc = " *MC*" if i in model_change_edges else ""
    print(f"  {i:3d}  | {tg_edges[i]:7.0f}  | {A_unwrap[i]:+8.1f}  | {A_lines[i]:+8.0f}  | {'AI' if edge_is_ai[i] else 'HU'}   | {m:12s} | {A_modules[i]:+6.1f}{mc}")
