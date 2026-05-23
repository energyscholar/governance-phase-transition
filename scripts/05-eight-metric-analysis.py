#!/usr/bin/env python3
"""
0361-P10-1: Eight-metric analysis with permutation tests.
Extends the 5 original metrics with 3 new ones:
  - deletions_fraction: lines_deleted / lines_changed
  - message_structure: binary, 1 if subject contains ":" (conventional structured prefix)
  - path_entropy: Shannon entropy of top-level directory distribution per commit

Adds permutation test: shuffle commit order 10,000x, compute max-F from null distribution.
This replaces the parametric p-value with a distribution-free alternative that inherently
accounts for the multiple-comparison problem across split points.

Uses min_segment=20 per P1 recommendation.
"""

import json
import math
import numpy as np
from scipy import stats
from collections import Counter
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
MIN_SEGMENT = 20
ALPHA = 0.05
N_PERMS = 10000
RNG_SEED = 42


def load_repo(name):
    with open(os.path.join(REPO_ROOT, 'data', name, 'commit-series.json')) as f:
        return json.load(f)


def extract_metrics(commits):
    n = len(commits)
    metrics = {
        'lines_changed': np.array([c['lines_changed'] for c in commits], dtype=float),
        'file_count': np.array([c['file_count'] for c in commits], dtype=float),
        'time_gap': np.array([c['time_gap_minutes'] for c in commits], dtype=float),
        'msg_length': np.array([len(c['subject']) for c in commits], dtype=float),
        'AI_fraction': np.array([c['is_ai'] for c in commits], dtype=float),
    }

    # --- New metric 1: deletions_fraction ---
    del_frac = np.zeros(n)
    for i, c in enumerate(commits):
        lc = c.get('lines_changed', 0)
        ld = c.get('lines_deleted', 0)
        del_frac[i] = ld / lc if lc > 0 else 0.0
    metrics['deletions_fraction'] = del_frac

    # --- New metric 2: message_structure ---
    msg_struct = np.zeros(n)
    for i, c in enumerate(commits):
        subj = c['subject']
        colon_pos = subj.find(':')
        if 0 < colon_pos < 50:
            msg_struct[i] = 1.0
    metrics['message_structure'] = msg_struct

    # --- New metric 3: path_entropy ---
    if 'files' in commits[0] and commits[0]['files']:
        pe = np.zeros(n)
        for i, c in enumerate(commits):
            files = c.get('files', [])
            if len(files) <= 1:
                pe[i] = 0.0
                continue
            dirs = [f.split('/')[0] if '/' in f else '.' for f in files]
            counts = Counter(dirs)
            total = sum(counts.values())
            entropy = 0.0
            for cnt in counts.values():
                p = cnt / total
                if p > 0:
                    entropy -= p * math.log2(p)
            pe[i] = entropy
        metrics['path_entropy'] = pe
    else:
        metrics['path_entropy'] = None

    return metrics


def structural_break_scan(series, min_segment=MIN_SEGMENT):
    n = len(series)
    if n < 2 * min_segment:
        return None, None, None
    best_f, best_k = 0, min_segment
    for k in range(min_segment, n - min_segment):
        pre, post = series[:k], series[k:]
        n1, n2 = len(pre), len(post)
        m1, m2 = np.mean(pre), np.mean(post)
        var_pooled = (np.sum((pre - m1)**2) + np.sum((post - m2)**2)) / (n1 + n2 - 2)
        if var_pooled == 0:
            continue
        f = (n1 * n2 * (m1 - m2)**2) / ((n1 + n2) * var_pooled)
        if f > best_f:
            best_f, best_k = f, k
    p = stats.f.sf(best_f, 1, n - 2)
    return best_k, best_f, p


def cohens_d(pre, post):
    n1, n2 = len(pre), len(post)
    m1, m2 = np.mean(pre), np.mean(post)
    s1, s2 = np.std(pre, ddof=1), np.std(post, ddof=1)
    s_pooled = np.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))
    if s_pooled == 0:
        return float('inf')
    return (m1 - m2) / s_pooled


def benjamini_hochberg(p_values, alpha=ALPHA):
    m = len(p_values)
    sorted_indices = np.argsort(p_values)
    sorted_p = p_values[sorted_indices]
    thresholds = np.array([(i + 1) / m * alpha for i in range(m)])
    survives = np.zeros(m, dtype=bool)
    last_significant = -1
    for i in range(m):
        if sorted_p[i] <= thresholds[i]:
            last_significant = i
    if last_significant >= 0:
        survives[sorted_indices[:last_significant + 1]] = True
    return survives


