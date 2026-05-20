#!/usr/bin/env python3
"""
Multi-repo structural break analysis.
Look for convergent phase transition signatures across all repos that
cross the Feb 2026 governance window.
"""

import json
import numpy as np
from scipy import stats
from datetime import datetime

import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
DATA = os.path.join(REPO_ROOT, 'data')

repos = {
    'aurasys-memory': os.path.join(DATA, 'aurasys', 'commit-series.json'),
    'traveller-private': os.path.join(DATA, 'traveller-private', 'commit-series.json'),
    'relinquishment': os.path.join(DATA, 'relinquishment', 'commit-series.json'),
}

# Reference date: the transition window center
TRANSITION_DATE = datetime(2026, 2, 15, tzinfo=None)

def naive(dt):
    return dt.replace(tzinfo=None)

def structural_break_scan(series, min_segment=15):
    n = len(series)
    if n < 2 * min_segment:
        return None, 0, []
    best_f = 0
    best_k = min_segment
    for k in range(min_segment, n - min_segment):
        s1 = series[:k]
        s2 = series[k:]
        f_stat, p_val = stats.f_oneway(s1, s2)
        if not np.isnan(f_stat) and f_stat > best_f:
            best_f = f_stat
            best_k = k
    _, p_val = stats.f_oneway(series[:best_k], series[best_k:])
    return best_k, best_f, p_val

def autocorrelation(x, max_lag=10):
    x = x - np.mean(x)
    n = len(x)
    var = np.sum(x**2)
    if var == 0:
        return np.zeros(max_lag)
    return np.array([np.sum(x[:n-lag] * x[lag:]) / var for lag in range(max_lag)])

print("=" * 80)
print("MULTI-REPO PHASE TRANSITION ANALYSIS")
print("=" * 80)
print(f"Reference transition window: ~2026-02-13 to 2026-03-04")
print()

all_breaks = {}

