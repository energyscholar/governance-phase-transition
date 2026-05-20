#!/usr/bin/env python3
"""
Phase transition analysis on aurasys-memory commit series.
Look for structural breaks WITHOUT assuming where they are.
If a phase transition occurred, the data should show it.

Approach:
  1. Compute metrics per commit (sliding windows)
  2. Apply changepoint detection (CUSUM, moving variance)
  3. Compute ABRCE operators and look for regime changes
  4. Report candidate transition points for external validation
"""

import json
import numpy as np
from scipy import stats
from datetime import datetime

import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

with open(os.path.join(REPO_ROOT, 'data', 'aurasys', 'commit-series.json')) as f:
    commits = json.load(f)

N = len(commits)

# --- Parse timestamps ---
timestamps = []
for c in commits:
    ts = c['timestamp']
    dt = datetime.fromisoformat(ts)
    timestamps.append(dt)

# Days since first commit (continuous time axis)
t0 = timestamps[0]
days_since_start = np.array([(t - t0).total_seconds() / 86400 for t in timestamps])

# --- Extract series ---
lines_changed = np.array([c['lines_changed'] for c in commits], dtype=float)
file_count = np.array([c['file_count'] for c in commits], dtype=float)
memory_files = np.array([c['memory_file_count'] for c in commits], dtype=float)
time_gap = np.array([c['time_gap_minutes'] for c in commits], dtype=float)
is_ai = np.array([c['is_ai'] for c in commits], dtype=bool)

# Session-numbered commits (binary: does it have a session number?)
has_session = np.array([c['session_num'] is not None for c in commits], dtype=float)
has_plan = np.array([c['plan_num'] is not None for c in commits], dtype=float)

# Commit message length as proxy for structure
msg_len = np.array([len(c['subject']) for c in commits], dtype=float)

# Commit rate (inverse of time_gap, clipped)
commit_rate = np.zeros(N)
for i in range(1, N):
    if time_gap[i] > 0:
        commit_rate[i] = 1.0 / time_gap[i]  # commits per minute
    else:
        commit_rate[i] = commit_rate[i-1] if i > 0 else 0

print("=" * 70)
print("PHASE TRANSITION ANALYSIS — AURASYS-MEMORY")
print("=" * 70)
print(f"N = {N} commits over {days_since_start[-1]:.0f} days")
print(f"AI commits: {np.sum(is_ai)} ({100*np.sum(is_ai)/N:.1f}%)")
print()

# ===== 1. SLIDING WINDOW METRICS =====
print("=" * 70)
print("1. SLIDING WINDOW METRICS (window=20 commits)")
print("=" * 70)
print()

W = 20  # window size