def permutation_test(series, observed_f, min_segment=MIN_SEGMENT, n_perms=N_PERMS, seed=RNG_SEED):
    """Permutation test: shuffle series, find max-F across all splits, compare to observed."""
    n = len(series)
    rng = np.random.default_rng(seed)
    count_ge = 0

    ks = np.arange(min_segment, n - min_segment)
    n1s = ks.astype(float)
    n2s = (n - ks).astype(float)

    for i in range(n_perms):
        shuffled = rng.permutation(series)
        cs = np.cumsum(shuffled)
        css = np.cumsum(shuffled**2)

        sum1 = cs[ks - 1]
        sum2 = cs[-1] - sum1
        m1 = sum1 / n1s
        m2 = sum2 / n2s

        ss1 = css[ks - 1]
        ss2 = css[-1] - ss1
        var_pooled = (ss1 - n1s * m1**2 + ss2 - n2s * m2**2) / (n - 2)

        valid = var_pooled > 0
        f_vals = np.zeros(len(ks))
        f_vals[valid] = (n1s[valid] * n2s[valid] * (m1[valid] - m2[valid])**2) / (n * var_pooled[valid])

        if np.max(f_vals) >= observed_f:
            count_ge += 1

    return count_ge / n_perms


def analyze_repo(name, commits, metrics_dict):
    n = len(commits)
    active_metrics = {k: v for k, v in metrics_dict.items() if v is not None}
    metric_names = list(active_metrics.keys())
    n_metrics = len(metric_names)
    n_splits = n - 2 * MIN_SEGMENT
    total_comparisons = n_metrics * n_splits
    bonferroni_threshold = ALPHA / total_comparisons

    print(f"  N = {n} commits")
    print(f"  Metrics analyzed: {n_metrics}")
    if metrics_dict.get('path_entropy') is None:
        print(f"  NOTE: path_entropy unavailable (no file paths in data)")
    print(f"  min_segment = {MIN_SEGMENT}")
    print(f"  Valid split points per metric: {n_splits}")
    print(f"  Total comparisons: {n_metrics} × {n_splits} = {total_comparisons}")
    print(f"  Bonferroni threshold: {ALPHA} / {total_comparisons} = {bonferroni_threshold:.2e}")
    print(f"  Permutation test: {N_PERMS} shuffles, seed={RNG_SEED}")
    print()

    results = []
    p_values = []

    for mname in metric_names:
        series = active_metrics[mname]
        k, f_stat, p_val = structural_break_scan(series)
        if k is None:
            continue

        pre, post = series[:k], series[k:]
        ts = commits[k]['timestamp']
        date_str = ts[:10]
        d = cohens_d(pre, post)

        # Permutation test
        sys.stdout.write(f"  Permuting {mname}... ")
        sys.stdout.flush()
        p_perm = permutation_test(series, f_stat)
        print(f"done (p_perm = {p_perm:.4f})")

        results.append({
            'metric': mname,
            'k': k,
            'date': date_str,
            'f': f_stat,
            'p_param': p_val,
            'p_perm': p_perm,
            'pre_mean': np.mean(pre),
            'post_mean': np.mean(post),
            'n_pre': len(pre),
            'n_post': len(post),
            'd': d,
        })
        p_values.append(p_val)

    p_values = np.array(p_values)
    bh_survives = benjamini_hochberg(p_values)

    # Also BH on permutation p-values
    perm_p_values = np.array([r['p_perm'] for r in results])
    bh_perm_survives = benjamini_hochberg(perm_p_values)

    print()
    print("  STRUCTURAL BREAKS — ALL 8 METRICS")
    print("  " + "-" * 140)
    hdr = f"  {'Metric':<20} {'Date':<12} {'F':>8} {'p(param)':>12} {'p(perm)':>10} {'Cohen d':>9} {'Bonf':>6} {'BH':>6} {'BH-perm':>8} {'n_pre':>6} {'n_post':>6} {'Pre-mean':>12} {'Post-mean':>12}"
    print(hdr)
    print("  " + "-" * 140)
    for i, r in enumerate(results):
        bonf_ok = "PASS" if r['p_param'] < bonferroni_threshold else "FAIL"
        bh_ok = "PASS" if bh_survives[i] else "FAIL"
        bh_perm_ok = "PASS" if bh_perm_survives[i] else "FAIL"
        print(f"  {r['metric']:<20} {r['date']:<12} {r['f']:>8.2f} {r['p_param']:>12.2e} {r['p_perm']:>10.4f} {r['d']:>+9.3f} {bonf_ok:>6} {bh_ok:>6} {bh_perm_ok:>8} {r['n_pre']:>6} {r['n_post']:>6} {r['pre_mean']:>12.2f} {r['post_mean']:>12.2f}")

    bonf_count = sum(1 for r in results if r['p_param'] < bonferroni_threshold)
    bh_count = sum(bh_survives)
    bh_perm_count = sum(bh_perm_survives)
    perm_sig = sum(1 for r in results if r['p_perm'] < 0.05)
    print()
    print(f"  Bonferroni survivors (parametric): {bonf_count}/{len(results)}")
    print(f"  BH survivors (parametric): {bh_count}/{len(results)}")
    print(f"  Permutation p < 0.05: {perm_sig}/{len(results)}")
    print(f"  BH survivors (permutation): {bh_perm_count}/{len(results)}")
    print()

    return results, bonferroni_threshold, bh_survives, bh_perm_survives


