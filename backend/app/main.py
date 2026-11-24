
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, timezone

from engineering.vehicle_dynamics.model import (
    calculate_vehicle_dynamics
)

app = FastAPI(
    title="E-TREAD TwinForge API",
    description="AI-powered Digital Twin platform for EV tyre engineering",
    version="0.2.0"
)


# EV configuration input schema
class VehicleDynamicsInput(BaseModel):
    mass_kg: float = Field(gt=0, description="Total vehicle mass in kg")
    acceleration_ms2: float = Field(description="Longitudinal acceleration in m/s²")
    speed_kmh: float = Field(ge=0, description="Vehicle speed in km/h")
    gradient_percent: float = Field(description="Road gradient in percentage")
    rolling_resistance_coefficient: float = Field(ge=0)
    drag_coefficient: float = Field(ge=0)
    frontal_area_m2: float = Field(ge=0)
    wheel_radius_m: float = Field(gt=0)
    drivetrain_efficiency: float = Field(gt=0, le=1, default=0.90)


@app.get("/")
def root():
    return {
        "project": "E-TREAD TwinForge",
        "status": "Running",
        "version": "0.2.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "Healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/api/v1")
def api_information():
    return {
        "platform": "E-TREAD TwinForge",
        "available_modules": [
            "Vehicle Dynamics",
            "Tyre Mechanics",
            "Thermal Modelling",
            "AI Prediction",
            "Multi-Objective Optimisation"
        ]
    }


@app.post("/api/v1/vehicle-dynamics")
def vehicle_dynamics(data: VehicleDynamicsInput):

    try:
        results = calculate_vehicle_dynamics(
            mass_kg=data.mass_kg,
            acceleration_ms2=data.acceleration_ms2,
            speed_kmh=data.speed_kmh,
            gradient_percent=data.gradient_percent,
            rolling_resistance_coefficient=(
                data.rolling_resistance_coefficient
            ),
            drag_coefficient=data.drag_coefficient,
            frontal_area_m2=data.frontal_area_m2,
            wheel_radius_m=data.wheel_radius_m,
            drivetrain_efficiency=data.drivetrain_efficiency
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
