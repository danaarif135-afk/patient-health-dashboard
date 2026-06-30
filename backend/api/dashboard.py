"""
Dashboard API
"""

from fastapi import APIRouter, HTTPException

from backend.database import engine
from backend.repository.dashboard_repository import DashboardRepository
from backend.services.dashboard_service import DashboardService

from backend.models.response_models import (
    PatientResponse,
    AnalyticsResponse,
    DashboardResponse,
)

# ==========================================================
# Initialize
# ==========================================================

router = APIRouter(tags=["Dashboard"])

repo = DashboardRepository(engine)
service = DashboardService(repo)

# ==========================================================
# Root Endpoint
# ==========================================================

@router.get("/")
def root():
    return {
        "message": "Patient Centric Dashboard API",
        "status": "running",
        "version": "2.0"
    }


# ==========================================================
# Health Check
# ==========================================================

@router.get("/health")
def health():
    return {
        "status": "healthy",
        "database": "connected"
    }


# ==========================================================
# Get All Patients
# ==========================================================

@router.get("/patients")
def get_all_patients():
    return repo.get_all_patients()


# ==========================================================
# Demo Patient
# ==========================================================

@router.get("/demo-patient")
def demo_patient():
    patient = repo.get_patient_with_complete_dashboard()

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="No suitable demo patient found."
        )

    return {
        "patient_id": patient
    }


# ==========================================================
# Patient Summary
# ==========================================================

@router.get(
    "/patients/{patient_id}",
    response_model=PatientResponse
)
def get_patient(patient_id: str):

    patient = service.get_patient_summary(patient_id)

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient


# ==========================================================
# Patient Analytics
# ==========================================================

@router.get(
    "/patients/{patient_id}/analytics",
    response_model=AnalyticsResponse
)
def get_patient_analytics(patient_id: str):

    patient = service.get_patient_summary(patient_id)

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return service.get_patient_analytics(patient_id)


# ==========================================================
# Complete Dashboard
# ==========================================================

@router.get(
    "/dashboard/{patient_id}",
    response_model=DashboardResponse
)
def get_dashboard(patient_id: str):

    dashboard = service.build_dashboard(patient_id)

    if dashboard is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return dashboard