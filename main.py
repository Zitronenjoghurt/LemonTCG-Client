import asyncio
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from src.ui.events.on_keyboard import on_keyboard
from src.ui.interface import UiInterface

class LemonTCGClient(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (1920, 1080)
        Window.bind(on_keyboard=on_keyboard)
        Builder.load_file('src/ui/designs/lemontcgclient.kv')

    def build(self):
        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = 'Purple'
        return UiInterface()

    async def async_run(self, **kwargs):
        await super().async_run(async_lib='asyncio', **kwargs)

    def on_start(self):
        asyncio.create_task(self.task_test())

    async def task_test(self):
        print("Test.")
    
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(LemonTCGClient().async_run())
    loop.close()