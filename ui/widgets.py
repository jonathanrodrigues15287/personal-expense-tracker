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
    ...
    
def make_scrollable_content(title, buttons, screen, show_header=True):
    ...
