from kivy.lang import Builder
from kivy.properties import ObjectProperty
from math import floor

from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.metrics import dp, sp
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.textfield import MDTextField

KV = '''
MDScreen:

    MDDropdownMenu:
        id: dropdown_menu
        items: ["Item 1", "Item 2", "Item 3"]
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        width: 200
        caller: app.root.ids.text_field

    MDTextField:
        id: text_field
        hint_text: "Selected Item"
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        size_hint_x: None
        width: 200
'''


class TestApp(MDApp):
    dropdown_menu = ObjectProperty()

    def build(self):
        self.root = Builder.load_string(KV)
        self.dropdown_menu = self.root.ids.dropdown_menu
        return self.root

    def on_start(self):
        self.dropdown_menu.menu.bind(on_release=self.print_current_item)

    def print_current_item(self, instance):
        print(f"Current item: {instance.current_item}")


TestApp().run()
