
"""
E-TREAD TwinForge
Tyre Thermal Simulation Engine

First-order lumped-parameter thermal model.

This model estimates bulk tyre temperature under
a specified heat-generation input and cooling conditions.
It is not a validated tyre temperature prediction model.
"""

import math


STEFAN_BOLTZMANN = 5.670374419e-8


def simulate_tyre_thermal_response(
    initial_temp_c: float,
    ambient_temp_c: float,
    heat_generation_w: float,
    convection_coefficient_w_m2k: float,
    surface_area_m2: float,
    thermal_capacity_j_k: float,
    duration_s: float,
    time_step_s: float = 0.5,
    emissivity: float = 0.9
) -> dict:

    # Input validation
    if surface_area_m2 <= 0:
        raise ValueError("Surface area must be positive.")

    if thermal_capacity_j_k <= 0:
        raise ValueError("Thermal capacity must be positive.")

    if duration_s <= 0 or time_step_s <= 0:
        raise ValueError("Duration and time step must be positive.")

    if heat_generation_w < 0:
        raise ValueError("Heat generation cannot be negative.")

    if convection_coefficient_w_m2k < 0:
        raise ValueError("Convection coefficient cannot be negative.")

    if not 0 <= emissivity <= 1:
        raise ValueError("Emissivity must be between 0 and 1.")

    if initial_temp_c <= -273.15 or ambient_temp_c <= -273.15:
        raise ValueError("Temperature must be above absolute zero.")

    # Initial temperature
    temperature_c = initial_temp_c

    results = [{
        "time_s": 0.0,
        "temperature_c": round(temperature_c, 4)
    }]

    elapsed_time = 0.0

    # Time integration using explicit Euler method
    while elapsed_time < duration_s:

        dt = min(time_step_s, duration_s - elapsed_time)

        temperature_k = temperature_c + 273.15
        ambient_k = ambient_temp_c + 273.15

        # Convective heat loss
        convection_loss = (
            convection_coefficient_w_m2k
            * surface_area_m2
            * (temperature_c - ambient_temp_c)
        )

        # Radiative heat loss
        radiation_loss = (
            emissivity
            * STEFAN_BOLTZMANN
            * surface_area_m2
            * (temperature_k**4 - ambient_k**4)
        )

        # Net heat flow
        net_heat_w = (
            heat_generation_w
            - convection_loss
            - radiation_loss
        )

        # Temperature rate of change
        temperature_rate = (
            net_heat_w / thermal_capacity_j_k
        )

        # Euler integration
        temperature_c += temperature_rate * dt
        elapsed_time += dt

        results.append({
            "time_s": round(elapsed_time, 3),
            "temperature_c": round(temperature_c, 4)
        })

    temperatures = [
        point["temperature_c"] for point in results
    ]

    return {
        "model": "Lumped Parameter Thermal Model",
        "final_temperature_c": round(temperature_c, 3),
        "maximum_temperature_c": round(max(temperatures), 3),
        "minimum_temperature_c": round(min(temperatures), 3),
        "temperature_rise_c": round(
            temperature_c - initial_temp_c, 3
        ),
        "simulation_duration_s": duration_s,
        "time_series": results
    }
