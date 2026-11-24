
"""
E-TREAD TwinForge
AI-Powered Digital Twin Platform for EV Two-Wheeler Tyre Engineering

Backend API connecting physics-based engineering models.
"""

from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from engineering.vehicle_dynamics.model import (
    calculate_vehicle_dynamics
)

from engineering.thermal_model.model import (
    simulate_tyre_thermal_response
)


# --------------------------------------------------
# APPLICATION CONFIGURATION
# --------------------------------------------------

app = FastAPI(
    title="E-TREAD TwinForge API",
    description=(
        "AI-powered Digital Twin platform "
        "for EV two-wheeler tyre engineering."
    ),
    version="0.3.0"
)


# --------------------------------------------------
# VEHICLE DYNAMICS INPUT SCHEMA
# --------------------------------------------------

class VehicleDynamicsInput(BaseModel):

    mass_kg: float = Field(gt=0)

    acceleration_ms2: float

    speed_kmh: float = Field(ge=0)

    gradient_percent: float

    rolling_resistance_coefficient: float = Field(ge=0)

    drag_coefficient: float = Field(ge=0)

    frontal_area_m2: float = Field(ge=0)

    wheel_radius_m: float = Field(gt=0)

    drivetrain_efficiency: float = Field(
        gt=0,
        le=1,
        default=0.90
    )


# --------------------------------------------------
# THERMAL SIMULATION INPUT SCHEMA
# --------------------------------------------------

class ThermalSimulationInput(BaseModel):

    initial_temp_c: float

    ambient_temp_c: float

    heat_generation_w: float = Field(ge=0)

    convection_coefficient_w_m2k: float = Field(ge=0)

    surface_area_m2: float = Field(gt=0)

    thermal_capacity_j_k: float = Field(gt=0)

    duration_s: float = Field(gt=0)

    time_step_s: float = Field(
        gt=0,
        default=0.5
    )

    emissivity: float = Field(
        ge=0,
        le=1,
        default=0.9
    )


# --------------------------------------------------
# ROOT ENDPOINT
# --------------------------------------------------

@app.get("/")
def root():

    return {
        "project": "E-TREAD TwinForge",
        "message": "EV Tyre Engineering Digital Twin API",
        "status": "Running",
        "version": "0.3.0"
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "Healthy",
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat()
    }


# --------------------------------------------------
# API INFORMATION
# --------------------------------------------------

@app.get("/api/v1")
def api_information():

    return {
        "platform": "E-TREAD TwinForge",

        "available_modules": [
            "Vehicle Dynamics",
            "Tyre Mechanics",
            "Tyre Thermal Simulation",
            "AI Prediction",
            "Multi-Objective Optimisation"
        ],

        "development_status": "Initial Engineering Backend"
    }


# --------------------------------------------------
# VEHICLE DYNAMICS API
# --------------------------------------------------

@app.post("/api/v1/vehicle-dynamics")
def vehicle_dynamics(data: VehicleDynamicsInput):

    try:

        results = calculate_vehicle_dynamics(
            **data.model_dump()
        )

        return {
            "project": "E-TREAD TwinForge",

            "module": "EV Vehicle Dynamics",

            "calculation_status": "Successful",

            "input_parameters": data.model_dump(),

            "engineering_results": results
        }

    except ValueError as error:

        raise HTTPException(
            status_code=422,
            detail=str(error)
        )


# --------------------------------------------------
# TYRE THERMAL SIMULATION API
# --------------------------------------------------

@app.post("/api/v1/thermal-simulation")
def thermal_simulation(data: ThermalSimulationInput):

    try:

        results = simulate_tyre_thermal_response(
            **data.model_dump()
        )

        return {
            "project": "E-TREAD TwinForge",

            "module": "Tyre Thermal Simulation",

            "calculation_status": "Successful",

            "input_parameters": data.model_dump(),

            "simulation_results": results
        }

    except ValueError as error:

        raise HTTPException(
            status_code=422,
            detail=str(error)
        )
