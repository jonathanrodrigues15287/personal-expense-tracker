import matplotlib
matplotlib.use('Agg')  # Non-interactive backend, no pop-ups
import matplotlib.pyplot as plt
from core.analytics import category_analysis

plt.style.use('dark_background')
BG_COLOR = '#0c1933'

def plot_category_pie_chart():
    category_data = category_analysis()
    if category_data.empty:
        return None

    fig = plt.figure(figsize=(8, 8))
    fig.patch.set_facecolor(BG_COLOR)
    ax = plt.gca()
    ax.set_facecolor(BG_COLOR)

    plt.plot(
        category_data.index,
        category_data.values,
        marker='o',
        color='#ff55ff',
        linewidth=2
    )

    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    path = "data/category_pie.png"
    plt.savefig(path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    return path

def plot_category_bar_graph():
    category_data = category_analysis()
    if category_data.empty:
        return None

    fig = plt.figure(figsize=(10, 5))
    fig.patch.set_facecolor(BG_COLOR)
    ax = plt.gca()
    ax.set_facecolor(BG_COLOR)

    plt.plot(
        category_data.index,
        category_data.values,
        marker='o',
        color='#55aaff',
        linewidth=2
    )

    plt.title("Category-wise Spending")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    path = "data/category_bar.png"
    plt.savefig(path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    return path
