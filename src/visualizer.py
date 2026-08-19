"""
SafeX Sentiment Visualizer
Author: Muhammad Abdullah (AI/ML Group 3)
Generates high quality charts for Sentiment Analysis distribution and reporting.
"""

import os
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def setup_style():
    """Configure modern plot aesthetics."""
    sns.set_theme(style="whitegrid", font="sans-serif")
    plt.rcParams['figure.autolayout'] = True
    plt.rcParams['font.family'] = 'DejaVu Sans'


def plot_sentiment_distribution(df: pd.DataFrame, output_path: str):
    """
    Creates a dual subplot (Pie chart + Count Bar chart) showing sentiment breakdown.
    """
    setup_style()
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
    
    category_counts = df['category'].value_counts()
    colors = {
        'Positive': '#10B981',  # Emerald Green
        'Neutral': '#64748B',   # Slate Grey
        'Negative': '#EF4444'   # Crimson Red
    }
    chart_colors = [colors.get(c, '#3B82F6') for c in category_counts.index]
    
    # 1. Donut / Pie Chart
    wedges, texts, autotexts = axes[0].pie(
        category_counts.values,
        labels=category_counts.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=chart_colors,
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2),
        textprops=dict(color='#1E293B', fontsize=12, weight='bold')
    )
    for at in autotexts:
        at.set_fontsize(11)
        at.set_color('white')
        at.set_weight('bold')
    axes[0].set_title("Sentiment Proportions", fontsize=15, weight='bold', pad=15)

    # 2. Bar Chart
    bars = axes[1].bar(
        category_counts.index,
        category_counts.values,
        color=chart_colors,
        width=0.55,
        edgecolor='#1E293B',
        linewidth=0.8
    )
    axes[1].set_title("Feedback Count by Sentiment Category", fontsize=15, weight='bold', pad=15)
    axes[1].set_ylabel("Total Reviews", fontsize=12, weight='bold')
    axes[1].set_xlabel("Sentiment Category", fontsize=12, weight='bold')
    axes[1].grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add count labels on top of bars
    for bar in bars:
        height = bar.get_height()
        axes[1].annotate(f'{height}',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 4),
                         textcoords="offset points",
                         ha='center', va='bottom',
                         fontsize=12, weight='bold')

    plt.suptitle("SafeX Client Feedback Sentiment Analysis (Week 1)", fontsize=17, weight='heavy', y=1.02)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"[+] Saved sentiment distribution chart to {output_path}")


def plot_service_breakdown(df: pd.DataFrame, output_path: str):
    """
    Creates a stacked bar chart of sentiment by SafeX Service Type.
    """
    setup_style()
    service_sentiment = pd.crosstab(df['service_type'], df['category'])
    
    # Ensure standard column order if present
    cols = [c for c in ['Positive', 'Neutral', 'Negative'] if c in service_sentiment.columns]
    service_sentiment = service_sentiment[cols]
    
    color_map = {'Positive': '#10B981', 'Neutral': '#64748B', 'Negative': '#EF4444'}
    plot_colors = [color_map[c] for c in cols]
    
    fig, ax = plt.subplots(figsize=(13, 7), dpi=300)
    service_sentiment.plot(
        kind='barh',
        stacked=True,
        color=plot_colors,
        ax=ax,
        edgecolor='white',
        linewidth=1
    )
    
    ax.set_title("Sentiment Breakdown Across SafeX Service Offerings", fontsize=15, weight='bold', pad=15)
    ax.set_xlabel("Number of Client Reviews", fontsize=12, weight='bold')
    ax.set_ylabel("Service Line", fontsize=12, weight='bold')
    ax.legend(title="Sentiment", loc='lower right', frameon=True)
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"[+] Saved service breakdown chart to {output_path}")


def plot_polarity_vs_subjectivity(df: pd.DataFrame, output_path: str):
    """
    Creates a scatter plot showing TextBlob Polarity vs Subjectivity.
    """
    setup_style()
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    color_map = {'Positive': '#10B981', 'Neutral': '#64748B', 'Negative': '#EF4444'}
    
    for cat, color in color_map.items():
        subset = df[df['category'] == cat]
        ax.scatter(
            subset['textblob_subjectivity'],
            subset['compound_score'],
            label=f"{cat} ({len(subset)})",
            color=color,
            alpha=0.85,
            s=90,
            edgecolors='#0F172A'
        )
        
    ax.axhline(0.05, color='#10B981', linestyle=':', alpha=0.7)
    ax.axhline(-0.05, color='#EF4444', linestyle=':', alpha=0.7)
    ax.set_title("VADER Compound Score vs. Subjectivity", fontsize=14, weight='bold', pad=15)
    ax.set_xlabel("Subjectivity (0 = Objective, 1 = Subjective)", fontsize=11, weight='bold')
    ax.set_ylabel("VADER Compound Score (-1 to +1)", fontsize=11, weight='bold')
    ax.legend(title="Category", loc="upper left")
    ax.grid(True, linestyle='--', alpha=0.6)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"[+] Saved polarity scatter chart to {output_path}")
