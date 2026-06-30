"""
Dashboard Service
Business Logic Layer
"""

from backend.utils.constants import VITAL_MAP
import numpy as np

from backend.analytics.trend import TrendAnalyzer
from backend.analytics.anomaly import AnomalyDetector
from backend.analytics.risk import RiskCalculator

class DashboardService:

    def __init__(self, repository):

        self.repo = repository

    # ==========================================================
    # PATIENT SUMMARY
    # ==========================================================

    def get_patient_summary(self, patient_id):

        patient = self.repo.get_patient(patient_id)

        if patient is None:

            return None

        vitals = self.repo.get_patient_vitals(patient_id)

        return {

            "patient": patient,

            "vitals": vitals

        }

    # ==========================================================
    # GROUP VITALS
    # ==========================================================

    def get_vitals_by_type(self, patient_id):

        vitals = self.repo.get_patient_vitals(patient_id)

        grouped = {}

        for row in vitals:

            key = VITAL_MAP.get(

                row["description"],

                row["description"]

            )

            grouped.setdefault(

                key,

                []

            ).append(row)

        return grouped

    # ==========================================================
    # REFERENCE RANGE
    # ==========================================================

    def get_reference_for_patient(self, patient_id):

        vitals = self.repo.get_patient_vitals(patient_id)

        if len(vitals) == 0:

            return None

        age_band = vitals[0]["age_band"]

        return self.repo.get_reference(age_band)

    # ==========================================================
    # LATEST VITALS
    # ==========================================================

    def get_latest_vitals(self, patient_id):

        grouped = self.get_vitals_by_type(patient_id)

        latest = {}

        for vital, readings in grouped.items():

            latest[vital] = readings[-1]

        return latest
    
        # ==========================================================
    # LATEST VALUE
    # ==========================================================

    def get_latest_value(self, patient_id, vital):

        latest = self.get_latest_vitals(patient_id)

        if vital not in latest:

            return None

        return latest[vital]["value"]


    # ==========================================================
    # GLUCOSE HISTORY
    # ==========================================================

    def get_glucose_history(self, patient_id):

        grouped = self.get_vitals_by_type(patient_id)

        return grouped.get("glucose", [])


    # ==========================================================
    # PATIENT ANALYTICS
    # ==========================================================

    def get_patient_analytics(self, patient_id):

        glucose = self.get_glucose_history(patient_id)

        values = [

            row["value"]

            for row in glucose

        ]

        if len(values) == 0:

            return {

                "patient_id": patient_id,

                "trend": "stable",

                "risk_band": "Low",

                "anomaly_count": 0,

                "mean_glucose": 0.0

            }

        trend = TrendAnalyzer.detect(values)

        anomalies = AnomalyDetector.detect(values)

        risk = RiskCalculator.calculate(

            len(anomalies)

        )

        return {

            "patient_id": patient_id,

            "trend": trend,

            "risk_band": risk,

            "anomaly_count": len(anomalies),

            "mean_glucose": round(

                float(np.mean(values)),

                2

            )

        }
        # ==========================================================
    # PATIENT OVERVIEW
    # ==========================================================

    def build_patient_overview(self, patient_id):

        patient = self.repo.get_patient(patient_id)

        if patient is None:

            return None

        latest = self.get_latest_vitals(patient_id)

        reference = self.get_reference_for_patient(patient_id)

        return {

            "patient": patient,

            "latest_vitals": latest,

            "reference": reference

        }


    # ==========================================================
    # SUMMARY
    # ==========================================================

    def generate_summary(self, patient_id):

        overview = self.build_patient_overview(patient_id)

        if overview is None:

            return "Patient not found."

        patient = overview["patient"]

        analytics = self.get_patient_analytics(patient_id)

        return (

            f"Patient is {patient['age']} years old. "

            f"Current glucose trend is "

            f"{analytics['trend']} "

            f"with a "

            f"{analytics['risk_band']} "

            f"risk classification."

        )


    # ==========================================================
    # COMPLETE DASHBOARD
    # ==========================================================

    def build_dashboard(self, patient_id):

        overview = self.build_patient_overview(patient_id)

        if overview is None:

            return None

        analytics = self.get_patient_analytics(patient_id)

        history = self.get_vitals_by_type(patient_id)

        return {

            "overview": overview,

            "analytics": analytics,

            "history": history,

            "summary": self.generate_summary(patient_id)

        }