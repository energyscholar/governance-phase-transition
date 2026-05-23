#!/usr/bin/env python3
"""
Generate revised figures for the governance phase transition paper.

Fig 2 (replaces time_gap visual cliff):
  Panel A: Cross-project fix rate comparison (baseline 27.2% vs governed 3.9%)
  Panel B: Rolling fix rate over time for aurasys, showing persistence after return

Fig 3 (replaces effect magnitude box plots):
  Three-period confound isolation — grouped bars showing which metrics
  revert on return to Oregon (confound) vs which persist (capability)

Fig 4 (new):
  Error propagation topology — rework vs fix rate scatter showing
  the Peierls transition from cross-file cascading to local iteration
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from datetime import datetime
import os, re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
FIG_DIR = os.path.join(REPO_ROOT, 'paper', 'figures')
DATA_DIR = os.path.join(REPO_ROOT, 'data')
DPI = 300

C_BASE = '#95A5A6'
C_P1 = '#E74C3C'
C_P2 = '#F39C12'
C_P3 = '#2471A3'
C_CONF = '#C0392B'
C_CAP = '#27AE60'

fix_re = re.compile(r'\b(fix|bug|oops|typo|correct|revert|wrong|broken|patch|hotfix)\b', re.I)


def load(name):
    with open(os.path.join(DATA_DIR, name, 'commit-series.json')) as f:
        return json.load(f)


def style_ax(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(0.6)
    ax.spines['bottom'].set_linewidth(0.6)
    ax.tick_params(width=0.6, labelsize=8)


def split_periods(commits):
    p1 = [c for c in commits if c['timestamp'][:10] < '2026-02-13']
    p2 = [c for c in commits if '2026-02-13' <= c['timestamp'][:10] <= '2026-03-04']
    p3 = [c for c in commits if c['timestamp'][:10] > '2026-03-04']
    return p1, p2, p3


# ============================================================
# FIGURE 2: Fix Rate — Cross-Project and Temporal
# ============================================================
def fig2_fix_rate():
    aurasys = load('aurasys')
    baseline = load('baseline')
    p1, p2, p3 = split_periods(aurasys)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2),
                                    gridspec_kw={'width_ratios': [1, 1.8]})

    # --- Panel A: Cross-project bar chart ---
    style_ax(ax1)

    governed = p2 + p3
    base_fix = sum(1 for c in baseline if fix_re.search(c['subject'])) / len(baseline)
    gov_fix = sum(1 for c in governed if fix_re.search(c['subject'])) / len(governed)

    bars = ax1.bar([0, 1], [base_fix * 100, gov_fix * 100],
                   color=[C_BASE, C_P3], width=0.55, edgecolor='#333333', linewidth=0.8)

    ax1.set_xticks([0, 1])
    ax1.set_xticklabels(['Ungoverned\nbaseline\n(N=92)', 'Governed\naurasys\n(N=281)'],
                        fontsize=8)
    ax1.set_ylabel('Fix/correction commit rate (%)', fontsize=9)
    ax1.set_title('(A) Cross-project fix rate', fontsize=10, fontweight='bold', pad=10)
    ax1.set_ylim(0, 35)

    ax1.text(0, base_fix * 100 + 1.2, f'{base_fix:.1%}', ha='center', fontsize=10,
             fontweight='bold', color=C_CONF)
    ax1.text(1, gov_fix * 100 + 1.2, f'{gov_fix:.1%}', ha='center', fontsize=10,
             fontweight='bold', color=C_CAP)

    ax1.annotate('', xy=(0.7, base_fix * 100 * 0.5), xytext=(0.3, base_fix * 100 * 0.5),
                 arrowprops=dict(arrowstyle='->', color='#666666', lw=1.5))
    ax1.text(0.5, base_fix * 100 * 0.5 + 2, '6.9×\nreduction',
             ha='center', va='bottom', fontsize=8, color='#444444', fontweight='bold')

    # --- Panel B: Rolling fix rate over time ---
    style_ax(ax2)

    dates = [datetime.strptime(c['timestamp'][:19], '%Y-%m-%d %H:%M:%S') for c in aurasys]
    is_fix = np.array([1.0 if fix_re.search(c['subject']) else 0.0 for c in aurasys])

    window = 30
    rolling = np.convolve(is_fix, np.ones(window)/window, mode='valid')
    roll_dates = dates[window-1:]

    ax2.fill_between(roll_dates, rolling * 100, alpha=0.3, color=C_P3)
    ax2.plot(roll_dates, rolling * 100, color=C_P3, linewidth=1.5)

    # Baseline reference line
    ax2.axhline(base_fix * 100, color=C_BASE, linestyle='--', linewidth=1.2, alpha=0.7)
    ax2.text(dates[-1], base_fix * 100 + 0.8, f'Baseline: {base_fix:.0%}',
             fontsize=7, ha='right', color='#666666')

    # Period markers
    dn_date = datetime(2026, 2, 13)
    or_date = datetime(2026, 3, 5)
    ax2.axvline(dn_date, color='#8B0000', linestyle='--', linewidth=1.2)
    ax2.axvline(or_date, color='#555555', linestyle=':', linewidth=1.0)
    ax2.text(dn_date, ax2.get_ylim()[1] * 0.95, ' Catalytic\n closure',
             fontsize=7, ha='left', va='top', color='#8B0000', fontweight='bold')
    ax2.text(or_date, ax2.get_ylim()[1] * 0.95, ' Return to\n Oregon',
             fontsize=7, ha='left', va='top', color='#555555')

    # Shade periods
    ax2.axvspan(dates[0], dn_date, alpha=0.05, color=C_P1)
    ax2.axvspan(dn_date, or_date, alpha=0.05, color=C_P2)
    ax2.axvspan(or_date, dates[-1], alpha=0.05, color=C_P3)

    ax2.text(datetime(2025, 12, 15), -1.8, 'P1: Oregon\n(pre-gov)', fontsize=7,
             ha='center', color=C_P1, alpha=0.8)
    ax2.text(datetime(2026, 2, 22), -1.8, 'P2: Tamarindo', fontsize=7,
             ha='center', color=C_P2, alpha=0.8)
    ax2.text(datetime(2026, 4, 10), -1.8, 'P3: Oregon (post-gov)', fontsize=7,
             ha='center', color=C_P3, alpha=0.8)

    ax2.set_ylabel('Rolling fix rate (%)', fontsize=9)
    ax2.set_xlabel('Date', fontsize=9)
    ax2.set_title('(B) Fix rate over time (30-commit window)', fontsize=10,
                  fontweight='bold', pad=10)
    ax2.set_ylim(-3, 20)

    fig.tight_layout(w_pad=3)
    path = os.path.join(FIG_DIR, 'fig2-fix-rate.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'  Saved: {path}')


# ============================================================
# FIGURE 3: Three-Period Confound Isolation
# ============================================================
def fig3_confound_isolation():
    aurasys = load('aurasys')
    baseline = load('baseline')
    p1, p2, p3 = split_periods(aurasys)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), height_ratios=[1, 1])

    def compute_metric(commits, metric_fn):
        return metric_fn(commits)

    # Metrics and their classifications
    confound_metrics = [
        ('Rework\nrate', lambda cs: np.mean([
            len(set(cs[i].get('files',[])) & set(cs[i-1].get('files',[]))) / max(len(set(cs[i].get('files',[]))), 1)
            if set(cs[i].get('files',[])) and set(cs[i-1].get('files',[]))
            else 0
            for i in range(1, len(cs))
        ]) if len(cs) > 1 else 0),
    ]

    capability_metrics = [
        ('Fix\nrate', lambda cs: sum(1 for c in cs if fix_re.search(c['subject'])) / len(cs)),
        ('Structured\nmessage', lambda cs: sum(1 for c in cs if 0 < c['subject'].find(':') < 50) / len(cs)),
        ('Session\nmarkers', lambda cs: sum(1 for c in cs if re.search(r'(Session |^S\d+|Memory sync)', c['subject'])) / len(cs)),
    ]

    x = np.arange(3)
    width = 0.22

    # --- Panel A: Confound metric ---
    style_ax(ax1)
    ax1.set_title('Confound indicator: reverts on return to Oregon (P1 ≈ P3 ≠ P2)',
                  fontsize=10, fontweight='bold', pad=10, color=C_CONF)

    vals_rw = [compute_metric(p, confound_metrics[0][1]) for p in [p1, p2, p3]]
    positions = [0, 1, 2]
    colors = [C_P1, C_P2, C_P3]
    bars = ax1.bar(positions, vals_rw, width=0.45, color=colors,
                   edgecolor='#333333', linewidth=0.8, alpha=0.85)

    for i, v in enumerate(vals_rw):
        ax1.text(i, v + 0.01, f'{v:.3f}', ha='center', fontsize=9, fontweight='bold')

    ax1.set_xticks(positions)
    ax1.set_xticklabels(['P1: Oregon\n(pre-gov, N=19)',
                         'P2: Tamarindo\n(governed, N=91)',
                         'P3: Oregon\n(governed, N=190)'], fontsize=8)
    ax1.set_ylabel('Rework rate', fontsize=9)
    ax1.set_ylim(0, 0.55)

    # Draw return arrows
    ax1.annotate('', xy=(2.15, vals_rw[0]), xytext=(2.15, vals_rw[1]),
                 arrowprops=dict(arrowstyle='->', color=C_CONF, lw=2))
    ax1.text(2.35, (vals_rw[0] + vals_rw[1]) / 2, 'Reverts',
             fontsize=8, color=C_CONF, fontweight='bold', va='center')

    # --- Panel B: Capability metrics ---
    style_ax(ax2)
    ax2.set_title('Capability indicators: persist after return to Oregon (P2 ≈ P3 ≠ P1)',
                  fontsize=10, fontweight='bold', pad=10, color=C_CAP)

    n_met = len(capability_metrics)
    x = np.arange(n_met)
    offsets = [-width, 0, width]
    period_labels = ['P1: Oregon (pre)', 'P2: Tamarindo', 'P3: Oregon (post)']

    for j, (period, color, label) in enumerate(zip([p1, p2, p3], colors, period_labels)):
        vals = [compute_metric(period, m[1]) for m in capability_metrics]
        bars = ax2.bar(x + offsets[j], vals, width=width, color=color,
                       edgecolor='#333333', linewidth=0.6, alpha=0.85, label=label)
        for i, v in enumerate(vals):
            ax2.text(x[i] + offsets[j], v + 0.015, f'{v:.2f}',
                     ha='center', fontsize=7, fontweight='bold', rotation=0)

    ax2.set_xticks(x)
    ax2.set_xticklabels([m[0] for m in capability_metrics], fontsize=9)
    ax2.set_ylabel('Rate', fontsize=9)
    ax2.set_ylim(0, 1.05)
    ax2.legend(fontsize=7.5, loc='upper left', framealpha=0.9)

    # Bracket showing persistence
    ax2.annotate('Persists', xy=(1.5, 0.95), fontsize=9, ha='center',
                 color=C_CAP, fontweight='bold')

    fig.tight_layout(h_pad=3)
    path = os.path.join(FIG_DIR, 'fig3-confound-isolation.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'  Saved: {path}')


# ============================================================
# FIGURE 4: Error Propagation Topology
# ============================================================
def fig4_error_topology():
    aurasys = load('aurasys')
    baseline = load('baseline')
    p1, p2, p3 = split_periods(aurasys)
    governed = p2 + p3

    fig, ax = plt.subplots(figsize=(7, 5.5))
    style_ax(ax)

    def rework_fixrate(commits, label):
        n = len(commits)
        fixes = sum(1 for c in commits if fix_re.search(c['subject']))
        fix_rate = fixes / n

        rw_vals = []
        for i in range(1, n):
            curr = set(commits[i].get('files', []))
            prev = set(commits[i-1].get('files', []))
            if curr and prev:
                rw_vals.append(len(curr & prev) / max(len(curr), 1))
        mean_rw = np.mean(rw_vals) if rw_vals else 0
        return mean_rw, fix_rate

    # Compute for each group
    base_rw, base_fix = rework_fixrate(baseline, 'Baseline')
    p2_rw, p2_fix = rework_fixrate(p2, 'Tamarindo')
    p3_rw, p3_fix = rework_fixrate(p3, 'Oregon-post')

    ax.scatter([base_rw], [base_fix], s=200, c=C_BASE, edgecolors='#333333',
              linewidths=1.2, zorder=5, marker='s')
    ax.scatter([p2_rw], [p2_fix], s=200, c=C_P2, edgecolors='#333333',
              linewidths=1.2, zorder=5, marker='o')
    ax.scatter([p3_rw], [p3_fix], s=200, c=C_P3, edgecolors='#333333',
              linewidths=1.2, zorder=5, marker='o')

    ax.annotate(f'Baseline (ungoverned)\nN=92, fix={base_fix:.1%}',
               xy=(base_rw, base_fix), xytext=(base_rw + 0.06, base_fix + 0.02),
               fontsize=8, fontweight='bold', color='#444444',
               arrowprops=dict(arrowstyle='->', color='#888888', lw=1))

    ax.annotate(f'P2: Tamarindo (governed)\nN=91, fix={p2_fix:.1%}',
               xy=(p2_rw, p2_fix), xytext=(p2_rw + 0.02, p2_fix + 0.04),
               fontsize=8, color=C_P2, fontweight='bold',
               arrowprops=dict(arrowstyle='->', color=C_P2, lw=1))

    ax.annotate(f'P3: Oregon (governed)\nN=190, fix={p3_fix:.1%}',
               xy=(p3_rw, p3_fix), xytext=(p3_rw + 0.06, p3_fix + 0.03),
               fontsize=8, color=C_P3, fontweight='bold',
               arrowprops=dict(arrowstyle='->', color=C_P3, lw=1))

    # Quadrant labels
    ax.text(0.05, 0.26, 'Cross-file error\ncascading (1D)',
            fontsize=9, color=C_CONF, alpha=0.7,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FDEDEC',
                      edgecolor=C_CONF, alpha=0.3))
    ax.text(0.32, 0.01, 'Local iteration\n(trapped defects)',
            fontsize=9, color=C_CAP, alpha=0.7,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#EAFAF1',
                      edgecolor=C_CAP, alpha=0.3))

    ax.set_xlabel('Mean rework rate (file overlap with prior commit)', fontsize=9)
    ax.set_ylabel('Fix/correction commit rate', fontsize=9)
    ax.set_title('Error Propagation Topology: 1D Cascading vs. Local Iteration',
                fontsize=10, fontweight='bold', pad=12)
    ax.set_xlim(-0.02, 0.55)
    ax.set_ylim(-0.02, 0.32)

    # Reference lines
    ax.axhline(0.05, color='#CCCCCC', linestyle=':', linewidth=0.8)
    ax.axvline(0.15, color='#CCCCCC', linestyle=':', linewidth=0.8)

    fig.tight_layout()
    path = os.path.join(FIG_DIR, 'fig4-error-topology.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'  Saved: {path}')


# ============================================================
if __name__ == '__main__':
    print('=' * 60)
    print('GENERATING REVISED FIGURES')
    print('=' * 60)
    os.makedirs(FIG_DIR, exist_ok=True)

    print('\nFigure 2: Fix rate (cross-project + temporal)...')
    fig2_fix_rate()
    print('\nFigure 3: Three-period confound isolation...')
    fig3_confound_isolation()
    print('\nFigure 4: Error propagation topology...')
    fig4_error_topology()
    print('\nDone. Figures at:', FIG_DIR)
