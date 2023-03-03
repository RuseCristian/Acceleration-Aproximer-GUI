import os
from kivy.core.window import Window
from kaki.app import App
from manager_screens import ManagerScreens


class Live(App):
    KV_FILES = {
        os.path.join(os.getcwd(), "manager_screens.kv")
    }

    CLASSES = {"ManagerScreens": "manager_screens"

               }

    AUTORELOADER_PATHS = [(".", {"recursive": True}), ]

    def build_app(self):
        Window.bind(on_reyboard=self._rebuild)
        self.manager_screens = ManagerScreens()
        return self.manager_screens

    def _rebuild(self, *args):
        if args[1] == 32:
            self.rebuild()


Live().run()