# ============================================================
print("=" * 80)
print("EIGHT-METRIC ANALYSIS WITH PERMUTATION TESTS — 0361-P10-1")
print("=" * 80)
print()
print(f"Parameters: min_segment={MIN_SEGMENT}, alpha={ALPHA}, n_perms={N_PERMS}, seed={RNG_SEED}")
print()

# --- AURASYS ---
print("=" * 80)
print("REPO: aurasys-memory")
print("=" * 80)
aurasys = load_repo('aurasys')
aurasys_metrics = extract_metrics(aurasys)
aurasys_results, aurasys_bonf, aurasys_bh, aurasys_bh_perm = analyze_repo(
    'aurasys', aurasys, aurasys_metrics)

# --- RELINQUISHMENT ---
print("=" * 80)
print("REPO: relinquishment")
print("=" * 80)
relin = load_repo('relinquishment')
relin_metrics = extract_metrics(relin)
relin_results, relin_bonf, relin_bh, relin_bh_perm = analyze_repo(
    'relinquishment', relin, relin_metrics)

# --- PARAMETRIC vs PERMUTATION COMPARISON ---
print("=" * 80)
print("PARAMETRIC vs PERMUTATION P-VALUE COMPARISON")
print("=" * 80)
print()
print(f"  {'Repo':<16} {'Metric':<20} {'p(param)':>12} {'p(perm)':>10} {'Agreement':>10}")
print("  " + "-" * 72)
for label, results in [("aurasys", aurasys_results), ("relinquishment", relin_results)]:
    for r in results:
        param_sig = r['p_param'] < 0.05
        perm_sig = r['p_perm'] < 0.05
        agree = "YES" if param_sig == perm_sig else "DISAGREE"
        print(f"  {label:<16} {r['metric']:<20} {r['p_param']:>12.2e} {r['p_perm']:>10.4f} {agree:>10}")
print()

# --- SUMMARY ---
print("=" * 80)
print("SUMMARY")
print("=" * 80)
print()

for label, results, bh, bh_perm, bonf_thresh in [
    ("aurasys", aurasys_results, aurasys_bh, aurasys_bh_perm, aurasys_bonf),
    ("relinquishment", relin_results, relin_bh, relin_bh_perm, relin_bonf),
]:
    n_metrics = len(results)
    bonf_count = sum(1 for r in results if r['p_param'] < bonf_thresh)
    bh_count = sum(bh)
    perm_sig = sum(1 for r in results if r['p_perm'] < 0.05)
    bh_perm_count = sum(bh_perm)
    print(f"  {label}: {n_metrics} metrics analyzed")
    print(f"    Bonferroni (parametric): {bonf_count}/{n_metrics}")
    print(f"    BH (parametric): {bh_count}/{n_metrics}")
    print(f"    Significant (permutation, α=0.05): {perm_sig}/{n_metrics}")
    print(f"    BH (permutation): {bh_perm_count}/{n_metrics}")
    print()
