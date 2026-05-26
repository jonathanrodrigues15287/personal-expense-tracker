import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from core.analytics import monthly_summary

plt.style.use('dark_background')
BG_COLOR = '#0c1933'

def plot_monthly_spending():
    monthly_data = monthly_summary()
    if monthly_data.empty:
        return None

    fig = plt.figure(figsize=(10, 5))
    fig.patch.set_facecolor(BG_COLOR)
    ax = plt.gca()
    ax.set_facecolor(BG_COLOR)
    
    plt.plot(
        monthly_data.index,
        monthly_data.values,
        marker='o',
        color='#00ffcc',
        linewidth=2
    )

    plt.title("Monthly Spending Trend")
    plt.xlabel("Month")
    plt.ylabel("Amount Spent")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    path = "data/monthly_spending.png"
    plt.savefig(path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    return path