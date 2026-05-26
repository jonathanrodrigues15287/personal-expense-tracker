from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

NAV_H = dp(60)
HEADER_H = dp(50)
H_SCROLL_H = dp(75)

def make_header(text):
    return Label(
        text=text,
        size_hint=(1, None),
        height=HEADER_H,
    )

def make_horizontal_scroll(buttons):
    h_scroll = ScrollView(
        size_hint=(1, None),
        height=H_SCROLL_H,
        do_scroll_x=True,
        do_scroll_y=False,
    )

    h_inner = BoxLayout(
        orientation='horizontal',
        size_hint_x=None,
        height=H_SCROLL_H,
        spacing=dp(8),
        padding=(dp(8), dp(5)),  # dp(5) top+bottom = dp(10) total vertical
    )
    h_inner.bind(minimum_width=h_inner.setter('width'))

    btn_size = H_SCROLL_H - dp(10)  # square: subtract top+bottom padding

    for label in buttons:
        h_inner.add_widget(Button(
            text=label,
            size_hint_x=None,
            width=btn_size,
        ))

    h_scroll.add_widget(h_inner)
    return h_scroll


def make_scrollable_content(title, buttons, screen, show_header=True):
    root = BoxLayout(orientation='vertical')

    if show_header:
        root.add_widget(make_header(title))

    v_scroll = ScrollView(
        size_hint=(1, 1),
        do_scroll_x=False,
        do_scroll_y=True,
    )

    inner = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        spacing=dp(2),
        padding=dp(2),
    )
    inner.bind(minimum_height=inner.setter('height'))

    v_scroll.add_widget(inner)
    root.add_widget(v_scroll)

    nav = BoxLayout(
        orientation='horizontal',
        size_hint=(1, None),
        height=NAV_H,
    )
    nav.add_widget(Button(text="Home"))
    root.add_widget(nav)

    return root, inner, buttons
