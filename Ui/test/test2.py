from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivymd.uix.picker import MDColorPicker


class ColorPickerScreen(Screen):
    primary_color = ObjectProperty(None)
    accent_color = ObjectProperty(None)
    allowed_colors = ["Red", "Pink", "Purple", "DeepPurple", "Indigo", "Blue",
                      "LightBlue", "Cyan", "Teal", "Green", "LightGreen", "Lime",
                      "Yellow", "Amber", "Orange", "DeepOrange", "Brown", "Gray",
                      "BlueGray"]

    def show_primary_color_picker(self):
        picker = MDColorPicker()
        picker.primary_color = self.primary_color.text
        picker.allow_custom_color = False
        picker.color = picker.primary_color
        picker.open(callback=self.set_primary_color)

    def show_accent_color_picker(self):
        picker = MDColorPicker()
        picker.primary_color = self.accent_color.text
        picker.allow_custom_color = False
        picker.color = picker.primary_color
        picker.open(callback=self.set_accent_color)

    def set_primary_color(self, instance):
        self.primary_color.text = instance.color

    def set_accent_color(self, instance):
        self.accent_color.text = instance.color


class PaletteSelectorApp(MDApp):
    def build(self):
        screen = ColorPickerScreen()
        screen.allowed_colors = ["Red", "Pink", "Purple", "DeepPurple", "Indigo", "Blue",
                                 "LightBlue", "Cyan", "Teal", "Green", "LightGreen", "Lime",
                                 "Yellow", "Amber", "Orange", "DeepOrange", "Brown", "Gray",
                                 "BlueGray"]
        return screen


if __name__ == "__main__":
    PaletteSelectorApp().run()