for repo_name, json_path in repos.items():
    with open(json_path) as f:
        commits = json.load(f)

    N = len(commits)
    timestamps = [datetime.fromisoformat(c['timestamp']).replace(tzinfo=None) for c in commits]
    days_since_start = np.array([(t - timestamps[0]).total_seconds() / 86400 for t in timestamps])

    # Days relative to transition date
    days_from_transition = np.array([(t - TRANSITION_DATE).total_seconds() / 86400 for t in timestamps])

    lines_changed = np.array([c['lines_changed'] for c in commits], dtype=float)
    file_count = np.array([c['file_count'] for c in commits], dtype=float)
    is_ai = np.array([c['is_ai'] for c in commits], dtype=float)
    time_gap = np.array([c['time_gap_minutes'] for c in commits], dtype=float)
    msg_len = np.array([len(c['subject']) for c in commits], dtype=float)
    has_plan = np.array([c['plan_num'] is not None for c in commits], dtype=float)

    print("=" * 80)
    print(f"REPO: {repo_name}")
    print(f"  N={N}, range: {commits[0]['timestamp'][:10]} to {commits[-1]['timestamp'][:10]}")
    print(f"  AI: {np.sum(is_ai):.0f} ({100*np.mean(is_ai):.1f}%)")

    # Does this repo cross the transition?
    pre_transition = sum(1 for t in timestamps if t < TRANSITION_DATE)
    post_transition = N - pre_transition
    print(f"  Pre-transition commits: {pre_transition}, Post: {post_transition}")

    if pre_transition < 10 or post_transition < 10:
        print(f"  SKIPPING structural break scan (insufficient pre or post commits)")
        print()

        # Still compute autocorrelation for post-transition-only repos
        if pre_transition < 10 and N >= 30:
            print(f"  Post-transition-only repo — computing baseline characteristics:")
            acf_lines = autocorrelation(lines_changed, 10)
            decorr = next((i for i in range(1, 10) if acf_lines[i] <= 0), 10)
            print(f"    ACF(lines)[1..5]: {' '.join(f'{acf_lines[i]:.3f}' for i in range(1, 6))}")
            print(f"    Decorrelation: {decorr} commits")
            print(f"    Mean lines/commit: {np.mean(lines_changed):.0f}")
            print(f"    Mean files/commit: {np.mean(file_count):.1f}")

            # A operator
            A_lines = np.diff(lines_changed)
            print(f"    Mean |A(lines)|: {np.mean(np.abs(A_lines)):.0f}")
            print()
        continue

    print()

    # Structural break scan on multiple metrics
    metrics = {
        'lines_changed': lines_changed,
        'file_count': file_count,
        'AI_fraction': is_ai,
        'time_gap': time_gap,
        'msg_length': msg_len,
    }

    repo_breaks = {}
    print(f"  {'Metric':<16} {'Break':>6} {'Date':>12} {'DaysFromTx':>10} {'F':>8} {'p':>12} {'Pre→Post':>20}")
    print("  " + "-" * 90)

    for name, series in metrics.items():
        best_k, best_f, p_val = structural_break_scan(series)
        if best_k is None:
            continue

        break_date = commits[best_k]['timestamp'][:10]
        break_dt = timestamps[best_k]
        days_from_tx = (break_dt - TRANSITION_DATE).total_seconds() / 86400

        pre_mean = np.mean(series[:best_k])
        post_mean = np.mean(series[best_k:])

        sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else ""

        ratio_str = f"{pre_mean:.1f}→{post_mean:.1f}"

        print(f"  {name:<16} {best_k:6d} {break_date:>12} {days_from_tx:+10.0f} {best_f:8.2f} {p_val:12.4e} {ratio_str:>20} {sig}")

        repo_breaks[name] = {
            'commit': best_k,
            'date': break_date,
            'days_from_transition': days_from_tx,
            'F': best_f,
            'p': p_val,
        }

    all_breaks[repo_name] = repo_breaks

    # Autocorrelation comparison: pre vs post transition
    tx_idx = pre_transition
    print()
    print(f"  Autocorrelation comparison (split at transition date, commit {tx_idx}):")

    for name, series in [('lines_changed', lines_changed), ('file_count', file_count)]:
        pre = series[:tx_idx]
        post = series[tx_idx:]

        if len(pre) >= 15 and len(post) >= 15:
            acf_pre = autocorrelation(pre, 10)
            acf_post = autocorrelation(post, 10)
            decorr_pre = next((i for i in range(1, 10) if acf_pre[i] <= 0), 10)
            decorr_post = next((i for i in range(1, 10) if acf_post[i] <= 0), 10)

            print(f"    {name}:")
            print(f"      Pre  ACF[1..5]: {' '.join(f'{acf_pre[i]:.3f}' for i in range(1, 6))} | decorr={decorr_pre}")
            print(f"      Post ACF[1..5]: {' '.join(f'{acf_post[i]:.3f}' for i in range(1, 6))} | decorr={decorr_post}")

    # Domain wall comparison
    print()
    print(f"  Domain wall magnitude |A(lines)| comparison:")
    A_pre = np.abs(np.diff(lines_changed[:tx_idx]))
    A_post = np.abs(np.diff(lines_changed[tx_idx:]))
    if len(A_pre) >= 5 and len(A_post) >= 5:
        print(f"    Pre:  mean={np.mean(A_pre):.0f}, median={np.median(A_pre):.0f}")
        print(f"    Post: mean={np.mean(A_post):.0f}, median={np.median(A_post):.0f}")
        u, p = stats.mannwhitneyu(A_pre, A_post, alternative='two-sided')
        print(f"    Mann-Whitney U={u:.0f}, p={p:.4f}")

    print()

# ===== CONVERGENCE ACROSS REPOS =====
print("=" * 80)
print("CONVERGENCE: Do structural breaks cluster at the same date across repos?")
print("=" * 80)
print()

