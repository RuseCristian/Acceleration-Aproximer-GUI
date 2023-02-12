def estimate_weight_shift(acceleration_values, wheelbase, track_width, roll_center_height, roll_stiffness):
    weight_shifts = []
    for acceleration in acceleration_values:
        # Compute the roll angle caused by the weight shift
        roll_angle = acceleration * wheelbase / (2 * roll_stiffness)

        # Compute the weight shift as a fraction of the track width
        weight_shift = roll_angle * track_width / 2 * roll_center_height

        weight_shifts.append(weight_shift)

    return weight_shifts
