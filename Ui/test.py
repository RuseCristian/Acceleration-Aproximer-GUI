from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty


class MainScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class InfoScreen(Screen):
    pass


class TabbedScreen(Screen):
    tab_content = ObjectProperty()

    def on_pre_enter(self):
        # Bind the button to the get_tab_data method
        self.ids.get_data_button.bind(on_press=self.get_tab_data)

    def get_tab_data(self, *args):
        data = {}
        for tab in self.tab_content.tab_list:
            for child in tab.content.children:
                if hasattr(child, "text"):
                    data.setdefault(tab.text, {})[child.id] = child.text
        print(data)


class MyApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(SettingsScreen(name="settings"))
        sm.add_widget(InfoScreen(name="info"))
        sm.add_widget(TabbedScreen(name="tabbed"))
        return sm

    def get_tab_data(self, *args):
        # Get the current screen and call its get_tab_data method
        screen = self.root.current_screen
        if isinstance(screen, TabbedScreen):
            screen.get_tab_data()


if __name__ == "__main__":
    MyApp().run()
