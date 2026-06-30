"""
Request Models
Patient-Centric Dashboard
"""

from pydantic import BaseModel
from typing import List


class TrendRequest(BaseModel):
    patient_id: str
    vital_type: str
    values: List[float]


class RiskRequest(BaseModel):
    patient_id: str
    bp: float
    glucose: float


class DashboardRequest(BaseModel):
    patient_id: str