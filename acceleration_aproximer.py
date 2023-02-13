import time
import tkinter as tk
from datetime import datetime
from tkinter import filedialog as fd, filedialog
import configparser
import numpy as np
from plotly.subplots import make_subplots
from scipy.interpolate import interp1d
import plotly.graph_objects as go


class INIEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.torque_text_box = None
        self.current_time = None
        self.datafile = None
        self.final_speed_entry = None
        self.initial_speed_entry = None
        self.car_downforce_distribution_entry = None
        self.tire_width_entry = None
        self.tire_aspect_entry = None
        self.tire_radial_entry = None
        self.tire_rolling_k_entry = None
        self.tire_mu_entry = None
        self.shifting_time_entry = None
        self.off_clutch_entry = None
        self.clutch_bite_entry = None
        self.gas_level_entry = None
        self.drivetrain_loss_entry = None
        self.layout_entry = None
        self.redline_entry = None
        self.idle_rpm_entry = None
        self.car_name_entry = None
        self.car_mass_entry = None
        self.front_weight_distribution_entry = None
        self.car_cd_entry = None
        self.car_frontal_area_entry = None
        self.car_air_density_entry = None
        self.car_lift_coefficient_entry = None
        self.car_downforce_total_area_entry = None
        self.final_drive_entry = None
        self.console = None

        self.title("Accelerator Approximate")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Create and set variables for each field
        self.drivetrain_gears = []

        # Create labels and entry widgets for each field
        self.create_torque_curve_section()
        self.create_engine_section()
        self.create_drivetrain_gears_section()
        self.create_drivetrain_section()
        self.create_tire_section()
        self.create_car_section()
        self.create_bottom_buttons()
        self.create_console_section()

    def check_data(self, export_to_file=False):
        self.append_text("Started Checking If All Fields Have The Needed Data.")

        # for idx, element in enumerate(self.torque_curve):
        #     if idx <= 1:
        #         if not self.check_if_int_or_float(element.get()):
        #             return
        #     else:
        #         if not self.check_if_int_or_float(element.get(), True):
        #             return
        rpm_to_torque_aux = self.torque_text_box.get("1.0", "end-1c")

        aux_rpm = 0
        for element in rpm_to_torque_aux.splitlines():
            if element != "":
                splitted_string = element.split('=')
                if len(splitted_string) != 2 or not self.check_if_int_or_float(
                        splitted_string[1]) or not self.check_if_int_or_float(splitted_string[0]):
                    return
                if aux_rpm >= int(splitted_string[0]):
                    return
                aux_rpm = int(splitted_string[0])

        for idx, element in enumerate(self.drivetrain_gears):
            if idx == 0:
                if not self.check_if_int_or_float(element.get()):
                    return
            else:
                if not self.check_if_int_or_float(element.get(), True):
                    return

        if not self.check_if_int_or_float(self.final_drive_entry.get()):
            return

        if len(self.car_name_entry.get()) == 0:
            return

        if not self.check_if_int_or_float(self.car_mass_entry.get()):
            return

        if not self.check_if_int_or_float(self.front_weight_distribution_entry.get()):
            return

        if not self.check_if_int_or_float(self.car_cd_entry.get()):
            return

        if not self.check_if_int_or_float(self.car_frontal_area_entry.get()):
            return

        if not self.check_if_int_or_float(self.car_lift_coefficient_entry.get()):
            return

        if not self.check_if_int_or_float(self.car_lift_coefficient_entry.get(), True):
            return

        if not self.check_if_int_or_float(self.car_downforce_total_area_entry.get(), True):
            return

        if not self.check_if_int_or_float(self.car_downforce_distribution_entry.get(), True):
            return

        if not self.check_if_int_or_float(self.idle_rpm_entry.get()):
            return

        if not self.check_if_int_or_float(self.redline_entry.get()):
            return

        if len(self.layout_entry.get()) == 0:
            return

        if not self.check_if_int_or_float(self.drivetrain_loss_entry.get(), True):
            return

        if not self.check_if_int_or_float(self.shifting_time_entry.get()):
            return

        if not self.check_if_int_or_float(self.off_clutch_entry.get()):
            return

        if not self.check_if_int_or_float(self.clutch_bite_entry.get()):
            return

        if not self.check_if_int_or_float(self.gas_level_entry.get()):
            return

        if not self.check_if_int_or_float(self.tire_width_entry.get()):
            return

        if not self.check_if_int_or_float(self.tire_aspect_entry.get()):
            return

        if not self.check_if_int_or_float(self.tire_radial_entry.get()):
            return

        if not self.check_if_int_or_float(self.tire_mu_entry.get()):
            return

        if not self.check_if_int_or_float(self.tire_rolling_k_entry.get()):
            return
        if not export_to_file:
            if not self.check_if_int_or_float(self.initial_speed_entry.get()):
                return

            if not self.check_if_int_or_float(self.final_speed_entry.get()):
                return

        self.append_text("All Fields Have The Needed Data.")
        return True

    def start_approximation_func(self):

        if not self.check_data():
            return

        def estimate_weight_shift(acceleration_value, wheelbase, track_width, roll_center_height, roll_stiffness):

            # Compute the roll angle caused by the weight shift
            roll_angle = acceleration_value * wheelbase / (2 * roll_stiffness)

            # Compute the weight shift as a fraction of the track width
            weight_shift = roll_angle * track_width / 2 * roll_center_height

            return weight_shift

        def find_accel_from_speed(speed, speed_values, accel_values):
            # acceleration is stored on an index based on the rpm, but because gears have different gear ratios
            # in each gear you will have different rpm at the same speed, this function, returns the acceleration value of the next gear
            # at the current speed
            rpm = np.searchsorted(speed_values, speed)
            return accel_values[rpm]

        def find_optimum_upshift_point(gears_data):
            optimum_shift_points = []

            for i in range(len(gears_data) - 1):
                current_gear_acceleration = gears_data[i].accel

                next_gear_acceleration = []
                for j in range(len(current_gear_acceleration)):
                    if j >= len(gears_data[i + 1].accel):
                        break
                    next_gear_acceleration.append(find_accel_from_speed(gears_data[i].speed[j], gears_data[i + 1].speed, gears_data[i + 1].accel))
                next_gear_acceleration = np.array(next_gear_acceleration)

                for index, j in enumerate(range(min(len(current_gear_acceleration), len(next_gear_acceleration)))):
                    if current_gear_acceleration[j] < next_gear_acceleration[j]:
                        optimum_shift_points.append(index)
                else:
                    optimum_shift_points.append(len(current_gear_acceleration))

            return optimum_shift_points

        def find_starting_parameters(speed_value):
            for i in range(0, number_of_gears):
                idx = np.searchsorted(gears[i].speed, speed_value, side='right')
                if idx < len(gears[i].speed):
                    gear_value = i
                    rpm_value = idx
                    break
            return gear_value, rpm_value

        fig = make_subplots(rows=2, cols=3)
        # target speeds
        initial_speed_kmh = int(self.initial_speed_entry.get())
        final_speed_kmh = int(self.final_speed_entry.get())

        # drivetrain info
        drivetrain_loss_percentage = float(self.drivetrain_loss_entry.get())
        layout = self.layout_entry.get()
        shift_time_s = float(self.shifting_time_entry.get())
        off_clutch = float(self.off_clutch_entry.get())
        clutch_bite = float(self.clutch_bite_entry.get())
        gas_level = float(self.gas_level_entry.get())
        idle_rpm = int(self.idle_rpm_entry.get())
        redline_rpm = int(self.redline_entry.get())

        # tire data
        tire_width = float(self.tire_width_entry.get())
        tire_aspect = float(self.tire_aspect_entry.get())
        tire_radial = float(self.tire_radial_entry.get())
        tire_mu = float(self.tire_mu_entry.get())
        rolling_k = float(self.tire_rolling_k_entry.get())

        # general car data
        car_name = self.car_name_entry.get()
        car_mass = float(self.car_mass_entry.get())
        front_weight_distribution = float(self.front_weight_distribution_entry.get())
        cd_car = float(self.car_cd_entry.get())
        frontal_area = float(self.car_frontal_area_entry.get())
        air_density = float(self.car_air_density_entry.get())
        lift_coefficient = float(self.car_lift_coefficient_entry.get())
        downforce_total_area = float(self.car_downforce_total_area_entry.get())
        downforce_distribution = float(self.car_downforce_distribution_entry.get())

        # gravitational acceleration m/s^2
        g = 9.81

        # transforming from km/h to m/s (SI units)
        initial_speed_ms = initial_speed_kmh / 3.6
        final_speed_ms = final_speed_kmh / 3.6

        # tire diameter in inch
        tire_diameter = (tire_width * tire_aspect * 2) / 25.4 + tire_radial

        # tire radius in meters (diameter in inch divided by 2 to get the radius)
        tire_radius = tire_diameter / 39.37 / 2

        # engine curves
        rpm_curve = np.array([])
        horsepower_curve = np.array([])
        torque_curve = np.array([])
        rpm_to_torque_aux = self.torque_text_box.get("1.0", "end-1c")

        # index 0 is rpm, index 1 is torque at that rpm
        for element in rpm_to_torque_aux.splitlines():
            rpm_torque = element.split("=")
            rpm_curve = np.append(rpm_curve, (int(rpm_torque[0])))
            torque_curve = np.append(torque_curve, (int((rpm_torque[1]))))

        # data interpolation
        max_rpm = int(rpm_curve[len(rpm_curve) - 1])
        torque_curve = [x * (1 - drivetrain_loss_percentage / 100) for x in torque_curve]
        rpm_torque_interpolation = interp1d(rpm_curve, torque_curve, kind="cubic")
        rpm_curve = np.linspace(np.min(rpm_curve), np.max(rpm_curve), max_rpm - idle_rpm)
        torque_curve = rpm_torque_interpolation(rpm_curve)[:redline_rpm + 1]
        horsepower_curve = np.array([int(torque * rpm / 7127) for torque, rpm in zip(torque_curve, rpm_curve)])
        rpm_torque_interpolation = interp1d(rpm_curve, torque_curve, kind="cubic")
        torque_curve = rpm_torque_interpolation(rpm_curve)[:redline_rpm + 1]
        horsepower_interpolation = interp1d(rpm_curve, horsepower_curve, kind="cubic")
        horsepower_curve = horsepower_interpolation(rpm_curve)[:redline_rpm + 1]

        # gear ratios
        gear_ratios = []
        for element in self.drivetrain_gears:
            if element.get() != "":
                gear_ratios.append(float(element.get()))
        gear_ratios.append(float(self.final_drive_entry.get()))
        number_of_gears = len(gear_ratios) - 1

        # limit of adhesion of tires in terms of max allowed force before entering dynamic friction
        if layout == "rwd":
            max_tractive_force = g * car_mass * (1 - front_weight_distribution) * tire_mu
        elif layout == "fwd":
            max_tractive_force = g * car_mass * front_weight_distribution * tire_mu

        class Gear:
            def __init__(self, ratio, accel, rpm, speed, torque_at_the_wheels, air_resistance_curve, downforce_curve):
                self.dropdown_rpm = None
                self.max_speed = None
                self.optimum_upshift = None
                self.ratio = ratio
                self.accel = accel
                self.rpm = rpm
                self.speed = speed
                self.torque_at_the_wheels = torque_at_the_wheels
                self.air_resistance = air_resistance_curve
                self.downforce_curve = downforce_curve

            def add_optimum_upshift(self, value):
                self.optimum_upshift = value
                self.max_speed = self.speed[min(value, len(self.accel) - 1)]

            def add_dropdown_rpm(self, value):
                self.dropdown_rpm = value

        # calculating relevant gear information
        gears = []
        for i in range(0, number_of_gears):

            # maximum speed at each rpm for specified gear, in m/s
            specific_speed = np.array([(x * tire_diameter) / (gear_ratios[i] * gear_ratios[len(gear_ratios) - 1] * 336) * 1.609 / 3.6 for x in rpm_curve])

            # air resistance in relation to speed, in Newtons
            air_resistance_curve = np.array([(cd_car * frontal_area * air_density * (x ** 2)) / 2 for x in specific_speed])

            # downforce in relation to speed, in Newtons
            downforce_curve = np.array([(lift_coefficient * downforce_total_area * air_density * (x ** 2)) / 2 for x in specific_speed])

            # torque at the wheels in Nm
            torque_at_the_wheels = np.array([x * gear_ratios[i] * gear_ratios[len(gear_ratios) - 1] for x in torque_curve])

            acceleration = np.array([])
            for index in range(0, len(torque_curve) - 1):
                if layout == 'fwd':
                    acceleration_at_specific_rpm = (min((max_tractive_force + downforce_curve[index] * downforce_distribution) * tire_mu,
                                                        torque_at_the_wheels[index] / tire_radius) - air_resistance_curve[index] - rolling_k * g * car_mass) / car_mass
                else:
                    acceleration_at_specific_rpm = (min((max_tractive_force + downforce_curve[index] * (1 - downforce_distribution)) * tire_mu,
                                                        torque_at_the_wheels[index] / tire_radius) - air_resistance_curve[index] - rolling_k * g * car_mass) / car_mass
                if acceleration_at_specific_rpm > 0:
                    acceleration = np.append(acceleration, acceleration_at_specific_rpm)

            # putting together all the info
            gear_info = Gear(gear_ratios[i], acceleration, rpm_curve, specific_speed, torque_at_the_wheels, air_resistance_curve,
                             downforce_curve)
            gears.append(gear_info)

        # finding the optimum upshift shift points for each gear
        optimum_upshift = find_optimum_upshift_point(gears)
        for i in range(len(gears) - 1):
            gears[i].add_optimum_upshift(optimum_upshift[i])

        # calculating gear rpm dropdown when upshifting
        for i in range(len(gears) - 2):
            gears[i].add_dropdown_rpm(np.searchsorted(gears[i + 1].speed, gears[i].max_speed))

        # finding initial starting parameters
        current_speed_ms = initial_speed_ms
        current_gear, current_rpm = find_starting_parameters(current_speed_ms)

        total_time = 0
        while current_speed_ms <= final_speed_ms and current_rpm != -1 and current_gear != -1:
            # upshift
            if current_rpm == optimum_upshift[current_gear]:
                total_time += shift_time_s
                current_rpm = gears[current_gear].dropdown_rpm
                current_gear += 1
            # accelerating
            try:
                if current_rpm != idle_rpm:
                    total_time = total_time + ((gears[current_gear].speed[current_rpm] - gears[current_gear].speed[current_rpm - 1]) / gears[current_gear].accel[current_rpm])
                else:
                    total_time = (gears[current_gear].speed[current_rpm] / gears[current_gear].accel[current_rpm])
                current_speed_ms = gears[current_gear].speed[current_rpm]
            except:
                pass
            current_rpm += 1

        for i in range(len(gears)):
            fig.add_trace(
                go.Scatter(x=gears[i].speed*3.6, y=gears[i].torque_at_the_wheels,
                           name="Gear {}".format(i + 1)
                           ), row=2, col=2
            )
            # torque vs speed in each gear (max potential speed)

            fig.add_trace(
                go.Scatter(x=gears[i].speed*3.6, y=gears[i].accel/g,
                           name="Gear {}".format(i + 1)
                           ), row=1, col=2
            )
            # acceleration vs speed graph
        self.append_text("", False)
        self.append_text("-----------------------------------RESULTS-------------------------------------", False)
        self.append_text("", False)
        for i in range(0, number_of_gears - 1):
            self.append_text(f"Gear {i + 1} Optimum Upshift - {gears[i].optimum_upshift + 1 + idle_rpm} RPM", False)
        self.append_text("", False)
        self.append_text("-------------------------------------------------------------------------------", False)
        self.append_text(f"{initial_speed_kmh} - {final_speed_kmh} km/h in {round(total_time, 3)} seconds", False)
        self.append_text("", False)
        fig.update_layout(showlegend=False)
        fig.show()

    def check_if_int_or_float(self, number, optional_flag=False):
        if not optional_flag:
            try:
                if len(number) != 0:
                    number = float(number)
                    return True
                self.append_text("There is an empty field!")
                return False
            except:
                self.append_text(f"The field that has the input '{number}' is not a number!")
                return False
        else:
            if len(number) == 0:
                return True
            else:
                try:
                    number = float(number)
                    return True
                except:
                    self.append_text(f"The field that has the input '{number}' is not a number!")
                    return False

    def update_text(self, textbox, new_text=''):
        textbox.delete("0", 'end')  # Delete the current contents of the Text widget
        textbox.insert('insert', new_text)  # Insert the new text

    def update_text2(self, textbox, new_text=''):
        # textbox.delete("0.0", 'end')  # Delete the current contents of the Text widget
        textbox.insert('insert', new_text + "\n")  # Insert the new text

    def import_data_set_func(self):

        def is_number(string):
            try:
                float(string)
                return True
            except ValueError:
                return False

        filetypes = (
            ('ini', '*.ini'),
        )
        self.datafile = fd.askopenfilename(
            title='Load Car Data',
            initialdir='/',
            filetypes=filetypes)

        config = configparser.ConfigParser()
        config.read(self.datafile)

        expected_keys = [
            {'section': 'torque_curve', 'options': ['1000', '2000']},
            {'section': 'engine', 'options': ['idle_rpm', 'redline']},
            {'section': 'drivetrain_gears', 'options': ['gear1', 'gear2', 'final_drive']},
            {'section': 'drivetrain',
             'options': ['layout', 'shifting_time', 'off_clutch', 'clutch_bite', 'gas_level']},
            {'section': 'tire', 'options': ['tire_width', 'tire_aspect', 'tire_radial', 'tire_mu', 'rolling_k']},
            {'section': 'car',
             'options': ['car_name', 'car_mass', 'front_weight_distribution', 'frontal_area', 'air_density', 'cd_car',
                         'lift_coefficient', 'downforce_total_area', 'downforce_distribution']}
        ]

        missing_keys = []
        for expected in expected_keys:
            section = expected['section']
            options = expected['options']
            for option in options:
                if not config.has_option(section, option):
                    missing_keys.append((section, option))

        if missing_keys:
            self.append_text(f"Missing keys: {missing_keys}")
            return
        else:
            self.append_text(f"All keys are present.")

        for section in config.sections():
            for option in config[section]:
                if option != 'layout' and option != 'car_name':
                    value = config[section][option]
                    if not is_number(value):
                        self.append_text(
                            f'Value "{value}" in section "{section}" and option "{option}" is not a number.')
                        return

        self.append_text("The file has correct data.")

        # clearing ui textboxes in preparation for new data
        self.torque_text_box.delete("0.0", 'end')

        for element in self.drivetrain_gears:
            self.update_text(element)
        self.update_text(self.redline_entry)
        self.update_text(self.idle_rpm_entry)
        self.update_text(self.final_drive_entry)
        self.update_text(self.car_name_entry)
        self.update_text(self.car_mass_entry)
        self.update_text(self.front_weight_distribution_entry)
        self.update_text(self.car_cd_entry)
        self.update_text(self.car_frontal_area_entry)
        self.update_text(self.car_air_density_entry)
        self.update_text(self.car_lift_coefficient_entry)
        self.update_text(self.car_downforce_total_area_entry)
        self.update_text(self.car_downforce_distribution_entry)
        self.update_text(self.layout_entry)
        self.update_text(self.drivetrain_loss_entry)
        self.update_text(self.shifting_time_entry)
        self.update_text(self.off_clutch_entry)
        self.update_text(self.clutch_bite_entry)
        self.update_text(self.gas_level_entry)
        self.update_text(self.tire_width_entry)
        self.update_text(self.tire_aspect_entry)
        self.update_text(self.tire_radial_entry)
        self.update_text(self.tire_mu_entry)
        self.update_text(self.tire_rolling_k_entry)

        # adding new data
        for option in config["torque_curve"]:
            value = config["torque_curve"][option]
            self.update_text2(self.torque_text_box, f"{option}={value}")

        for option, text_box in zip(config["drivetrain_gears"], self.drivetrain_gears):
            if option != "final_drive":
                value = config["drivetrain_gears"][option]
                self.update_text(text_box, value)

        self.update_text(self.final_drive_entry, config["drivetrain_gears"]["final_drive"])
        self.update_text(self.idle_rpm_entry, config["engine"]["idle_rpm"])
        self.update_text(self.redline_entry, config["engine"]["redline"])
        self.update_text(self.car_name_entry, config["car"]["car_name"])
        self.update_text(self.car_mass_entry, config["car"]["car_mass"])
        self.update_text(self.front_weight_distribution_entry, config["car"]["front_weight_distribution"])
        self.update_text(self.car_frontal_area_entry, config["car"]["frontal_area"])
        self.update_text(self.car_air_density_entry, config["car"]["air_density"])
        self.update_text(self.car_cd_entry, config["car"]["Cd_car"])
        self.update_text(self.car_lift_coefficient_entry, config["car"]["lift_coefficient"])

        try:
            # optional values
            self.update_text(self.car_downforce_total_area_entry, config["car"]["downforce_total_area"])
            self.update_text(self.car_downforce_distribution_entry, config["car"]["downforce_distribution"])
        except:
            pass

        # tire
        self.update_text(self.tire_width_entry, config["tire"]["tire_width"])
        self.update_text(self.tire_aspect_entry, config["tire"]["tire_aspect"])
        self.update_text(self.tire_radial_entry, config["tire"]["tire_radial"])
        self.update_text(self.tire_mu_entry, config["tire"]["tire_mu"])
        self.update_text(self.tire_rolling_k_entry, config["tire"]["rolling_k"])

        # drivetrain
        self.update_text(self.layout_entry, config["drivetrain"]["layout"])
        try:
            # optional
            self.update_text(self.drivetrain_loss_entry, config["drivetrain"]["drivetrain_loss"])
        except:
            pass
        self.update_text(self.shifting_time_entry, config["drivetrain"]["shifting_time"])
        self.update_text(self.clutch_bite_entry, config["drivetrain"]["clutch_bite"])
        self.update_text(self.off_clutch_entry, config["drivetrain"]["off_clutch"])
        self.update_text(self.gas_level_entry, config["drivetrain"]["gas_level"])

        self.append_text("Data set import was successful!")

    def export_data_set_func(self):
        if not self.check_data(export_to_file=True):
            self.append_text("The Data Could Not Be Exported Because Not All Fields Have Correct Information.")
            return

        base_dictionary = {
            'torque_curve': {},
            'engine': {'idle_rpm': '', 'redline': ''},
            'drivetrain_gears': {'gear1': '', 'gear2': '', 'gear3': '', 'gear4': '', 'gear5': '', 'gear6': '',
                                 'final_drive': ''},
            'drivetrain': {'layout': '', 'drivetrain_loss': '', 'shifting_time': '', 'off_clutch': '',
                           'clutch_bite': '', 'gas_level': ''},
            'tire': {'tire_width': '', 'tire_aspect': '', 'tire_radial': '', 'tire_mu': '', 'rolling_k': ''},
            'car': {'car_name': '', 'car_mass': '', 'front_weight_distribution': '', 'frontal_area': '',
                    'air_density': '', 'cd_car': '', 'lift_coefficient': '0', 'downforce_total_area': '',
                    'downforce_distribution': ''}}

        rpm_to_torque_aux = self.torque_text_box.get("1.0", "end-1c")
        for element in rpm_to_torque_aux.splitlines():
            rpm_torque = element.split("=")
            base_dictionary["torque_curve"][rpm_torque[0]] = rpm_torque[1]

        base_dictionary["engine"]["idle_rpm"] = self.idle_rpm_entry.get()
        base_dictionary["engine"]["redline"] = self.redline_entry.get()

        for idx, element in enumerate(self.drivetrain_gears):
            base_dictionary["drivetrain_gears"][f"gear{(idx + 1)}"] = element.get()

        base_dictionary["drivetrain_gears"]["final_drive"] = self.final_drive_entry.get()

        base_dictionary["car"]["car_name"] = self.car_name_entry.get()
        base_dictionary["car"]["car_mass"] = self.car_mass_entry.get()
        base_dictionary["car"]["front_weight_distribution"] = self.front_weight_distribution_entry.get()
        base_dictionary["car"]["frontal_area"] = self.car_frontal_area_entry.get()
        base_dictionary["car"]["air_density"] = self.car_air_density_entry.get()
        base_dictionary["car"]["cd_car"] = self.car_cd_entry.get()

        try:
            # optional values
            base_dictionary["car"]["lift_coefficient"] = self.car_lift_coefficient_entry.get()
            base_dictionary["car"]["downforce_total_area"] = self.car_downforce_total_area_entry.get()
            base_dictionary["car"]["downforce_distribution"] = self.car_downforce_distribution_entry.get()
        except:
            pass

        base_dictionary["drivetrain"]["layout"] = self.layout_entry.get()

        try:
            # optional value
            base_dictionary["drivetrain"]["drivetrain_loss"] = self.drivetrain_loss_entry.get()
        except:
            pass
        base_dictionary["drivetrain"]["shifting_time"] = self.shifting_time_entry.get()
        base_dictionary["drivetrain"]["off_clutch"] = self.off_clutch_entry.get()
        base_dictionary["drivetrain"]["clutch_bite"] = self.clutch_bite_entry.get()
        base_dictionary["drivetrain"]["gas_level"] = self.gas_level_entry.get()

        base_dictionary["tire"]["tire_width"] = self.tire_width_entry.get()
        base_dictionary["tire"]["tire_aspect"] = self.tire_aspect_entry.get()
        base_dictionary["tire"]["tire_radial"] = self.tire_radial_entry.get()
        base_dictionary["tire"]["tire_mu"] = self.tire_mu_entry.get()
        base_dictionary["tire"]["rolling_k"] = self.tire_rolling_k_entry.get()

        def data_stripper(data):
            new_data = {}
            for k, v in data.items():
                if isinstance(v, dict):
                    v = data_stripper(v)
                if not v in (u'', None, {}):
                    new_data[k] = v
            return new_data

        base_dictionary = data_stripper(base_dictionary)

        def save_ini():
            # Get the file name to save the INI file
            ini_file = filedialog.asksaveasfilename(defaultextension=".ini", filetypes=[("INI files", "*.ini")])

            # Create the ConfigParser object and add the data from the dictionary
            config = configparser.ConfigParser()
            for section, kv_pairs in base_dictionary.items():
                config[section] = kv_pairs

            # Write the config to the chosen file
            with open(ini_file, 'w') as f:
                config.write(f)

        save_ini()
        self.append_text("Data Set Export Was Successful.")

    def append_text(self, text, show_datetime=True):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        self.console.config(state='normal')
        if show_datetime:
            self.console.insert('end', text + f" [{dt_string}]" + "\n")
        else:
            self.console.insert('end', text + "\n")
        self.console.config(state='disabled')
        self.console.yview(tk.END)

    def create_bottom_buttons(self):
        bottom_btns = tk.LabelFrame(self, text="Buttons", padx=5, pady=5)
        bottom_btns.grid(row=2, column=0, columnspan=3, sticky=tk.N + tk.S + tk.W + tk.E, pady=5, padx=5)
        bottom_btns.grid_columnconfigure(tuple(range(15)), weight=1)
        bottom_btns.grid_rowconfigure(tuple(range(15)), weight=1)

        tk.Label(bottom_btns, text="(km/h)", justify="center").grid(row=0, column=0)
        tk.Label(bottom_btns, text="Initial Speed").grid(row=1, column=0, pady=5, padx=5)
        tk.Label(bottom_btns, text="Final Speed").grid(row=2, column=0, pady=5, padx=5)

        self.initial_speed_entry = tk.Entry(bottom_btns)
        self.initial_speed_entry.grid(row=1, column=1, pady=5, padx=5)
        self.final_speed_entry = tk.Entry(bottom_btns)
        self.final_speed_entry.grid(row=2, column=1, pady=5, padx=5)

        start_approx = tk.Button(bottom_btns, text="Start Approximation", command=self.start_approximation_func)
        start_approx.grid(row=1, column=4, pady=5, padx=5)

        import_data = tk.Button(bottom_btns, text="Import data set", command=self.import_data_set_func)
        import_data.grid(row=1, column=6, pady=5, padx=5)

        export_data = tk.Button(bottom_btns, text="Export data set", command=self.export_data_set_func)
        export_data.grid(row=2, column=6, pady=5, padx=5)

    def create_console_section(self):
        console_area = tk.LabelFrame(self, text="Console Output", padx=5, pady=5)
        console_area.grid(row=4, column=0, columnspan=3, sticky=tk.N + tk.S + tk.W + tk.E, pady=5, padx=5)
        console_area.grid_columnconfigure(tuple(range(15)), weight=1)
        console_area.grid_rowconfigure(tuple(range(15)), weight=1)

        self.console = tk.Text(console_area, state='disabled', wrap='word', pady=5, padx=5)
        self.console.grid(row=0, column=0)

        def clear_console():
            self.console.config(state='normal')
            self.console.delete("0.0", 'end')
            self.console.config(state='disabled')

        clear_console_btn = tk.Button(console_area, text="Clear Console", command=clear_console)
        clear_console_btn.grid(row=0, column=4, pady=5, padx=5)

    def create_torque_curve_section(self):
        torque_curve_frame = tk.LabelFrame(self, text="Torque Curve", padx=5, pady=5)
        torque_curve_frame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        torque_curve_frame.grid_columnconfigure(tuple(range(15)), weight=1, )
        torque_curve_frame.grid_rowconfigure(tuple(range(15)), weight=1)

        tk.Label(torque_curve_frame, text="RPM").grid(row=0, column=0)
        tk.Label(torque_curve_frame, text="Torque (Nm)").grid(row=0, column=1)

        # for i in range(1, 13):
        #     tk.Label(torque_curve_frame, text=1000 * i).grid(row=i, column=0)
        #     torque_entry = tk.Entry(torque_curve_frame)
        #     torque_entry.grid(row=i, column=1)
        #
        #     self.torque_curve.append(torque_entry)
        self.torque_text_box = tk.Text(torque_curve_frame, pady=5, padx=5)
        self.torque_text_box.grid(row=0, column=0, columnspan=1)
        self.torque_text_box.config(width=30)

    def create_engine_section(self):
        engine_frame = tk.LabelFrame(self, text="Engine", padx=5, pady=5)
        engine_frame.grid(row=1, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        engine_frame.grid_columnconfigure(tuple(range(15)), weight=1)
        engine_frame.grid_rowconfigure(tuple(range(15)), weight=1)

        tk.Label(engine_frame, text="Idle RPM").grid(row=0, column=0)
        self.idle_rpm_entry = tk.Entry(engine_frame)
        self.idle_rpm_entry.grid(row=0, column=1)

        tk.Label(engine_frame, text="Redline").grid(row=1, column=0)
        self.redline_entry = tk.Entry(engine_frame)
        self.redline_entry.grid(row=1, column=1)

    def create_drivetrain_gears_section(self):
        drivetrain_gears_frame = tk.LabelFrame(self, text="Drivetrain Gears", padx=5, pady=5)
        drivetrain_gears_frame.grid(row=0, column=1, sticky=tk.N + tk.S + tk.W + tk.E)
        drivetrain_gears_frame.grid_columnconfigure(tuple(range(15)), weight=1)
        drivetrain_gears_frame.grid_rowconfigure(tuple(range(15)), weight=1)

        tk.Label(drivetrain_gears_frame, text="Gear Ratios").grid(row=0, column=0)

        for i in range(1, 7):
            tk.Label(drivetrain_gears_frame, text="Gear {}".format(i)).grid(row=i, column=0)
            gear_ratio_entry = tk.Entry(drivetrain_gears_frame)
            gear_ratio_entry.grid(row=i, column=1)
            self.drivetrain_gears.append(gear_ratio_entry)

        tk.Label(drivetrain_gears_frame, text="Final Drive".format(i)).grid(row=7, column=0)
        self.final_drive_entry = tk.Entry(drivetrain_gears_frame)
        self.final_drive_entry.grid(row=7, column=1)

    def create_drivetrain_section(self):
        drivetrain_frame = tk.LabelFrame(self, text="Drivetrain", padx=5, pady=5)
        drivetrain_frame.grid(row=1, column=1, sticky=tk.N + tk.S + tk.W + tk.E)
        drivetrain_frame.grid_columnconfigure(tuple(range(15)), weight=1)
        drivetrain_frame.grid_rowconfigure(tuple(range(15)), weight=1)

        tk.Label(drivetrain_frame, text="Layout (fwd/rwd)").grid(row=0, column=0)
        self.layout_entry = tk.Entry(drivetrain_frame)
        self.layout_entry.grid(row=0, column=1)

        tk.Label(drivetrain_frame, text="Drivetrain Loss (%)").grid(row=1, column=0)
        self.drivetrain_loss_entry = tk.Entry(drivetrain_frame)
        self.drivetrain_loss_entry.grid(row=1, column=1)

        tk.Label(drivetrain_frame, text="Shifting Time (s)").grid(row=2, column=0)
        self.shifting_time_entry = tk.Entry(drivetrain_frame)
        self.shifting_time_entry.grid(row=2, column=1)

        tk.Label(drivetrain_frame, text="Off Clutch RPM").grid(row=3, column=0)
        self.off_clutch_entry = tk.Entry(drivetrain_frame)
        self.off_clutch_entry.grid(row=3, column=1)

        tk.Label(drivetrain_frame, text="Clutch Bite Point").grid(row=4, column=0)
        self.clutch_bite_entry = tk.Entry(drivetrain_frame)
        self.clutch_bite_entry.grid(row=4, column=1)

        tk.Label(drivetrain_frame, text="Gas Level").grid(row=5, column=0)
        self.gas_level_entry = tk.Entry(drivetrain_frame)
        self.gas_level_entry.grid(row=5, column=1)

    def create_tire_section(self):
        tire_frame = tk.LabelFrame(self, text="Tire", padx=5, pady=5)
        tire_frame.grid(row=1, column=2, sticky=tk.N + tk.S + tk.W + tk.E)
        tire_frame.grid_columnconfigure(tuple(range(15)), weight=1)
        tire_frame.grid_rowconfigure(tuple(range(15)), weight=1)

        tk.Label(tire_frame, text="Width (mm)").grid(row=0, column=0)
        self.tire_width_entry = tk.Entry(tire_frame)
        self.tire_width_entry.grid(row=0, column=1)

        tk.Label(tire_frame, text="Aspect Ratio (0-100)").grid(row=1, column=0)
        self.tire_aspect_entry = tk.Entry(tire_frame)
        self.tire_aspect_entry.grid(row=1, column=1)

        tk.Label(tire_frame, text="Radius (inches)").grid(row=2, column=0)
        self.tire_radial_entry = tk.Entry(tire_frame)
        self.tire_radial_entry.grid(row=2, column=1)

        tk.Label(tire_frame, text="Friction Coefficient (µ)").grid(row=3, column=0)
        self.tire_mu_entry = tk.Entry(tire_frame)
        self.tire_mu_entry.grid(row=3, column=1)

        tk.Label(tire_frame, text="Rolling Resistance Coefficient (k)").grid(row=4, column=0)
        self.tire_rolling_k_entry = tk.Entry(tire_frame)
        self.tire_rolling_k_entry.grid(row=4, column=1)

    def create_car_section(self):
        car_frame = tk.LabelFrame(self, text="Car", padx=5, pady=5)
        car_frame.grid(row=0, column=2, sticky=tk.N + tk.S + tk.W + tk.E)
        car_frame.grid_columnconfigure(tuple(range(15)), weight=1)
        car_frame.grid_rowconfigure(tuple(range(15)), weight=1)

        tk.Label(car_frame, text="Car Name").grid(row=0, column=0)
        self.car_name_entry = tk.Entry(car_frame)
        self.car_name_entry.grid(row=0, column=1)

        tk.Label(car_frame, text="Car Mass (kg)").grid(row=1, column=0)
        self.car_mass_entry = tk.Entry(car_frame)
        self.car_mass_entry.grid(row=1, column=1)

        tk.Label(car_frame, text="Front Weight Distribution (%)").grid(row=2, column=0)
        self.front_weight_distribution_entry = tk.Entry(car_frame)
        self.front_weight_distribution_entry.grid(row=2, column=1)

        tk.Label(car_frame, text="Cd Value").grid(row=3, column=0)
        self.car_cd_entry = tk.Entry(car_frame)
        self.car_cd_entry.grid(row=3, column=1)

        tk.Label(car_frame, text="Frontal Area (m^2)").grid(row=4, column=0)
        self.car_frontal_area_entry = tk.Entry(car_frame)
        self.car_frontal_area_entry.grid(row=4, column=1)

        tk.Label(car_frame, text="Air Density (kg/m^3)").grid(row=5, column=0)
        self.car_air_density_entry = tk.Entry(car_frame)
        self.car_air_density_entry.grid(row=5, column=1)

        tk.Label(car_frame, text="Lift Coefficient").grid(row=6, column=0)
        self.car_lift_coefficient_entry = tk.Entry(car_frame)
        self.car_lift_coefficient_entry.grid(row=6, column=1)

        tk.Label(car_frame, text="Downforce Total Area (m^2)").grid(row=7, column=0)
        self.car_downforce_total_area_entry = tk.Entry(car_frame)
        self.car_downforce_total_area_entry.grid(row=7, column=1)

        tk.Label(car_frame, text="Downforce Distribution %").grid(row=8, column=0)
        self.car_downforce_distribution_entry = tk.Entry(car_frame)
        self.car_downforce_distribution_entry.grid(row=8, column=1)

    def save_data(self):
        pass


app = INIEditor()
app.mainloop()
