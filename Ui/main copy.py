from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase


class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Light"
        return Builder.load_file('drivetrain_screen.kv')

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        pass



if __name__ == '__main__':
    MainApp().run()
