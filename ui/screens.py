from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from datetime import datetime
import uuid

from ui.widgets import make_scrollable_content
from ui.theme import (
    make_card, make_section_label, make_value_label,
    make_styled_input, make_accent_button, make_spacer, make_divider,
    BG_CARD, BG_CARD_LIGHT,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    ACCENT_CYAN, ACCENT_GREEN, ACCENT_PINK,
    ACCENT_BLUE, ACCENT_ORANGE, ACCENT_PURPLE,
)
from core.analytics import total_spending, highest_expense, total_number_of_expenses
from core.expense_manager import add_expense
from core.budget_manager import save_budget
from core.history_manager import archive_period
from graphs.category_graph import plot_category_line_chart, plot_category_bar_graph
from graphs.spending_graph import plot_monthly_spending
from graphs.daily_expense_graph import plot_daily_expenses


class AnalyticsScreen(Screen):

    def on_enter(self, *args):
        super().on_enter(*args)
        # Refresh stats
        spent = total_spending() or 0
        self.spent_value.text = f"₹{spent:,.2f}"

        num = total_number_of_expenses()
        self.count_value.text = str(num)

        highest = highest_expense()
        if highest is not None:
            self.highest_value.text = (
                f"₹{highest['Amount']:,.2f}  •  {highest['Category']}"
            )
        else:
            self.highest_value.text = "—"

        # Refresh graphs
        for loader, image_widget in [
            (plot_category_line_chart, self.pie_image),
            (plot_category_bar_graph, self.bar_image),
            (plot_monthly_spending, self.spend_image),
            (plot_daily_expenses, self.daily_image),
        ]:
            try:
                path = loader()
                if path:
                    image_widget.source = path
                    image_widget.reload()
            except Exception:
                pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout, inner, _ = make_scrollable_content(
            "Analytics", [], self, show_header=True,
        )

        # Summary card 
        summary = make_card()
        summary.add_widget(make_section_label("Overview"))

        row = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            spacing=dp(8),
        )
        row.height = max(dp(60), self.height * 0.08)
        self.bind(height=lambda _, h: setattr(row, 'height', max(dp(60), h * 0.08)))

        # Spent
        col1 = BoxLayout(orientation='vertical', size_hint_x=1)
        col1.add_widget(make_section_label("Spent", font_size='10sp'))
        self.spent_value = make_value_label(
            "₹0.00", font_size='17sp', color=ACCENT_PINK,
        )
        col1.add_widget(self.spent_value)
        row.add_widget(col1)

        # Count
        col2 = BoxLayout(orientation='vertical', size_hint_x=1)
        col2.add_widget(make_section_label("Count", font_size='10sp'))
        self.count_value = make_value_label(
            "0", font_size='17sp', color=ACCENT_PURPLE,
        )
        col2.add_widget(self.count_value)
        row.add_widget(col2)

        # Highest
        col3 = BoxLayout(orientation='vertical', size_hint_x=1.4)
        col3.add_widget(make_section_label("Highest", font_size='10sp'))
        self.highest_value = make_value_label(
            "—", font_size='13sp', color=ACCENT_ORANGE,
        )
        col3.add_widget(self.highest_value)
        row.add_widget(col3)

        summary.add_widget(row)
        inner.add_widget(summary)

        # Graph cards
        graphs = [
            ("Spending by Category",  "pie_image"),
            ("Category-wise Trend",   "bar_image"),
            ("Monthly Spending Trend", "spend_image"),
            ("Daily Expense Trend",    "daily_image"),
        ]
        for title, attr in graphs:
            card = make_card(padding=(dp(8), dp(8)))
            card.add_widget(make_section_label(title))
            img = Image(size_hint=(1, 1))
            setattr(self, attr, img)
            card.add_widget(img)
            card.height = max(dp(240), self.height * 0.35)
            self.bind(height=lambda _, h, card=card: setattr(card, 'height', max(dp(240), h * 0.35)))
            inner.add_widget(card)

        inner.add_widget(make_spacer(dp(8)))
        self.add_widget(layout)


