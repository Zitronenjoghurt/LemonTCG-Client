from kivy.uix.screenmanager import ScreenManager
from src.ui.screens.main_menu import MainMenuScreen

class UiInterface(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_menu = MainMenuScreen(name='main_menu')
        self.add_widget(self.main_menu)
        self.current = "main_menu"