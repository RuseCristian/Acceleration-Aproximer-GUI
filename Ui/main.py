from math import floor

from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.textfield import MDTextField


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


dialog_text_dictionary = {
    "downforce": "Downforce is a downward force that is generated by the aerodynamic design of a car. This force pushes the car onto the ground, increasing the "
                 "friction between the tires and the road surface, which increases the car's grip. Without downforce, "
                 "the car's grip limit would be significantly lower, and it would be more challenging to accelerate",
    "weight_shifting": "When a car accelerates, its body wants to stay put due to its inertia. This causes the weight of the car to shift towards the rear, "
                       "which helps increase the grip on the rear wheels. This simulates said phenomena, but needs some hard to get information, thus it is optional.",
}


class AccelerationApproximator(MDApp):

    def build(self):
        self.dialog = None
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Dark"
        self.rpm_torque_rows = 0
        Window.size = (1080, 2220)
        return Builder.load_file('aero_screen.kv')

    def show_hide_ui(self, switchObject, switchValue, *args):
        if switchValue:
            for i in args:
                i.visible = True
        else:
            for i in args:
                i.visible = False

    def dialog_information(self, dictionary_entry):
        if not self.dialog:
            self.dialog = MDDialog(
                text=dialog_text_dictionary[dictionary_entry],
                buttons=[
                    MDFlatButton(
                        text="Continue",
                        theme_text_color="Primary",
                        text_color=self.theme_cls.primary_color,
                        on_press=lambda x: self.close_dialog()
                    )
                ],
            )
        self.dialog.open()

    def close_dialog(self):
        self.dialog.dismiss()

    def add_rpm_torque_text_field(self):

        self.rpm_torque_rows += 1
        self.box_layout = MDBoxLayout(orientation='horizontal', size_hint_x=.493, spacing=dp(20), id=f"rpm_torque{self.rpm_torque_rows}_boxlayout")
        self.rpm_text_field = MDTextField(hint_text=f"RPM", mode="fill", size_hint_x=.5, input_filter="float")
        self.torque_text_field = MDTextField(hint_text=f"Torque", mode="fill", size_hint_x=.5, input_filter="float")
        self.box_layout.add_widget(self.rpm_text_field)
        self.box_layout.add_widget(self.torque_text_field)
        self.root.ids.engine_screen_vertical_boxlayout.add_widget(self.box_layout)

    def remove_rpm_torque_text_field(self):
        try:
            if len(self.root.ids.engine_screen_vertical_boxlayout.children) > 5:
                # Get the first child widget and set its size_hint_y to None
                first_child = self.root.ids.engine_screen_vertical_boxlayout.children[0]
                first_child.size_hint_y = None

                # Remove the first child widget
                self.root.ids.engine_screen_vertical_boxlayout.remove_widget(first_child)
                self.rpm_torque_rows -= 1
        except Exception as e:
            print(e)
            pass

    def add_gear_text_fields(self):
        self.remove_gear_text_fields()
        if len(self.root.ids.drivetrain_vertical_boxlayout.children) >= 10:
            for i in range(2, floor(self.root.ids.number_of_gears_slider.value)):
                self.box_layout = MDBoxLayout(orientation='horizontal', size_hint_x=.493, spacing=dp(20), id=f"gear_{i+1}_boxlayout")
                self.gear_textfield = MDTextField(hint_text=f"Gear {i+1} Ratio", mode="fill", size_hint_x=.5, input_filter="float")
                self.box_layout.add_widget(self.gear_textfield)
                self.root.ids.drivetrain_vertical_boxlayout.add_widget(self.box_layout)
        else:
            for i in range(floor(self.root.ids.number_of_gears_slider.value)):
                self.box_layout = MDBoxLayout(orientation='horizontal', size_hint_x=.493, spacing=dp(20), id=f"gear_{i + 1}_boxlayout")
                self.gear_textfield = MDTextField(hint_text=f"Gear {i + 1} Ratio", mode="fill", size_hint_x=.5, input_filter="float")
                self.box_layout.add_widget(self.gear_textfield)
                self.root.ids.drivetrain_vertical_boxlayout.add_widget(self.box_layout)

    def remove_gear_text_fields(self):
        try:
            if len(self.root.ids.drivetrain_vertical_boxlayout.children) > 10:
                while len(self.root.ids.drivetrain_vertical_boxlayout.children) != 10:
                    self.root.ids.drivetrain_vertical_boxlayout.remove_widget(self.root.ids.drivetrain_vertical_boxlayout.children[0])
        except Exception as e:
            print(e)
            pass

AccelerationApproximator().run()
