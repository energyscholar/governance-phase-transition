#!/usr/bin/env python3
"""
0361-P10-5: Generate publication figures for the governance phase transition paper.
  Fig 1: Topology comparison (1D chain vs K3 governance)
  Fig 2: Timeline (time_gap scatter with governance installation dates)
  Fig 3: Effect magnitude (pre/post box plots for 3 metrics)

matplotlib + numpy only. Deterministic. 300 DPI PNG to paper/figures/.
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
from datetime import datetime
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
FIG_DIR = os.path.join(REPO_ROOT, 'paper', 'figures')
DATA_DIR = os.path.join(REPO_ROOT, 'data')
DPI = 300
BREAK_K = 20

C_PRE = '#C0392B'
C_POST = '#2471A3'
C_WALL = '#8B0000'


def load_aurasys():
    with open(os.path.join(DATA_DIR, 'aurasys', 'commit-series.json')) as f:
        return json.load(f)


def style_ax(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(0.6)
    ax.spines['bottom'].set_linewidth(0.6)
    ax.tick_params(width=0.6, labelsize=8)


def edge_pt(center, target, radius):
    dx = target[0] - center[0]
    dy = target[1] - center[1]
    d = np.hypot(dx, dy)
    return (center[0] + radius * dx / d, center[1] + radius * dy / d)


# ============================================================
# FIGURE 1: Topology Comparison
# ============================================================
def fig1_topology():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2))

    # --- Left: 1D chain ---
    ax1.set_xlim(-0.8, 12.8)
    ax1.set_ylim(-2.0, 3.0)
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_title('1D Chain (Ungoverned)', fontsize=11, fontweight='bold', pad=12)

    n = 13
    spins = [1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0]
    y0 = 0.5
    r = 0.32

    for i in range(n - 1):
        wall = spins[i] != spins[i + 1]
        if wall:
            ax1.plot([i + r, i + 1 - r], [y0, y0],
                     color=C_WALL, linewidth=2.5, linestyle=(0, (3, 2)), zorder=1)
        else:
            ax1.plot([i + r, i + 1 - r], [y0, y0],
                     color='#AAAAAA', linewidth=1.2, zorder=1)

    for i in range(n):
        fc = C_POST if spins[i] else C_PRE
        c = Circle((i, y0), r, facecolor=fc, edgecolor='#333333', linewidth=1.0, zorder=2)
        ax1.add_patch(c)
        arrow_dy = 0.12 if spins[i] else -0.12
        ax1.annotate('', xy=(i, y0 + arrow_dy + 0.04 * (1 if spins[i] else -1)),
                     xytext=(i, y0 - arrow_dy),
                     arrowprops=dict(arrowstyle='->', color='white', lw=1.3))

    walls = [i + 0.5 for i in range(n - 1) if spins[i] != spins[i + 1]]
    ax1.annotate('domain walls', xy=(walls[2], y0 - 0.35), xytext=(6, -1.2),
                 fontsize=8, ha='center', color=C_WALL, fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color=C_WALL, lw=1))

    ax1.text(6, 2.3,
             'Domain wall cost: O(1)\nEntropy gain: O(log N)\n→ Disorder always wins',
             fontsize=8.5, ha='center', va='center',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF3E0',
                       edgecolor='#E65100', alpha=0.9))

    # --- Right: K3 governance triangle ---
    ax2.set_xlim(-2.5, 2.5)
    ax2.set_ylim(-2.2, 3.0)
    ax2.set_aspect('equal')
    ax2.axis('off')
    ax2.set_title(u'K₃ Governance Topology', fontsize=11, fontweight='bold', pad=12)

    R = 1.5
    verts = {
        'S': (0, R + 0.2),
        'T': (-R * np.cos(np.pi / 6), -R * np.sin(np.pi / 6)),
        'C': (R * np.cos(np.pi / 6), -R * np.sin(np.pi / 6)),
    }
    node_c = {'S': '#2E86C1', 'T': '#28B463', 'C': '#D35400'}
    nr = 0.38

    edges = [('S', 'T'), ('T', 'S'), ('T', 'C'), ('C', 'T'), ('C', 'S'), ('S', 'C')]
    rads = {
        ('S', 'T'): 0.2, ('T', 'S'): 0.2,
        ('T', 'C'): 0.2, ('C', 'T'): 0.2,
        ('C', 'S'): 0.2, ('S', 'C'): 0.2,
    }
    for a, b in edges:
        pa = edge_pt(verts[a], verts[b], nr)
        pb = edge_pt(verts[b], verts[a], nr)
        rad = rads[(a, b)]
        arrow = FancyArrowPatch(pa, pb,
                                connectionstyle=f'arc3,rad={rad}',
                                arrowstyle='->', mutation_scale=14,
                                linewidth=1.5, color='#555555', zorder=1)
        ax2.add_patch(arrow)

    for key, (x, y) in verts.items():
        c = Circle((x, y), nr, facecolor=node_c[key],
                    edgecolor='#333333', linewidth=1.3, zorder=3)
        ax2.add_patch(c)
        ax2.text(x, y, key, fontsize=13, fontweight='bold', ha='center', va='center',
                 color='white', zorder=4)

    ax2.text(verts['S'][0] + 0.8, verts['S'][1] + 0.15, 'Structural\n(Triad)',
             fontsize=8, ha='left', va='center')
    ax2.text(verts['T'][0] - 0.55, verts['T'][1], 'Temporal\n(Memory)',
             fontsize=8, ha='right', va='center')
    ax2.text(verts['C'][0] + 0.55, verts['C'][1], 'Corrective\n(Dignity Net)',
             fontsize=8, ha='left', va='center')

    ax2.annotate('Food set F = {LLM, git, filesystem, protocols}',
                 xy=(0, -1.2), xytext=(0, -1.9),
                 fontsize=7.5, ha='center', color='#555555',
                 arrowprops=dict(arrowstyle='->', color='#999999', lw=1),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#F5F5F5',
                           edgecolor='#CCCCCC'))

    ax2.text(0, 2.65, 'Six catalytic links\n→ Mutual reinforcement sustains order',
             fontsize=8.5, ha='center', va='center',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#E8F5E9',
                       edgecolor='#2E7D32', alpha=0.9))

    fig.tight_layout(pad=2.0)
    path = os.path.join(FIG_DIR, 'fig1-topology.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'  Saved: {path}')


# ============================================================
# FIGURE 2: Timeline
# ============================================================
def fig2_timeline():
    commits = load_aurasys()
    dates = [datetime.strptime(c['timestamp'][:19], '%Y-%m-%d %H:%M:%S') for c in commits]
    time_gaps = np.array([c['time_gap_minutes'] for c in commits], dtype=float)

    fig, ax = plt.subplots(figsize=(10, 3.8))
    style_ax(ax)

    for i in range(len(commits)):
        c = C_PRE if i < BREAK_K else C_POST
        val = max(time_gaps[i], 1)
        ax.scatter(dates[i], val, c=c, s=16, alpha=0.65, edgecolors='none', zorder=3)

    ax.set_yscale('log')
    ax.set_ylim(0.5, 60000)
    ax.set_ylabel('Time gap (minutes)', fontsize=9)
    ax.set_xlabel('Date', fontsize=9)

    triad_date = datetime(2025, 12, 8)
    dn_date = datetime(2026, 2, 13)

    ax.axvline(triad_date, color='#888888', linestyle='--', linewidth=1.0, alpha=0.6, zorder=1)
    ax.axvline(dn_date, color=C_WALL, linestyle='--', linewidth=1.4, zorder=1)

    ax.text(triad_date, 50000, ' Triad installed', fontsize=7.5, ha='left', va='top',
            color='#666666', style='italic')
    ax.text(dn_date, 50000, ' Catalytic closure', fontsize=7.5, ha='left', va='top',
            color=C_WALL, fontweight='bold')

    # Break marker
    break_date = dates[BREAK_K]
    ax.scatter([break_date], [max(time_gaps[BREAK_K], 1)], c='none', s=80,
              edgecolors=C_WALL, linewidths=2, zorder=5, marker='D')

    pre_mean = np.mean(time_gaps[:BREAK_K])
    post_mean = np.mean(time_gaps[BREAK_K:])
    ax.text(dates[2], pre_mean * 1.5, f'Pre-mean: {pre_mean:,.0f} min',
            fontsize=7.5, color=C_PRE, fontweight='bold')
    ax.text(dates[180], post_mean * 0.4, f'Post-mean: {post_mean:,.0f} min',
            fontsize=7.5, color=C_POST, fontweight='bold')

    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor=C_PRE, markersize=6,
               label='Pre-transition (n=20)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=C_POST, markersize=6,
               label='Post-transition (n=280)'),
        Line2D([0], [0], marker='D', color='w', markeredgecolor=C_WALL, markersize=6,
               markerfacecolor='none', markeredgewidth=1.5, label='Detected break'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=7, framealpha=0.9)

    fig.tight_layout()
    path = os.path.join(FIG_DIR, 'fig2-timeline.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'  Saved: {path}')


# ============================================================
# FIGURE 3: Effect Magnitude
# ============================================================
def fig3_effect():
    commits = load_aurasys()

    data = {
        'Time gap\n(minutes)': [c['time_gap_minutes'] for c in commits],
        'Lines\nchanged': [c['lines_changed'] for c in commits],
        'Files\nmodified': [c['file_count'] for c in commits],
    }

    fig, axes = plt.subplots(1, 3, figsize=(9, 4))

    for idx, (label, values) in enumerate(data.items()):
        ax = axes[idx]
        style_ax(ax)

        pre = np.array(values[:BREAK_K], dtype=float)
        post = np.array(values[BREAK_K:], dtype=float)

        bp = ax.boxplot(
            [pre, post], positions=[1, 2], widths=0.55,
            patch_artist=True, showfliers=False,
            medianprops=dict(color='#222222', linewidth=1.5),
            whiskerprops=dict(color='#666666', linewidth=0.8),
            capprops=dict(color='#666666', linewidth=0.8),
        )
        bp['boxes'][0].set(facecolor=C_PRE, alpha=0.7, edgecolor='#333333', linewidth=0.8)
        bp['boxes'][1].set(facecolor=C_POST, alpha=0.7, edgecolor='#333333', linewidth=0.8)

        ax.set_yscale('log')

        pm = np.mean(pre)
        qm = np.mean(post)
        ax.plot(1, pm, 'o', color='white', markersize=5, markeredgecolor=C_PRE,
                markeredgewidth=1.5, zorder=5)
        ax.plot(2, qm, 'o', color='white', markersize=5, markeredgecolor=C_POST,
                markeredgewidth=1.5, zorder=5)
        ax.text(1.35, pm, f'{pm:,.0f}', fontsize=8, ha='left', va='center',
                fontweight='bold', color=C_PRE)
        ax.text(2.35, qm, f'{qm:,.0f}', fontsize=8, ha='left', va='center',
                fontweight='bold', color=C_POST)

        ax.set_xticks([1, 2])
        ax.set_xticklabels(['Pre\n(n=20)', 'Post\n(n=280)'], fontsize=8)
        ax.set_title(label.replace('\n', ' '), fontsize=9, pad=8)

    fig.tight_layout(w_pad=3)
    path = os.path.join(FIG_DIR, 'fig3-effect.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'  Saved: {path}')


# ============================================================
if __name__ == '__main__':
    print('=' * 60)
    print('GENERATING FIGURES — 0361-P10-5')
    print('=' * 60)
    os.makedirs(FIG_DIR, exist_ok=True)

    print('\nFigure 1: Topology comparison...')
    fig1_topology()
    print('Figure 2: Timeline...')
    fig2_timeline()
    print('Figure 3: Effect magnitude...')
    fig3_effect()
    print('\nDone. All figures at:', FIG_DIR)
