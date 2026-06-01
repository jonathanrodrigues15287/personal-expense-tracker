import matplotlib
matplotlib.use('Agg')  # Non-interactive backend, no pop-ups
import matplotlib.pyplot as plt
from core.analytics import category_analysis

plt.style.use('dark_background')
BG_COLOR = '#0c1933'

def plot_category_line_chart():
    category_data = category_analysis()
    if category_data.empty:
        return None

    # Sort ascending so the line trends upward
    category_data = category_data.sort_values(ascending=True)

    fig = plt.figure(figsize=(10, 5))
    fig.patch.set_facecolor(BG_COLOR)
    ax = plt.gca()
    ax.set_facecolor(BG_COLOR)

    ax.plot(
        category_data.index,
        category_data.values,
        marker='o',
        color='#ff6699',
        linewidth=2,
        markersize=8,
    )

    # Fill area under the line for visual appeal
    ax.fill_between(
        range(len(category_data)),
        category_data.values,
        alpha=0.15,
        color='#ff6699',
    )
    ax.set_xticks(range(len(category_data)))
    ax.set_xticklabels(category_data.index, rotation=45, ha='right')

    plt.title("Spending by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    path = "data/category_pie.png"
    plt.savefig(path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    return path

def plot_category_bar_graph():
    """Line plot of category-wise spending (sorted descending)."""
    category_data = category_analysis()
    if category_data.empty:
        return None

    # Sort descending so highest-spend category comes first
    category_data = category_data.sort_values(ascending=False)

    fig = plt.figure(figsize=(10, 5))
    fig.patch.set_facecolor(BG_COLOR)
    ax = plt.gca()
    ax.set_facecolor(BG_COLOR)

    ax.plot(
        category_data.index,
        category_data.values,
        marker='s',
        color='#55aaff',
        linewidth=2,
        markersize=8,
    )

    ax.fill_between(
        range(len(category_data)),
        category_data.values,
        alpha=0.15,
        color='#55aaff',
    )
    ax.set_xticks(range(len(category_data)))
    ax.set_xticklabels(category_data.index, rotation=45, ha='right')

    plt.title("Category-wise Spending")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    path = "data/category_bar.png"
    plt.savefig(path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    return path
