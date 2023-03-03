from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase


class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


class ContentNavigationDrawer(MDBoxLayout):
    pass


class CarScreen(Screen):
    pass


class EngineScreen(Screen):
    pass


class DrivetrainScreen(Screen):
    pass


class TireScreen(Screen):
    pass


class AeroScreen(Screen):
    pass


class ResultsScreen(Screen):
    pass


# Define main app
class AccelerationApproximator(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Light"
        return Builder.load_file('app.kv')


AccelerationApproximator().run()
