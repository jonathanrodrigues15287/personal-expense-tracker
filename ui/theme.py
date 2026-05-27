"""
Centralised design-system for the Expense Tracker UI.

Colours, rounded-rect helpers, and reusable styled widget factories live here
so every screen looks consistent without duplicating canvas code.
"""
from kivy.graphics import Color, RoundedRectangle, Rectangle, Line
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex

# ─── Colour palette ───────────────────────────────────────────────
BG_PRIMARY      = get_color_from_hex("#0B1120")   # deep navy
BG_CARD         = (0.08, 0.12, 0.22, 0.85)        # glass card
BG_CARD_LIGHT   = (0.12, 0.17, 0.28, 0.90)        # lighter card
BG_INPUT        = (0.06, 0.09, 0.18, 1.0)          # input field bg
ACCENT_CYAN     = get_color_from_hex("#00E5CC")
ACCENT_PURPLE   = get_color_from_hex("#7C4DFF")
ACCENT_PINK     = get_color_from_hex("#FF4081")
ACCENT_BLUE     = get_color_from_hex("#448AFF")
ACCENT_ORANGE   = get_color_from_hex("#FF9100")
ACCENT_GREEN    = get_color_from_hex("#00E676")
TEXT_PRIMARY     = (1, 1, 1, 1)
TEXT_SECONDARY   = (0.65, 0.70, 0.80, 1)
TEXT_MUTED       = (0.45, 0.50, 0.60, 1)
DIVIDER          = (1, 1, 1, 0.06)
BORDER_SUBTLE    = (1, 1, 1, 0.08)
NAV_BG           = (0.06, 0.08, 0.14, 0.97)
NAV_ACTIVE       = ACCENT_CYAN
NAV_INACTIVE     = TEXT_MUTED
RADIUS           = dp(14)
RADIUS_SM        = dp(10)


# ─── Canvas helpers ───────────────────────────────────────────────
def _bind_rounded_bg(widget, color, radius=RADIUS):
    """Draw a rounded rectangle behind *widget* that auto-resizes."""
    with widget.canvas.before:
        Color(*color)
        rr = RoundedRectangle(pos=widget.pos, size=widget.size, radius=[radius])
    widget.bind(
        pos=lambda w, v: setattr(rr, 'pos', v),
        size=lambda w, v: setattr(rr, 'size', v),
    )
    return rr


def _bind_border(widget, color=BORDER_SUBTLE, radius=RADIUS, width=1):
    with widget.canvas.after:
        Color(*color)
        ln = Line(
            rounded_rectangle=(*widget.pos, *widget.size, radius),
            width=width,
        )

    def _update(w, _):
        ln.rounded_rectangle = (*w.pos, *w.size, radius)

    widget.bind(pos=_update, size=_update)


# ─── Reusable widgets ────────────────────────────────────────────
def make_card(orientation='vertical', padding=None, spacing=None,
              height=None, bg=BG_CARD, radius=RADIUS):
    """BoxLayout with a rounded glass-card background."""
    pad = padding if padding is not None else (dp(16), dp(12))
    spc = spacing if spacing is not None else dp(8)
    kw = dict(
        orientation=orientation,
        size_hint_y=None,
        spacing=spc,
        padding=pad,
    )
    card = BoxLayout(**kw)
    card.bind(minimum_height=card.setter('height'))
    if height:
        card.height = height
    _bind_rounded_bg(card, bg, radius)
    _bind_border(card, radius=radius)
    return card


def make_section_label(text, color=TEXT_SECONDARY, font_size='13sp'):
    """Small uppercase section heading."""
    lbl = Label(
        text=text.upper(),
        size_hint_y=None,
        height=dp(28),
        font_size=font_size,
        color=color,
        halign='left',
        valign='middle',
        bold=True,
    )
    lbl.bind(size=lbl.setter('text_size'))
    return lbl


def make_value_label(text, font_size='22sp', color=TEXT_PRIMARY, bold=True, height=dp(36)):
    lbl = Label(
        text=text,
        size_hint_y=None,
        height=height,
        font_size=font_size,
        color=color,
        bold=bold,
        halign='left',
        valign='middle',
    )
    lbl.bind(size=lbl.setter('text_size'))
    return lbl


def make_styled_input(hint, text='', input_filter=None):
    """TextInput with dark background, rounded corners, and subtle border."""
    ti = TextInput(
        hint_text=hint,
        text=text,
        size_hint_y=None,
        height=dp(44),
        multiline=False,
        input_filter=input_filter,
        background_color=(0, 0, 0, 0),  # transparent – we draw our own bg
        foreground_color=TEXT_PRIMARY,
        hint_text_color=TEXT_MUTED,
        cursor_color=ACCENT_CYAN,
        padding=(dp(14), dp(10)),
        font_size='14sp',
    )
    _bind_rounded_bg(ti, BG_INPUT, RADIUS_SM)
    _bind_border(ti, color=(1, 1, 1, 0.10), radius=RADIUS_SM)
    return ti


def make_accent_button(text, bg_color=ACCENT_CYAN, text_color=(0, 0, 0, 1)):
    """Flat rounded button with an accent colour fill."""
    btn = Button(
        text=text,
        size_hint_y=None,
        height=dp(48),
        background_normal='',
        background_down='',
        background_color=(0, 0, 0, 0),
        color=text_color,
        bold=True,
        font_size='15sp',
    )
    rr = _bind_rounded_bg(btn, bg_color, RADIUS_SM)

    # Darken on press
    orig = list(bg_color[:3])
    dark = [max(0, c - 0.12) for c in orig]

    def _press(inst):
        rr.source = ''  # force redraw
        with btn.canvas.before:
            Color(*dark, bg_color[3] if len(bg_color) > 3 else 1)
            RoundedRectangle(pos=btn.pos, size=btn.size, radius=[RADIUS_SM])

    def _release(inst):
        btn.canvas.before.clear()
        _bind_rounded_bg(btn, bg_color, RADIUS_SM)

    btn.bind(on_press=_press, on_release=_release)
    return btn


def make_spacer(height=dp(10)):
    return Widget(size_hint_y=None, height=height)


def make_divider():
    w = Widget(size_hint_y=None, height=dp(1))
    with w.canvas:
        Color(*DIVIDER)
        r = Rectangle(pos=w.pos, size=w.size)
    w.bind(
        pos=lambda ww, v: setattr(r, 'pos', v),
        size=lambda ww, v: setattr(r, 'size', v),
    )
    return w
