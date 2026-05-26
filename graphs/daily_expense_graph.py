import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from core.analytics import daily_spending_trend

plt.style.use('dark_background')
BG_COLOR = '#0c1933'

def plot_daily_expenses():
    daily_data = daily_spending_trend()
    if daily_data.empty:
        return None

    fig = plt.figure(figsize=(12, 5))
    fig.patch.set_facecolor(BG_COLOR)
    ax = plt.gca()
    ax.set_facecolor(BG_COLOR)

    plt.plot(
        daily_data.index,
        daily_data.values,
        marker='o',
        color='#ffaa00',
        linewidth=2
    )

    plt.title("Daily Expense Trend")
    plt.xlabel("Date")
    plt.ylabel("Amount Spent")
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    path = "data/daily_expense.png"
    plt.savefig(path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    return path