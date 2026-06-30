"""
Response Models
Patient-Centric Dashboard
"""

from pydantic import BaseModel
from typing import Dict, List, Any


class PatientResponse(BaseModel):

    patient: Dict[str, Any]

    vitals: List[Dict[str, Any]]


class AnalyticsResponse(BaseModel):

    patient_id: str

    trend: str

    risk_band: str

    anomaly_count: int

    mean_glucose: float


class DashboardResponse(BaseModel):

    overview: Dict[str, Any]

    analytics: AnalyticsResponse

    history: Dict[str, List[Dict[str, Any]]]

    summary: str