class ManageScreen(Screen):

    def on_enter(self, *args):
        super().on_enter(*args)
        self.status_label.text = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout, inner, _ = make_scrollable_content(
            "Manage", [], self, show_header=True,
        )

        # Add Expense card 
        exp_card = make_card()
        exp_card.add_widget(make_section_label("New Expense"))

        self.date_input = make_styled_input(
            "Date (YYYY-MM-DD)",
            text=datetime.now().strftime("%Y-%m-%d"),
        )
        exp_card.add_widget(self.date_input)

        self.category_input = make_styled_input("Category (e.g. Food, Transport)")
        exp_card.add_widget(self.category_input)

        self.amount_input = make_styled_input("Amount (e.g. 150.00)", input_filter="float")
        exp_card.add_widget(self.amount_input)

        self.desc_input = make_styled_input("Description")
        exp_card.add_widget(self.desc_input)

        add_btn = make_accent_button("Submit Expense", bg_color=ACCENT_GREEN)
        add_btn.bind(on_release=self._submit_expense)
        exp_card.add_widget(add_btn)

        inner.add_widget(exp_card)

        # Budget card
        bud_card = make_card()
        bud_card.add_widget(make_section_label("Monthly Budget"))

        self.budget_input = make_styled_input(
            "Budget Amount (e.g. 5000.00)", input_filter="float",
        )
        bud_card.add_widget(self.budget_input)

        budget_btn = make_accent_button("Save Budget", bg_color=ACCENT_BLUE)
        budget_btn.bind(on_release=self._save_budget)
        bud_card.add_widget(budget_btn)

        inner.add_widget(bud_card)

        # Archive card
        arc_card = make_card()
        arc_card.add_widget(make_section_label("Archive Period"))

        self.archive_start_input = make_styled_input(
            "Start Date (YYYY-MM-DD)",
            text=datetime.now().replace(day=1).strftime("%Y-%m-%d"),
        )
        arc_card.add_widget(self.archive_start_input)

        self.archive_end_input = make_styled_input(
            "End Date (YYYY-MM-DD)",
            text=datetime.now().strftime("%Y-%m-%d"),
        )
        arc_card.add_widget(self.archive_end_input)

        archive_btn = make_accent_button("Archive Period", bg_color=ACCENT_ORANGE)
        archive_btn.bind(on_release=self._archive_month)
        arc_card.add_widget(archive_btn)

        inner.add_widget(arc_card)

        # Status label      
        self.status_label = Label(
            text="",
            size_hint_y=None,
            font_size='13sp',
            color=ACCENT_GREEN,
            halign='center', valign='middle',
        )
        self.status_label.height = max(dp(36), self.height * 0.05)
        self.bind(height=lambda _, h: setattr(self.status_label, 'height', max(dp(36), h * 0.05)))
        self.status_label.bind(size=self.status_label.setter('text_size'))
        inner.add_widget(self.status_label)

        inner.add_widget(make_spacer(dp(8)))
        self.add_widget(layout)

    # Handlers 
    def _submit_expense(self, instance):
        date = self.date_input.text.strip()
        category = self.category_input.text.strip()
        amount_text = self.amount_input.text.strip()
        desc = self.desc_input.text.strip()

        if not date or not category or not amount_text:
            self.status_label.color = ACCENT_PINK
            self.status_label.text = "Please fill Date, Category, and Amount."
            return

        try:
            amount = float(amount_text)
        except ValueError:
            self.status_label.color = ACCENT_PINK
            self.status_label.text = "Invalid amount."
            return

        expense_id = str(uuid.uuid4())[:8]
        add_expense(expense_id, date, category, amount, desc)

        self.category_input.text = ""
        self.amount_input.text = ""
        self.desc_input.text = ""

        self.status_label.color = ACCENT_GREEN
        self.status_label.text = f"Expense ₹{amount:.2f} added!"

    def _save_budget(self, instance):
        budget_text = self.budget_input.text.strip()
        if not budget_text:
            self.status_label.color = ACCENT_PINK
            self.status_label.text = "Please enter a budget amount."
            return

        try:
            budget = float(budget_text)
        except ValueError:
            self.status_label.color = ACCENT_PINK
            self.status_label.text = "Invalid budget amount."
            return

        month = datetime.now().strftime("%Y-%m")
        save_budget(month, budget)

        self.budget_input.text = ""
        self.status_label.color = ACCENT_GREEN
        self.status_label.text = f"Budget ₹{budget:.2f} saved for {month}!"

    def _archive_month(self, instance):
        start = self.archive_start_input.text.strip() or None
        end = self.archive_end_input.text.strip() or None
        try:
            archive_period(start, end)
            period = f"{start or 'month start'} to {end or 'today'}"
            self.status_label.color = ACCENT_GREEN
            self.status_label.text = f"Archived: {period}"
        except Exception as e:
            self.status_label.color = ACCENT_PINK
            self.status_label.text = f"Archive failed: {e}"
