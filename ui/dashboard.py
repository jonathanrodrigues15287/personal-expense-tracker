from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.metrics import dp

from ui.widgets import (
    make_scrollable_content,
    make_horizontal_scroll
)

class Homescreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        h_buttons = [f"Button {i+1}" for i in range(10)]

        layout, inner, buttons = make_scrollable_content(
            "Home Screen",
            h_buttons,
            self,
            show_header=False
        )

        inner.add_widget(Label(
            text="Welcome",
            size_hint_y=None,
            height=dp(40),
        ))

        inner.add_widget(make_horizontal_scroll(buttons))

        self.add_widget(layout)
