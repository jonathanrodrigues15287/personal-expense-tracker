from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

Window.size = (360, 640)

NAV_H = dp(60)
HEADER_H = dp(50)


def make_header(text):
    return Label(
        text=text,
        size_hint=(1, None),          # stretch full width
        height=HEADER_H,
    )


def make_scrollable_content(header_text, screen):
    # BoxLayout stacks header / scroll / nav vertically — no magic coords
    root = BoxLayout(orientation='vertical')

    root.add_widget(make_header(header_text))

    scroll = ScrollView(size_hint=(1, 1))  # takes all remaining space

    inner = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        spacing=dp(2),
        padding=dp(2),
    )
    inner.bind(minimum_height=inner.setter('height'))

    scroll.add_widget(inner)
    root.add_widget(scroll)

    # Nav bar
    nav = BoxLayout(
        orientation='horizontal',
        size_hint=(1, None),
        height=NAV_H,
    )
    home_btn = Button(text="Home")
    nav.add_widget(home_btn)
    root.add_widget(nav)

    return root, inner


class Homescreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout, inner = make_scrollable_content("Home Screen", self)
        for i in range(9):
            inner.add_widget(Button(
                text=f"Button {i+1}",
                size_hint_y=None,
                height=dp(50),
            ))
        self.add_widget(layout)


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Homescreen(name="home"))
        return sm


MyApp().run()