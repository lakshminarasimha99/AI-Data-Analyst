import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# ── Premium dark theme ──────────────────────────────────────────────────────
PALETTE = ['#5B6EF5', '#8B5CF6', '#06B6D4', '#10B981', '#F59E0B', '#F43F5E']

def _apply_dark_style():
    plt.rcParams.update({
        'figure.facecolor':  '#0D1526',
        'axes.facecolor':    '#111D35',
        'axes.edgecolor':    '#334155',
        'axes.labelcolor':   '#A8B8D8',
        'xtick.color':       '#607090',
        'ytick.color':       '#607090',
        'text.color':        '#F1F5FF',
        'grid.color':        '#1E2D47',
        'grid.linestyle':    '--',
        'grid.linewidth':    0.8,
        'axes.grid':         True,
        'font.family':       ['DejaVu Sans'],
        'axes.titlesize':    13,
        'axes.titleweight':  'bold',
        'axes.labelsize':    11,
        'axes.spines.top':   False,
        'axes.spines.right': False,
    })


def analyze_data(filepath):
    df = pd.read_csv(filepath)
    return {
        "shape":    list(df.shape),
        "columns":  list(df.columns),
        "describe": df.describe().to_dict(),
        "missing":  df.isnull().sum().to_dict(),
    }


def generate_charts(filepath):
    df = pd.read_csv(filepath)
    chart_paths = []
    os.makedirs("static", exist_ok=True)
    _apply_dark_style()

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    cat_cols     = df.select_dtypes(include=['object']).columns.tolist()

    # ── 1. Histogram: first numeric column ─────────────────────────────────
    if numeric_cols:
        fig, ax = plt.subplots(figsize=(9, 5))
        col = numeric_cols[0]
        n, bins, patches = ax.hist(
            df[col].dropna(), bins=20,
            color=PALETTE[0], edgecolor='#1E2D47', linewidth=0.6, alpha=0.9
        )
        # gradient colour fill
        for i, patch in enumerate(patches):
            patch.set_facecolor(
                plt.cm.cool(i / max(len(patches) - 1, 1))
            )
        ax.set_title(f'Distribution of {col}', pad=12, color='#F1F5FF')
        ax.set_xlabel(col)
        ax.set_ylabel('Frequency')
        ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
        fig.tight_layout(pad=1.5)
        fig.savefig('static/histogram.png', dpi=140, bbox_inches='tight')
        plt.close(fig)
        chart_paths.append('histogram.png')

    # ── 2. Correlation heatmap (if > 1 numeric) ─────────────────────────────
    if len(numeric_cols) > 1:
        corr = df[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(10, 7))
        mask = None
        cmap = sns.diverging_palette(230, 20, as_cmap=True)
        sns.heatmap(
            corr, ax=ax, cmap=cmap, annot=True, fmt='.2f',
            linewidths=0.5, linecolor='#111D35',
            cbar_kws={'shrink': 0.8, 'pad': 0.02},
            annot_kws={'size': 9, 'color': '#F1F5FF'}
        )
        ax.set_title('Correlation Heatmap', pad=12, color='#F1F5FF')
        ax.tick_params(axis='x', rotation=30)
        ax.tick_params(axis='y', rotation=0)
        fig.tight_layout(pad=1.5)
        fig.savefig('static/heatmap.png', dpi=140, bbox_inches='tight')
        plt.close(fig)
        chart_paths.append('heatmap.png')

    # ── 3. Bar chart: first categorical column ──────────────────────────────
    if cat_cols:
        col = cat_cols[0]
        counts = df[col].value_counts().head(12)
        fig, ax = plt.subplots(figsize=(9, 5))
        bars = ax.bar(
            counts.index, counts.values,
            color=PALETTE[:len(counts)], edgecolor='#1E2D47', linewidth=0.6
        )
        ax.set_title(f'{col} — Top Categories', pad=12, color='#F1F5FF')
        ax.set_xlabel(col)
        ax.set_ylabel('Count')
        ax.tick_params(axis='x', rotation=35)
        for bar, val in zip(bars, counts.values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5,
                str(val),
                ha='center', va='bottom',
                fontsize=8, color='#A8B8D8'
            )
        fig.tight_layout(pad=1.5)
        fig.savefig('static/bar.png', dpi=140, bbox_inches='tight')
        plt.close(fig)
        chart_paths.append('bar.png')

    # ── 4. Line chart: second numeric vs index (trend) ───────────────────────
    if len(numeric_cols) >= 2:
        col = numeric_cols[1]
        fig, ax = plt.subplots(figsize=(9, 5))
        series = df[col].dropna()
        ax.plot(series.index, series.values,
                color=PALETTE[2], linewidth=1.8, alpha=0.9)
        ax.fill_between(series.index, series.values,
                        alpha=0.12, color=PALETTE[2])
        ax.set_title(f'{col} — Trend Over Rows', pad=12, color='#F1F5FF')
        ax.set_xlabel('Row Index')
        ax.set_ylabel(col)
        fig.tight_layout(pad=1.5)
        fig.savefig('static/trend.png', dpi=140, bbox_inches='tight')
        plt.close(fig)
        chart_paths.append('trend.png')

    return chart_paths
