
"""
E-TREAD TwinForge
EV Two-Wheeler Vehicle Dynamics Engine

Calculates longitudinal tractive force, resistance forces,
wheel torque and power requirements.

All calculations use SI units internally.
"""

import math


GRAVITY = 9.81


def calculate_vehicle_dynamics(
    mass_kg: float,
    acceleration_ms2: float,
    speed_kmh: float,
    gradient_percent: float,
    rolling_resistance_coefficient: float,
    drag_coefficient: float,
    frontal_area_m2: float,
    wheel_radius_m: float,
    drivetrain_efficiency: float = 0.90,
    air_density_kg_m3: float = 1.225
) -> dict:

    # Input validation
    if mass_kg <= 0:
        raise ValueError("Vehicle mass must be positive.")

    if wheel_radius_m <= 0:
        raise ValueError("Wheel radius must be positive.")

    if speed_kmh < 0:
        raise ValueError("Speed cannot be negative.")

    if rolling_resistance_coefficient < 0:
        raise ValueError("Rolling resistance coefficient cannot be negative.")

    if drag_coefficient < 0 or frontal_area_m2 < 0:
        raise ValueError("Drag coefficient and frontal area cannot be negative.")

    if not 0 < drivetrain_efficiency <= 1:
        raise ValueError("Drivetrain efficiency must be between 0 and 1.")

    if air_density_kg_m3 <= 0:
        raise ValueError("Air density must be positive.")

    # Convert speed into metres per second
    speed_ms = speed_kmh / 3.6

    # Convert road gradient percentage into angle
    gradient_angle = math.atan(gradient_percent / 100.0)

    # Calculate resistance forces
    rolling_resistance = (
        rolling_resistance_coefficient
        * mass_kg
        * GRAVITY
        * math.cos(gradient_angle)
    )

    aerodynamic_drag = (
        0.5
        * air_density_kg_m3
        * drag_coefficient
        * frontal_area_m2
        * speed_ms ** 2
    )

    gradient_resistance = (
        mass_kg
        * GRAVITY
        * math.sin(gradient_angle)
    )

    # Force required at the tyre contact patch
    acceleration_force = mass_kg * acceleration_ms2

    total_tractive_force = (
        acceleration_force
        + rolling_resistance
        + aerodynamic_drag
        + gradient_resistance
    )

    # Wheel torque and power
    wheel_torque = total_tractive_force * wheel_radius_m

    wheel_power = total_tractive_force * speed_ms

    # Motor input power estimate
    motor_input_power = wheel_power / drivetrain_efficiency

    return {
        "speed_ms": round(speed_ms, 3),
        "rolling_resistance_N": round(rolling_resistance, 3),
        "aerodynamic_drag_N": round(aerodynamic_drag, 3),
        "gradient_resistance_N": round(gradient_resistance, 3),
        "acceleration_force_N": round(acceleration_force, 3),
        "total_tractive_force_N": round(total_tractive_force, 3),
        "wheel_torque_Nm": round(wheel_torque, 3),
        "wheel_power_W": round(wheel_power, 3),
        "motor_input_power_W": round(motor_input_power, 3)
    }
