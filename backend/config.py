"""
Application Configuration
Patient-Centric Dashboard Backend
"""

import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")
# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

DATABASE_URL = os.getenv("DATABASE_URL")

# ==========================================================
# API CONFIGURATION
# ==========================================================

API_TITLE = "Patient-Centric Dashboard API"

API_VERSION = "2.0"

API_DESCRIPTION = (
    "Backend API for Patient-Centric Dashboard"
)

# ==========================================================
# SERVER CONFIGURATION
# ==========================================================

HOST = "127.0.0.1"

PORT = 8000