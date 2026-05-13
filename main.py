from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from ui.dashboard import Homescreen

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Homescreen(name="home"))
        return sm

MyApp().run()