def sliding_stats(series, window=W):
    """Compute sliding mean, std, and coefficient of variation."""
    n = len(series)
    means = np.zeros(n)
    stds = np.zeros(n)
    for i in range(n):
        lo = max(0, i - window // 2)
        hi = min(n, i + window // 2)
        chunk = series[lo:hi]
        means[i] = np.mean(chunk)
        stds[i] = np.std(chunk)
    return means, stds

# Key metric: memory files per commit (governance activity)
mem_mean, mem_std = sliding_stats(memory_files)

# Key metric: AI fraction in window
ai_mean, _ = sliding_stats(is_ai.astype(float))

# Key metric: lines per commit (productivity/scope)
lines_mean, lines_std = sliding_stats(lines_changed)

# Key metric: session-numbered fraction (governance formalization)
session_mean, _ = sliding_stats(has_session)

# Key metric: plan-tagged fraction
plan_mean, _ = sliding_stats(has_plan)

# Print regime summary at key points
print(f"{'Commit':>6} {'Date':>12} {'Day':>5} {'Mem/cmt':>8} {'AI%':>5} {'Lines':>7} {'Sess%':>6} {'Plan%':>6}")
print("-" * 60)
for i in [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 299]:
    if i < N:
        print(f"{i:6d} {commits[i]['timestamp'][:10]:>12} {days_since_start[i]:5.0f} "
              f"{mem_mean[i]:8.2f} {100*ai_mean[i]:5.1f} {lines_mean[i]:7.0f} "
              f"{100*session_mean[i]:6.1f} {100*plan_mean[i]:6.1f}")
print()

# ===== 2. CUSUM CHANGEPOINT DETECTION =====
print("=" * 70)
print("2. CUSUM CHANGEPOINT DETECTION")
print("=" * 70)
print()

def cusum(series, target=None):
    """Cumulative sum control chart. Returns upper CUSUM and changepoint candidates."""
    if target is None:
        target = np.mean(series)
    s_pos = np.zeros(len(series))
    s_neg = np.zeros(len(series))
    for i in range(1, len(series)):
        s_pos[i] = max(0, s_pos[i-1] + (series[i] - target))
        s_neg[i] = max(0, s_neg[i-1] - (series[i] - target))
    return s_pos, s_neg

# CUSUM on memory_files (governance output)
cusum_pos, cusum_neg = cusum(memory_files)
# Find the maximum excursion point
max_pos_idx = np.argmax(cusum_pos)
max_neg_idx = np.argmax(cusum_neg)

print(f"  Memory files CUSUM:")
print(f"    Max positive excursion at commit {max_pos_idx} ({commits[max_pos_idx]['timestamp'][:10]}): {cusum_pos[max_pos_idx]:.1f}")
print(f"    Max negative excursion at commit {max_neg_idx} ({commits[max_neg_idx]['timestamp'][:10]}): {cusum_neg[max_neg_idx]:.1f}")
print()

# CUSUM on session-numbered fraction (governance formalization)
cusum_pos_s, cusum_neg_s = cusum(has_session)
max_pos_idx_s = np.argmax(cusum_pos_s)
print(f"  Session numbering CUSUM:")
print(f"    Max positive excursion at commit {max_pos_idx_s} ({commits[max_pos_idx_s]['timestamp'][:10]}): {cusum_pos_s[max_pos_idx_s]:.1f}")
print()

# CUSUM on lines_changed (productivity regime)
cusum_pos_l, cusum_neg_l = cusum(lines_changed)
max_pos_idx_l = np.argmax(cusum_pos_l)
print(f"  Lines changed CUSUM:")
print(f"    Max positive excursion at commit {max_pos_idx_l} ({commits[max_pos_idx_l]['timestamp'][:10]}): {cusum_pos_l[max_pos_idx_l]:.1f}")
print()

# ===== 3. STRUCTURAL BREAK TEST (Chow test equivalent) =====
print("=" * 70)
print("3. STRUCTURAL BREAK SCAN — F-statistic across all possible split points")
print("=" * 70)
print()

def structural_break_scan(series, min_segment=20):
    """Scan for the split point that maximizes F-statistic (Chow-like test)."""
    n = len(series)
    best_f = 0
    best_k = min_segment
    f_values = []

    for k in range(min_segment, n - min_segment):
        s1 = series[:k]
        s2 = series[k:]
        # F-test for difference in means
        f_stat, p_val = stats.f_oneway(s1, s2)
        if not np.isnan(f_stat):
            f_values.append((k, f_stat, p_val))
            if f_stat > best_f:
                best_f = f_stat
                best_k = k

    return best_k, best_f, f_values

for name, series in [
    ("memory_files", memory_files),
    ("lines_changed", lines_changed),
    ("file_count", file_count),
    ("has_session", has_session),
    ("AI fraction (binary)", is_ai.astype(float)),
    ("commit_msg_length", msg_len),
]:
    best_k, best_f, f_vals = structural_break_scan(series)
    # Find p-value for best split
    _, p_val = stats.f_oneway(series[:best_k], series[best_k:])

    pre_mean = np.mean(series[:best_k])
    post_mean = np.mean(series[best_k:])

    print(f"  {name}:")
    print(f"    Best split at commit {best_k} ({commits[best_k]['timestamp'][:10]}, day {days_since_start[best_k]:.0f})")
    print(f"    F = {best_f:.2f}, p = {p_val:.4e}")
    print(f"    Pre-mean = {pre_mean:.2f}, Post-mean = {post_mean:.2f} (ratio = {post_mean/pre_mean:.2f}x)" if pre_mean > 0 else f"    Pre-mean = {pre_mean:.2f}, Post-mean = {post_mean:.2f}")
    print(f"    Subject: \"{commits[best_k]['subject'][:60]}\"")
    print()

# ===== 4. ABRCE OPERATORS =====
print("=" * 70)
print("4. ABRCE OPERATORS — regime comparison")
print("=" * 70)
print()

def op_A(x):
    return np.diff(x)

def autocorrelation(x, max_lag=10):
    x = x - np.mean(x)
    n = len(x)
    var = np.sum(x**2)
    if var == 0:
        return np.zeros(max_lag)
    return np.array([np.sum(x[:n-lag] * x[lag:]) / var for lag in range(max_lag)])

# Find the most significant structural break to use as split point
# Use has_session as primary governance indicator
best_k_gov, _, _ = structural_break_scan(has_session)

print(f"  Split point for regime comparison: commit {best_k_gov} ({commits[best_k_gov]['timestamp'][:10]})")
print(f"  Pre-transition: commits 0-{best_k_gov-1} ({best_k_gov} commits)")
print(f"  Post-transition: commits {best_k_gov}-{N-1} ({N-best_k_gov} commits)")
print()

# A operator on lines_changed in each regime
A_pre = op_A(lines_changed[:best_k_gov])
A_post = op_A(lines_changed[best_k_gov:])

print(f"  A(lines_changed) — domain wall magnitudes:")
print(f"    Pre:  mean |A| = {np.mean(np.abs(A_pre)):.0f}, std = {np.std(A_pre):.0f}")
print(f"    Post: mean |A| = {np.mean(np.abs(A_post)):.0f}, std = {np.std(A_post):.0f}")
u_stat, p_val = stats.mannwhitneyu(np.abs(A_pre), np.abs(A_post), alternative='two-sided')
print(f"    Mann-Whitney U: U={u_stat:.0f}, p={p_val:.4f}")
print()

# Autocorrelation in each regime
print(f"  Autocorrelation of lines_changed:")
if len(lines_changed[:best_k_gov]) >= 15:
    acf_pre = autocorrelation(lines_changed[:best_k_gov], 10)
    print(f"    Pre  ACF[1..5]: {' '.join(f'{acf_pre[i]:.3f}' for i in range(1, 6))}")
    decorr_pre = next((i for i in range(1, 10) if acf_pre[i] <= 0), 10)
    print(f"    Pre  decorrelation: {decorr_pre} commits")

acf_post = autocorrelation(lines_changed[best_k_gov:], 10)
print(f"    Post ACF[1..5]: {' '.join(f'{acf_post[i]:.3f}' for i in range(1, 6))}")
decorr_post = next((i for i in range(1, 10) if acf_post[i] <= 0), 10)
print(f"    Post decorrelation: {decorr_post} commits")
print()

# Autocorrelation of memory_files
print(f"  Autocorrelation of memory_files:")
if len(memory_files[:best_k_gov]) >= 15:
    acf_pre_m = autocorrelation(memory_files[:best_k_gov], 10)
    print(f"    Pre  ACF[1..5]: {' '.join(f'{acf_pre_m[i]:.3f}' for i in range(1, 6))}")
    decorr_pre_m = next((i for i in range(1, 10) if acf_pre_m[i] <= 0), 10)
    print(f"    Pre  decorrelation: {decorr_pre_m} commits")

acf_post_m = autocorrelation(memory_files[best_k_gov:], 10)
print(f"    Post ACF[1..5]: {' '.join(f'{acf_post_m[i]:.3f}' for i in range(1, 6))}")
decorr_post_m = next((i for i in range(1, 10) if acf_post_m[i] <= 0), 10)
print(f"    Post decorrelation: {decorr_post_m} commits")
print()

# ===== 5. MULTI-METRIC REGIME DETECTION =====
print("=" * 70)
print("5. CONVERGENCE OF STRUCTURAL BREAKS ACROSS METRICS")
print("=" * 70)
print()

# Collect all best-split points
break_points = {}
for name, series in [
    ("memory_files", memory_files),
    ("lines_changed", lines_changed),
    ("file_count", file_count),
    ("has_session", has_session),
    ("AI_fraction", is_ai.astype(float)),
    ("msg_length", msg_len),
    ("time_gap", time_gap),
]:
    best_k, best_f, _ = structural_break_scan(series)
    _, p = stats.f_oneway(series[:best_k], series[best_k:])
    break_points[name] = {
        'commit': best_k,
        'date': commits[best_k]['timestamp'][:10],
        'day': days_since_start[best_k],
        'F': best_f,
        'p': p
    }

print(f"  {'Metric':<16} {'Commit':>6} {'Date':>12} {'Day':>6} {'F-stat':>8} {'p-value':>10}")
print("  " + "-" * 62)
for name, bp in sorted(break_points.items(), key=lambda x: x[1]['day']):
    sig = "***" if bp['p'] < 0.001 else "**" if bp['p'] < 0.01 else "*" if bp['p'] < 0.05 else ""
    print(f"  {name:<16} {bp['commit']:6d} {bp['date']:>12} {bp['day']:6.0f} {bp['F']:8.2f} {bp['p']:10.4e} {sig}")

# Check for clustering
days_list = sorted([bp['day'] for bp in break_points.values()])
print(f"\n  Break point days (sorted): {[f'{d:.0f}' for d in days_list]}")

# Find clusters (breaks within 30 days of each other)
clusters = []
current_cluster = [days_list[0]]
for d in days_list[1:]:
    if d - current_cluster[-1] < 30:
        current_cluster.append(d)
    else:
        clusters.append(current_cluster)
        current_cluster = [d]
clusters.append(current_cluster)

print(f"  Clusters (within 30 days): {len(clusters)}")
for i, cl in enumerate(clusters):
    mean_day = np.mean(cl)
    # Find the date
    closest_commit = min(range(N), key=lambda j: abs(days_since_start[j] - mean_day))
    print(f"    Cluster {i+1}: days {[f'{d:.0f}' for d in cl]}, center ≈ day {mean_day:.0f} ({commits[closest_commit]['timestamp'][:10]})")


# ===== 6. COMMIT FREQUENCY REGIMES =====
print()
print("=" * 70)
print("6. COMMIT FREQUENCY AND BURST PATTERNS")
print("=" * 70)
print()

# Weekly commit counts
from collections import Counter
weeks = Counter()
for c in commits:
    dt = datetime.fromisoformat(c['timestamp'])
    week = dt.strftime('%Y-W%W')
    weeks[week] += 1

sorted_weeks = sorted(weeks.items())
print(f"  {'Week':<10} {'Commits':>7}")
print("  " + "-" * 20)
for week, count in sorted_weeks:
    bar = '#' * min(count, 40)
    print(f"  {week:<10} {count:7d}  {bar}")

# ===== 7. TIMELINE WITH KNOWN GOVERNANCE EVENTS =====
print()
print("=" * 70)
print("7. KNOWN GOVERNANCE EVENTS (from commit messages)")
print("=" * 70)
print()

events = []
for i, c in enumerate(commits):
    subj = c['subject'].lower()
    if any(kw in subj for kw in ['triad', 'dignity', 'protocol', 'correction', 'hot five',
                                   'longmem', 'disaster recovery', 'health vector',
                                   'schema', 'plan 0308', 'plan 0299', 'retract']):
        events.append((i, days_since_start[i], c['timestamp'][:10], c['subject'][:70]))

print(f"  {'Idx':>4} {'Day':>5} {'Date':>12} Subject")
print("  " + "-" * 80)
for idx, day, date, subj in events:
    print(f"  {idx:4d} {day:5.0f} {date:>12} {subj}")
