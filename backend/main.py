"""
Patient-Centric Dashboard Backend
Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import (

    API_TITLE,

    API_VERSION,

    API_DESCRIPTION,

    HOST,

    PORT

)

from backend.api.dashboard import router

import uvicorn


# ==========================================================
# FASTAPI APPLICATION
# ==========================================================

app = FastAPI(

    title=API_TITLE,

    version=API_VERSION,

    description=API_DESCRIPTION

)

# ==========================================================
# CORS
# ==========================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)

# ==========================================================
# REGISTER ROUTES
# ==========================================================

app.include_router(router)

# ==========================================================
# RUN SERVER
# ==========================================================

if __name__ == "__main__":

    uvicorn.run(

        "main:app",

        host=HOST,

        port=PORT,

        reload=True

    )