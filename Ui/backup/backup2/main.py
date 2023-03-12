from math import floor
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.textfield import MDTextField

Builder.load_file("aero_screen.kv")
Builder.load_file("car_info_screen.kv")
Builder.load_file("drivetrain_screen.kv")
Builder.load_file("engine_screen.kv")
#Builder.load_file("info_screen.kv")
Builder.load_file("results_screen.kv")
Builder.load_file("settings_screen.kv")
Builder.load_file("tire_screen.kv")

class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


class ContentNavigationDrawer(MDBoxLayout):
    pass


class SettingsScreen(Screen):
    pass
    # switchTestMode = ObjectProperty(active=True)
    # testModus = BooleanProperty(store.get('mode')['dev'])
    #
    # def save_settings(self):
    #     print(self.switchTestMode.active)
    #     store.put('mode', dev=self.switchTestMode.active)
    #     print("saved settings")
    #


class InfoScreen(Screen):
    pass


class MainScreen(Screen):
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
    "add_gear": "Select the number of gears your car has and input their gear ratios.",
    "downforce": "Downforce is a downward force that is generated by the aerodynamic design of a car. This force pushes the car onto the ground, increasing the "
                 "friction between the tires and the road surface, which increases the car's grip. Without downforce, "
                 "the car's grip limit would be significantly lower, and it would be more challenging to accelerate.",
    "weight_shifting": "When a car accelerates, its body wants to stay put due to its inertia. This causes the weight of the car to shift towards the rear, "
                       "which helps increase the grip on the rear wheels. This simulates said phenomena, but needs some hard to get information, thus it is optional.",
    "car_mass_distribution": "Car mass distribution refers to how the weight of a car is distributed among its 2 axles, front and rear, due to its components, "
                             "such as the engine, chassis, and wheels. A car with more mass on the driven wheels will allow for better acceleration in lower gears. ",
    "car_wheel_base": "The wheelbase of a car represents the distance between the front and rear axles, measured from the geometric center of the wheels. A longer "
                      "wheelbase generally means that the effect of squatting when accelerating is lower.",
    "car_roll_center_height": "Roll center height is a suspension geometry parameter that determines the height of the imaginary point around which a car's body rolls "
                              "or pivots when it is subject to lateral forces. When a car is accelerating in a straight line, the roll center height has no direct "
                              "impact on its behavior. However, it can indirectly affect acceleration performance by influencing weight transfer during launch. A "
                              "higher roll center height can cause more weight transfer to the rear wheels during acceleration, which can improve traction and grip, "
                              "while a lower roll center height can reduce weight transfer and potentially reduce traction and grip.",
    "car_track_width": "Track car width refers to the distance between the left and right wheels of a car on the driven axle.",
    "car_roll_stiffness": "Roll stiffness refers to the car's resistance to body roll or lean during cornering. It is determined by the car's suspension geometry, "
                          "including the spring rates, anti-roll bars, and roll center height. A car with high roll stiffness will resist body roll more, "
                          "improving stability and handling during cornering, while a car with low roll stiffness will experience more body roll, potentially reducing "
                          "grip and stability.",
    "engine_idle_rpm": "Idle RPM (Revolutions Per Minute) is the speed at which a car's engine crankshaft rotates when the engine is in idle or neutral gear and there "
                       "is no load on the engine. In other words, it is the minimum speed at which the engine can operate without stalling.",
    "engine_redline_rpm": "The redline RPM is the maximum engine speed at which an engine can operate without causing damage to its internal components. ",
    "add_rpm_torque_entries": "Add RPM:Torque values for the engine horsepower and torque graphs. In the left field input the RPM and in the right filed input the torque at said "
                              "RPM. RPM entries must be made in an increasing manner. I.e if RPM entry 1 is 3000, RPM entry 2 cannot be 2500.",
    "drivetrain_layout": "A car's layout refers to how its drivetrain is configured to deliver power to the wheels. Rear-wheel drive (RWD) provides better handling but "
                         "can be less practical, front-wheel drive (FWD) provides better traction in slippery conditions, while all-wheel drive (AWD) delivers power to "
                         "all four wheels offers best all around traction, but usually comes with a bigger mass handicap.",
    "drivetrain_loss": "Drivetrain loss is the amount of power lost between the engine and the wheels due to friction and other inefficiencies in the drivetrain. It is "
                       "expressed as a percentage of the engine's total output and can vary between 5% and 15%, depending on the car's make and model and the type of "
                       "transmission and other components used.",
    "drivetrain_shift_time": "Shifting time represents how much time elapses from the moment the the car disengages the driven wheels from the engine, switches to the "
                             "next gear and then fully engages the driven wheels. A skilled driver can do this in about 0.25s in a manual car, while automatic cars can "
                             "do it a lot faster depending on the type of transmission and technologies used, example: Porsche's PDK can up-shift in just a few "
                             "milliseconds.",
    "drivetrain_off_clutch": "Off Clutch Rpm represents the rpm value at which the clutch is fully disengaged ( in starting from a stop conditions )."
                             "\n\nRestraints : Idle RPM < Off Clutch RPM < Redline RPM",
    "drivetrain_gas_level": "Gas Level represents how much the driver is pressing the gas pedal in terms of percentages, where 0 - represents not pressed at all, "
                            "and 1 represents fully pressed. ( in starting from a stop conditions ) If the user inputs a very low gas level ( lower than the minimum "
                            "needed to start moving the car), the program will use the minimum value needed to move the car instead.",
    "drivetrain_final_gear": "The final gear ratio refers to the ratio between the rotational speed of the car's drive shaft and the rotational speed of the wheels. It "
                             "is determined by the ratio between the number of teeth on the ring gear and the pinion gear in the differential. A higher ratio will "
                             "provide more acceleration (provided there is sufficient grip) but lower top speed, while a lower ratio will provide less acceleration but "
                             "higher top speed.",
    "tire_width": "The tire width is the width of the tire's contact patch with the road surface, which can be determined by reading the first three values on the "
                  "tire's sidewall, where the first number represents the tire width in millimeters.",
    "tire_aspect_ratio": "The tire aspect ratio is the height of a tire's sidewall expressed as a percentage of the tire's width, which can be determined by reading "
                         "the second value on the tire's sidewall. The aspect ratio affects the tire's overall diameter, with lower ratios providing a smaller diameter "
                         "and a shorter effective final gear ratio, resulting in faster acceleration, lower top speeds, and higher ratios result in lower acceleration "
                         "but higher top speeds.",
    "tire_wheel_diameter": "Wheel diameter refers to the distance across a wheel at its widest point. A larger wheel diameter can improve top speed but decrease "
                           "acceleration, while a smaller diameter can do the opposite. The tire's sidewall displays three values: width, aspect ratio, and diameter, "
                           "with the diameter being the third number, measured in inches.",
    "tire_friction_coeff": "Tire friction coefficient is the measure of grip between the tire and the road surface. It affects acceleration because a higher "
                           "coefficient of friction means the tire can transfer more force to the road, resulting in faster acceleration. Conversely, "
                           "a lower coefficient of friction means less grip and slower acceleration.",
    "tire_rolling_res_coeff": "Rolling resistance is the force required to keep a tire rolling. It is caused by the deformation of the tire as it rolls and the "
                              "friction between the tire and the road. Rolling resistance affects acceleration because it can act as a drag force, slowing down the "
                              "vehicle and reducing acceleration. Tires with lower rolling resistance require less force to roll and can improve acceleration and fuel "
                              "efficiency.",
    "aero_drag_coeff": "Coefficient of drag is a measure of resistance experienced by an object as it moves through a fluid. Higher values mean more resistance, "
                       "lower efficiency, and reduced acceleration, conversely lower values mean better acceleration.",
    "aero_frontal_area": "Frontal area of a car is the total area of its front surface that faces the direction of motion. It includes the area of the hood, "
                         "windshield, and front side windows. It affects the amount of air resistance the car encounters while moving, with larger frontal areas "
                         "generally leading to higher drag and slower acceleration.",
    "aero_air_density": "Air density is a measure of the mass of air per unit volume. It depends on factors such as temperature, pressure, and humidity. As air density "
                        "increases, the air becomes more resistant to motion, which can reduce acceleration. This is because a denser fluid provides more resistance, "
                        "resulting in greater drag forces acting on an object moving through it.",
    "results_initial_speed": "Initial Speed represents the speed at which the estimation first starts.\n\nRestraints: 0 <= Initial Speed < Final Speed",
    "results_final_speed": "Final Speed represents the speed at which the estimation ends. \n\nRestraints: Initial Speed < Final Speed <= Max Reachable Speed",
}


