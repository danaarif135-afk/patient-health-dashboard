"""
Database Connection
Patient-Centric Dashboard Backend
"""

from sqlalchemy import create_engine
from sqlalchemy import text

from backend.config import DATABASE_URL


# ==========================================================
# CREATE ENGINE
# ==========================================================

engine = create_engine(

    DATABASE_URL,

    pool_pre_ping=True,

    future=True

)


# ==========================================================
# DATABASE CONNECTION TEST
# ==========================================================

def test_connection():

    try:

        with engine.connect() as conn:

            result = conn.execute(

                text("SELECT NOW()")

            )

            current_time = result.scalar()

            print()

            print("=" * 60)

            print("DATABASE CONNECTED SUCCESSFULLY")

            print(current_time)

            print("=" * 60)

            print()

            return True

    except Exception as e:

        print()

        print("=" * 60)

        print("DATABASE CONNECTION FAILED")

        print(e)

        print("=" * 60)

        print()

        return False