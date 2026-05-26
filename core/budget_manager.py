from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from ui.dashboard import Homescreen
from ui.screens import AnalyticsScreen, ManageScreen
from core.csv_handler import initialize_csv_files

Window.size = (360, 640)
Window.clearcolor = (0.05, 0.1, 0.2, 1)  # Dark blue background

class ExpenseTrackerApp(App):
    def build(self):
        # Ensure CSV files exist before the app tries to read them
        initialize_csv_files()
        
        sm = ScreenManager()
        sm.add_widget(Homescreen(name="home"))
        sm.add_widget(AnalyticsScreen(name="analytics"))
        sm.add_widget(ManageScreen(name="manage"))
        return sm

if __name__ == "__main__":
    ExpenseTrackerApp().run()
