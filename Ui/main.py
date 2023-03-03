from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
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
        self.dialog = None
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Light"
        return Builder.load_file('app.kv')

    def weight_shifting_turned_off(self, switchObject, switchValue):

        if switchValue:
            self.root.ids.wheelbase_field.visible = True
            self.root.ids.track_width_field.visible = True
            self.root.ids.roll_center_height_field.visible = True
            self.root.ids.roll_stiffness_field.visible = True

        else:
            self.root.ids.wheelbase_field.visible = False
            self.root.ids.track_width_field.visible = False
            self.root.ids.roll_center_height_field.visible = False
            self.root.ids.roll_stiffness_field.visible = False

    def show_weight_shifting_extra_information(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="When a car accelerates, its body wants to stay put due to its inertia. This causes the weight of the car to shift towards the rear, "
                     "which helps increase the grip on the rear wheels. This simulates said phenomena, but needs some hard to get information, thus it is optional.",
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


AccelerationApproximator().run()
