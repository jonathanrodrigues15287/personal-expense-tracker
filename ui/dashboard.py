from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.metrics import dp

from ui.widgets import make_scrollable_content, make_horizontal_scroll
from ui.theme import (
    make_card, make_section_label, make_value_label, make_spacer,
    make_divider,
    BG_CARD, BG_CARD_LIGHT,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    ACCENT_CYAN, ACCENT_GREEN, ACCENT_PINK, ACCENT_PURPLE,
)
from core.budget_manager import calculate_balance
from core.analytics import total_spending, total_number_of_expenses


class Homescreen(Screen):
    # Refresh data on every visit 
    def on_enter(self, *args):
        super().on_enter(*args)
        balance = calculate_balance()
        spent = total_spending() or 0
        count = total_number_of_expenses()

        self.balance_value.text = f"₹{balance:,.2f}"
        self.spent_value.text = f"₹{spent:,.2f}"
        self.count_value.text = str(count)

        # colour-code balance
        if balance >= 0:
            self.balance_value.color = ACCENT_GREEN
        else:
            self.balance_value.color = ACCENT_PINK

    #  Build UI 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout, inner, _ = make_scrollable_content(
            "Dashboard", [], self, show_header=True,
        )

        # Greeting 
        greeting = Label(
            text="Welcome back!",
            size_hint_y=None,
            font_size='14sp', color=TEXT_MUTED,
            halign='left', valign='middle',
        )
        greeting.height = max(dp(30), self.height * 0.05)
        self.bind(height=lambda _, h: setattr(greeting, 'height', max(dp(30), h * 0.05)))
        greeting.bind(size=greeting.setter('text_size'))
        inner.add_widget(greeting)

        # Balance card 
        card_balance = make_card()

        card_balance.add_widget(make_section_label("Current Balance"))
        self.balance_value = make_value_label("₹0.00", font_size='28sp', color=ACCENT_GREEN)
        card_balance.add_widget(self.balance_value)

        inner.add_widget(card_balance)

        #  Stats row (two mini cards)
        row = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            spacing=dp(10),
        )
        row.height = max(dp(100), self.height * 0.15)
        self.bind(height=lambda _, h: setattr(row, 'height', max(dp(100), h * 0.15)))

        # Total Spent mini-card
        c_spent = make_card(bg=BG_CARD_LIGHT)
        c_spent.add_widget(make_section_label("Total Spent", font_size='11sp'))
        self.spent_value = make_value_label("₹0.00", font_size='20sp', color=ACCENT_PINK)
        c_spent.add_widget(self.spent_value)
        row.add_widget(c_spent)

        # Count mini-card
        c_count = make_card(bg=BG_CARD_LIGHT)
        c_count.add_widget(make_section_label("Expenses", font_size='11sp'))
        self.count_value = make_value_label("0", font_size='20sp', color=ACCENT_PURPLE)
        c_count.add_widget(self.count_value)
        row.add_widget(c_count)

        inner.add_widget(row)

        # Quick tip card 
        tip_card = make_card(bg=(0.05, 0.08, 0.16, 0.7))
        tip_label = Label(
            text="Tip: Head to [b]Manage[/b] to add expenses and set your monthly budget.",
            markup=True,
            size_hint_y=None,
            font_size='12sp',
            color=TEXT_MUTED,
            halign='left', valign='middle',
        )
        tip_label.height = max(dp(44), self.height * 0.07)
        self.bind(height=lambda _, h: setattr(tip_label, 'height', max(dp(44), h * 0.07)))
        tip_label.bind(size=tip_label.setter('text_size'))
        tip_card.add_widget(tip_label)
        inner.add_widget(tip_card)

        #  Bottom spacer 
        inner.add_widget(make_spacer(dp(8)))

        self.add_widget(layout)
