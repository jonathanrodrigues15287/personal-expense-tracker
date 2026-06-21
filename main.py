from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, SlideTransition

from ui.dashboard import Homescreen
from ui.screens import AnalyticsScreen, ManageScreen
from core.db_handler import initialize_database

from kivy.utils import platform

if platform not in ('android', 'ios'):
    Window.size = (380, 680)
Window.clearcolor = (0.043, 0.067, 0.126, 1)


class ExpenseTrackerApp(App):
    def build(self):
        self.title = "Expense Tracker"
        initialize_database()

        sm = ScreenManager(transition=SlideTransition(duration=0.25))
        sm.add_widget(Homescreen(name="home"))
        sm.add_widget(AnalyticsScreen(name="analytics"))
        sm.add_widget(ManageScreen(name="manage"))
        return sm


if __name__ == "__main__":
    ExpenseTrackerApp().run()
