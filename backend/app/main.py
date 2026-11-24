
from fastapi import FastAPI
from datetime import datetime, timezone

app = FastAPI(
    title="E-TREAD TwinForge API",
    description=(
        "AI-powered Digital Twin platform for "
        "EV two-wheeler tyre engineering."
    ),
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "project": "E-TREAD TwinForge",
        "message": "EV Tyre Engineering Digital Twin API",
        "status": "Running",
        "version": "0.1.0"
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
        "modules": [
            "Vehicle Dynamics",
            "Tyre Mechanics",
            "Thermal Modelling",
            "AI Prediction",
            "Multi-Objective Optimisation"
        ],
        "development_status": "Initial Backend Development"
    }
