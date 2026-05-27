from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.metrics import dp

from ui.theme import (
    BG_PRIMARY, NAV_BG, NAV_ACTIVE, NAV_INACTIVE,
    TEXT_PRIMARY, TEXT_SECONDARY, ACCENT_CYAN,
    _bind_rounded_bg, RADIUS_SM, make_spacer,
)

NAV_H = dp(56)
HEADER_H = dp(56)

def make_header(text):
    box = BoxLayout(
        orientation='horizontal',
        size_hint=(1, None),
        height=HEADER_H,
        padding=(dp(16), 0),
    )
    lbl = Label(
        text=text,
        font_size='20sp',
        bold=True,
        color=TEXT_PRIMARY,
        halign='left',
        valign='middle',
    )
    lbl.bind(size=lbl.setter('text_size'))
    box.add_widget(lbl)
    return box

def make_horizontal_scroll(buttons):
    h_scroll = ScrollView(
        size_hint=(1, None), height=dp(75),
        do_scroll_x=True, do_scroll_y=False,
    )
    h_inner = BoxLayout(
        orientation='horizontal', size_hint_x=None,
        height=dp(75), spacing=dp(8), padding=(dp(8), dp(5)),
    )
    h_inner.bind(minimum_width=h_inner.setter('width'))
    for label in buttons:
        h_inner.add_widget(Button(text=label, size_hint_x=None, width=dp(65)))
    h_scroll.add_widget(h_inner)
    return h_scroll

class _NavButton(BoxLayout):
    def __init__(self, icon, label, active=False, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.size_hint = (1, 1)
        col = NAV_ACTIVE if active else NAV_INACTIVE
        self._icon = Label(
            text=icon, font_size='22sp', color=col,
            size_hint_y=0.55, halign='center', valign='bottom',
        )
        self._icon.bind(size=self._icon.setter('text_size'))
        self._label = Label(
            text=label, font_size='10sp', color=col,
            size_hint_y=0.45, halign='center', valign='top',
        )
        self._label.bind(size=self._label.setter('text_size'))
        self.add_widget(self._icon)
        self.add_widget(self._label)

    def set_active(self, active):
        col = NAV_ACTIVE if active else NAV_INACTIVE
        self._icon.color = col
        self._label.color = col


def _make_nav_bar(screen):
    nav = BoxLayout(
        orientation='horizontal',
        size_hint=(1, None),
        height=NAV_H,
        padding=(dp(4), dp(4)),
    )

    with nav.canvas.before:
        Color(*NAV_BG)
        r = Rectangle(pos=nav.pos, size=nav.size)
    nav.bind(
        pos=lambda w, v: setattr(r, 'pos', v),
        size=lambda w, v: setattr(r, 'size', v),
    )

    items = [
        ("\u2302", "Home",      "home"),       
        ("\u2261", "Analytics", "analytics"),  
        ("\u270E", "Manage",    "manage"),      
    ]
    nav_btns = []
    for icon, label, target in items:
        nb = _NavButton(icon, label)
        nav_btns.append((nb, target))

        def _on_touch(instance, touch, tgt=target, btns=nav_btns):
            if instance.collide_point(*touch.pos):
                if screen.manager:
                    screen.manager.current = tgt
                for b, t in btns:
                    b.set_active(t == tgt)
                return True

        nb.bind(on_touch_down=_on_touch)
        nav.add_widget(nb)

    return nav

def make_scrollable_content(title, buttons, screen, show_header=True):
    root = BoxLayout(orientation='vertical')

    if show_header:
        root.add_widget(make_header(title))

    v_scroll = ScrollView(
        size_hint=(1, 1),
        do_scroll_x=False,
        do_scroll_y=True,
        bar_width=dp(3),
        bar_color=(*ACCENT_CYAN[:3], 0.4),
        bar_inactive_color=(*ACCENT_CYAN[:3], 0.1),
    )

    inner = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        spacing=dp(12),
        padding=(dp(14), dp(8)),
    )
    inner.bind(minimum_height=inner.setter('height'))

    v_scroll.add_widget(inner)
    root.add_widget(v_scroll)

    nav = _make_nav_bar(screen)
    root.add_widget(nav)

    return root, inner, buttons
