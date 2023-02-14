import numpy as np


def estimate_weight_shift(acceleration_values, wheelbase, track_width, roll_center_height, roll_stiffness):
    weight_shifts = []
    for acceleration in acceleration_values:
        # Compute the roll angle caused by the weight shift
        roll_angle = acceleration * wheelbase / (2 * roll_stiffness)

        # Compute the weight shift as a fraction of the track width
        weight_shift = roll_angle * track_width / 2 * roll_center_height

        weight_shifts.append(weight_shift)

    return weight_shifts


# # graphs
# # torque vs rpm graph
# fig = make_subplots(rows=2, cols=3)
# fig.add_trace(
#     go.Scatter(x=rpm_curve, y=torque_curve,
#                name="Torque(Nm)"
#                ), row=1, col=1
# )
#
# # horsepower vs rpm graph
# fig.add_trace(
#     go.Scatter(x=rpm_curve, y=horsepower,
#                name='HP'
#                ), row=1, col=1
# )


# def find_optimum_upshift_point(torque_values, find_torque_at_speed):
#     optimum_shift_points = []
#
#     for i in range(len(torque_values) - 1):
#         for j in range(len(torque_values[i])):
#             next_gear_torque = find_torque_at_speed(i, i + 1, j)
#             if next_gear_torque > torque_values[i][j]:
#                 lower_torque_index = j
#                 break
#         else:
#             optimum_shift_points.append(len(torque_values[i]) - 1)
#             continue
#
#         current_gear_sum = 0
#         next_gear_sum = 0
#
#         positive_accel = []
#         for count, index in enumerate(range(lower_torque_index, min(len(torque_values[i]), len(next_gear_torque))), start=1):
#             current_gear_sum += torque_values[i][index]
#             next_gear_sum += next_gear_torque[index]
#             if current_gear_sum/count > next_gear_sum/count:
#                 positive_accel.append([current_gear_sum/count, index])
#
#         if not positive_accel:
#             optimum_shift_points.append(lower_torque_index)
#         else:
#             max_accel = -float('inf')
#             for avg_torque in positive_accel:
#                 if avg_torque[0] > max_accel:
#                     max_accel = avg_torque
#             optimum_shift_points.append(max_accel[1])
#
#     return optimum_shift_points
#
#
#


idle_rpm = 1000
time = 0
rolling_coefficient = 0.001
car_mass = 1000
torque = [200, 300, 400, 100]


# calculeaza din nou acceleratia, inmultind cuplul cu gas level?

for index in range(0, len(torque_curve) - 1):
    if layout == 'fwd':
        acceleration_at_specific_rpm = (min((max_tractive_force + downforce_curve[index] * downforce_distribution) * tire_mu,
                                            torque_at_the_wheels[index] / tire_radius) - air_resistance_curve[index] - rolling_k * g * car_mass) / car_mass
    else:
        acceleration_at_specific_rpm = (min((max_tractive_force + downforce_curve[index] * (1 - downforce_distribution)) * tire_mu,torque_at_the_wheels[index] / tire_radius) - air_resistance_curve[
                                            index] - rolling_k * g * car_mass) / car_mass


for index in range(0, len(torque_curve) - 1):
    downforce = downforce_curve[index] * (downforce_distribution if layout == 'fwd' else (1 - downforce_distribution))
    air_resistance = air_resistance_curve[index]
    rolling_resistance = rolling_k * g * car_mass
    traction = min((max_tractive_force + downforce) * tire_mu, torque_at_the_wheels[index] / tire_radius - air_resistance - rolling_resistance)/ car_mass

    acceleration_at_specific_rpm = traction / car_mass