print(f"{'Repo':<20} {'Metric':<16} {'Break Date':>12} {'Days from Tx':>12} {'p-value':>12}")
print("-" * 75)

all_days_from_tx = []
for repo_name, breaks in all_breaks.items():
    for metric, bp in sorted(breaks.items(), key=lambda x: x[1]['days_from_transition']):
        sig = "***" if bp['p'] < 0.001 else "**" if bp['p'] < 0.01 else "*" if bp['p'] < 0.05 else ""
        print(f"{repo_name:<20} {metric:<16} {bp['date']:>12} {bp['days_from_transition']:+12.0f} {bp['p']:12.4e} {sig}")
        if bp['p'] < 0.05:  # only count significant breaks
            all_days_from_tx.append(bp['days_from_transition'])

print()
if all_days_from_tx:
    arr = np.array(all_days_from_tx)
    print(f"Significant breaks: n={len(arr)}")
    print(f"  Mean days from transition: {np.mean(arr):+.1f}")
    print(f"  Median days from transition: {np.median(arr):+.1f}")
    print(f"  Std dev: {np.std(arr):.1f} days")
    print(f"  Range: [{np.min(arr):+.0f}, {np.max(arr):+.0f}] days from transition")

    # How many fall within ±30 days of transition?
    within_30 = np.sum(np.abs(arr) <= 30)
    print(f"  Within ±30 days of transition: {within_30}/{len(arr)} ({100*within_30/len(arr):.0f}%)")

    # One-sample t-test: are breaks centered on transition date?
    t_stat, t_p = stats.ttest_1samp(arr, 0)
    print(f"  One-sample t-test (H0: centered on transition): t={t_stat:.2f}, p={t_p:.4f}")

# ===== COMPARISON WITH UNGOVERNED REPO-008 =====
print()
print("=" * 80)
print("COMPARISON: Governed repos vs ungoverned repo-008")
print("=" * 80)
print()

with open(os.path.join(DATA, 'baseline', 'commit-series.json')) as f:
    r008 = json.load(f)

r008_lines = np.array([c['lines_changed'] for c in r008], dtype=float)
r008_A = np.abs(np.diff(r008_lines))
r008_acf = autocorrelation(r008_lines, 10)
r008_decorr = next((i for i in range(1, 10) if r008_acf[i] <= 0), 10)

print(f"  Repo-008 (ungoverned, {len(r008)} commits):")
print(f"    Mean lines/commit: {np.mean(r008_lines):.0f}")
print(f"    Mean |A(lines)|: {np.mean(r008_A):.0f}")
print(f"    ACF(lines)[1..3]: {' '.join(f'{r008_acf[i]:.3f}' for i in range(1, 4))}")
print(f"    Decorrelation: {r008_decorr} commits")
print()

# Post-transition governed repos
for repo_name, json_path in repos.items():
    with open(json_path) as f:
        commits = json.load(f)
    timestamps = [datetime.fromisoformat(c['timestamp']).replace(tzinfo=None) for c in commits]

    # Only post-transition commits
    post_commits = [c for c, t in zip(commits, timestamps) if t >= TRANSITION_DATE]
    if len(post_commits) < 20:
        continue

    gov_lines = np.array([c['lines_changed'] for c in post_commits], dtype=float)
    gov_A = np.abs(np.diff(gov_lines))
    gov_acf = autocorrelation(gov_lines, 10)
    gov_decorr = next((i for i in range(1, 10) if gov_acf[i] <= 0), 10)

    print(f"  {repo_name} (post-transition, {len(post_commits)} commits):")
    print(f"    Mean lines/commit: {np.mean(gov_lines):.0f}")
    print(f"    Mean |A(lines)|: {np.mean(gov_A):.0f}")
    print(f"    ACF(lines)[1..3]: {' '.join(f'{gov_acf[i]:.3f}' for i in range(1, 4))}")
    print(f"    Decorrelation: {gov_decorr} commits")
    print()
