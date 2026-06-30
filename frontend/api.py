"""
Frontend API Layer
Patient-Centric Dashboard

Handles all communication between
Streamlit and the FastAPI backend.
"""

import requests

# ==========================================================
# Backend Configuration
# ==========================================================

BASE_URL = "http://127.0.0.1:8000"

TIMEOUT = 60


# ==========================================================
# Generic GET Request
# ==========================================================

def get(endpoint: str):
    """
    Generic GET request.

    Raises RuntimeError if the backend
    cannot be reached.
    """

    url = f"{BASE_URL}{endpoint}"

    try:

        response = requests.get(
            url,
            timeout=TIMEOUT
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:

        raise RuntimeError(
            "Backend request timed out."
        )

    except requests.exceptions.ConnectionError:

        raise RuntimeError(
            "Unable to connect to backend."
        )

    except requests.exceptions.HTTPError as e:

        raise RuntimeError(
            f"HTTP Error: {e}"
        )

    except requests.exceptions.RequestException as e:

        raise RuntimeError(
            f"Request Failed: {e}"
        )


# ==========================================================
# Root
# ==========================================================

def get_root():

    return get("/")


# ==========================================================
# Health
# ==========================================================

def get_health():

    return get("/health")


# ==========================================================
# Patients
# ==========================================================

def get_patients():

    return get("/patients")


# ==========================================================
# Demo Patient
# ==========================================================

def get_demo_patient():

    return get("/demo-patient")


# ==========================================================
# Patient Summary
# ==========================================================

def get_patient(patient_id):

    return get(
        f"/patients/{patient_id}"
    )


# ==========================================================
# Analytics
# ==========================================================

def get_analytics(patient_id):

    return get(
        f"/patients/{patient_id}/analytics"
    )


# ==========================================================
# Dashboard
# ==========================================================

def get_dashboard(patient_id):

    return get(
        f"/dashboard/{patient_id}"
    )


# ==========================================================
# Backend Availability
# ==========================================================

def backend_available():

    try:

        get_health()

        return True

    except Exception:

        return False


# ==========================================================
# API Connectivity Test
# ==========================================================

if __name__ == "__main__":

    print("=" * 70)
    print("PATIENT-CENTRIC DASHBOARD")
    print("FRONTEND API TEST")
    print("=" * 70)

    print()

    print("Checking Backend...")

    if not backend_available():

        print("Backend is Offline")

        exit()

    print("Backend Connected")

    print()

    # ------------------------------------------------------
    # Root
    # ------------------------------------------------------

    print("-" * 70)
    print("ROOT")
    print("-" * 70)

    root = get_root()

    print(root)

    print()

    # ------------------------------------------------------
    # Health
    # ------------------------------------------------------

    print("-" * 70)
    print("HEALTH")
    print("-" * 70)

    health = get_health()

    print(health)

    print()

    # ------------------------------------------------------
    # Patients
    # ------------------------------------------------------

    print("-" * 70)
    print("PATIENTS")
    print("-" * 70)

    patients = get_patients()

    print("Total Patients :", len(patients))

    print()

    first_patient = patients[0]

    print(first_patient)

    patient_id = first_patient["patient_id"]

    print()

    # ------------------------------------------------------
    # Patient
    # ------------------------------------------------------

    print("-" * 70)
    print("PATIENT SUMMARY")
    print("-" * 70)

    patient = get_patient(patient_id)

    print(patient.keys())

    print()

    # ------------------------------------------------------
    # Analytics
    # ------------------------------------------------------

    print("-" * 70)
    print("ANALYTICS")
    print("-" * 70)

    analytics = get_analytics(patient_id)

    print(analytics)

    print()

    # ------------------------------------------------------
    # Dashboard
    # ------------------------------------------------------

    print("-" * 70)
    print("DASHBOARD")
    print("-" * 70)

    dashboard = get_dashboard(patient_id)

    print(dashboard.keys())

    print()

    print("=" * 70)
    print("ALL API TESTS PASSED")
    print("=" * 70)