class AccelerationApproximator(MDApp):

    def build(self):
        self.dialog = None
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Dark"
        self.rpm_torque_rows = 0
        Window.size = (1080, 2220)
        return Builder.load_file('main_ui.kv')

    def show_hide_ui(self, switchObject, switchValue, *args):
        if switchValue:
            for i in args:
                i.visible = True
        else:
            for i in args:
                i.visible = False
        for i in self.root.ids.items():
            print(i)

    def dialog_information(self, dictionary_entry):

        if not self.dialog:
            print(dialog_text_dictionary[dictionary_entry])
            self.dialog = MDDialog(
                text=dialog_text_dictionary[dictionary_entry],
                buttons=[
                    MDFlatButton(
                        text="Continue",
                        theme_text_color="Primary",
                        text_color=self.theme_cls.primary_color,
                        on_press=lambda x: (self.close_dialog(), self.dialog.dismiss(), setattr(self, 'dialog', None))
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
        self.root.ids.enginescreen_1.ids.engine_screen_vertical_boxlayout.add_widget(self.box_layout)

    def remove_rpm_torque_text_field(self):
        try:
            if len(self.root.ids.enginescreen_1.ids.engine_screen_vertical_boxlayout.children) > 6:
                # Get the first child widget and set its size_hint_y to None
                first_child = self.root.ids.enginescreen_1.ids.engine_screen_vertical_boxlayout.children[0]
                first_child.size_hint_y = None

                # Remove the first child widget
                self.root.ids.enginescreen_1.ids.engine_screen_vertical_boxlayout.remove_widget(first_child)
                self.rpm_torque_rows -= 1
        except Exception as e:
            print(e)
            pass

    def add_gear_text_fields(self):
        self.remove_gear_text_fields()
        if len(self.root.ids.drivetrainscreen_1.ids.drivetrain_vertical_boxlayout.children) >= 10:
            for i in range(2, floor(self.root.ids.drivetrainscreen_1.ids.number_of_gears_slider.value)):
                self.box_layout = MDBoxLayout(orientation='horizontal', size_hint_x=.493, spacing=dp(20), id=f"gear_{i + 1}_boxlayout")
                self.gear_textfield = MDTextField(hint_text=f"Gear {i + 1} Ratio", mode="fill", size_hint_x=.5, input_filter="float")
                self.box_layout.add_widget(self.gear_textfield)
                self.root.ids.drivetrainscreen_1.ids.drivetrain_vertical_boxlayout.add_widget(self.box_layout)
        else:
            for i in range(floor(self.root.ids.drivetrainscreen_1.ids.ids.number_of_gears_slider.value)):
                self.box_layout = MDBoxLayout(orientation='horizontal', size_hint_x=.493, spacing=dp(20), id=f"gear_{i + 1}_boxlayout")
                self.gear_textfield = MDTextField(hint_text=f"Gear {i + 1} Ratio", mode="fill", size_hint_x=.5, input_filter="float")
                self.box_layout.add_widget(self.gear_textfield)
                self.root.ids.drivetrainscreen_1.ids.drivetrain_vertical_boxlayout.add_widget(self.box_layout)

    def remove_gear_text_fields(self):
        try:
            if len(self.root.ids.drivetrain_vertical_boxlayout.children) > 10:
                while len(self.root.ids.drivetrain_vertical_boxlayout.children) != 10:
                    self.root.ids.drivetrain_vertical_boxlayout.remove_widget(self.root.ids.drivetrain_vertical_boxlayout.children[0])
        except Exception as e:
            print(e)
            pass


AccelerationApproximator().run()